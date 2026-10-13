# MCP Academy — future-proof architecture (planning only)

**Status:** Main platform configured and Essentials content complete. Advanced content is intentionally **not started**.

## Tracks

- `essentials`: live. Lesson IDs `e1`…`e5`; step IDs `eNsM`.
- `advanced`: reserved for subsequent integration, with planned modules A1–A8 and optional Developer Lab. No lesson content, quiz questions, or placeholder lessons implemented.

## Content and UI principles

- One shared static application and one language toggle independent of track progress.
- Translations colocated with their language-neutral identifiers.
- Preserve identifiers when translations change.
- Lesson completion and assessment passing remain distinct.
- Final quiz threshold: 80%; unlimited attempts; best score persists.
- Optional laboratories must not affect the mandatory completion percentage.
- Live demonstrations and simulated data clearly distinguished.
- No paid software requirements other than Revit; free AI tiers must be verified at implementation time.

## Progress structure in v1

Browser key: `mcp-academy-progress-v1`.
Current persisted properties: `lang`, `lessonId`, `step`, `completed`, `best`.

For Advanced, add a separate `advanced` object (or key `mcp-academy-advanced-progress-v1`) without overwriting v1 Essentials data. Import/export should preserve both tracks in a migrated schema. Advanced will need model-specific expected results, to be calibrated after receipt of the RVT model.

## Future implementation workflow

1. Obtain and inspect the provided RVT learning model.
2. Verify Autodesk Revit 2027.2 MCP official available tools, free client capabilities, and environment-specific setup.
3. Author and review eight Advanced modules, including working lab prompts and model-specific verification checklists.
4. Integrate the Advanced lesson dataset and navigation, preserving stored Essentials progress and current website URL.
5. Implement optional read/write labs and Developer Lab using a guided starter project; validate on an actual Revit installation.
6. Rebuild the single-file web distribution, test offline and GitHub Pages deployments, and publish an update.

## Deployment

Static root file is `index.html`, generated from source with `python build.py`. No external runtime scripts. Hosted paths are relative, so this works under a GitHub Pages project subpath (`username.github.io/repository/`) and can be opened as a local file.

**Note:** A static site cannot run a local Autodesk MCP server or access Revit from users' browsers; the real practical labs will require a separate local Windows/Autodesk environment.