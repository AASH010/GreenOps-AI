# dev-assistants/

AI development assistants (area A13) — **tool-agnostic**: one or more assistants, including provider-offered ones such as CodeArts Agent, may be used.

## Operating rules (draft for task DEV-02)
- Assistants run with **restricted permissions**.
- Creating cloud resources requires **explicit human confirmation**.
- Generated code passes review and tests before it is merged.
- Assistants are **not part of the product runtime**: not the Researcher, not the Safety Guard.
- Assisted work is logged as it happens (task, outcome, reviewed diff, test result) as evidence.

Skill and workflow definitions live in [`skills/`](skills/README.md).
