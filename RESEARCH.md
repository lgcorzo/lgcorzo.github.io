# Dark Gravity — Explicit Research Vision & Research Questions (`RQ1`–`RQ4`)

**Canonical Portal**: <https://lgcorzo.github.io/start-here> · **Agent Hub**: <https://lgcorzo.github.io/ai-agents> · **Auditor Pack**: <https://lgcorzo.github.io/docs/auditor/>

## 1. Research Vision

Dark Gravity investigates whether **autonomous AI software engineering agents** can operate inside **deterministic security, kernel, budget, and governance boundaries** across a multi-repository Kubernetes platform while maintaining verifiable engineering traceability and mandatory **Human-in-the-Loop (HITL)** merge control.

All claims follow strict epistemic hygiene:
- **Verification Lifecycle**: `OPEN -> IMPLEMENTED -> TESTED -> VERIFIED` (`mock` evidence is never accepted for `verified` claims).
- **Qualification of `FR-008` / `CTRL-02`**: Live `gVisor (runsc)` sandbox admission and exit remain labeled **`TESTED`** while host CRI shim finding `AUD-010` remains open (`CTRL-04/05/07/08` are `runtime_verified`).
- **Zero Fabricated Metrics**: Fleet-wide aggregates without multi-run verifiable telemetry are marked `UNMEASURED` / `baseline_pending` (`value: null`) in [data/metrics.json](data/metrics.json) and [docs/auditor/metrics.md](docs/auditor/metrics.md).
- **Regulatory Scope**: Controls implement architectural readiness (EU AI Act Art. 12/14, SOC 2 Type II, ISO/IEC 25059); **no third-party certification is claimed**.
- **`DOC-011` Disclosure Boundary**: Public research documents never expose private repository names, cluster secrets, internal IPs, or local workstation paths.

---

## 2. Formal Research Questions & Hypothesis Matrix (`RQ1`–`RQ4`)

| ID | Research Question | Hypothesis Statement | Target KPIs (`metric_id`) | Linked Experiments | Evaluation Status |
|---|---|---|---|---|---|
| `RQ1` | Can autonomous agents safely reduce Mean Time to Recovery (`MTTR`) under strict HITL gates? | Contract-driven agent pipelines backed by durable Hatchet checkpoints, R2R GraphRAG context, and Review Guidance loops reduce remediation cycle time and MTTR without sacrificing CI verification or Vertex 4 human approval. | `development.mttr_hours`, `development.cycle_time_hours`, `security.mean_remediation_time_hours`, `agents.agent_success_rate_pct` | `EXP-2026-003`, `EXP-2026-006`, `EXP-2026-011`, `EXP-2026-012`, `EXP-2026-013`, `EXP-2026-014` | `partially_supported` |
| `RQ2` | Can cryptographic Non-Human Identities (NHI) and Verifiable Credentials improve governance and traceability? | Binding agent missions to Ed25519 W3C Verifiable Credentials (`Ed25519Signature2020`), 300 s Vault JIT tokens (`54.2 ns` `ZeroizeOnDrop`), LiteLLM `X-Vtag-*` FinOps headers, and causal Semantica lineage yields tamper-evident attribution across multi-repo PRs. | `agents.hitl_approval_rate_pct`, `agents.agent_success_rate_pct`, `development.lead_time_hours` | `EXP-2026-005`, `EXP-2026-011`, `EXP-2026-013` | `evidence_collecting` |
| `RQ3` | Can declarative GitOps, admission policies, and kernel sandboxing act as an enforceable security boundary? | Combining FluxCD v2 declarative reconciliation, OpenZiti mTLS 1.3, default-deny NetworkPolicies, `ValidatingAdmissionPolicy` resource clamps (`<= 30 Mi` / `250m` micro-sandbox, `<= 512 Mi` / `500m` compilation), and `gVisor (runsc)` prevents privilege escalation and fleet regressions. | `security.vulnerabilities_found_count`, `security.vulnerabilities_fixed_count`, `quality.escaped_defects_count` | `EXP-2026-001`, `EXP-2026-002`, `EXP-2026-004`, `EXP-2026-005`, `EXP-2026-006`, `EXP-2026-007`, `EXP-2026-010`, `EXP-2026-011`, `EXP-2026-012` | `partially_supported` |
| `RQ4` | Can structured, AST- and GraphRAG-grounded agentic workflows outperform ad-hoc workflows on reliability and token efficiency? | Pairing AST neighborhood extraction (`OSR < 5%`), deterministic test verification (replacing pure LLM judges), R2R Leiden GraphRAG with `r2r-reader` RO replicas, and parallel Swarm `[P]` execution yields higher first-pass accuracy and lower token overhead per merged PR. | `agents.autonomous_completion_rate_pct`, `quality.pr_acceptance_rate_pct`, `quality.defect_density_per_kloc`, `development.deployment_frequency_per_week` | `EXP-2026-002`, `EXP-2026-003`, `EXP-2026-008`, `EXP-2026-009`, `EXP-2026-010`, `EXP-2026-013`, `EXP-2026-014` | `partially_supported` |

