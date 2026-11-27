# Dark Gravity — Structured Experiment Catalog (`EXP-2026-001` .. `EXP-2026-014`)

**Human Notebook**: <https://lgcorzo.github.io/notebooks.html> · **Research Questions**: [RESEARCH.md](RESEARCH.md) · **Auditor Research Summary**: [docs/auditor/research.md](docs/auditor/research.md)

Every entry below mirrors the verified empirical records published in `notebooks.html` and serves as a deterministic source for `knowledge_graph.{json,graphml,rdf}` and `dark-gravity-mcp` (`get_experiments`). Private infrastructure repositories are referenced generically as `Internal GitOps Control Plane` and `Internal Incident Remediation Service` under `DOC-011`.

## Summary Index

| ID | Date | Title | Outcome | Related RQs | Evidence Anchor |
|---|---|---|---|---|---|
| `EXP-2026-001` | `2026-09-18` | FluxCD CI Pipeline: Kubeconform Validation False Positives on Helm Values & Raw Pod Templates | `passed` | `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-001> |
| `EXP-2026-002` | `2026-10-13` | Cargo Audit Gates vs. Unmaintained Transitive Crates | `passed` | `RQ3`, `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-002> |
| `EXP-2026-003` | `2026-10-01` | Durable Orchestration: Hatchet DAGs vs. In-House Actor State Machines | `baseline` | `RQ1`, `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-003> |
| `EXP-2026-004` | `2026-05-14` | Kubernetes Control Plane & Worker Node Hardening: CIS Benchmark Audit | `passed` | `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-004> |
| `EXP-2026-005` | `2026-06-22` | Asymmetric Secret Governance: SealedSecrets Key Rotation & Disaster Recovery | `passed` | `RQ2`, `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-005> |
| `EXP-2026-006` | `2026-07-09` | Durable Execution & Idempotency: Crash Resilience Under Node Termination | `passed` | `RQ1`, `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-006> |
| `EXP-2026-007` | `2026-08-11` | Zero-Trust Execution Boundary: Syscall Filtering and Calico Egress Blocking | `passed` | `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-007> |
| `EXP-2026-008` | `2026-08-29` | Verification Triad: Deterministic Pytest Suites vs. LLM-as-a-Judge Plausibility Bias | `passed` | `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-008> |
| `EXP-2026-009` | `2026-09-04` | AST Subgraphs vs. Raw Grep: Token Reduction and First-Pass Code Generation | `passed` | `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-009> |
| `EXP-2026-010` | `2026-09-27` | Predictable Cloud-Native Execution: Strict 512Mi Memory Clamping & Safe OOM Termination | `passed` | `RQ3`, `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-010> |
| `EXP-2026-011` | `2026-10-20` | Autonomous Security Remediation at Scale Across Historical 69-Repo Portfolio (`ADR-008` ref `#exp-2026-011-adr008`) | `passed` | `RQ1`, `RQ2`, `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-011> |
| `EXP-2026-012` | `2026-10-25` | Supply Chain Upgrade Paradox: Critical Vulnerability Triage Across Fleet & Cluster | `passed` | `RQ1`, `RQ3` | <https://lgcorzo.github.io/notebooks.html#exp-2026-012> |
| `EXP-2026-013` | `2026-11-26` | End-to-End Autonomous Mission & Hatchet-Orchestrated R2R GraphRAG Memory (Mission `#476`) | `passed` | `RQ1`, `RQ2`, `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-013> |
| `EXP-2026-014` | `2026-11-26` | Parallel Autonomous Swarm Mode Execution & Contention-Free R2R GraphRAG (Mission `#478`) | `passed` | `RQ1`, `RQ4` | <https://lgcorzo.github.io/notebooks.html#exp-2026-014> |

---

## Detailed Records

### `EXP-2026-001` — FluxCD CI Pipeline: Kubeconform Validation False Positives
- **date**: `2026-09-18`
- **outcome**: `passed`
- **related_rqs**: `RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-001`
- **hypothesis**: Filtering raw Helm values and unrendered templates eliminates false-positive schema validation failures in GitOps CI while keeping rendered manifests strictly validated.
- **key_metrics**: `{"false_positive_ci_blocks": 0, "rendered_kustomize_validation": "passed"}`

### `EXP-2026-002` — Cargo Audit Gates vs. Unmaintained Transitive Crates
- **date**: `2026-10-13`
- **outcome**: `passed`
- **related_rqs**: `RQ3, RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-002`
- **hypothesis**: Explicit risk-acceptance registries (`.cargo/audit.toml`) prevent unexploitable transitive Rust advisories from halting delivery without disabling CVE gates.
- **key_metrics**: `{"risk_register": ".cargo/audit.toml", "unexploitable_gate_bypass": false}`

### `EXP-2026-003` — Durable Orchestration: Hatchet DAGs vs. In-House Actor State Machines
- **date**: `2026-10-01`
- **outcome**: `baseline`
- **related_rqs**: `RQ1, RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-003`
- **hypothesis**: Adopting Hatchet durable workflows backed by PostgreSQL eliminates bespoke scheduler crashes during worker node eviction.
- **key_metrics**: `{"orchestrator": "Hatchet + CloudNativePG", "status": "implemented_production"}`

### `EXP-2026-004` — Kubernetes Control Plane & Worker Node Hardening
- **date**: `2026-05-14`
- **outcome**: `passed`
- **related_rqs**: `RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-004`
- **hypothesis**: Systematic CIS Kubernetes benchmark auditing eliminates privileged service accounts and enforces least-privilege RBAC across namespaces.
- **key_metrics**: `{"audit_scope": "control-plane + worker-nodes", "privileged_sa_eliminated": true}`

