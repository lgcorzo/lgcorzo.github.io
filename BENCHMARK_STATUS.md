# Dark Gravity — Operational Benchmark Status

## Summary

- **Fleet-wide Benchmarks**: `UNMEASURED` (`baseline_pending`, `value: null` in `data/metrics.json`).
- **Single-Mission Execution (`N=1`)**: Mission `real-mission-e7-001-1795803707` executed `T001`–`T003` and `zeroclaw-validate` (`cargo test` in `gvisor`, `10,068 ms`). Because `N=1`, this is recorded as an operational smoke check, not a statistically meaningful fleet benchmark.
- **Jules Benchmark**: `NOT_RUN` against frozen repositories.

## Limitations

- Single-node `31 GiB` host environment; concurrent LLM/Kafka/R2R workloads affect wall-clock timings.
- Statistical confidence requires `N >= 10` reproducible runs against pinned commit snapshots.
