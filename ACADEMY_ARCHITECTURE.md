# MCP Academy — Architecture note (v2)

Author: **Ygor Fasanella**. Updated October 2026.

## Paths and state

| Track | Entry | Storage key |
|---|---|---|
| Essentials (existing) | `index.html` | `mcp-academy-progress-v1` |
| Advanced | `advanced.html` | `mcp-academy-advanced-v2` |

The language toggle in Advanced updates the existing Essentials key's `lang` property in-place, preserving progress and `best`; Essentials remains unchanged otherwise. Advanced initialises from the Essentials language if its own key does not yet exist.

## Why a separate static page?

To preserve the approved Essentials single-file experience and its stable state schema. Advanced has independent modules, module quizzes, optional labs and model snapshots. Both run on GitHub Pages, without backend, accounts, or network calls from app code. The only external URLs are user-initiated links to primary documentation.

## Authoring and reproducibility

- `build_data.py` regenerates `assets/advanced-data.js`/`.json`, with 28 bilingual lessons and 40 module questions.
- Advanced source is readable, with no paid or bundled external dependencies.
- Interactive IFC widgets are **static educational snapshots**, based on raw EXPRESS/STEP entity counts observed in the supplied IFC4X3_ADD2 export. They do not connect to Revit.
- Developer Lab starter is source code only, awaiting validation/compilation on a Windows Revit 2027.3 workstation.

## Security and distribution

- Do **not** add the user's raw IFC or RVT to GitHub until public redistribution and metadata/privacy are expressly approved.
- IFC export header may contain email and organisational metadata; only non-identifying counts and type names are included on the website.
- The Developer Lab localhost bridge is unauthenticated and read-only; it must not be exposed outside a trusted lab computer without authentication and further hardening.
- The course targets **Revit 2027.3**. Compatibility with the MCP integration is confirmed by the course author. The provided IFC export metadata indicates Revit 27.3.0.28. Actual lab results and exact Tools must be checked on the target machine.

## Testing expectation

Automated browser tests: lessons, navigation, quiz threshold, language continuity, new/old progress preservation, optional lab checklist, and local static asset accessibility. Independently validate the Revit API starter on the target Revit build before presenting it as fully operational.