---

## 3. Detailed Question Framing

### `RQ1` — Reducing MTTR Without Removing Human Merge Authority
- **Anchor Observations**: `EXP-2026-006` demonstrated Hatchet workflow recovery within `8.4 s` after worker pod termination; `EXP-2026-013` (Mission `#476`) completed the 5-step Hatchet DAG (`rustant-plan`, `zeroclaw-execute`, `zeroclaw-validate`, `rustant-review`, `factory-deliver`) in `2m57s` (`0.049 h`); `EXP-2026-014` (Mission `#478`) validated `swarm_mode=true` (`peak_parallel_lanes=3`).
- **Pending Multi-Run Baseline**: Cross-fleet multi-month `development.mttr_hours` and `security.mean_remediation_time_hours` averages remain marked `baseline_pending` (`UNMEASURED`) until continuous collector snapshots accumulate sufficient merged-PR telemetry.

### `RQ2` — Verifiable Governance Over Non-Human Agent Identities
- **Anchor Observations**: `ed25519-dalek` v2 payload signing, 300 s Vault JIT credentials wiped in `54.2 ns` (`ZeroizeOnDrop`), LiteLLM `X-Vtag-*` cost telemetry (`+$1.00 / 60s` velocity guard, `90%` daily hard-stop), and strict Vertex 4 HITL enforcement (`autonomous merge prohibited`) are implemented and tested.
- **Next Verification Milestones**: Closing multi-run `agents.hitl_approval_rate_pct` collection across sustained autonomous missions and integrating `dark-gravity-mcp` audit consumption.

### `RQ3` — GitOps & Sandboxing as a First-Class Security Boundary
- **Anchor Observations**: `EXP-2026-012` tracked cluster/fleet Trivy remediation from `429 -> 396` CRITICAL and `3,660 -> 2,973` HIGH (`720` fixed) with `9/11` audit findings (`AUD-001`..`AUD-009`) closed and `CTRL-04/05/07/08` `runtime_verified`. `FR-008` / `CTRL-02` stays **`TESTED`** while `AUD-010` remains open.

### `RQ4` — Structured Spec-Driven + GraphRAG Agent Engineering
- **Anchor Observations**: `EXP-2026-008` exposed a `44%` false-negative rate when relying solely on LLM-as-a-Judge checks, motivating mandatory deterministic test execution. `EXP-2026-009` achieved `91.8%` token reduction and `94%` first-pass code accuracy via 2-hop AST subgraphs (`deepwiki-rs`), while `EXP-2026-013` achieved `87` COMPLETED / `0` failed Hatchet R2R tasks (`180` entities, `232` relationships, `17` communities in `lgcorzo-mlops-python-package`).
