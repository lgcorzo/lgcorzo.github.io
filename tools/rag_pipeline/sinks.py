"""Knowledge sink adapters for Dark Gravity RAG pipeline (T049)."""

from __future__ import annotations

import abc
import dataclasses
import json
import os
import uuid
from typing import Any

import httpx

UUID_NAMESPACE = uuid.UUID("8f5c7f8e-3d21-4c9a-9c5b-009a6e1d4b01")


@dataclasses.dataclass(slots=True)
class RagDocument:
    doc_key: str
    source_category: str
    visibility: str
    title: str
    source_uri: str
    content: str
    content_sha256: str
    collection_name: str
    entity_refs: list[str]
    last_indexed_at: str

    def deterministic_id(self) -> str:
        return str(uuid.uuid5(UUID_NAMESPACE, self.doc_key))


class KnowledgeSink(abc.ABC):
    name: str

    @abc.abstractmethod
    def is_configured(self) -> bool:
        raise NotImplementedError

    def status_if_unconfigured(self) -> str:
        return "sink_skipped: unconfigured"

    @abc.abstractmethod
    def ensure_target(self, collection_name: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def upsert_document(self, doc: RagDocument, target_id: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_document(self, document_id: str) -> None:
        raise NotImplementedError


class R2RPgVectorSink(KnowledgeSink):
    """Primary sovereign R2R v3 + CloudNativePG pgvector sink."""

    name = "r2r_pgvector"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        *,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("R2R_BASE_URL", "http://r2r.llm-apps.svc.cluster.local:7272")).rstrip("/")
        self.api_key = api_key if api_key is not None else os.getenv("R2R_API_KEY")
        headers: dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        self._owns_client = client is None
        self._client = client or httpx.Client(base_url=self.base_url, headers=headers, timeout=60.0)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def is_configured(self) -> bool:
        return bool(self.base_url)

    def ensure_target(self, collection_name: str) -> str:
        resp = self._client.get(f"/v3/collections/name/{collection_name}")
        if resp.status_code == 200:
            payload = resp.json()
            cid = _extract_id(payload)
            if cid:
                return cid

        create_resp = self._client.post(
            "/v3/collections",
            json={
                "name": collection_name,
                "description": "Dark Gravity Autonomous Software Factory canonical knowledge base (Feature 009).",
            },
        )
        if create_resp.status_code in (200, 201, 202):
            cid = _extract_id(create_resp.json())
            if cid:
                return cid

        # Handle idempotent creation race cleanly
        retry = self._client.get(f"/v3/collections/name/{collection_name}")
        if retry.status_code == 200:
            cid = _extract_id(retry.json())
            if cid:
                return cid

        raise RuntimeError(
            f"Failed ensuring R2R collection '{collection_name}': status={create_resp.status_code} body={create_resp.text}"
        )

    def upsert_document(self, doc: RagDocument, target_id: str) -> str:
        doc_id = doc.deterministic_id()
        metadata = {
            "collection_id": target_id,
            "doc_key": doc.doc_key,
            "source_category": doc.source_category,
            "visibility": doc.visibility,
            "title": doc.title,
            "source_uri": doc.source_uri,
            "content_sha256": doc.content_sha256,
            "entity_refs": doc.entity_refs,
            "last_indexed_at": doc.last_indexed_at,
        }
        # NOTE: Deliberately omit multipart `collection_ids` (FastAPI 0.156.2 HTTP 422) and send
        # `raw_text` as multipart fields so R2R uses DocumentType.TXT without failing on non-dotted titles.
        multipart_fields = [
            ("id", (None, doc_id)),
            ("raw_text", (None, doc.content)),
            ("run_with_orchestration", (None, "true")),
            ("metadata", (None, json.dumps(metadata, ensure_ascii=False))),
        ]

        resp = self._client.post("/v3/documents", files=multipart_fields)
        if resp.status_code in (400, 409) and "already exists" in resp.text.lower():
            self.delete_document(doc_id)
            resp = self._client.post("/v3/documents", files=multipart_fields)

        if resp.status_code not in (200, 201, 202):
            raise RuntimeError(
                f"R2R POST /v3/documents failed for '{doc.doc_key}': status={resp.status_code} body={resp.text}"
            )

        returned_id = _extract_doc_id(resp.json()) or doc_id
        assign_resp = self._client.post(f"/v3/collections/{target_id}/documents/{returned_id}")
        if assign_resp.status_code not in (200, 201, 202, 204, 409):
            raise RuntimeError(
                f"R2R POST /v3/collections/{target_id}/documents/{returned_id} failed: status={assign_resp.status_code} body={assign_resp.text}"
            )
        return returned_id

    def delete_document(self, document_id: str) -> None:
        resp = self._client.delete(f"/v3/documents/{document_id}")
        if resp.status_code not in (200, 202, 204, 404):
            raise RuntimeError(
                f"R2R DELETE /v3/documents/{document_id} failed: status={resp.status_code} body={resp.text}"
            )


class Neo4jGraphSink(KnowledgeSink):
    name = "neo4j"

    def __init__(self, *, client: httpx.Client | None = None) -> None:
        self.uri = os.getenv("DARK_GRAVITY_NEO4J_URI", "").rstrip("/")
        self.user = os.getenv("DARK_GRAVITY_NEO4J_USER", "")
        self.password = os.getenv("DARK_GRAVITY_NEO4J_PASSWORD", "")
        self._client = client

    def is_configured(self) -> bool:
        return bool(self.uri and self.user and self.password)

    def ensure_target(self, collection_name: str) -> str:
        if not self.is_configured():
            return self.status_if_unconfigured()
        return collection_name

    def upsert_document(self, doc: RagDocument, target_id: str) -> str:
        if not self.is_configured():
            return self.status_if_unconfigured()
        client = self._client or httpx.Client(auth=(self.user, self.password), timeout=20.0)
        stmt = {
            "statements": [
                {
                    "statement": (
                        "MERGE (d:DarkGravityDocument {doc_key: $doc_key}) "
                        "SET d.title = $title, d.source_category = $source_category, "
                        "d.visibility = $visibility, d.content_sha256 = $sha, d.source_uri = $uri"
                    ),
                    "parameters": {
                        "doc_key": doc.doc_key,
                        "title": doc.title,
                        "source_category": doc.source_category,
                        "visibility": doc.visibility,
                        "sha": doc.content_sha256,
                        "uri": doc.source_uri,
                    },
                }
            ]
        }
        resp = client.post(f"{self.uri}/db/neo4j/tx/commit", json=stmt)
        resp.raise_for_status()
        return doc.deterministic_id()

    def delete_document(self, document_id: str) -> None:
        if not self.is_configured():
            return


class AzureAISearchSink(KnowledgeSink):
    name = "azure_ai_search"

    def __init__(self, *, client: httpx.Client | None = None) -> None:
        self.endpoint = os.getenv("DARK_GRAVITY_AZURE_SEARCH_ENDPOINT", "").rstrip("/")
        self.api_key = os.getenv("DARK_GRAVITY_AZURE_SEARCH_API_KEY", "")
        self._client = client

    def is_configured(self) -> bool:
        return bool(self.endpoint and self.api_key)

    def ensure_target(self, collection_name: str) -> str:
        return collection_name if self.is_configured() else self.status_if_unconfigured()

    def upsert_document(self, doc: RagDocument, target_id: str) -> str:
        if not self.is_configured():
            return self.status_if_unconfigured()
        client = self._client or httpx.Client(
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            timeout=20.0,
        )
        payload = {
            "value": [
                {
                    "@search.action": "mergeOrUpload",
                    "id": doc.deterministic_id(),
                    "doc_key": doc.doc_key,
                    "source_category": doc.source_category,
                    "visibility": doc.visibility,
                    "title": doc.title,
                    "content": doc.content,
                    "content_sha256": doc.content_sha256,
                }
            ]
        }
        resp = client.post(
            f"{self.endpoint}/indexes/{target_id}/docs/index?api-version=2024-07-01",
            json=payload,
        )
        resp.raise_for_status()
        return doc.deterministic_id()

    def delete_document(self, document_id: str) -> None:
        return


class DatabricksVectorSearchSink(KnowledgeSink):
    name = "databricks_vector_search"

    def __init__(self, *, client: httpx.Client | None = None) -> None:
        self.host = os.getenv("DARK_GRAVITY_DATABRICKS_HOST", "").rstrip("/")
        self.token = os.getenv("DARK_GRAVITY_DATABRICKS_TOKEN", "")
        self._client = client

    def is_configured(self) -> bool:
        return bool(self.host and self.token)

    def ensure_target(self, collection_name: str) -> str:
        return collection_name if self.is_configured() else self.status_if_unconfigured()

    def upsert_document(self, doc: RagDocument, target_id: str) -> str:
        if not self.is_configured():
            return self.status_if_unconfigured()
        client = self._client or httpx.Client(
            headers={"Authorization": f"Bearer {self.token}"},
            timeout=20.0,
        )
        resp = client.post(
            f"{self.host}/api/2.0/vector-search/indexes/{target_id}/upsert-data",
            json={
                "inputs_json": json.dumps(
                    [
                        {
                            "id": doc.deterministic_id(),
                            "doc_key": doc.doc_key,
                            "source_category": doc.source_category,
                            "visibility": doc.visibility,
                            "title": doc.title,
                            "text": doc.content,
                            "content_sha256": doc.content_sha256,
                        }
                    ]
                )
            },
        )
        resp.raise_for_status()
        return doc.deterministic_id()

    def delete_document(self, document_id: str) -> None:
        return


def _extract_id(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    results = payload.get("results")
    if isinstance(results, dict):
        return results.get("id") or results.get("collection_id")
    return payload.get("id") or payload.get("collection_id")


def _extract_doc_id(payload: Any) -> str | None:
    if not isinstance(payload, dict):
        return None
    results = payload.get("results")
    if isinstance(results, dict):
        return results.get("document_id") or results.get("id")
    return payload.get("document_id") or payload.get("id")
