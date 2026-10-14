# MCP Academy · Essentials + Advanced

**Author: Ygor Fasanella · 2026**

A free, bilingual (Italian/English), self-paced website about the **Model Context Protocol (MCP)** and applying it to **Autodesk Revit 2027.3**. Published using GitHub Pages.

## Course structure

- **Essentials**: five interactive lessons, about 30 minutes. Entry: `index.html`.
- **Advanced**: eight modules, 28 lessons/labs, 40 assessment questions, approx. seven hours including guided exercises. Entry: `advanced.html`.
- **Optional labs**: write-tool safety exercise and a read-only Python/C# Developer Lab starter (~2.5 additional hours).

Both tracks have independent progress tracking, one cross-track **Search**, one combined modal **Glossary**, and a shared **Progress** page with selectable Essentials/Advanced tabs, plus a consistent top navigation bar, free navigation, IT/EN language switching, and assessment feedback. The Advanced percentage counts only the 28 core lessons; optional Write and Developer Labs never affect it. Progress is saved in localStorage and can be exported as JSON; different browsers/devices do not sync automatically. Essentials uses its pre-existing `mcp-academy-progress-v1` key and has not been migrated or reset; Advanced uses `mcp-academy-advanced-v2`.

## Repository contents

| Path | Meaning |
|---|---|
| `index.html` | Essentials single-file application, includes both courses’ search indices and glossary; links to Advanced |
| `advanced.html` | Advanced front end |
| `assets/advanced-app.js` | Advanced navigation, widgets, quizzes and persistence |
| `assets/advanced-data.js` | Structured bilingual course content |
| `assets/advanced.css` | Advanced styling and responsive layout |
| `assets/advanced-data.json` | Editable copy of course data |
| `src/shared-progress.js` and `.css` | Shared two-track progress overview (inlined into Essentials for offline support) |
| `src/shared-header.css` | Advanced top bar styled identically to the site-wide header |
| `src/academy-global.js` and `.css` | Global Search, unified glossary modal and Advanced-style tabbed Progress page (Essentials includes inlined copies) |
| `build.py` | Regenerates self-contained `index.html` from editable `src/` files |
| `developer-lab/mcp-revit-starter.zip` | Optional Python + C# source-code starter |
| `build_data.py` | Generator/editor of Advanced content data |
| `ACADEMY_ARCHITECTURE.md` | Architecture, limits and update notes |

## Global navigation and deep links

The Search, Glossary and Progress controls are **global** in both tracks and the home page. Search uses lesson content from both tracks (with module and step context); selecting a result opens the matching lesson or step, including cross-track results. The modal glossary merges the two dictionaries by term, keeping the existing Essentials visual language. Progress maintains Advanced's original detailed layout, with Essentials/Advanced tabs, course-specific backup tools and module/lesson summaries. Only the core 28 Advanced lessons count towards its progress bar; optional labs are separate.

Search and Progress are non-destructive overlays: Back returns to the original view and scroll position. Glossary closes using X, Escape or clicking outside. Content and translations use the same locale selected in the site header. Native progress keys, completion ids and quiz scores remain intact.

The `src/data.js` source is also included in `advanced.html` to enable global search and glossary; the Advanced data is inlined into the standalone `index.html` by `build.py`. Offline users must retain the supporting files for `advanced.html`.

## Publishing with GitHub Pages

In repository settings, configure **Pages → Deploy from a branch → main → /(root)**. GitHub Pages serves both `index.html` and `advanced.html`. Relative links work under a project-site subpath. No backend is needed for reading the lessons or answering quizzes.

## Offline use

Download the whole repository as ZIP and open `index.html` locally. `advanced.html` loads local JS/CSS via relative paths; keep the repository folder structure intact. If a browser restricts localStorage under `file://`, progress may not persist; use export/import or serve the folder locally (`python -m http.server 8000`).

## Important BIM and tool limits

- The course uses **observed counts** from a reference IFC4X3_ADD2 export supplied for development: `IfcWall=30`, `IfcDoor=15`, `IfcWindow=7`, `IfcBuildingStorey=6`, etc. They are **not** live MCP queries.
- The original RVT and IFC files are **not hosted or redistributed**: the IFC header contains personal metadata and public redistribution must be authorised separately.
- The IFC metadata identifies Autodesk Revit 27.3.0.28. MCP Academy uses **Revit 2027.3**; compatibility with the Autodesk MCP integration is confirmed by the course author. Confirm individual Tools and configurations in your installed environment.
- The optional C# Revit add-in is source code awaiting build/validation on Windows with Revit and the Revit API. It is not an Autodesk-certified solution or a tested release.
- All course materials and the static Python snapshot can be used without paid AI services; the real conversational labs use a compatible free-tier client where available. The student requires Revit for live Revit operations, and free-tier AI limits may apply.
- Read-only tools should be preferred. Optional write operations must use a project copy and explicit verification.

## Primary references

- [MCP official specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [Autodesk Revit Public MCP Server](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_revit_mcp_server_html)
- [Autodesk Revit MCP setup](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_setting_up_revit_mcp_server_html)

**Copyright © 2026 Ygor Fasanella.** No license for redistribution of the supplied RVT/IFC models is granted by this repository.

## Unified global navigation (October 2026)

The header is generated by `src/academy-header.js` on both pages. Search, Glossary, and the tabbed Progress view use the same `src/academy-global.js` regardless of the active track. The Glossary is an overlay that does not change the background route. Progress has two separate clickable cards (5 Essentials / 28 Advanced core lessons), never an Academy-wide aggregate. Old progress localStorage keys remain unchanged.