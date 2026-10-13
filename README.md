# MCP Academy — Essentials Edition

**Versione / Version:** 1.0.0 — 13 October 2026

## Italiano

Questa è la prima versione funzionante di **MCP Academy**, una piattaforma web didattica interattiva sul Model Context Protocol e sulle applicazioni a Autodesk Revit.

**Contenuto pubblicato in questa versione:** solo **MCP Essentials** (5 lezioni, durata obiettivo ≤30 minuti). **Advanced non è stato sviluppato:** la sua scheda compare come «In preparazione», senza contenuti incompleti. Sarà aggiunto successivamente senza eliminare i progressi di Essentials.

### Come usare il corso

1. Apri `index.html` con un browser moderno (Chrome, Edge, Firefox o Safari). Non servono account o installazioni.
2. Seleziona **Inizia Essentials**; le lezioni sono navigabili liberamente tramite indice e passaggi numerati.
3. Cambia lingua in qualsiasi momento usando **IT / EN** in alto.
4. Esplora diagrammi, esercizi e simulazioni. **Non sono connessi a Revit**.
5. Completa le lezioni e affronta il quiz finale di 10 domande, superato con l’80%.
6. Apri **Progressi** per esportare un backup JSON o importarlo su un altro browser/dispositivo.

### Caratteristiche

- Funziona interamente lato browser, senza backend o servizi a pagamento.
- Due lingue complete: italiano e inglese.
- Diagrammi interattivi, navigazione guidata/libera, ricerca e glossario.
- Quiz con feedback, tentativi illimitati e miglior punteggio conservato.
- Dati salvati localmente (`localStorage`) quando consentito dal browser. In modalità `file://`, la persistenza può variare fra browser; in ogni caso è disponibile l’esportazione dei progressi quando il salvataggio è permesso.
- Nessuna libreria, immagine o font caricati dall'esterno.
- Link a documentazione tecnica ufficiale (richiedono Internet per essere aperti).

### Pubblicazione su GitHub Pages

**Non eseguire questi passaggi prima di avere autorizzato la pubblicazione.**

1. Crea un **repository pubblico** su GitHub, per esempio `mcp-academy`.
2. Carica nella radice del repository `index.html` e `.nojekyll`. Puoi includere anche `src/`, `build.py` e questa documentazione per permettere aggiornamenti futuri.
3. Apri **Settings → Pages** del repository.
4. In **Build and deployment**, seleziona **Deploy from a branch**, poi il branch `main` e la directory `/ (root)`.
5. Salva e attendi la pubblicazione; GitHub mostrerà l'indirizzo effettivo del sito.
6. Per aggiornare Essentials o aggiungere Advanced, aggiorna gli stessi file nel repository: l'URL può rimanere invariato.

### Modificare o ricostruire il sito

- Sorgenti in `src/data.js`, `src/app.js`, `src/style.css`, `src/template.html`.
- Per ricostruire `index.html`: `python build.py` (Python 3 standard, nessuna libreria aggiuntiva).
- Per le prossime versioni, mantenere stabili gli ID `e1`–`e5`, gli ID dei passaggi e la chiave di progressi `mcp-academy-progress-v1`, oppure introdurre una migrazione esplicita.

### Limiti

Questa edizione **non installa un MCP reale** e **non accede a modelli RVT**. I valori numerici, gli URI e i nomi dei Tools presenti nelle simulazioni sono esempi didattici, non dati estratti da Autodesk Revit. Il server Autodesk Revit MCP in Technical Preview richiede Revit 2027.2 secondo la documentazione consultata alla data di rilascio.

## English

This is the first working release of **MCP Academy**, a bilingual, browser-based learning platform about the Model Context Protocol and Autodesk Revit applications.

**Available in this edition:** **MCP Essentials only** (five lessons, designed to take at most 30 minutes). **Advanced has not been developed**; its card is clearly marked *Coming soon*.

### Quick start

1. Open `index.html` in a modern browser; no account or installation needed.
2. Select **Start Essentials**, navigate freely, and use **IT / EN** at any time.
3. Explore the four interactive activities, complete lessons, and take the ten-question final assessment (80% pass threshold).
4. Use **Progress** to export/import a JSON backup between devices.

The application is fully static, has no remote dependencies, and does not connect to any real Revit model. Some browsers restrict `localStorage` for directly opened local files; saving progress is browser-dependent in `file://` mode. Official reference links require an Internet connection.

### GitHub Pages release

After explicit authorization, create a public GitHub repository, upload `index.html` and `.nojekyll` to its root, then choose **Settings → Pages → Deploy from a branch → main → / (root)**. GitHub will supply the actual website address.

### Maintainability

Sources are in `src/`; run `python build.py` to generate a self-contained `index.html`. Keep the existing lesson identifiers and stored-progress key unchanged when adding Advanced, or implement a migration.

## Sources

- [MCP specification](https://modelcontextprotocol.io/specification/2026-07-28)
- [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- [Autodesk Revit Public MCP Server](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_revit_mcp_server_html)
- [Autodesk Revit MCP setup](https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_setting_up_revit_mcp_server_html)