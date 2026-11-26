# Evaluation methodology

Summary of the approach; tasks are in [`TRACKING.md`](../../TRACKING.md) (area A11). **No numerical performance, energy-saving, accuracy or cost-reduction result is promised in advance.**

## Three systems on identical inputs
| System | Configuration | Question |
|---|---|---|
| A — Traditional baseline | Monitoring, rule/statistical detection, conventional optimizer | How does a conventional workflow perform? |
| B — Without Researcher | Cockpit, Digital Twin, forecasting, optimizer, safety | What does the integrated platform add? |
| C — Full | System B plus the continuous Researcher and active experiment selection | Does the Researcher add value beyond B? |

All three run on identical workload traces, initial states, scenario seeds, constraints and disclosed compute budgets.

## Measured dimensions
Operational outcomes (SLA and performance, energy, thermal constraints, resource use) · research quality (diagnosis quality, hypothesis discrimination, time to diagnosis) · experiment efficiency (experiments to evidence, information gain, runtime and cost) · verification quality (repeatability, uncertainty, false improvement claims) · safety (hard-constraint violations, guard behaviour, audit completeness, cloud-loss behaviour).

## Ablations
No active experiment selection · no competing hypotheses · no research memory · no uncertainty reporting.

## Core pass condition
System C shows a meaningful incremental improvement over System B on at least one **pre-registered** research metric, without unacceptable operational regression or overhead. Negative results are reported. The metrics are recorded before any result is collected (task EVL-01).

## Reporting rules
- Distinguish measured, replayed, estimated and simulated data in every table.
- Report limitations and failed cases next to positive results.
- Never report a single headline metric without the test setup.
