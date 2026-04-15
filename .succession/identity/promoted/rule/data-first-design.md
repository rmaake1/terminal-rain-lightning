---
succession/entity-type: card
card/id: data-first-design
card/tier: rule
card/category: strategy
card/provenance:
  provenance/born-at: '2026-04-14T00:00:00Z'
  provenance/born-in-session: starter-pack
  provenance/born-from: seed
  provenance/born-context: Bundled starter card — enforces data-driven design discipline before writing code.
---

Design data-first: before writing code, define the data shapes (maps, keys, types) that each layer produces and consumes. **Applies when:** introducing new entities, changing existing data contracts, or coordinating multi-layer flows. Plans and PRs for these changes should lead with "Data shapes — what changes" showing before/after for every modified entity, then "Data flow — layer by layer" tracing how data moves through the system. Implementation (files, functions) comes last — it follows from the shapes, not the other way around. When proposing such a change, answer: what is the new shape, who produces it, who consumes it, what is the contract between them? If that isn't clear, the design isn't ready to implement. **Exempt:** targeted bug fixes, single-function refactors, and changes that touch no data contracts — for these, leading with data shapes adds friction without signal.
