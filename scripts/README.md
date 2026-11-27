# Dark Gravity Ecosystem Scripts & Rollout Policy

This directory contains deterministic validation and knowledge-consistency checks for Dark Gravity (`009-agent-knowledge-remediation`).

## Multi-Repository Rollout Rules

1. **Feature Branches Only (HITL Vertex 4)**: Never push directly to `main` in any Dark Gravity repository. Every rollout change uses a dedicated branch (e.g., `feat/009-agent-knowledge-remediation`) and merges via manual Pull Request review.
2. **`DOC-011` Public/Private Boundary**: Public repositories, schemas, manifests, and portal outputs MUST NEVER reference private repository names, internal cluster IPs, or local workstation paths. Private GitOps control-plane and remediation repositories are denoted generically in public documents as `"Internal GitOps Control Plane"` and `"Internal Incident Remediation Service"`.
3. **Maintained Forks & Frozen Archive Policy**:
   - The `42` maintained forks preserve `MAINTAINED_FORK_PROFILE`: no upstream directory restructuring that breaks upstream patch compatibility, no `upstream` Git remote, original `LICENSE` preserved, Fork Notice preamble, `SECURITY.md` Private Advisory routing, `[agent]` commit prefix, and hermetic builds under `v*.*.*-lgcorzo.*`.
   - `lgcorzo/kes` is permanently `archived: true` (`FROZEN_READONLY`) and is cataloged read-only without repository edits.
4. **Canonical Claim Reconciliation**: Public docs MUST match `data/canonical-claims.json` (`64` public repositories = `22` original + `42` maintained forks; `69` historical baseline; `72` Spec `004` inventory; `5` Hatchet phases post-Kafka ingestion; no claimed third-party regulatory certifications).

## Scripts

- `check_public_claims.py`: Verifies HTML portal claim consistency and linked evidence records.
- `verify_ecosystem_knowledge.py`: Verifies `data/ecosystem-registry.json`, standardized per-repository files (`AGENTS.md`, `ARCHITECTURE.md`, `REPOSITORIES.md`, `DARK_GRAVITY_MANIFEST.md`), preserved marker blocks, token budgets (`< 1,200` tokens), and `DOC-011` redaction rules.