### `EXP-2026-005` — Asymmetric Secret Governance: SealedSecrets Key Rotation & DR
- **date**: `2026-06-22`
- **outcome**: `passed`
- **related_rqs**: `RQ2, RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-005`
- **hypothesis**: Strict-scoped Bitnami SealedSecrets allow safe public/private GitOps declarative secrets without storing private decryption keys in Git.
- **key_metrics**: `{"scope": "strict", "git_plaintext_secrets": 0}`

### `EXP-2026-006` — Durable Execution & Idempotency Under Node Termination
- **date**: `2026-07-09`
- **outcome**: `passed`
- **related_rqs**: `RQ1, RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-006`
- **hypothesis**: Hatchet step checkpointing resumes killed workflows automatically without corrupting repository state.
- **key_metrics**: `{"resume_latency_seconds": 8.4, "state_corruption": false}`

### `EXP-2026-007` — Zero-Trust Execution Boundary: Syscall Filtering & Calico Egress Blocking
- **date**: `2026-08-11`
- **outcome**: `passed`
- **related_rqs**: `RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-007`
- **hypothesis**: Combining gVisor user-space syscall interception with default-deny NetworkPolicies blocks raw sockets and unauthorized exfiltration attempts.
- **key_metrics**: `{"raw_socket_blocked": true, "egress_exfiltration_blocked": true}`

### `EXP-2026-008` — Verification Triad: Deterministic Pytest Suites vs. LLM-as-a-Judge
- **date**: `2026-08-29`
- **outcome**: `passed`
- **related_rqs**: `RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-008`
- **hypothesis**: Relying solely on LLM judges misses subtle logic defects, whereas mandatory deterministic test execution eliminates silent logic regressions.
- **key_metrics**: `{"llm_judge_false_negative_rate_pct": 44.0, "deterministic_suite_required": true}`

### `EXP-2026-009` — AST Subgraphs vs. Raw Grep
- **date**: `2026-09-04`
- **outcome**: `passed`
- **related_rqs**: `RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-009`
- **hypothesis**: 2-hop Tree-sitter AST neighborhood extraction reduces prompt context size while increasing first-pass code generation accuracy.
- **key_metrics**: `{"token_reduction_pct": 91.8, "first_pass_accuracy_pct": 94.0}`

### `EXP-2026-010` — Predictable Cloud-Native Execution: Strict 512Mi Memory Clamping
- **date**: `2026-09-27`
- **outcome**: `passed`
- **related_rqs**: `RQ3, RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-010`
- **hypothesis**: Explicit cgroup memory limits (`512Mi` compilation profile, `30Mi` micro-sandbox) prevent noisy-neighbor OOM exhaustion on host nodes.
- **key_metrics**: `{"compilation_ram_limit": "512Mi", "micro_sandbox_ram_limit": "30Mi", "host_oom_incidents": 0}`

### `EXP-2026-011` — Autonomous Security Remediation at Scale
- **date**: `2026-10-20`
- **outcome**: `passed`
- **related_rqs**: `RQ1, RQ2, RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-011`
- **hypothesis**: Separating meta-orchestration, credentialed factory controls, and surgical code-fix loops enables automated CVE remediation with sharp LLM token savings across the historical 69-repo portfolio (`64` public = `22` original + `42` maintained forks, plus `5` private/archived). Also links `ADR-008` (`#exp-2026-011-adr008`).
- **key_metrics**: `{"historical_repos_audited": 69, "public_repos_total": 64, "token_savings_pct": 85.0, "merged_remediation_prs": 10}`

### `EXP-2026-012` — Supply Chain Upgrade Paradox Across Fleet & Cluster
- **date**: `2026-10-25`
- **outcome**: `passed`
- **related_rqs**: `RQ1, RQ3`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-012`
- **hypothesis**: Synchronized lockfile exports and hash-pinned transitives prevent secondary vulnerabilities introduced by naive package bumps while reducing active Trivy cluster findings (`429 -> 396` CRITICAL, `3,660 -> 2,973` HIGH, `720` fixed).
- **key_metrics**: `{"trivy_critical_before": 429, "trivy_critical_after": 396, "trivy_high_before": 3660, "trivy_high_after": 2973, "vulnerabilities_fixed": 720}`

### `EXP-2026-013` — End-to-End Autonomous Mission & Hatchet-Orchestrated R2R GraphRAG (`Mission #476`)
- **date**: `2026-11-26`
- **outcome**: `passed`
- **related_rqs**: `RQ1, RQ2, RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-013`
- **hypothesis**: Post-merge-only R2R v3 GraphRAG ingestion orchestrated via Hatchet produces zero duplicate ingestions, reliable Leiden community graphs, and grounded MCP retrieval.
- **key_metrics**: `{"mission_id": 476, "pr_number": 477, "cycle_time_seconds": 177, "hatchet_r2r_tasks_completed": 87, "hatchet_r2r_tasks_failed": 0, "mlops_entities": 180, "mlops_relationships": 232, "mlops_communities": 17}`

### `EXP-2026-014` — Parallel Autonomous Swarm Mode & Contention-Free R2R GraphRAG (`Mission #478`)
- **date**: `2026-11-26`
- **outcome**: `passed`
- **related_rqs**: `RQ1, RQ4`
- **evidence_url**: `https://lgcorzo.github.io/notebooks.html#exp-2026-014`
- **hypothesis**: Parallel `[P]` execution across isolated gVisor lanes with `fan-in-synthesize` and read/write-split `r2r-reader` RO replicas increases throughput without Postgres/pgvector lock contention.
- **key_metrics**: `{"mission_id": 478, "pr_number": 479, "swarm_mode": true, "peak_parallel_lanes": 3, "r2r_reader_replicas": 3, "mlops_collection_docs": 5}`
