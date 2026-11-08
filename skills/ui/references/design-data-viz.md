# Design Reference: Data Visualization

Load this only when the surface is a dashboard, analytics view, chart-heavy interface, or any number-dense data display. Marketing pages, landing pages, and generic component work do not need it.

## Dashboard defaults

Start with the business question, a few core metrics and the next action. Keep time periods, units and comparison baselines consistent across related metrics.

- Primary layout: status summary at top, detail below; or sidebar filters + main chart area. The main question must be answerable without expansion; disclose supplementary records, not the answer itself. Check sparse and typical data without padding gaps with filler.
- Whitespace: tighter than marketing pages; users scan, not read. Use generous column spacing, not generous row height.
- Keep related values easy to scan. For B 端 filtering, bulk actions and table layout, see [B 端设计系统](design-b-end.md).

## Chart selection

| Use case | Chart type |
|---|---|
| Comparing values across categories | Bar chart (horizontal if labels are long) |
| Trend over time | Line chart; avoid bars for time series with many points |
| Part-to-whole relationships | Stacked bar or treemap. A pie can work for a few nonnegative, mutually exclusive categories that add up to the whole. |
| Distribution | Histogram or box plot; never pie chart |
| Correlation | Scatter plot; do not use line chart |

Label units and comparison periods. Use a bar chart or ranked list when readers need to compare close values precisely. Represent missing values explicitly.

## Number-dense interfaces

- `font-variant-numeric: tabular-nums` on every number column so digits align vertically.
- Right-align comparable values, left-align labels, and center fixed-width icon or selection columns.
- Use the project’s subtle divider and spacing tokens. Separate groups with spacing, and use a light row separator or alternating surfaces if readers lose their place.

## Using a product as a benchmark

When the user references a product for visual benchmark ("make it feel like Grafana" / "similar to Linear analytics"): extract concrete data-visualization properties from the real reference rather than relying on the product name or vague aesthetic adjectives. Useful properties: chart color palette (exact values), grid line weight and opacity, axis label size and color, tooltip border-radius and shadow, empty-state treatment. Do not extract "minimal" or "clean" as properties; those are not actionable.
