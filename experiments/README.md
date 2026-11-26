# experiments/

Reproducible evaluation (area A11). Methodology: [`docs/methodology`](../docs/methodology/README.md).

| Folder | Content |
|---|---|
| `systems/` | Implementations or configurations of System A (traditional baseline), System B (without Researcher) and System C (full) |
| `scenarios/` | Scenario definitions: traces, initial states, injected conditions, constraints |
| `configs/` | Fixed configurations with seeds and disclosed compute budgets, including ablation switches |
| `results/` | Recorded outputs and the evaluation report (measured values only) |

Every experiment needs matched scenarios, a fixed seed, a defined metric calculation, recorded outputs and one reproducible command. The metrics are pre-registered (task EVL-01) before any result is collected. The harness arrives with task EVL-03. **No result exists yet.**
