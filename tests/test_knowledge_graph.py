from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

import jsonschema
import rdflib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import verify_ecosystem_knowledge as vek  # noqa: E402

KG_JSON = REPO_ROOT / "knowledge_graph.json"
KG_GRAPHML = REPO_ROOT / "knowledge_graph.graphml"
KG_RDF = REPO_ROOT / "knowledge_graph.rdf"
KG_SCHEMA = REPO_ROOT / "data" / "schemas" / "knowledge-graph.schema.json"
ONTOLOGY_NS = "https://lgcorzo.github.io/ontology/dark-gravity#"
GRAPHML_NS = "http://graphml.graphdrawing.org/xmlns"


def _id_from_kg_uri(uri: str) -> str:
    prefix = "https://lgcorzo.github.io/kg/"
    assert uri.startswith(prefix), f"Unexpected KG URI: {uri}"
    tail = uri[len(prefix) :]
    for entity_prefix in ("repo/", "agent/", "svc/"):
        if tail.startswith(entity_prefix):
            return entity_prefix[:-1] + ":" + tail[len(entity_prefix) :]
    return tail


def test_knowledge_graph_json_schema_and_entities() -> None:
    kg = json.loads(KG_JSON.read_text(encoding="utf-8"))
    schema = json.loads(KG_SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(instance=kg, schema=schema)

    counts = kg["summary"]["counts_by_type"]
    for etype in ("Repository", "Agent", "Service", "Experiment", "ArchitectureDecision", "ResearchHypothesis"):
        assert counts[etype] >= 1, f"Missing entity type {etype}"
    assert counts["Experiment"] == 14
    assert counts["ResearchHypothesis"] == 4

    node_ids = {n["id"] for n in kg["nodes"]}
    for edge in kg["edges"]:
        assert edge["source"] in node_ids, f"Orphan edge source: {edge['source']}"
        assert edge["target"] in node_ids, f"Orphan edge target: {edge['target']}"


def test_knowledge_graph_doc011_redaction() -> None:
    for path in (KG_JSON, KG_GRAPHML, KG_RDF):
        text = path.read_text(encoding="utf-8")
        leaks = vek.detect_doc011_leaks(text, path.name)
        assert not leaks, f"DOC-011 leaks in {path.name}: {leaks}"


def test_triple_format_equivalence_json_graphml_rdf() -> None:
    kg = json.loads(KG_JSON.read_text(encoding="utf-8"))
    json_nodes = {n["id"] for n in kg["nodes"]}
    json_edges = {(e["source"], e["relation"], e["target"]) for e in kg["edges"]}

    # GraphML check
    tree = ET.fromstring(KG_GRAPHML.read_text(encoding="utf-8"))
    graph_el = tree.find(f"{{{GRAPHML_NS}}}graph")
    assert graph_el is not None
    assert graph_el.attrib.get("id") == "dark-gravity"
    assert graph_el.attrib.get("edgedefault") == "directed"

    graphml_nodes = {el.attrib["id"] for el in graph_el.findall(f"{{{GRAPHML_NS}}}node")}
    graphml_edges: set[tuple[str, str, str]] = set()
    for eel in graph_el.findall(f"{{{GRAPHML_NS}}}edge"):
        rel = next(
            dat.text for dat in eel.findall(f"{{{GRAPHML_NS}}}data") if dat.attrib.get("key") == "d_relation"
        )
        graphml_edges.add((eel.attrib["source"], rel, eel.attrib["target"]))

    assert graphml_nodes == json_nodes
    assert graphml_edges == json_edges

    # RDF/XML check via rdflib
    rdf_graph = rdflib.Graph()
    rdf_graph.parse(data=KG_RDF.read_text(encoding="utf-8"), format="xml")

    rdf_type = rdflib.RDF.type
    node_id_pred = rdflib.URIRef(f"{ONTOLOGY_NS}nodeId")

    rdf_nodes: set[str] = set()
    for s, _, o in rdf_graph.triples((None, node_id_pred, None)):
        rdf_nodes.add(str(o))
        assert any(rdf_graph.triples((s, rdf_type, None)))

    rdf_edges: set[tuple[str, str, str]] = set()
    allowed_relations = {e["relation"] for e in kg["edges"]}
    for rel in allowed_relations:
        pred = rdflib.URIRef(f"{ONTOLOGY_NS}{rel}")
        for s, _, o in rdf_graph.triples((None, pred, None)):
            rdf_edges.add((_id_from_kg_uri(str(s)), rel, _id_from_kg_uri(str(o))))

    assert rdf_nodes == json_nodes
    assert rdf_edges == json_edges


def test_incremental_synthetic_repo_and_adr_refresh(tmp_path: pathlib.Path) -> None:
    reg = json.loads((REPO_ROOT / "data" / "ecosystem-registry.json").read_text(encoding="utf-8"))
    reg["repositories"].append(
        {
            "id": "repo:synthetic-edge-module",
            "name": "synthetic-edge-module",
            "owner": "lgcorzo",
            "tier": "owned_domain",
            "visibility": "public",
            "is_fork": False,
            "archived": False,
            "fork_profile": None,
            "upstream_repo": None,
            "primary_language": "Rust",
            "role": "Synthetic test repository verifying incremental KG updates.",
            "canonical_url": "https://github.com/lgcorzo/synthetic-edge-module",
            "has_agents_md": True,
            "has_architecture_md": True,
            "has_repositories_md": True,
            "has_manifest_md": True,
            "direct_injection_target": False,
            "dependencies": ["repo:rust_CACD_autonomous_factory"],
        }
    )
    syn_reg = tmp_path / "registry.json"
    syn_reg.write_text(json.dumps(reg, indent=2), encoding="utf-8")

    adr_dir = tmp_path / "adrs"
    adr_dir.mkdir()
    (adr_dir / "adr-999-synthetic-test.md").write_text(
        "---\ntitle: \"ADR-999: Synthetic Incremental Update Test\"\nstatus: \"accepted\"\ndate: \"2026-11-27\"\ndescription: \"Validates dynamic ADR discovery.\"\ngoverns:\n  - \"repo:synthetic-edge-module\"\n---\n\n# ADR-999: Synthetic Incremental Update Test\n",
        encoding="utf-8",
    )

    out_dir = tmp_path / "out"
    start = time.monotonic()
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "knowledge_graph" / "build_knowledge_graph.py"),
            "--registry",
            str(syn_reg),
            "--adr-dirs",
            str(adr_dir),
            "--out-dir",
            str(out_dir),
            "--refresh-auditor",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed = time.monotonic() - start
    assert proc.returncode == 0, proc.stderr
    assert elapsed < 10.0, f"KG build took {elapsed:.2f}s (>= 10s)"

    syn_kg = json.loads((out_dir / "knowledge_graph.json").read_text(encoding="utf-8"))
    ids = {n["id"] for n in syn_kg["nodes"]}
    assert "repo:synthetic-edge-module" in ids
    assert "ADR-999" in ids
    assert "synthetic-edge-module" in (out_dir / "docs" / "auditor" / "ecosystem.md").read_text(encoding="utf-8")
    assert "ADR-999" in (out_dir / "docs" / "auditor" / "architecture.md").read_text(encoding="utf-8")
