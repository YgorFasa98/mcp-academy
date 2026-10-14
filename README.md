# MCP Academy · Essentials + Advanced

**Author: Ygor Fasanella · 2026**

A free, bilingual (Italian/English), self-paced website about the **Model Context Protocol (MCP)** and applying it to **Autodesk Revit 2027**. Published using GitHub Pages.

## Course structure

- **Essentials**: five interactive lessons, about 30 minutes. Entry: `index.html`.
- **Advanced**: eight modules, 28 lessons/labs, 40 assessment questions, approx. seven hours including guided exercises. Entry: `advanced.html`.
- **Optional labs**: write-tool safety exercise and a read-only Python/C# Developer Lab starter (~2.5 additional hours).

Both tracks have independent progress tracking, free navigation, IT/EN language switching, and assessment feedback. Progress is saved in localStorage and can be exported as JSON; different browsers/devices do not sync automatically. Essentials uses its pre-existing `mcp-academy-progress-v1` key and has not been migrated or reset; Advanced uses `mcp-academy-advanced-v2`.

## Repository contents

| Path | Meaning |
|---|---|
| `index.html` | Essentials single-file application; links to Advanced |
| `advanced.html` | Advanced front end |
| `assets/advanced-app.js` | Advanced navigation, widgets, quizzes and persistence |
| `assets/advanced-data.js` | Structured bilingual course content |
| `assets/advanced.css` | Advanced styling and responsive layout |
| `assets/advanced-data.json` | Editable copy of course data |
| `developer-lab/mcp-revit-starter.zip` | Optional Python + C# source-code starter |
| `build_data.py` | Generator/editor of Advanced content data |
| `ACADEMY_ARCHITECTURE.md` | Architecture, limits and update notes |

## Publishing with GitHub Pages

In repository settings, configure **Pages → Deploy from a branch → main → /(root)**. GitHub Pages serves both `index.html` and `advanced.html`. Relative links work under a project-site subpath. No backend is needed for reading the lessons or answering quizzes.

## Offline use

Download the whole repository as ZIP and open `index.html` locally. `advanced.html` loads local JS/CSS via relative paths; keep the repository folder structure intact. If a browser restricts localStorage under `file://`, progress may not persist; use export/import or serve the folder locally (`python -m http.server 8000`).

## Important BIM and tool limits

- The course uses **observed counts** from a reference IFC4X3_ADD2 export supplied for development: `IfcWall=30`, `IfcDoor=15`, `IfcWindow=7`, `IfcBuildingStorey=6`, etc. They are **not** live MCP queries.
- The original RVT and IFC files are **not hosted or redistributed**: the IFC header contains personal metadata and public redistribution must be authorised separately.
- The IFC was exported with metadata naming Autodesk Revit 27.3.0.28. Autodesk's official Revit Public MCP Technical Preview documentation currently specifies **Revit 2027.2**; compatibility with other builds requires verification.
- The optional C# Revit add-in is source code awaiting build/validation on Windows with Revit and the Revit API. It is not an Autodesk-certified solution or a tested release.
- All course materials and the static Python snapshot can be used without paid AI services; the real conversational labs use a compatible free-tier client where available. The student requires Revit for live Revit operations, and free-tier AI limits may apply.
- Read-only tools should be preferred. Optional write operations must use a project copy and explicit verification.

## Primary references

- [MCP official specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP Python SDK v2](https://py.sdk.modelcontextprotocol.io/)
- [Autodesk Revit Public MCP Server](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_revit_mcp_server_html)
- [Autodesk Revit MCP setup](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_setting_up_revit_mcp_server_html)

**Copyright © 2026 Ygor Fasanella.** No license for redistribution of the supplied RVT/IFC models is granted by this repository.