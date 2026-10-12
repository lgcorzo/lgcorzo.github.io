const GITHUB_REPOS = [
  {
    "name": "rust_CACD_autonomous_factory",
    "description": "Dark Gravity CA/CD Core: Autonomous Agent Factory orchestrating Hatchet DAGs (Ingest->Plan->Code->Verify->Deliver) with Ed25519 NHI credentials & gVisor sandboxing.",
    "url": "https://github.com/lgcorzo/rust_CACD_autonomous_factory",
    "stars": 2,
    "forks": 0,
    "language": "Rust",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "Documentation_agent",
    "description": "Dark Gravity Doc Worker: Autonomous agent extracting AST codebase knowledge graphs and generating ISO/OpenWiki architecture documentation.",
    "url": "https://github.com/lgcorzo/Documentation_agent",
    "stars": 1,
    "forks": 0,
    "language": "Shell",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "fastapi-autogen-team",
    "description": "Dark Gravity Multi-Agent Pair Programming: Production FastAPI service deploying AutoGen multi-agent teams with OpenAI-compatible endpoints for code synthesis.",
    "url": "https://github.com/lgcorzo/fastapi-autogen-team",
    "stars": 1,
    "forks": 0,
    "language": "Rust",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "gitops_internal_lgcorzo",
    "description": "Dark Gravity GitOps Layer: FluxCD v2 declarative manifests, SealedSecrets, and network zero-trust policies orchestrating Dark Gravity Kubernetes clusters.",
    "url": "https://github.com/lgcorzo/gitops_internal_lgcorzo",
    "stars": 1,
    "forks": 0,
    "language": "Shell",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "Jules_remediator",
    "description": "Dark Gravity Auto-Remediator: Autonomous Kubernetes error remediation engine listening to FluxCD alerts, driving Jules SDK fixes, and auditing to MLflow.",
    "url": "https://github.com/lgcorzo/Jules_remediator",
    "stars": 1,
    "forks": 0,
    "language": "Rust",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "llmops-python-package",
    "description": "Dark Gravity LLMOps Standard: ISO/IEC/IEEE 42010 agent observability, prompt lineage, and runtime guardrails for autonomous agents in the Dark Gravity factory.",
    "url": "https://github.com/lgcorzo/llmops-python-package",
    "stars": 1,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "mlops-python-package",
    "description": "Dark Gravity MLOps Standard: Deterministic ML pipelines, DVC data versioning, MLflow S3 tracking, and model lineage testing under strict gVisor sandboxing bounds.",
    "url": "https://github.com/lgcorzo/mlops-python-package",
    "stars": 1,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "R2R-Application",
    "description": "Dark Gravity Storage & RAG UI: Full-stack dashboard for inspecting autonomous RAG retrieval pipelines, documents, and agent semantic memory.",
    "url": "https://github.com/lgcorzo/R2R-Application",
    "stars": 1,
    "forks": 0,
    "language": "TypeScript",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "R2R-Engine",
    "description": "Dark Gravity RAG Engine: Sovereign production-ready retrieval-augmented generation engine powering contextual memory and documentation retrieval for agents.",
    "url": "https://github.com/lgcorzo/R2R-Engine",
    "stars": 1,
    "forks": 0,
    "language": "Python",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "semantica",
    "description": "Dark Gravity Semantic Provenance: Graph-native context infrastructure tracking accountable AI artifacts and compliance lineage across factory workflows.",
    "url": "https://github.com/lgcorzo/semantica",
    "stars": 1,
    "forks": 0,
    "language": "Python",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "deepwiki-rs",
    "description": "Dark Gravity Architecture Knowledge Graph: High-performance Rust engine generating AST-driven OpenWiki documentation and code context for autonomous agents.",
    "url": "https://github.com/lgcorzo/deepwiki-rs",
    "stars": 0,
    "forks": 0,
    "language": "Rust",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "speckit-superpowers-bridge",
    "description": "Dark Gravity Spec-Execution Bridge: Architectural handoff connecting Spec-Driven Development (Spec Kit) with Superpowers TDD execution discipline for agents.",
    "url": "https://github.com/lgcorzo/speckit-superpowers-bridge",
    "stars": 0,
    "forks": 0,
    "language": "Shell",
    "category": "core",
    "category_label": "Autonomous Factory Core"
  },
  {
    "name": "cli",
    "description": "Dark Gravity CLI Tools: Command-line utilities for deploying and managing sovereign S3 storage infrastructure in Dark Gravity namespaces.",
    "url": "https://github.com/lgcorzo/cli",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "console",
    "description": "Dark Gravity Storage Console: Sovereign web administration dashboard for monitoring Dark Gravity S3 object storage health and bucket quotas.",
    "url": "https://github.com/lgcorzo/console",
    "stars": 1,
    "forks": 0,
    "language": "JavaScript",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "directpv",
    "description": "Dark Gravity CSI Driver: Kubernetes CSI direct-attached NVMe storage driver independently maintained for high-throughput pipeline execution.",
    "url": "https://github.com/lgcorzo/directpv",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "docs",
    "description": "Dark Gravity Sovereign Storage Docs: Complete operational architecture and API specifications for Dark Gravity's hardened S3 storage tier.",
    "url": "https://github.com/lgcorzo/docs",
    "stars": 1,
    "forks": 0,
    "language": "SCSS",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "dperf",
    "description": "Dark Gravity Network Benchmarker: High-speed TCP/UDP network throughput testing utility validating low-latency inter-agent communication.",
    "url": "https://github.com/lgcorzo/dperf",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "kes",
    "description": "Dark Gravity Sovereign KMS: Key Encryption Server providing hardware-backed zero-trust authenticated encryption at rest for sensitive model weights.",
    "url": "https://github.com/lgcorzo/kes",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "kms-go",
    "description": "Dark Gravity KMS Driver: Go client library for cryptographic key management communication across Dark Gravity storage nodes.",
    "url": "https://github.com/lgcorzo/kms-go",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "mc",
    "description": "Dark Gravity Storage CLI: MinIO Client (mc) utility independently maintained for CI/CD bucket mirroring, checkpoint archiving, and S3 permission audits.",
    "url": "https://github.com/lgcorzo/mc",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "minio",
    "description": "Dark Gravity Sovereign Storage: Hardened, zero-CVE S3 object storage server independently maintained to insulate the autonomous factory from upstream licensing closures.",
    "url": "https://github.com/lgcorzo/minio",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "minio-go",
    "description": "Dark Gravity S3 Client SDK: Hardened Go client library for zero-trust, high-throughput artifact and checkpoint transmission in Dark Gravity.",
    "url": "https://github.com/lgcorzo/minio-go",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "mint",
    "description": "Dark Gravity S3 Conformance Suite: Comprehensive S3 API compatibility verification suite executed during Dark Gravity release gates.",
    "url": "https://github.com/lgcorzo/mint",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "mtls",
    "description": "Dark Gravity Mutual TLS: Hardened cryptographic mTLS protocol utilities securing zero-trust node-to-node communication in Dark Gravity.",
    "url": "https://github.com/lgcorzo/mtls",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "mux",
    "description": "Dark Gravity HTTP Router: High-throughput HTTP multiplexer powering sovereign S3 API routing and agent telemetry endpoints.",
    "url": "https://github.com/lgcorzo/mux",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "operator",
    "description": "Dark Gravity Storage Operator: Hardened Kubernetes Operator automating in-cluster sovereign S3 storage deployment and lifecycle for Dark Gravity.",
    "url": "https://github.com/lgcorzo/operator",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "pkg",
    "description": "Dark Gravity Storage Libraries: Shared core utility and networking packages powering the sovereign S3 storage cluster in Dark Gravity.",
    "url": "https://github.com/lgcorzo/pkg",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "websocket",
    "description": "Dark Gravity Realtime Transport: Hardened WebSocket transport layer for streaming telemetry between agent runtimes and storage daemons.",
    "url": "https://github.com/lgcorzo/websocket",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "mds",
    "description": "Dark Gravity Storage Design System: Sovereign mirror of MinIO Design System powering responsive dashboards for Dark Gravity storage.",
    "url": "https://github.com/lgcorzo/mds",
    "stars": 0,
    "forks": 0,
    "language": "TypeScript",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "minio-cf",
    "description": "Dark Gravity Cloud Templates: Infrastructure-as-code deployment templates for distributed sovereign storage nodes.",
    "url": "https://github.com/lgcorzo/minio-cf",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "sidekick",
    "description": "Dark Gravity HTTP Load Balancer: High-performance sidecar load balancer optimizing S3 traffic distribution across sovereign storage pods.",
    "url": "https://github.com/lgcorzo/sidekick",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "storage",
    "category_label": "Sovereign S3 Storage"
  },
  {
    "name": "colorjson",
    "description": "Dark Gravity Telemetry Formatter: Zero-overhead syntax-highlighted JSON formatter for Dark Gravity CLI diagnostics and task inspection.",
    "url": "https://github.com/lgcorzo/colorjson",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "crc64nvme",
    "description": "Dark Gravity NVMe Checksum: CLMUL SIMD-accelerated CRC64 computation verifying NVMe block payloads at line rate in Dark Gravity.",
    "url": "https://github.com/lgcorzo/crc64nvme",
    "stars": 1,
    "forks": 0,
    "language": "Assembly",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "csvparser",
    "description": "Dark Gravity Streaming Parser: High-throughput zero-buffer CSV parser processing metric dumps without exceeding sandbox memory bounds.",
    "url": "https://github.com/lgcorzo/csvparser",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "dnscache",
    "description": "Dark Gravity Zero-Allocation DNS: Concurrent DNS caching library optimizing outbound GitPlatformPoller queries in Dark Gravity.",
    "url": "https://github.com/lgcorzo/dnscache",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "filepath",
    "description": "Dark Gravity Lexical Traversal: Flat-key filesystem traversal optimized for S3 prefix walking across sovereign storage buckets.",
    "url": "https://github.com/lgcorzo/filepath",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "highwayhash",
    "description": "Dark Gravity Stream Indexer: Assembly HighwayHash (>10 GB/s/core) enabling instantaneous AST symbol indexing and artifact hashing.",
    "url": "https://github.com/lgcorzo/highwayhash",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "madmin-go",
    "description": "Dark Gravity Storage Admin SDK: Go management SDK automating bucket quotas, node health inspection, and rolling storage updates.",
    "url": "https://github.com/lgcorzo/madmin-go",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "md5-simd",
    "description": "Dark Gravity Parallel Hashing: AVX-512 & AVX2 hardware-accelerated parallel MD5 engine for high-speed artifact deduplication.",
    "url": "https://github.com/lgcorzo/md5-simd",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "pkger",
    "description": "Dark Gravity Binary Packager: Toolchain building reproducible Debian, RPM, and APK packages for sovereign storage binaries.",
    "url": "https://github.com/lgcorzo/pkger",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "selfupdate",
    "description": "Dark Gravity Binary Updater: Secure, atomic self-update engine for sovereign CLI tools without external package manager dependencies.",
    "url": "https://github.com/lgcorzo/selfupdate",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "simdjson-go",
    "description": "Dark Gravity High-Throughput Parser: AVX-512 SIMD-accelerated JSON parser streaming gigabytes/sec within strict 30 MiB sandbox limits.",
    "url": "https://github.com/lgcorzo/simdjson-go",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "sio",
    "description": "Dark Gravity DARE Encryption: Pure Go Data At Rest Encryption (DARE) implementing authenticated encryption for model weights and tokens.",
    "url": "https://github.com/lgcorzo/sio",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "warp",
    "description": "Dark Gravity Storage Benchmark: S3 IOPS and latency stress-testing tool validating storage SLA gates before Dark Gravity deployments.",
    "url": "https://github.com/lgcorzo/warp",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "xxml",
    "description": "Dark Gravity Fast XML: High-performance memory-efficient XML 1.0 parser for parsing AWS S3 response envelopes.",
    "url": "https://github.com/lgcorzo/xxml",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "zipindex",
    "description": "Dark Gravity Archive Indexer: Compresses and indexes ZIP archives for O(1) random artifact access without full disk extraction.",
    "url": "https://github.com/lgcorzo/zipindex",
    "stars": 1,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "asm2plan9s",
    "description": "Dark Gravity SIMD Compiler: Translates AMD64 assembly into Plan 9 bytes for Go, enabling custom SIMD crypto compilation in Dark Gravity.",
    "url": "https://github.com/lgcorzo/asm2plan9s",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "blake2b-simd",
    "description": "Dark Gravity BLAKE2b Primitive: SIMD-vectorized pure Go BLAKE2b hashing for cryptographic integrity in Dark Gravity pipelines.",
    "url": "https://github.com/lgcorzo/blake2b-simd",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "certgen",
    "description": "Dark Gravity Certificate Authority: Generates self-signed TLS/mTLS X.509 certificates for air-gapped Dark Gravity Kubernetes pods.",
    "url": "https://github.com/lgcorzo/certgen",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "multipart-debug",
    "description": "Dark Gravity Streaming Diagnostics: HTTP multipart upload tracing utility for troubleshooting large model weight transfers.",
    "url": "https://github.com/lgcorzo/multipart-debug",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "sha256-simd",
    "description": "Dark Gravity Hardware Crypto: AVX-512 & ARM64 SIMD hardware-accelerated SHA256 hashing for tamper-proof artifact verification in Dark Gravity.",
    "url": "https://github.com/lgcorzo/sha256-simd",
    "stars": 0,
    "forks": 0,
    "language": "Go",
    "category": "crypto",
    "category_label": "SIMD & Hardened Crypto"
  },
  {
    "name": "Asynchronous-Optimization",
    "description": "asynchronous-optimization",
    "url": "https://github.com/lgcorzo/Asynchronous-Optimization",
    "stars": 1,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "FinRobot",
    "description": "FinRobot: An Open-Source AI Agent Platform for Financial Analysis using LLMs \ud83d\ude80 \ud83d\ude80 \ud83d\ude80 ",
    "url": "https://github.com/lgcorzo/FinRobot",
    "stars": 1,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "la_consulta_de_marta",
    "description": "Clinical psychology web platform and digital consult for Marta M\u00f3stoles, maintained under Dark Gravity continuous delivery.",
    "url": "https://github.com/lgcorzo/la_consulta_de_marta",
    "stars": 1,
    "forks": 0,
    "language": "TypeScript",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "lgcorzo.github.io",
    "description": "",
    "url": "https://github.com/lgcorzo/lgcorzo.github.io",
    "stars": 1,
    "forks": 0,
    "language": "Markdown",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "adk-rust",
    "description": "Rust Agent Development Kit (ADK-Rust): Build AI agents in Rust with modular components for models, tools, memory, realtime voice, and more. ADK-Rust is a flexible framework for developing AI agents with simplicity and power. Model-agnostic, deployment-agnostic, optimized for frontier AI models. Includes support for real-time voice agents.",
    "url": "https://github.com/lgcorzo/adk-rust",
    "stars": 0,
    "forks": 0,
    "language": "Rust",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "ai-agents-for-beginners",
    "description": "10 Lessons to Get Started Building AI Agents",
    "url": "https://github.com/lgcorzo/ai-agents-for-beginners",
    "stars": 0,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "cod_fish_classification_app",
    "description": "",
    "url": "https://github.com/lgcorzo/cod_fish_classification_app",
    "stars": 0,
    "forks": 0,
    "language": "C#",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "cod_fish_classification_keras_model",
    "description": "A keras model to classify cod fish",
    "url": "https://github.com/lgcorzo/cod_fish_classification_keras_model",
    "stars": 0,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "CodeWiki",
    "description": "[ACL 2026] Open-source framework for holistic, structured repository-level documentation across multilingual codebases",
    "url": "https://github.com/lgcorzo/CodeWiki",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "deepwiki-open",
    "description": "Open Source DeepWiki: AI-Powered Wiki Generator for GitHub/Gitlab/Bitbucket Repositories. Join the discord: https://discord.gg/gMwThUMeme",
    "url": "https://github.com/lgcorzo/deepwiki-open",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "devops_job_shop_scheduling",
    "description": "Dark Gravity Scheduling Research: Mathematical modeling and heuristic optimization of DevOps pipelines via Job Shop Scheduling (JSP).",
    "url": "https://github.com/lgcorzo/devops_job_shop_scheduling",
    "stars": 0,
    "forks": 0,
    "language": "Jupyter Notebook",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "GEN_AI_Course",
    "description": "",
    "url": "https://github.com/lgcorzo/GEN_AI_Course",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "knowledge-catalog",
    "description": "Google Cloud Knowledge Catalog Tools and Samples",
    "url": "https://github.com/lgcorzo/knowledge-catalog",
    "stars": 0,
    "forks": 0,
    "language": "TypeScript",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "lgcorzo",
    "description": "Dark Gravity Founder Profile: Architectural portfolio, sovereign infrastructure, and autonomous agent factories engineered by Luis Galo Corzo.",
    "url": "https://github.com/lgcorzo/lgcorzo",
    "stars": 0,
    "forks": 0,
    "language": "Markdown",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "mocogpt",
    "description": "MocoGPT is an GPT mock server, which can be used to test your GPT API calls.",
    "url": "https://github.com/lgcorzo/mocogpt",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "openevolve",
    "description": "Open-source implementation of AlphaEvolve",
    "url": "https://github.com/lgcorzo/openevolve",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "openwiki",
    "description": "OpenWiki is a CLI that writes and maintains agent documentation for your codebase.",
    "url": "https://github.com/lgcorzo/openwiki",
    "stars": 0,
    "forks": 0,
    "language": "TypeScript",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "rig",
    "description": "\u2699\ufe0f\ud83e\udd80 Build modular and scalable LLM Applications in Rust",
    "url": "https://github.com/lgcorzo/rig",
    "stars": 0,
    "forks": 0,
    "language": "Rust",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "spec-kit",
    "description": "\ud83d\udcab Toolkit to help you get started with SDD or any other process!",
    "url": "https://github.com/lgcorzo/spec-kit",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "superpowers",
    "description": "An agentic skills framework & software development methodology that works.",
    "url": "https://github.com/lgcorzo/superpowers",
    "stars": 0,
    "forks": 0,
    "language": "Shell",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "TradingAgents",
    "description": "TradingAgents: Multi-Agents LLM Financial Trading Framework",
    "url": "https://github.com/lgcorzo/TradingAgents",
    "stars": 0,
    "forks": 0,
    "language": "Python",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  },
  {
    "name": "vscode_developer",
    "description": "",
    "url": "https://github.com/lgcorzo/vscode_developer",
    "stars": 0,
    "forks": 0,
    "language": "Dockerfile",
    "category": "apps",
    "category_label": "Ecosystem & Apps"
  }
];
