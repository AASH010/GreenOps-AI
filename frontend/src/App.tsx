import { ProvenanceBadge } from "./ProvenanceBadge";
import type { Provenance } from "./provenance";
import { PROVENANCE } from "./provenance";

// Cockpit skeleton (tasks COK-01 to COK-07). Panels are placeholders until their tasks are done.
const PANELS = [
  { id: "COK-02", name: "Topology and assets", purpose: "Site, zone, rack and server view with data provenance." },
  { id: "COK-03", name: "KPIs", purpose: "Utilization, capacity, performance, energy, temperature and alarms." },
  { id: "COK-04", name: "Cases", purpose: "Situations with evidence, data quality and status." },
  { id: "COK-05", name: "Research timeline", purpose: "Competing hypotheses and the evidence for and against each." },
  { id: "COK-06", name: "Scenario comparison", purpose: "Baseline versus candidates with trade-offs and uncertainty." },
  { id: "COK-07", name: "Decision Certificate", purpose: "Recommendation, rationale, limitations and operator review." },
];

export default function App() {
  const labels = Object.keys(PROVENANCE) as Provenance[];
  return (
    <main className="page">
      <header>
        <h1>GreenOps AI</h1>
        <p className="tagline">Autonomous data-center operations</p>
        <p className="notice" role="note">
          Competition prototype skeleton. Values will be synthetic, replayed, estimated or simulated and labelled as such.
          No production control is performed and no measured savings are claimed.
        </p>
      </header>
      <section aria-labelledby="labels">
        <h2 id="labels">Provenance labels</h2>
        <p className="legend">
          {labels.map((label) => (
            <ProvenanceBadge key={label} label={label} />
          ))}
        </p>
      </section>
      <section aria-labelledby="panels">
        <h2 id="panels">Planned cockpit panels</h2>
        <ul className="cards">
          {PANELS.map((panel) => (
            <li key={panel.id} className="card">
              <span className="id">{panel.id}</span>
              <h3>{panel.name}</h3>
              <p>{panel.purpose}</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
