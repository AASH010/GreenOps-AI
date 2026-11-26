import type { Provenance } from "./provenance";
import { PROVENANCE } from "./provenance";

export function ProvenanceBadge({ label }: { label: Provenance }) {
  return (
    <span className={`badge badge-${label.toLowerCase()}`} title={PROVENANCE[label]}>
      {label}
    </span>
  );
}
