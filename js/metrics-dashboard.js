(() => {
  const DOMAINS = [
    ["development", "Development KPIs"],
    ["quality", "Quality KPIs"],
    ["security", "Security KPIs"],
    ["agents", "Agents KPIs"],
  ];

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function statusClass(status) {
    if (status === "verified") return "status-tag status-verified";
    if (status === "partial") return "status-tag status-implemented";
    return "status-tag status-designed";
  }

  function formatValue(item) {
    if (item.value === null || item.value === undefined || item.measurement_status === "baseline_pending") {
      return "UNMEASURED";
    }
    return `${item.value} ${item.unit}`;
  }

  async function renderMetrics() {
    const summaryEl = document.getElementById("metrics-summary");
    const containerEl = document.getElementById("metrics-domains");
    if (!summaryEl || !containerEl) return;

    try {
      const resp = await fetch("data/metrics.json", { cache: "no-store" });
      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }
      const data = await resp.json();
      summaryEl.innerHTML =
        `Snapshot <code>${escapeHtml(data.generated_at)}</code> &bull; Window: <code>${escapeHtml(data.window)}</code> &bull; Sources: <code>${escapeHtml((data.collection_sources || []).join(", "))}</code>`;

      const sections = DOMAINS.map(([key, title]) => {
        const items = (data.domains && data.domains[key]) || [];
        const rows = items
          .map(
            (item) => `
              <tr>
                <td><code>${escapeHtml(item.metric_id)}</code></td>
                <td>${escapeHtml(item.name)}</td>
                <td><strong>${escapeHtml(formatValue(item))}</strong></td>
                <td><span class="${statusClass(item.measurement_status)}">${escapeHtml(item.measurement_status)}</span></td>
                <td><a href="${escapeHtml(item.evidence_source)}">${escapeHtml(item.collection_method)}</a> &mdash; ${escapeHtml(item.notes)}</td>
              </tr>`
          )
          .join("");

        return `
          <section id="domain-${escapeHtml(key)}">
            <h2>${escapeHtml(title)}</h2>
            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th scope="col">Metric ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Value</th>
                    <th scope="col">Status</th>
                    <th scope="col">Evidence &amp; Qualification</th>
                  </tr>
                </thead>
                <tbody>${rows}</tbody>
              </table>
            </div>
          </section>`;
      });

      containerEl.innerHTML = sections.join("\n");
    } catch (err) {
      summaryEl.innerHTML =
        `Unable to fetch <code>data/metrics.json</code> dynamically (${escapeHtml(err.message)}). Inspect <a href="data/metrics.json">raw JSON</a> or <a href="docs/auditor/metrics.md">Auditor Metrics</a>.`;
    }
  }

  document.addEventListener("DOMContentLoaded", renderMetrics);
})();
