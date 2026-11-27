#!/usr/bin/env python3
"""Incremental 8-Category RAG Knowledge Base Sync targeting R2R v3 + Optional Sinks (T050)."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html as html_lib
import json
import os
import pathlib
import re
import sys
from typing import Any

import httpx

if __package__ in (None, ""):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "scripts"))
import verify_ecosystem_knowledge as vek  # noqa: E402

from tools.rag_pipeline.sinks import (
    AzureAISearchSink,
    DatabricksVectorSearchSink,
    KnowledgeSink,
    Neo4jGraphSink,
    R2RPgVectorSink,
    RagDocument,
)

SOURCE_CATEGORIES = (
    "github_repo",
    "adr",
    "architecture_doc",
    "research_doc",
    "experiment",
    "metrics",
    "blog_post",
    "presentation",
)

COLLECTION_NAME = os.getenv("R2R_COLLECTION_NAME", "dark-gravity-knowledge-base")


def normalize_sha256(text: str) -> str:
    normalized = text.replace("\r\n", "\n").strip() + "\n"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def html_to_text(raw_html: str) -> str:
    without_scripts = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw_html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", without_scripts)
    return re.sub(r"\s+", " ", html_lib.unescape(text)).strip()


def extract_title(rel_path: str, content: str) -> str:
    if rel_path.endswith(".html"):
        m = re.search(r"<title>(.*?)</title>", content, re.S | re.I)
        if m:
            return html_lib.unescape(m.group(1)).strip()
    else:
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    return rel_path


def sanitize_doc011_public(text: str) -> str:
    """Redact any DOC-011 private identifiers or internal workstation paths using SHA-256 lookup."""
    redacted = vek.PRIVATE_PATH_OR_IP_RE.sub("[REDACTED-INTERNAL-PATH]", text)
    alias_by_sha = {
        "25e807c8ddcd4cb4d30a92c45e13f34b1e2f62cd2e8a98289c76dc32ecc46a63": "Internal GitOps Control Plane",
        "dec27274da7cfd135996435c4e254ba774bc1ac0921154bcef1e935bddd4b577": "Internal Incident Remediation Service",
    }

    def _replace_token(match: re.Match[str]) -> str:
        tok = match.group(0)
        digest = hashlib.sha256(tok.lower().encode("utf-8")).hexdigest()
        if digest in alias_by_sha:
            return alias_by_sha[digest]
        if digest in vek.DOC011_FORBIDDEN_REPO_SHA256:
            return "[REDACTED-PRIVATE-REPO]"
        return tok

    return re.sub(r"[A-Za-z0-9._-]+", _replace_token, redacted)


def extract_entity_refs(text: str) -> list[str]:
    refs: set[str] = set()
    refs.update(re.findall(r"\b(EXP-\d{4}-\d{3})\b", text))
    refs.update(re.findall(r"\b(ADR-\d{3,})\b", text))
    refs.update(re.findall(r"\b(RQ[1-9])\b", text))
    refs.update(re.findall(r"\b(repo:[a-z0-9._-]+|svc:[a-z0-9-]+|agent:[a-z0-9-]+)\b", text))
    return sorted(refs)[:32]


def _load_source_text(
    rel_path: str,
    *,
    data_dir: pathlib.Path | None,
    base_url: str,
    http_client: httpx.Client | None,
) -> str | None:
    if data_dir is not None:
        candidate = data_dir / rel_path
        if candidate.is_file():
            return candidate.read_text(encoding="utf-8")
    if http_client is not None:
        try:
            resp = http_client.get(f"{base_url.rstrip('/')}/{rel_path.lstrip('/')}")
            if resp.status_code == 200:
                return resp.text
        except Exception:
            return None
    return None


def collect_documents(
    *,
    data_dir: pathlib.Path | None = None,
    repos_root: pathlib.Path | None = None,
    base_url: str = "https://lgcorzo.github.io",
    collection_name: str = COLLECTION_NAME,
    include_private: bool = False,
) -> list[RagDocument]:
    now_ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    use_remote = data_dir is None or not (data_dir / "DARK_GRAVITY_MANIFEST.md").is_file()
    http_client = httpx.Client(timeout=20.0) if use_remote else None

    try:
        manifest: list[tuple[str, str, str, str]] = [
            # (doc_key, source_category, visibility, rel_path)
            ("github_repo:lgcorzo.github.io:DARK_GRAVITY_MANIFEST.md", "github_repo", "public", "DARK_GRAVITY_MANIFEST.md"),
            ("github_repo:lgcorzo.github.io:REPOSITORIES.md", "github_repo", "public", "REPOSITORIES.md"),
            ("github_repo:lgcorzo.github.io:AGENTS.md", "github_repo", "public", "AGENTS.md"),
            ("github_repo:lgcorzo.github.io:ARCHITECTURE.md", "github_repo", "public", "ARCHITECTURE.md"),
            ("architecture_doc:lgcorzo.github.io:DARK_GRAVITY_ARCHITECTURE.md", "architecture_doc", "public", "DARK_GRAVITY_ARCHITECTURE.md"),
            ("architecture_doc:lgcorzo.github.io:docs/auditor/architecture.md", "architecture_doc", "public", "docs/auditor/architecture.md"),
            ("architecture_doc:lgcorzo.github.io:architecture.html", "architecture_doc", "public", "architecture.html"),
            ("research_doc:lgcorzo.github.io:RESEARCH.md", "research_doc", "public", "RESEARCH.md"),
            ("research_doc:lgcorzo.github.io:docs/auditor/research.md", "research_doc", "public", "docs/auditor/research.md"),
            ("experiment:lgcorzo.github.io:EXPERIMENTS.md", "experiment", "public", "EXPERIMENTS.md"),
            ("experiment:lgcorzo.github.io:docs/auditor/executive-summary.md", "experiment", "public", "docs/auditor/executive-summary.md"),
            ("metrics:lgcorzo.github.io:data/metrics.json", "metrics", "public", "data/metrics.json"),
            ("metrics:lgcorzo.github.io:docs/auditor/metrics.md", "metrics", "public", "docs/auditor/metrics.md"),
            ("metrics:lgcorzo.github.io:metrics.html", "metrics", "public", "metrics.html"),
            ("blog_post:lgcorzo.github.io:index.html", "blog_post", "public", "index.html"),
            ("blog_post:lgcorzo.github.io:lifecycle.html", "blog_post", "public", "lifecycle.html"),
            ("blog_post:lgcorzo.github.io:fork-policy.html", "blog_post", "public", "fork-policy.html"),
            ("blog_post:lgcorzo.github.io:start-here/index.html", "blog_post", "public", "start-here/index.html"),
            ("blog_post:lgcorzo.github.io:ai-agents/index.html", "blog_post", "public", "ai-agents/index.html"),
            ("blog_post:lgcorzo.github.io:docs/auditor/ecosystem.md", "blog_post", "public", "docs/auditor/ecosystem.md"),
            ("presentation:lgcorzo.github.io:docs/presentations/dark-gravity-overview.md", "presentation", "public", "docs/presentations/dark-gravity-overview.md"),
        ]

        docs: list[RagDocument] = []
        for doc_key, category, visibility, rel_path in manifest:
            raw = _load_source_text(rel_path, data_dir=data_dir, base_url=base_url, http_client=http_client)
            if raw is None:
                continue
            title = extract_title(rel_path, raw)
            body = html_to_text(raw) if rel_path.endswith(".html") else raw
            docs.append(
                RagDocument(
                    doc_key=doc_key,
                    source_category=category,
                    visibility=visibility,
                    title=title,
                    source_uri=f"{base_url.rstrip('/')}/{rel_path}",
                    content=body,
                    content_sha256=normalize_sha256(body),
                    collection_name=collection_name,
                    entity_refs=extract_entity_refs(body),
                    last_indexed_at=now_ts,
                )
            )

        # ADR indexing: prefer local checked-out ADRs, else synthesize from public knowledge_graph.json
        adr_found = False
        if repos_root is not None:
            adr_dir = repos_root / "rust_CACD_autonomous_factory" / "wiki" / "architecture" / "decisions"
            if adr_dir.is_dir():
                for md in sorted(adr_dir.glob("adr-*.md")):
                    adr_found = True
                    content = sanitize_doc011_public(md.read_text(encoding="utf-8"))
                    docs.append(
                        RagDocument(
                            doc_key=f"adr:rust_CACD_autonomous_factory:wiki/architecture/decisions/{md.name}",
                            source_category="adr",
                            visibility="public",
                            title=extract_title(md.name, content),
                            source_uri=f"https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/wiki/architecture/decisions/{md.name}",
                            content=content,
                            content_sha256=normalize_sha256(content),
                            collection_name=collection_name,
                            entity_refs=extract_entity_refs(content),
                            last_indexed_at=now_ts,
                        )
                    )

        if not adr_found:
            kg_raw = _load_source_text("knowledge_graph.json", data_dir=data_dir, base_url=base_url, http_client=http_client)
            if kg_raw:
                kg = json.loads(kg_raw)
                for node in kg.get("nodes", []):
                    if node.get("entity_type") == "ArchitectureDecision":
                        summary_md = f"# {node['label']}\n\n{node['summary']}\n\nSource: {node['canonical_url']}\n"
                        docs.append(
                            RagDocument(
                                doc_key=f"adr:knowledge_graph:{node['id']}",
                                source_category="adr",
                                visibility="public",
                                title=node["label"],
                                source_uri=node["canonical_url"],
                                content=summary_md,
                                content_sha256=normalize_sha256(summary_md),
                                collection_name=collection_name,
                                entity_refs=[node["id"]],
                                last_indexed_at=now_ts,
                            )
                        )

        # Optional sibling public repos when running locally
        if repos_root is not None:
            reg_raw = _load_source_text("data/ecosystem-registry.json", data_dir=data_dir, base_url=base_url, http_client=http_client)
            if reg_raw:
                registry = json.loads(reg_raw)
                for repo in registry.get("repositories", []):
                    rname = repo.get("name", "")
                    vis = repo.get("visibility", "public")
                    if vis != "public" and not include_private:
                        continue
                    if not repo.get("direct_injection_target") or rname == "lgcorzo.github.io":
                        continue
                    repo_dir = repos_root / rname
                    if not repo_dir.is_dir():
                        continue
                    for fname in ("DARK_GRAVITY_MANIFEST.md", "ARCHITECTURE.md"):
                        fpath = repo_dir / fname
                        if fpath.is_file():
                            raw_text = fpath.read_text(encoding="utf-8")
                            text = sanitize_doc011_public(raw_text) if vis == "public" else raw_text
                            docs.append(
                                RagDocument(
                                    doc_key=f"github_repo:{rname}:{fname}",
                                    source_category="github_repo",
                                    visibility=vis,
                                    title=f"{rname} — {extract_title(fname, text)}",
                                    source_uri=f"https://github.com/lgcorzo/{rname}/blob/main/{fname}",
                                    content=text,
                                    content_sha256=normalize_sha256(text),
                                    collection_name=collection_name,
                                    entity_refs=extract_entity_refs(text),
                                    last_indexed_at=now_ts,
                                )
                            )

        docs.sort(key=lambda d: d.doc_key)
        return docs
    finally:
        if http_client is not None:
            http_client.close()


def sync_knowledge_base(
    *,
    docs: list[RagDocument],
    primary_sink: KnowledgeSink,
    optional_sinks: list[KnowledgeSink] | None = None,
    state_file: pathlib.Path,
    collection_name: str = COLLECTION_NAME,
    dry_run: bool = False,
) -> dict[str, Any]:
    prev_state: dict[str, dict[str, str]] = {}
    if state_file.is_file():
        loaded = json.loads(state_file.read_text(encoding="utf-8"))
        prev_state = loaded.get("documents", {})

    current_by_key = {d.doc_key: d for d in docs}
    to_upsert: list[RagDocument] = []
    skipped_unchanged: list[str] = []

    for doc in docs:
        prev = prev_state.get(doc.doc_key)
        if prev and prev.get("content_sha256") == doc.content_sha256:
            skipped_unchanged.append(doc.doc_key)
        else:
            to_upsert.append(doc)

    to_prune = [key for key in sorted(prev_state) if key not in current_by_key]

    sink_statuses: dict[str, str] = {}
    opt_sinks = optional_sinks or []
    for osink in opt_sinks:
        sink_statuses[osink.name] = "configured" if osink.is_configured() else osink.status_if_unconfigured()

    if dry_run:
        return {
            "dry_run": True,
            "collection_name": collection_name,
            "total_docs": len(docs),
            "upserted": [d.doc_key for d in to_upsert],
            "skipped_unchanged": skipped_unchanged,
            "pruned": to_prune,
            "categories_present": sorted({d.source_category for d in docs}),
            "optional_sinks": sink_statuses,
        }

    collection_id = primary_sink.ensure_target(collection_name)
    new_state: dict[str, dict[str, str]] = {
        key: prev_state[key] for key in skipped_unchanged
    }

    upserted_keys: list[str] = []
    for doc in to_upsert:
        doc_id = primary_sink.upsert_document(doc, collection_id)
        new_state[doc.doc_key] = {
            "doc_id": doc_id,
            "content_sha256": doc.content_sha256,
            "source_category": doc.source_category,
            "visibility": doc.visibility,
        }
        upserted_keys.append(doc.doc_key)
        for osink in opt_sinks:
            if osink.is_configured():
                osink.ensure_target(collection_name)
                osink.upsert_document(doc, collection_id)

    pruned_keys: list[str] = []
    for old_key in to_prune:
        old_id = prev_state[old_key].get("doc_id")
        if old_id:
            primary_sink.delete_document(old_id)
        pruned_keys.append(old_key)

    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(
            {
                "collection_name": collection_name,
                "collection_id": collection_id,
                "updated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "documents": new_state,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    return {
        "dry_run": False,
        "collection_name": collection_name,
        "collection_id": collection_id,
        "total_docs": len(docs),
        "upserted": upserted_keys,
        "skipped_unchanged": skipped_unchanged,
        "pruned": pruned_keys,
        "categories_present": sorted({d.source_category for d in docs}),
        "optional_sinks": sink_statuses,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Incremental 8-category Dark Gravity RAG Knowledge Base Sync.")
    parser.add_argument("--data-dir", type=pathlib.Path, default=None, help="Local lgcorzo.github.io path (optional; defaults to DARK_GRAVITY_BASE_URL)")
    parser.add_argument("--repos-root", type=pathlib.Path, default=None, help="Optional parent checkout directory for sibling public repos/ADRs")
    parser.add_argument("--base-url", type=str, default=os.getenv("DARK_GRAVITY_BASE_URL", "https://lgcorzo.github.io"))
    parser.add_argument("--r2r-url", type=str, default=os.getenv("R2R_BASE_URL", "http://r2r.llm-apps.svc.cluster.local:7272"))
    parser.add_argument("--collection", type=str, default=COLLECTION_NAME)
    parser.add_argument("--state-file", type=pathlib.Path, default=pathlib.Path(os.getenv("SYNC_STATE_FILE", "/tmp/rag-sync-state.json")))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    docs = collect_documents(
        data_dir=args.data_dir,
        repos_root=args.repos_root,
        base_url=args.base_url,
        collection_name=args.collection,
    )
    primary = R2RPgVectorSink(base_url=args.r2r_url)
    optionals: list[KnowledgeSink] = [
        Neo4jGraphSink(),
        AzureAISearchSink(),
        DatabricksVectorSearchSink(),
    ]
    try:
        summary = sync_knowledge_base(
            docs=docs,
            primary_sink=primary,
            optional_sinks=optionals,
            state_file=args.state_file,
            collection_name=args.collection,
            dry_run=args.dry_run,
        )
    finally:
        primary.close()

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
