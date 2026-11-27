from __future__ import annotations

import json
import pathlib
import sys

import httpx

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_ecosystem_knowledge as vek  # noqa: E402
from tools.rag_pipeline.sinks import (  # noqa: E402
    AzureAISearchSink,
    DatabricksVectorSearchSink,
    Neo4jGraphSink,
    R2RPgVectorSink,
)
from tools.rag_pipeline.sync_knowledge_base import (  # noqa: E402
    SOURCE_CATEGORIES,
    collect_documents,
    sync_knowledge_base,
)


def _mock_r2r_client(recorded: dict) -> httpx.Client:
    def handler(request: httpx.Request) -> httpx.Response:
        recorded["calls"].append((request.method, request.url.path))
        if request.method == "GET" and request.url.path == "/v3/collections/name/dark-gravity-knowledge-base":
            if recorded["collection_exists"]:
                return httpx.Response(200, json={"results": {"id": "col-uuid-009"}})
            return httpx.Response(404, json={"detail": "Not found"})
        if request.method == "POST" and request.url.path == "/v3/collections":
            recorded["collection_exists"] = True
            return httpx.Response(201, json={"results": {"id": "col-uuid-009"}})
        if request.method == "POST" and request.url.path == "/v3/documents":
            raw_body = request.content.decode("utf-8", errors="ignore")
            # Crucial contract: never send multipart collection_ids (FastAPI 0.156.2 HTTP 422 guard)
            assert 'name="collection_ids"' not in raw_body
            assert 'name="raw_text"' in raw_body
            assert 'name="run_with_orchestration"' in raw_body
            assert '"collection_id": "col-uuid-009"' in raw_body
            recorded["uploads"].append(raw_body)
            # Extract id field from multipart payload
            did = "doc-id"
            for line in raw_body.splitlines():
                if len(line) == 36 and line.count("-") == 4:
                    did = line.strip()
                    break
            return httpx.Response(202, json={"results": {"document_id": did}})
        if request.method == "POST" and request.url.path.startswith("/v3/collections/col-uuid-009/documents/"):
            recorded["assignments"].append(request.url.path)
            return httpx.Response(200, json={"results": {"assigned": True}})
        if request.method == "DELETE" and request.url.path.startswith("/v3/documents/"):
            recorded["deletes"].append(request.url.path)
            return httpx.Response(200, json={"results": {"deleted": True}})
        return httpx.Response(500, text=f"Unhandled {request.method} {request.url.path}")

    return httpx.Client(base_url="http://r2r.test:7272", transport=httpx.MockTransport(handler))


def test_collect_covers_all_8_categories_and_doc011() -> None:
    docs = collect_documents(data_dir=REPO_ROOT, repos_root=REPO_ROOT.parent)
    categories = {d.source_category for d in docs}
    assert categories == set(SOURCE_CATEGORIES), f"Missing categories: {set(SOURCE_CATEGORIES) - categories}"
    for d in docs:
        assert d.visibility == "public"
        assert len(d.content_sha256) == 64
        assert not vek.detect_doc011_leaks(d.content, d.doc_key)


def test_incremental_sync_dedup_pruning_and_unconfigured_optional_sinks(tmp_path: pathlib.Path, monkeypatch) -> None:
    for var in (
        "DARK_GRAVITY_NEO4J_URI",
        "DARK_GRAVITY_AZURE_SEARCH_ENDPOINT",
        "DARK_GRAVITY_DATABRICKS_HOST",
    ):
        monkeypatch.delenv(var, raising=False)

    recorded = {"calls": [], "uploads": [], "assignments": [], "deletes": [], "collection_exists": False}
    client = _mock_r2r_client(recorded)
    primary = R2RPgVectorSink(base_url="http://r2r.test:7272", client=client)
    optionals = [Neo4jGraphSink(), AzureAISearchSink(), DatabricksVectorSearchSink()]
    state_file = tmp_path / "sync-state.json"

    docs = collect_documents(data_dir=REPO_ROOT, repos_root=None)
    # 1. Dry-run makes zero mutating requests
    dry = sync_knowledge_base(docs=docs, primary_sink=primary, optional_sinks=optionals, state_file=state_file, dry_run=True)
    assert dry["dry_run"] is True
    assert len(recorded["calls"]) == 0
    assert all(v == "sink_skipped: unconfigured" for v in dry["optional_sinks"].values())

    # 2. First real sync uploads all docs
    first = sync_knowledge_base(docs=docs, primary_sink=primary, optional_sinks=optionals, state_file=state_file)
    assert first["collection_id"] == "col-uuid-009"
    assert len(first["upserted"]) == len(docs)
    assert len(recorded["uploads"]) == len(docs)
    assert len(recorded["assignments"]) == len(docs)

    # 3. Second sync skips 100% unchanged docs
    before_uploads = len(recorded["uploads"])
    second = sync_knowledge_base(docs=docs, primary_sink=primary, optional_sinks=optionals, state_file=state_file)
    assert second["upserted"] == []
    assert len(second["skipped_unchanged"]) == len(docs)
    assert len(recorded["uploads"]) == before_uploads

    # 4. Removing a doc prunes its ID cleanly
    removed_doc = docs[-1]
    third = sync_knowledge_base(docs=docs[:-1], primary_sink=primary, optional_sinks=optionals, state_file=state_file)
    assert third["pruned"] == [removed_doc.doc_key]
    assert f"/v3/documents/{removed_doc.deterministic_id()}" in recorded["deletes"]
