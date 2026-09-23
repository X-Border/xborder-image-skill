# Category profiles — per-category buyer concerns and visual systems

The shared files (`SKILL.md`, `amazon-image-strategy.md`) hold category-agnostic
craft: modes, evidence rules, layout decisions, thumbnail hierarchy, anti-AI-poster
rules. A category profile adds only what that category knows: buyer-concern priority
order, recommended secondary-image pool, carousel patterns, scene/prop/persona
language, and safety notes.

## Resolution at runtime (SKILL.md STEP 0)

Detect the category from the product photo, analysis, and request. If a profile file
here matches, load it on top of the shared rules. If none matches, derive category
norms from the product itself and the competitor scan — do not borrow another
category's props, scenes, or personas.

## Files

| file | status |
|---|---|
| `fitness-equipment.md` | ✅ extracted from the original fitness-flavored guidance |

## Adding a category (checklist)

1. Copy an existing profile's headings.
2. Fill: buyer-concern priority order, recommended secondary-image pool, category
   carousel patterns, scene/prop/persona language, compliance and safety notes.
3. Keep it category-specific — anything true for all products belongs in the shared
   files, not here.
4. Do not duplicate platform rules (`platforms/`) or the backend contract
   (`image-backend.md`); profiles compose with those, they never override them.
