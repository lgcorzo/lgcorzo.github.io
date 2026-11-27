#!/usr/bin/env python3
"""Deterministic Multi-Format Knowledge Graph Builder for Dark Gravity (T036-T037).

Builds one shared in-memory graph across all 6 entity classes and 12 typed predicates
from ecosystem-registry.json, canonical-claims.json, RESEARCH.md, EXPERIMENTS.md,
data/metrics.json, and discovered adr-*.md files, and writes:
  - knowledge_graph.json (JSON-LD)
  - knowledge_graph.graphml (GraphML 1.0 XML)
  - knowledge_graph.rdf (RDF/XML using exact uppercase dg:<RELATION> predicates)
Optionally refreshes docs/auditor/{ecosystem,architecture,metrics}.md while preserving
DOC-011 redaction and verified: "false" defaults.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Any

import jsonschema
import rdflib
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "tools" / "metrics"))

import verify_ecosystem_knowledge as vek  # noqa: E402
from collect_platform_metrics import render_auditor_metrics_markdown  # noqa: E402

ONTOLOGY_NS = "https://lgcorzo.github.io/ontology/dark-gravity#"
GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NS = "http://www.w3.org/2000/01/rdf-schema#"

KG_SCHEMA_PATH = REPO_ROOT / "data" / "schemas" / "knowledge-graph.schema.json"
DEFAULT_ADR_DIR = REPO_ROOT.parent / "rust_CACD_autonomous_factory" / "wiki" / "architecture" / "decisions"

ALLOWED_RELATIONS = {
    "OWNS_SERVICE",
    "EXECUTES_AGENT",
    "VALIDATES_HYPOTHESIS",
    "GOVERNS_COMPONENT",
    "DEPENDS_ON",
    "PRODUCES_EVIDENCE",
    "FORKED_FROM",
    "DEPLOYED_BY",
    "AUDITS",
    "INDEXES",
    "MEASURES",
    "IMPLEMENTS",
}

ENTITY_TYPES = [
    "Repository",
    "Agent",
    "Service",
    "Experiment",
    "ArchitectureDecision",
    "ResearchHypothesis",
]


def truncate_summary(text: str, limit: int = 279) -> str:
    clean = re.sub(r"\s+", " ", text).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def kg_uri_for_id(node_id: str) -> str:
    safe = urllib.parse.quote(node_id.replace(":", "/"), safe="/-_.")
    return f"https://lgcorzo.github.io/kg/{safe}"


def parse_research_hypotheses(research_path: pathlib.Path, updated_at: str) -> list[dict[str, Any]]:
    text = research_path.read_text(encoding="utf-8")
    nodes: list[dict[str, Any]] = []
    seen: set[str] = set()
    row_re = re.compile(
        r"^\|\s*`(RQ\d+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*`([a-z_]+)`\s*\|$",
        re.M,
    )
    for m in row_re.finditer(text):
        rq_id = m.group(1).strip()
        if rq_id in seen:
            continue
        seen.add(rq_id)
        question = m.group(2).strip()
        hypothesis = m.group(3).strip()
        metrics_raw = re.findall(r"`([a-z]+\.[a-z0-9_]+)`", m.group(4))
        exps_raw = re.findall(r"`(EXP-\d{4}-\d{3})`", m.group(5))
        eval_status = m.group(6).strip()
        nodes.append(
            {
                "id": rq_id,
                "entity_type": "ResearchHypothesis",
                "label": f"{rq_id}: {question}",
                "summary": truncate_summary(hypothesis),
                "verification_status": "verified" if eval_status == "supported" else "experimental",
                "canonical_url": f"https://lgcorzo.github.io/RESEARCH.md#{rq_id.lower()}",
                "updated_at": updated_at,
                "properties": {
                    "question": question,
                    "evaluation_status": eval_status,
                    "target_metrics": metrics_raw,
                    "linked_experiments": exps_raw,
                },
            }
        )
    return nodes


def parse_experiments(experiments_path: pathlib.Path, updated_at: str) -> list[dict[str, Any]]:
    text = experiments_path.read_text(encoding="utf-8")
    nodes: list[dict[str, Any]] = []
    block_re = re.compile(
        r"^###\s+`(EXP-\d{4}-\d{3})`\s+[—-]\s+(.+?)\n(.*?)(?=^###\s+`EXP-|\Z)",
        re.M | re.S,
    )
    for m in block_re.finditer(text):
        exp_id = m.group(1).strip()
        title = m.group(2).strip()
        body = m.group(3)
        date_m = re.search(r"-\s+\*\*date\*\*:\s*`([^`]+)`", body)
        outcome_m = re.search(r"-\s+\*\*outcome\*\*:\s*`([^`]+)`", body)
        rqs_m = re.search(r"-\s+\*\*related_rqs\*\*:\s*`([^`]+)`", body)
        url_m = re.search(r"-\s+\*\*evidence_url\*\*:\s*`([^`]+)`", body)
        hyp_m = re.search(r"-\s+\*\*hypothesis\*\*:\s*(.+)", body)
        km_m = re.search(r"-\s+\*\*key_metrics\*\*:\s*`(\{.*?\})`", body)
        related_rqs = [x.strip() for x in rqs_m.group(1).split(",")] if rqs_m else []
        outcome = outcome_m.group(1).strip() if outcome_m else "baseline"
        ver_status = "verified" if outcome == "passed" else "implemented"
        try:
            key_metrics = json.loads(km_m.group(1)) if km_m else {}
        except Exception:
            key_metrics = {}
        nodes.append(
            {
                "id": exp_id,
                "entity_type": "Experiment",
                "label": title,
                "summary": truncate_summary(hyp_m.group(1).strip() if hyp_m else title),
                "verification_status": ver_status,
                "canonical_url": url_m.group(1).strip() if url_m else f"https://lgcorzo.github.io/notebooks.html#{exp_id.lower()}",
                "updated_at": f"{date_m.group(1).strip()}T00:00:00Z" if date_m else updated_at,
                "properties": {
                    "date": date_m.group(1).strip() if date_m else updated_at[:10],
                    "outcome": outcome,
                    "related_rqs": related_rqs,
                    "key_metrics": key_metrics,
                },
            }
        )
    return nodes


def discover_adr_nodes(registry_adrs: list[dict[str, Any]], adr_dirs: list[pathlib.Path], updated_at: str) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for adr in registry_adrs:
        adr_id = adr["id"]
        date_val = adr.get("date")
        by_id[adr_id] = {
            "id": adr_id,
            "entity_type": "ArchitectureDecision",
            "label": f"{adr_id}: {adr['title']}",
            "summary": truncate_summary(f"Status: {adr['status']}. Source: {adr['source_path']}."),
            "verification_status": "verified" if adr["status"] == "accepted" else "designed",
            "canonical_url": f"https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/{adr['source_path'].split('/', 1)[-1]}",
            "updated_at": f"{date_val}T00:00:00Z" if date_val else updated_at,
            "properties": {
                "adr_status": adr["status"],
                "date": date_val,
                "source_path": adr["source_path"],
                "governs": list(adr.get("governs", [])),
            },
        }

    for adr_dir in adr_dirs:
        if not adr_dir.is_dir():
            continue
        for md in sorted(adr_dir.glob("adr-*.md")):
            m = re.match(r"adr-(\d{3,})", md.name, re.I)
            if not m:
                continue
            adr_id = f"ADR-{m.group(1)}"
            raw = md.read_text(encoding="utf-8")
            fm: dict[str, Any] = {}
            fm_m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
            if fm_m:
                parsed = yaml.safe_load(fm_m.group(1))
                if isinstance(parsed, dict):
                    fm = parsed
            heading_m = re.search(r"^#\s+(.+)$", raw, re.M)
            title = fm.get("title") or (heading_m.group(1).strip() if heading_m else md.stem)
            desc = fm.get("description") or f"Architecture decision parsed from {md.name}."
            status = str(fm.get("status", "accepted" if "Accepted" in raw[:1200] else "proposed")).lower()
            if adr_id in by_id:
                by_id[adr_id]["summary"] = truncate_summary(desc)
                continue
            by_id[adr_id] = {
                "id": adr_id,
                "entity_type": "ArchitectureDecision",
                "label": title if title.startswith(adr_id) else f"{adr_id}: {title}",
                "summary": truncate_summary(desc),
                "verification_status": "verified" if status == "accepted" else "designed",
                "canonical_url": f"https://lgcorzo.github.io/docs/auditor/architecture.md#{adr_id.lower()}",
                "updated_at": updated_at,
                "properties": {
                    "adr_status": status if status in {"proposed", "accepted", "superseded", "deprecated"} else "proposed",
                    "date": str(fm.get("date") or updated_at[:10]),
                    "source_path": f"wiki/architecture/decisions/{md.name}",
                    "governs": list(fm.get("governs", ["repo:rust_CACD_autonomous_factory"])),
                },
            }
    return [by_id[k] for k in sorted(by_id)]


def build_knowledge_graph_model(
    *,
    registry_path: pathlib.Path,
    claims_path: pathlib.Path,
    research_path: pathlib.Path,
    experiments_path: pathlib.Path,
    metrics_path: pathlib.Path,
    adr_dirs: list[pathlib.Path],
    generated_at: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    registry, reg_errors = vek.validate_registry(
        registry_path=registry_path,
        claims_path=claims_path,
    )
    if reg_errors:
        raise RuntimeError(f"Ecosystem registry validation failed: {reg_errors}")

    ts = generated_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    metrics_data = json.loads(metrics_path.read_text(encoding="utf-8")) if metrics_path.is_file() else {}

    nodes: list[dict[str, Any]] = []

    for repo in registry["repositories"]:
        canon = repo.get("canonical_url") or "https://lgcorzo.github.io/docs/auditor/ecosystem.md"
        nodes.append(
            {
                "id": repo["id"],
                "entity_type": "Repository",
                "label": repo["name"],
                "summary": truncate_summary(repo["role"]),
                "verification_status": "implemented" if repo.get("archived") else "verified",
                "canonical_url": canon,
                "updated_at": ts,
                "properties": {
                    "tier": repo["tier"],
                    "visibility": repo["visibility"],
                    "is_fork": repo["is_fork"],
                    "fork_profile": repo.get("fork_profile"),
                    "upstream_repo": repo.get("upstream_repo"),
                    "primary_language": repo["primary_language"],
                    "direct_injection_target": repo["direct_injection_target"],
                    "has_agents_md": repo["has_agents_md"],
                    "has_architecture_md": repo["has_architecture_md"],
                    "has_repositories_md": repo["has_repositories_md"],
                    "has_manifest_md": repo["has_manifest_md"],
                },
            }
        )

    for agent in registry["agents"]:
        nodes.append(
            {
                "id": agent["id"],
                "entity_type": "Agent",
                "label": agent["name"],
                "summary": truncate_summary(
                    f"Role: {agent['role']}. Phases: {', '.join(agent['execution_phases'])}. Auth: {agent['nhi_auth_method']}."
                ),
                "verification_status": "implemented",
                "canonical_url": "https://lgcorzo.github.io/docs/auditor/ecosystem.md",
                "updated_at": ts,
                "properties": {
                    "role": agent["role"],
                    "execution_phases": agent["execution_phases"],
                    "sandbox_profile": agent["sandbox_profile"],
                    "hitl_constrained": agent["hitl_constrained"],
                    "nhi_auth_method": agent["nhi_auth_method"],
                    "home_repo": agent["home_repo"],
                },
            }
        )

    for svc in registry["services"]:
        if svc["id"] == "svc:gvisor":
            vstatus = "tested"
        elif svc["id"] == "svc:dark-gravity-mcp":
            vstatus = "implemented"
        else:
            vstatus = "deployed"
        nodes.append(
            {
                "id": svc["id"],
                "entity_type": "Service",
                "label": svc["name"],
                "summary": truncate_summary(
                    f"Namespace `{svc['cluster_namespace']}` ({svc['category']}): {svc['security_boundary']}."
                ),
                "verification_status": vstatus,
                "canonical_url": "https://lgcorzo.github.io/docs/auditor/architecture.md",
                "updated_at": ts,
                "properties": {
                    "category": svc["category"],
                    "cluster_namespace": svc["cluster_namespace"],
                    "upstream_repo": svc.get("upstream_repo"),
                    "security_boundary": svc["security_boundary"],
                },
            }
        )

    exp_nodes = parse_experiments(experiments_path, ts)
    rq_nodes = parse_research_hypotheses(research_path, ts)
    adr_nodes = discover_adr_nodes(registry["adrs"], adr_dirs, ts)

    nodes.extend(exp_nodes)
    nodes.extend(adr_nodes)
    nodes.extend(rq_nodes)

    nodes.sort(key=lambda n: n["id"])
    node_ids = {n["id"] for n in nodes}

    edge_map: dict[str, dict[str, Any]] = {}

    def add_edge(source: str, relation: str, target: str, evidence_url: str, confidence: str = "documented") -> None:
        if relation not in ALLOWED_RELATIONS:
            raise ValueError(f"Invalid relation '{relation}'")
        if source not in node_ids or target not in node_ids:
            return
        eid = f"edge:{source}--{relation}--{target}"
        edge_map[eid] = {
            "id": eid,
            "source": source,
            "target": target,
            "relation": relation,
            "evidence_url": evidence_url,
            "confidence": confidence,
        }

    # Repository dependencies
    for repo in registry["repositories"]:
        ev = repo.get("canonical_url") or "https://lgcorzo.github.io/data/ecosystem-registry.json"
        for dep in repo.get("dependencies", []):
            add_edge(repo["id"], "DEPENDS_ON", dep, ev, "documented")
        if repo.get("is_fork") and repo.get("dependencies"):
            for dep in repo["dependencies"]:
                if dep.startswith("svc:"):
                    add_edge(repo["id"], "FORKED_FROM", dep, ev, "verified")

    # Service ownership, upstream provenance & GitOps deployment
    for svc in registry["services"]:
        if svc.get("upstream_repo"):
            add_edge(svc["upstream_repo"], "OWNS_SERVICE", svc["id"], "https://lgcorzo.github.io/data/ecosystem-registry.json", "documented")
        add_edge(svc["id"], "DEPLOYED_BY", "repo:internal-gitops-control-plane", "https://lgcorzo.github.io/docs/auditor/ecosystem.md", "documented")

    # Agent execution bindings & home repo
    for agent in registry["agents"]:
        add_edge(agent["home_repo"], "EXECUTES_AGENT", agent["id"], "https://lgcorzo.github.io/docs/auditor/ecosystem.md", "documented")
        add_edge("svc:hatchet", "EXECUTES_AGENT", agent["id"], "https://lgcorzo.github.io/architecture.html", "documented")

    # Experiment <-> RQ validation and quantitative links
    for exp in exp_nodes:
        ev = exp["canonical_url"]
        for rq in exp["properties"].get("related_rqs", []):
            add_edge(exp["id"], "VALIDATES_HYPOTHESIS", rq, ev, "verified")
            add_edge(exp["id"], "MEASURES", rq, ev, "verified")

    add_edge("repo:mlops-python-package", "PRODUCES_EVIDENCE", "EXP-2026-013", "https://lgcorzo.github.io/notebooks.html#exp-2026-013", "verified")
    add_edge("repo:mlops-python-package", "PRODUCES_EVIDENCE", "EXP-2026-014", "https://lgcorzo.github.io/notebooks.html#exp-2026-014", "verified")
    add_edge("agent:zeroclaw", "PRODUCES_EVIDENCE", "EXP-2026-013", "https://lgcorzo.github.io/notebooks.html#exp-2026-013", "verified")
    add_edge("agent:auditor", "PRODUCES_EVIDENCE", "EXP-2026-011", "https://lgcorzo.github.io/notebooks.html#exp-2026-011", "verified")

    # ADR governance & implementation links
    for adr in adr_nodes:
        ev = adr["canonical_url"]
        for target in adr["properties"].get("governs", []):
            add_edge(adr["id"], "GOVERNS_COMPONENT", target, ev, "verified")
        add_edge("repo:rust_CACD_autonomous_factory", "IMPLEMENTS", adr["id"], ev, "verified")

    for rq in rq_nodes:
        add_edge("repo:lgcorzo.github.io", "IMPLEMENTS", rq["id"], "https://lgcorzo.github.io/RESEARCH.md", "documented")
        add_edge("svc:dark-gravity-mcp", "INDEXES", rq["id"], "https://lgcorzo.github.io/ai-agents/", "documented")

    for adr in adr_nodes:
        add_edge("svc:dark-gravity-mcp", "INDEXES", adr["id"], "https://lgcorzo.github.io/ai-agents/", "documented")
    add_edge("svc:r2r", "INDEXES", "EXP-2026-013", "https://lgcorzo.github.io/notebooks.html#exp-2026-013", "verified")
    add_edge("svc:r2r", "INDEXES", "repo:mlops-python-package", "https://lgcorzo.github.io/notebooks.html#exp-2026-014", "verified")

    # Auditing relations
    add_edge("agent:auditor", "AUDITS", "repo:rust_CACD_autonomous_factory", "https://lgcorzo.github.io/docs/auditor/executive-summary.md", "documented")
    add_edge("agent:auditor", "AUDITS", "svc:gvisor", "https://lgcorzo.github.io/docs/auditor/architecture.md", "documented")
    add_edge("agent:auditor", "AUDITS", "EXP-2026-012", "https://lgcorzo.github.io/notebooks.html#exp-2026-012", "verified")

    edges = [edge_map[k] for k in sorted(edge_map)]
    counts_by_type = {t: sum(1 for n in nodes if n["entity_type"] == t) for t in ENTITY_TYPES}

    graph_json: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": ts,
        "ontology_namespace": ONTOLOGY_NS,
        "@context": {
            "dg": ONTOLOGY_NS,
            "rdfs": RDFS_NS,
            "id": "@id",
            "entity_type": "@type",
        },
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "counts_by_type": counts_by_type,
        },
        "nodes": nodes,
        "edges": edges,
    }

    schema = json.loads(KG_SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(instance=graph_json, schema=schema)
    return graph_json, registry, metrics_data


def serialize_graphml(graph_json: dict[str, Any]) -> str:
    ET.register_namespace("", GRAPHML_NS)
    root = ET.Element(f"{{{GRAPHML_NS}}}graphml")

    node_keys = [
        ("d_entity_type", "entity_type", "string"),
        ("d_label", "label", "string"),
        ("d_summary", "summary", "string"),
        ("d_verification_status", "verification_status", "string"),
        ("d_canonical_url", "canonical_url", "string"),
        ("d_properties_json", "properties_json", "string"),
    ]
    edge_keys = [
        ("d_relation", "relation", "string"),
        ("d_evidence_url", "evidence_url", "string"),
        ("d_confidence", "confidence", "string"),
    ]
    for kid, name, ktype in node_keys:
        ET.SubElement(root, f"{{{GRAPHML_NS}}}key", {"id": kid, "for": "node", "attr.name": name, "attr.type": ktype})
    for kid, name, ktype in edge_keys:
        ET.SubElement(root, f"{{{GRAPHML_NS}}}key", {"id": kid, "for": "edge", "attr.name": name, "attr.type": ktype})

    graph_el = ET.SubElement(root, f"{{{GRAPHML_NS}}}graph", {"id": "dark-gravity", "edgedefault": "directed"})

    for node in graph_json["nodes"]:
        nel = ET.SubElement(graph_el, f"{{{GRAPHML_NS}}}node", {"id": node["id"]})
        for kid, field in (
            ("d_entity_type", "entity_type"),
            ("d_label", "label"),
            ("d_summary", "summary"),
            ("d_verification_status", "verification_status"),
            ("d_canonical_url", "canonical_url"),
        ):
            dat = ET.SubElement(nel, f"{{{GRAPHML_NS}}}data", {"key": kid})
            dat.text = str(node[field])
        pdat = ET.SubElement(nel, f"{{{GRAPHML_NS}}}data", {"key": "d_properties_json"})
        pdat.text = json.dumps(node.get("properties", {}), sort_keys=True)

    for edge in graph_json["edges"]:
        eel = ET.SubElement(
            graph_el,
            f"{{{GRAPHML_NS}}}edge",
            {"id": edge["id"], "source": edge["source"], "target": edge["target"]},
        )
        for kid, field in (
            ("d_relation", "relation"),
            ("d_evidence_url", "evidence_url"),
            ("d_confidence", "confidence"),
        ):
            dat = ET.SubElement(eel, f"{{{GRAPHML_NS}}}data", {"key": kid})
            dat.text = str(edge[field])

    ET.indent(root, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"


def serialize_rdf_xml(graph_json: dict[str, Any]) -> str:
    ET.register_namespace("rdf", RDF_NS)
    ET.register_namespace("rdfs", RDFS_NS)
    ET.register_namespace("dg", ONTOLOGY_NS)

    root = ET.Element(f"{{{RDF_NS}}}RDF")

    edges_by_source: dict[str, list[dict[str, Any]]] = {}
    for edge in graph_json["edges"]:
        edges_by_source.setdefault(edge["source"], []).append(edge)

    for node in graph_json["nodes"]:
        desc = ET.SubElement(root, f"{{{RDF_NS}}}Description", {f"{{{RDF_NS}}}about": kg_uri_for_id(node["id"])})
        ET.SubElement(desc, f"{{{RDF_NS}}}type", {f"{{{RDF_NS}}}resource": f"{ONTOLOGY_NS}{node['entity_type']}"})

        nid = ET.SubElement(desc, f"{{{ONTOLOGY_NS}}}nodeId")
        nid.text = node["id"]
        lbl = ET.SubElement(desc, f"{{{RDFS_NS}}}label")
        lbl.text = node["label"]
        vs = ET.SubElement(desc, f"{{{ONTOLOGY_NS}}}verificationStatus")
        vs.text = node["verification_status"]
        curl = ET.SubElement(desc, f"{{{ONTOLOGY_NS}}}canonicalUrl")
        curl.text = node["canonical_url"]
        sm = ET.SubElement(desc, f"{{{ONTOLOGY_NS}}}summary")
        sm.text = node["summary"]

        for edge in edges_by_source.get(node["id"], []):
            ET.SubElement(
                desc,
                f"{{{ONTOLOGY_NS}}}{edge['relation']}",
                {f"{{{RDF_NS}}}resource": kg_uri_for_id(edge["target"])},
            )

    ET.indent(root, space="  ")
    rdf_text = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode") + "\n"
    # Verify well-formed RDF/XML round-trip parsing immediately.
    g = rdflib.Graph()
    g.parse(data=rdf_text, format="xml")
    return rdf_text


def refresh_auditor_pack(
    *,
    out_root: pathlib.Path,
    graph_json: dict[str, Any],
    registry: dict[str, Any],
    metrics_data: dict[str, Any],
) -> None:
    auditor_dir = out_root / "docs" / "auditor"
    auditor_dir.mkdir(parents=True, exist_ok=True)
    as_of = graph_json["generated_at"][:10]

    # 1. ecosystem.md
    stats = registry["repository_statistics"]
    repo_rows = []
    for node in graph_json["nodes"]:
        if node["entity_type"] != "Repository":
            continue
        p = node["properties"]
        name = f"[{node['label']}]({node['canonical_url']})" if p["visibility"] == "public" else f"`{node['label']}` (`DOC-011`)"
        profile = p.get("fork_profile") or "First-party"
        repo_rows.append(f"| {name} | `{p['visibility']}` | `{p['tier']}` | `{profile}` | {node['summary']} |")

    eco_md = "\n".join(
        [
            "---",
            'title: "Dark Gravity AI Auditor Pack — Ecosystem Topology & Fork Policy"',
            'doc_role: "ecosystem"',
            'schema_version: "1.0"',
            f'as_of_date: "{as_of}"',
            'verification_status: "verified"',
            'verified: "false"',
            'visibility: "public"',
            "canonical_sources:",
            '  - "https://lgcorzo.github.io/data/ecosystem-registry.json"',
            '  - "https://lgcorzo.github.io/data/canonical-claims.json"',
            '  - "https://lgcorzo.github.io/REPOSITORIES.md"',
            '  - "https://lgcorzo.github.io/fork-policy.html"',
            "---",
            "",
            "# Ecosystem Repository Map & Fork Governance",
            "",
            f"- **Public Portfolio**: **`{stats['public_repositories_total']}`** repositories (`{stats['original_repositories']}` original + `{stats['maintained_forks']}` maintained open-source forks under `MAINTAINED_FORK_PROFILE`).",
            f"- **Historical Baseline**: `{stats['historical_portfolio_total_with_private_and_archived']}` (`EXP-2026-011`).",
            f"- **Spec `004` Inventory**: `{stats['spec_004_total']}` (`{stats['spec_004_public']}` public + `{stats['spec_004_private']}` private anonymized under `DOC-011`).",
            "- **Archived Fork Exception**: `lgcorzo/kes` is permanently **`FROZEN_READONLY`** (`archived: true`).",
            "",
            "| Repository / Alias | Visibility | Tier | Profile | Summary |",
            "|---|---|---|---|---|",
            *repo_rows,
            "",
        ]
    )

    # 2. architecture.md
    adr_rows = []
    for node in graph_json["nodes"]:
        if node["entity_type"] != "ArchitectureDecision":
            continue
        p = node["properties"]
        adr_rows.append(f"| `{node['id']}` | {node['label']} | `{p['adr_status']}` | {node['summary']} |")

    arch_md = "\n".join(
        [
            "---",
            'title: "Dark Gravity AI Auditor Pack — System Architecture"',
            'doc_role: "architecture"',
            'schema_version: "1.0"',
            f'as_of_date: "{as_of}"',
            'verification_status: "mixed"',
            'verified: "false"',
            'visibility: "public"',
            "canonical_sources:",
            '  - "https://lgcorzo.github.io/architecture.html"',
            '  - "https://lgcorzo.github.io/ARCHITECTURE.md"',
            '  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/Cargo.toml"',
            '  - "https://github.com/lgcorzo/rust_CACD_autonomous_factory/blob/main/wiki/architecture/decisions/adr-008-google-ax-crd-workspace-standard-v3.1.md"',
            "---",
            "",
            "# System Architecture Overview",
            "",
            "1. **5-Crate Rust Edition 2024 Workspace**: `factory-core`, `factory-application`, `factory-infrastructure`, `factory-mcp-server`, `factory-cli` (`rust_CACD_autonomous_factory`).",
            "2. **Orchestration (`Kafka -> 5 Hatchet Steps`)**: `rustant-plan`, `zeroclaw-execute`, `zeroclaw-validate`, `rustant-review`, `factory-deliver` (strict Vertex 4 HITL blocks autonomous merge).",
            "3. **Security & Isolation**: `gVisor (runsc)` (`30Mi`/`250m` micro-sandbox; `512Mi`/`500m` compilation), Ed25519 W3C-VC NHI, 300 s Vault JIT (`54.2 ns` `ZeroizeOnDrop`), OpenZiti mTLS 1.3. **`FR-008`/`CTRL-02` remains labeled `TESTED` while `AUD-010` is open.**",
            "4. **Read-Only Knowledge MCP (`dark-gravity-mcp`)**: Decoupled Rust Edition 2024 `rmcp` server in `lgcorzo.github.io/dark-gravity-mcp/`.",
            "",
            "## Indexed Architecture Decision Records",
            "",
            "| ADR ID | Title | Status | Summary |",
            "|---|---|---|---|",
            *adr_rows,
            "",
        ]
    )

    (auditor_dir / "ecosystem.md").write_text(eco_md, encoding="utf-8")
    (auditor_dir / "architecture.md").write_text(arch_md, encoding="utf-8")
    if metrics_data:
        (auditor_dir / "metrics.md").write_text(render_auditor_metrics_markdown(metrics_data), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build deterministic Dark Gravity Knowledge Graph exports.")
    parser.add_argument("--registry", type=pathlib.Path, default=REPO_ROOT / "data" / "ecosystem-registry.json")
    parser.add_argument("--claims", type=pathlib.Path, default=REPO_ROOT / "data" / "canonical-claims.json")
    parser.add_argument("--research", type=pathlib.Path, default=REPO_ROOT / "RESEARCH.md")
    parser.add_argument("--experiments", type=pathlib.Path, default=REPO_ROOT / "EXPERIMENTS.md")
    parser.add_argument("--metrics", type=pathlib.Path, default=REPO_ROOT / "data" / "metrics.json")
    parser.add_argument("--adr-dirs", type=pathlib.Path, nargs="*", default=[DEFAULT_ADR_DIR])
    parser.add_argument("--out-dir", type=pathlib.Path, default=REPO_ROOT)
    parser.add_argument("--auditor-root", type=pathlib.Path, default=None, help="Root directory for --refresh-auditor (defaults to --out-dir)")
    parser.add_argument("--refresh-auditor", action="store_true")
    parser.add_argument("--generated-at", type=str, default=None)
    args = parser.parse_args()

    graph_json, registry, metrics_data = build_knowledge_graph_model(
        registry_path=args.registry,
        claims_path=args.claims,
        research_path=args.research,
        experiments_path=args.experiments,
        metrics_path=args.metrics,
        adr_dirs=args.adr_dirs,
        generated_at=args.generated_at,
    )

    json_text = json.dumps(graph_json, indent=2) + "\n"
    graphml_text = serialize_graphml(graph_json)
    rdf_text = serialize_rdf_xml(graph_json)

    for label, payload in (
        ("knowledge_graph.json", json_text),
        ("knowledge_graph.graphml", graphml_text),
        ("knowledge_graph.rdf", rdf_text),
    ):
        leaks = vek.detect_doc011_leaks(payload, label)
        if leaks:
            for leak in leaks:
                print(f"ERROR: {leak}", file=sys.stderr)
            return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "knowledge_graph.json").write_text(json_text, encoding="utf-8")
    (args.out_dir / "knowledge_graph.graphml").write_text(graphml_text, encoding="utf-8")
    (args.out_dir / "knowledge_graph.rdf").write_text(rdf_text, encoding="utf-8")

    if args.refresh_auditor:
        auditor_root = args.auditor_root or args.out_dir
        refresh_auditor_pack(
            out_root=auditor_root,
            graph_json=graph_json,
            registry=registry,
            metrics_data=metrics_data,
        )

    s = graph_json["summary"]
    print(f"OK: Built knowledge_graph.{{json,graphml,rdf}} with {s['node_count']} nodes and {s['edge_count']} edges.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
