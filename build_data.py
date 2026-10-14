import json
from pathlib import Path
ROOT=Path(__file__).parent
MODULES=[]
def mod(mid,it,en,mins,subtitle_it,subtitle_en):
    module={'id':mid,'title':{'it':it,'en':en},'subtitle':{'it':subtitle_it,'en':subtitle_en},'mins':mins,'lessons':[],'quiz':[]}
    MODULES.append(module)
    return module

def add(m,code,it,en,mins,ex_it,ex_en,mechanism_it,mechanism_en,example_it,example_en,task_it,task_en,check_it,check_en,code_text='',kind='theory'):
    def step(st_it,st_en,text_it,text_en,syntax=None,widget=None):
        x={'title':{'it':st_it,'en':st_en},'text':{'it':text_it,'en':text_en}}
        if syntax:x['code']=syntax
        if widget:x['widget']=widget
        return x
    m['lessons'].append({'id':code,'title':{'it':it,'en':en},'mins':mins,'kind':kind,'steps':[
        step('Il concetto','The concept',ex_it,ex_en),
        step('Come funziona','How it works',mechanism_it,mechanism_en,code_text or None),
        step('Caso applicativo','Applied example',example_it,example_en,widget='ifc' if kind=='ifc' else ('flow' if kind=='flow' else None)),
        step('Esercitazione e verifica','Practice and verify',task_it+'\n\n**Controllo:** '+check_it,task_en+'\n\n**Check:** '+check_en)
    ]})

def quiz(m,items):
    for it_q,en_q,it_opts,en_opts,ans,it_ex,en_ex in items:
        assert len(it_opts)==len(en_opts)==3 and ans in range(3)
        m['quiz'].append({'q':{'it':it_q,'en':en_q},'opts':{'it':it_opts,'en':en_opts},'correct':ans,'why':{'it':it_ex,'en':en_ex}})
    assert len(m['quiz'])>=5

m=mod('m1','Fondamenti MCP','MCP foundations',30,'Principi, benefici e limiti del protocollo','Purpose, value and limits of the protocol')
add(m,'a1.1','Perché nasce MCP','Why MCP exists',10,
'Un modello linguistico può redigere istruzioni o codice, ma non accede automaticamente ai documenti e alle applicazioni presenti su un computer. MCP nasce per normalizzare l’interazione tra applicazioni AI e strumenti esterni. Il protocollo non crea permessi e non aggiunge capacità che il server non abbia implementato.',
'A language model can draft instructions or code, but it does not automatically access documents and applications on your computer. MCP standardises interaction between AI applications and external tools. The protocol does not grant permissions or invent capabilities absent from the server.',
'L’applicazione host mantiene la conversazione. Uno o più client MCP dialogano con altrettanti server; ciascun server dichiara le funzioni che può esporre. Il modello può decidere quale funzione chiedere di usare, mentre l’host governa l’esecuzione e le eventuali autorizzazioni.',
'The host application owns the conversation. One or more MCP clients connect to servers, each declaring the functionality it offers. The model may choose which tool to request, while the host controls execution and any permissions.',
'In un flusso BIM, chiedere «quante porte sono presenti?» a un chatbot non connesso a Revit produce soltanto una procedura ipotetica. Con un server MCP opportuno, lo stesso chatbot può chiedere dati reali e presentare una risposta verificabile.',
'In a BIM workflow, asking an unconnected chatbot “how many doors are there?” produces only hypothetical instructions. With an appropriate MCP server, the same chatbot can request actual model data and present a verifiable answer.',
'Formula due esempi: uno in cui basta una risposta testuale e uno in cui servono dati correnti da un programma. Identifica quali informazioni non sono già incluse nel prompt.',
'Write two requests: one answerable as text alone and another requiring live application data. Identify what information is missing from the prompt itself.',
'Secondo esempio: serve un server collegato all’applicazione e il relativo Tool, non soltanto un modello AI più avanzato.',
'Second example: you need a server connected to the application and a relevant tool, not merely a more powerful language model.',kind='flow')
add(m,'a1.2','MCP e API: due livelli distinti','MCP versus APIs: different layers',10,
'Le API espongono funzionalità di un programma a un altro programma. MCP definisce invece un linguaggio standard perché un’applicazione AI possa scoprire e richiamare funzionalità offerte da server. Le due tecnologie operano a livelli diversi e spesso vengono impiegate insieme.',
'APIs expose an application’s capabilities to other software. MCP defines a common language for an AI application to discover and request functionality exposed by servers. They operate at different layers and are often combined.',
'Un add-in C# può usare la Revit API per recuperare elementi. Un server MCP può esporre quell’operazione come Tool con nome, descrizione e schema degli argomenti. Il client chiama il Tool; è il codice dell’add-in, non MCP, che interroga davvero Revit.',
'A C# add-in can use the Revit API to retrieve elements. An MCP server can expose that operation as a named tool with a description and argument schema. The client calls the tool; the add-in code—not MCP itself—actually queries Revit.',
'Confronta `FilteredElementCollector` della Revit API con un ipotetico Tool `get_elements(category="Walls")`: il secondo è un’interfaccia semplificata definita dal server, non un metodo standard di Revit.',
'Compare Revit API `FilteredElementCollector` with a hypothetical tool `get_elements(category="Walls")`: the latter is a simplified interface defined by the server, not a built-in Revit method.',
'Indica chi definisce la forma del Tool e chi esegue la selezione effettiva degli elementi.',
'Identify who defines the tool interface and who actually selects the elements.',
'Il server definisce il Tool, mentre l’implementazione usa API o altra logica per operare sui dati.',
'The server defines the tool, while its implementation uses APIs or other logic to work on the data.',kind='flow')
add(m,'a1.3','Ecosistema e casi d’uso','Ecosystem and use cases',10,
'Un host può collegarsi a molti server MCP diversi: file, database, repository di codice, applicazioni di produttività o ambienti BIM. L’interoperabilità riguarda l’interfaccia di comunicazione e non implica automaticamente interoperabilità semantica tra tutti i dati.',
'One host may connect to many MCP servers for files, databases, code repositories, productivity apps, or BIM environments. Interoperability applies to the communication interface and does not automatically mean semantic interoperability of all exchanged data.',
'I Tool sono eseguiti attraverso connessioni configurate: processi locali via STDIO o server raggiungibili via HTTP. Una soluzione locale può comunque inviare risultati a un LLM cloud se l’host è configurato per farlo: trattamento dei dati e permessi vanno esaminati separatamente.',
'Tools are invoked over configured connections: local STDIO processes or HTTP services. A local server can still pass results to a cloud LLM if the host works that way; permissions and data handling must be assessed separately.',
'Un assistente collegato a Revit e a un database può ricavare una lista di elementi BIM e confrontarla con un elenco di requisiti. La qualità del confronto dipenderà dalle definizioni e dalla mappatura informativa sviluppate, non solo da MCP.',
'An assistant connected to Revit and a database can retrieve BIM elements and compare them against requirements. The quality of that comparison depends on the definitions and information mapping implemented, not simply on MCP.',
'Disegna un diagramma con un host e tre server. Per ciascun server indica una funzione plausibile e un potenziale limite.',
'Sketch one host connecting to three servers. Identify one plausible capability and one limitation of each server.',
'Distingui sempre «server connesso» da «Tool realmente disponibile e autorizzato».',
'Always distinguish “server connected” from “tool actually available and permitted”.')
quiz(m,[
('Che cosa standardizza MCP?','What does MCP standardise?',['La comunicazione tra host AI e server','Tutte le geometrie Revit','Il linguaggio di programmazione C#'],['Communication between AI hosts and servers','All Revit geometry','The C# programming language'],0,'MCP specifica un’interfaccia comune, non una struttura geometrica BIM.','MCP specifies a common interface, not a BIM geometry structure.'),
('Una API e MCP...','An API and MCP...',['sono sempre equivalenti','possono essere usati insieme','richiedono entrambi un LLM'],['are always equivalent','can be used together','both require an LLM'],1,'La API esegue operazioni; MCP può esporle come strumenti.','An API performs operations; MCP can expose them as tools.'),
('Un LLM senza strumenti connessi può contare le pareti aperte in Revit?','Can an LLM without connected tools count walls in an open Revit model?',['Sì, sempre','Solo se indovina','No, non accede automaticamente al modello'],['Yes, always','Only by guessing','No, it does not automatically access the model'],2,'Servono dati forniti dall’utente o un’integrazione autorizzata.','It needs user-provided data or an authorised integration.'),
('Un server MCP locale garantisce che i dati non raggiungano mai il cloud?','Does a local MCP server guarantee data never leaves for the cloud?',['No, dipende anche dal client AI','Sì, per definizione','Soltanto per i file IFC'],['No, it also depends on the AI client','Yes, by definition','Only for IFC files'],0,'L’host AI potrebbe trasmettere i risultati a un servizio remoto.','The AI host may forward the results to a remote service.'),
('Se un server non espone un Tool di modifica...','If a server exposes no write tool...',['basta un prompt più forte','non si modifica il modello tramite quel Tool','MCP lo crea automaticamente'],['a stronger prompt is enough','that tool cannot modify the model','MCP creates it automatically'],1,'Un prompt non aggiunge funzioni inesistenti.','A prompt cannot create missing functionality.')])

m=mod('m2','Architettura MCP','MCP architecture',45,'Componenti, lifecycle, flussi e trasporti','Components, lifecycle, message flows, transports')
add(m,'a2.1','Host, Client e Server','Host, Client and Server',15,
'L’Host è l’ambiente che coordina la sessione AI. Un Client MCP è il componente dell’host che instaura una connessione verso uno specifico server. Il Server MCP espone capacità e risponde alle richieste. Il modello linguistico non coincide con nessuna di queste primitive, pur contribuendo alla selezione delle operazioni.',
'The host coordinates the AI session. An MCP client is the part of a host that establishes a connection with a particular server. The MCP server exposes capabilities and handles requests. The language model is not identical to any of these protocol roles, although it may select operations.',
'Un host può creare una connessione distinta per server. Durante l’avvio e la discovery, i partecipanti apprendono capacità compatibili. I controlli dell’host stabiliscono se un tool sia disponibile al modello e se richieda approvazione da parte dell’utente.',
'A host can create a separate connection for each server. During startup and discovery, the peers learn about compatible capabilities. Host policies decide which tools are available to the model and whether a user must approve their execution.',
'Immagina Claude Desktop come host, il client MCP integrato al suo interno e l’eseguibile Autodesk RevitMcpServer come server locale. Revit è il software esterno cui il server si collega.',
'Imagine Claude Desktop as host, an MCP client within it, and Autodesk RevitMcpServer as a local server process. Revit is the external application accessed by that server.',
'Nel diagramma interattivo seleziona ciascun componente e indica chi possiede l’interfaccia utente, chi comunica e chi esegue le funzioni.',
'In the interactive diagram, select each component and identify who owns the interface, who communicates, and who executes functions.',
'La Revit API resta nell’area dell’applicazione esterna: non è una primitiva MCP.',
'The Revit API remains at the external application layer: it is not an MCP primitive.',kind='flow')
add(m,'a2.2','Lifecycle e chiamate','Lifecycle and tool calls',15,
'Una sessione MCP non consiste in una semplice frase inviata a un programma. Il client deve poter stabilire una comunicazione valida, negoziare la versione/capacità secondo la revisione del protocollo usata, scoprire le funzioni esposte e infine richiamare i Tools necessari. Le implementazioni variano fra revisioni MCP.',
'An MCP session is more than a sentence sent to a program. The client must establish valid communication, agree on compatible protocol version/capabilities as defined by the revision in use, discover exposed functions, and then invoke the required tools. Details vary across protocol revisions.',
'La chiamata di un Tool trasporta nome e argomenti. Il server valida l’input, esegue la propria logica e restituisce contenuti strutturati o un errore. Le richieste hanno identificativi che permettono di associare la risposta alla chiamata.',
'A tool invocation carries a name and arguments. The server validates input, executes its logic, and returns structured content or an error. Requests have identifiers so responses can be associated with their calls.',
'Un flusso dimostrativo per una interrogazione di pareti: prompt → selezione di Tool disponibile → `tools/call` → accesso al documento → dati degli elementi → sintesi AI. I nomi dei Tools mostrati sono didattici e non attribuiti ad Autodesk.',
'An illustrative wall query flows as: prompt → selecting an available tool → `tools/call` → document access → element data → AI summary. Tool names shown are educational examples, not claims about Autodesk tool names.',
'Apri il simulatore, passa dalla fase di discovery a una Tool call e annota in quale fase può comparire una richiesta di permesso.',
'Use the simulator to move from discovery to a tool call and note where a permission request may arise.',
'La conferma dell’utente è gestita dall’host, non è una proprietà che garantisce da sola la correttezza del Tool.',
'User confirmation belongs to the host and does not in itself guarantee correct tool behaviour.',code_text='{"jsonrpc":"2.0","id":7,"method":"tools/call","params":{"name":"demo_count_by_category","arguments":{"category":"IfcWall"}}}',kind='flow')
add(m,'a2.3','STDIO, HTTP e sicurezza','STDIO, HTTP and security',15,
'STDIO è adatto a server locali avviati dal client AI come sottoprocesso. Streamable HTTP trasporta MCP mediante endpoint HTTP e viene utilizzato per servizi di rete. Il trasporto non decide da solo dove vengono elaborate le conversazioni o dove finiscono i dati estratti.',
'STDIO suits local servers launched as subprocesses by an AI client. Streamable HTTP transports MCP through HTTP endpoints and suits network services. Transport choice alone does not determine where conversations are processed or where extracted data ends up.',
'Nella comunicazione STDIO, stdout è riservato ai messaggi del protocollo: stampare log di debug su stdout può rompere il parsing. Usa stderr o gli strumenti di logging supportati. Con HTTP considera autenticazione, rete, TLS, controllo degli accessi e esposizione degli endpoint.',
'With STDIO, stdout carries protocol messages: printing debug logs to stdout can corrupt parsing. Use stderr or supported logging facilities. With HTTP, consider authentication, networking, TLS, access control, and endpoint exposure.',
'Il server ufficiale Revit è locale e comunica tramite STDIO. Un server personalizzato per una dashboard web potrebbe invece esporre un endpoint HTTP su una porta locale o remota, opportunamente protetta.',
'Autodesk’s official Revit server is local and communicates over STDIO. A custom server for a web dashboard might instead expose an HTTP endpoint on a properly secured local or remote port.',
'Classifica tre scenari — uso sullo stesso PC, server condiviso in rete, lettura di dati sensibili — individuando trasporto e controlli di sicurezza.',
'Classify three scenarios—same-PC use, network service, sensitive data access—by transport and security controls.',
'Non dedurre che «locale» implichi assenza di trasmissione a un LLM cloud.',
'Do not infer that “local” means no data is transmitted to a cloud LLM.')
quiz(m,[
('Chi ospita la sessione AI?','Who hosts the AI session?',['Il Server MCP','L’Host','La Revit API'],['The MCP server','The host','The Revit API'],1,'L’Host gestisce esperienza, client e policy.','The host manages the experience, clients and policies.'),
('Quale metodo è usato per richiamare un Tool?','Which method invokes a tool?',['tools/call','tools/style','revit/execute'],['tools/call','tools/style','revit/execute'],0,'tools/call è il metodo MCP per richiamare un Tool.','tools/call is the MCP method for invoking tools.'),
('STDIO viene usato spesso quando...','STDIO is commonly used when...',['il server è un sottoprocesso locale','serve un dominio Internet','non esistono processi'],['the server is a local subprocess','an Internet domain is required','there are no processes'],0,'In STDIO il client avvia e comunica con un processo.','With STDIO the client launches and communicates with a process.'),
('È sicuro scrivere log arbitrari su stdout di un server STDIO?','Is it safe to print arbitrary logs to stdout in a STDIO MCP server?',['Sì','No','Solo con file IFC'],['Yes','No','Only with IFC files'],1,'stdout è destinato ai messaggi MCP.','stdout is reserved for MCP protocol messages.'),
('Dove si definiscono i permessi di esecuzione lato utente?','Where are user-facing execution permissions handled?',['Solo dentro la geometria IFC','Nell’host e nelle configurazioni del server','Nel nome del Tool'],['Only in IFC geometry','In host controls and server configuration','In the tool name'],1,'I permessi non si deducono dal solo protocollo o dal prompt.','Permissions are not inferred from the protocol or the prompt alone.')])
m=mod('m3','Tools, Resources e Prompts','Tools, Resources and Prompts',40,'Definizioni, schemi, risultati e messaggi','Definitions, schemas, results and messages')
add(m,'a3.1','Definire un Tool','Defining a tool',15,
'Un Tool è una funzione che il server offre a un client: il suo contratto dichiara nome, descrizione e schema degli argomenti. Una buona descrizione specifica cosa fa davvero la funzione, limiti e unità di misura; aiuta il modello a non selezionare il Tool sbagliato.',
'A tool is a function offered by a server to its client: its contract declares name, description, and argument schema. A good description states what the function really does, its limits, and units; this helps the model avoid choosing the wrong tool.',
'Uno schema JSON può richiedere un parametro `category` e limitare i valori accettati. Il modello propone gli argomenti, ma il server deve validarli comunque. La risposta va distinta da una spiegazione generata dall’LLM: è un risultato dell’esecuzione.',
'A JSON schema may require a `category` argument and restrict accepted values. The model proposes arguments, but the server must validate them regardless. The response differs from an LLM explanation: it is an execution result.',
'Il Tool dimostrativo `count_by_category` riceve `IfcWall` e restituisce 30 per lo snapshot IFC del corso. Non è il nome di un Tool Autodesk e non prova il conteggio corrente nel modello RVT aperto.',
'The demo tool `count_by_category` receives `IfcWall` and returns 30 for the course IFC snapshot. It is not an Autodesk tool name and does not prove the live open RVT model count.',
'Individua nome, argomento obbligatorio, tipo di ritorno e possibili errori nella definizione dimostrativa.',
'Identify name, required argument, return type and possible errors in the demo definition.',
'Un server reale dovrebbe distinguere categoria inesistente, dato assente e errore di connessione.',
'A real server should distinguish an unknown category, missing data and connection failure.',code_text='{"name":"count_by_category","description":"Count IFC entities in the course snapshot","inputSchema":{"type":"object","properties":{"category":{"type":"string"}},"required":["category"]}}',kind='ifc')
add(m,'a3.2','Resources, Prompts e URI','Resources, Prompts and URIs',10,
'Una Resource è un contenuto consultabile, di norma identificato da URI. Un Prompt è un modello di istruzioni riutilizzabile con eventuali argomenti. Diversamente dai Tools, questi meccanismi non descrivono necessariamente l’esecuzione di un’azione esterna.',
'A resource is readable content, typically identified by a URI. A prompt is a reusable instruction template, optionally parameterised. Unlike tools, these mechanisms do not necessarily describe an executable external action.',
'Il server può esporre `bim://project/overview` come risorsa informativa e un prompt `review_missing_parameters` come traccia guidata. Il supporto concreto dipende dalle primitive implementate; non tutti i server espongono tutte le tipologie.',
'A server might expose `bim://project/overview` as an information resource and `review_missing_parameters` as a reusable prompt. Support depends on implementation; not every server implements all primitive types.',
'Le proprietà IFC associate a un edificio potrebbero costituire una Resource JSON, mentre un controllo di completezza su categorie multiple può richiedere uno o più Tools. Non attribuire un’azione a una Resource senza definirne il comportamento.',
'IFC properties associated with a building could be exposed as a JSON resource, while completeness checks across categories may require one or more tools. Do not attribute executable actions to a resource without defining them.',
'Classifica: (1) contenuto IFC leggibile, (2) funzione di lettura parametri, (3) traccia di controllo informativo riutilizzabile.',
'Classify: (1) readable IFC content, (2) parameter retrieval function, (3) reusable information-check template.',
'La corrispondenza attesa è Resource, Tool, Prompt.','The expected mapping is Resource, Tool, Prompt.')
add(m,'a3.3','Messaggi strutturati ed errori','Structured messages and errors',15,
'Le richieste MCP utilizzano JSON-RPC 2.0 come struttura di base. L’oggetto di richiesta contiene un metodo, parametri e identificativo; una risposta può riportare un risultato oppure un errore. Un Tool può inoltre segnalare un errore applicativo nel proprio risultato.',
'MCP requests use JSON-RPC 2.0 as their messaging basis. A request has a method, parameters and an identifier; a response may contain a result or an error. A tool may also report an application-level error in its result.',
'Un Tool dovrebbe trattare esplicitamente valori nulli, categorie prive di oggetti, problemi di autorizzazione e timeout. In BIM va posta attenzione a unità, tipi di dati, GUID e differenza tra entità IFC e oggetti di Revit.',
'A tool should explicitly handle null values, empty categories, authorisation failures and timeouts. In BIM, units, data types, GUIDs and differences between IFC entities and Revit objects deserve special attention.',
'Una richiesta valida `tools/call` potrebbe chiedere `category=IfcWindow`. Nel file IFC fornito sono presenti 7 istanze `IfcWindow`; una chiamata a un server reale andrebbe comunque verificata sul documento corrente.',
'A valid `tools/call` might request `category=IfcWindow`. The supplied IFC contains 7 `IfcWindow` instances; a live server query still needs validation against the current document.',
'Confronta i tre esiti: 7 elementi, 0 elementi e errore di connessione. Spiega perché non sono intercambiabili.',
'Compare three outcomes: seven elements, zero elements, and a connection error. Explain why they are not interchangeable.',
'Un elenco vuoto è un risultato valido; un errore significa che l’operazione non è stata completata.',
'An empty list may be valid; an error means the operation was not completed.',code_text='{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"demo_count_by_category","arguments":{"category":"IfcWindow"}}}',kind='ifc')
quiz(m,[
('Quale parte descrive gli argomenti ammessi da un Tool?','What declares allowed tool arguments?',['inputSchema','IfcSite','README soltanto'],['inputSchema','IfcSite','README only'],0,'Lo schema definisce la struttura attesa degli input.','The schema defines the expected input structure.'),
('Un identificativo URI di contenuto caratterizza soprattutto...','A content URI chiefly characterises...',['un Resource','una Transaction Revit','un LLM'],['a Resource','a Revit Transaction','an LLM'],0,'Le risorse sono accessibili tramite identificatori.','Resources are addressed by identifiers.'),
('Un Prompt MCP è...','An MCP Prompt is...',['un file RVT','una traccia di istruzioni riutilizzabile','un Tool sempre distruttivo'],['an RVT file','a reusable instruction template','an always-destructive Tool'],1,'I Prompt forniscono template, non necessariamente operazioni.','Prompts provide templates, not necessarily operations.'),
('Qual è il metodo JSON-RPC per eseguire un Tool?','Which JSON-RPC method executes a tool?',['tools/call','tools/scanBIM','ifc/query'],['tools/call','tools/scanBIM','ifc/query'],0,'tools/call è previsto dal protocollo MCP.','tools/call is defined by MCP.'),
('Una risposta con zero elementi significa sempre un errore?','Does a result containing zero elements always mean an error?',['Sì','No, può essere un risultato valido','Significa scrittura del modello'],['Yes','No, it may be a valid result','It means a model write'],1,'La lista vuota non coincide con un fallimento.','An empty list is not necessarily a failure.')])

m=mod('m4','Primo server MCP','Your first MCP server',45,'Ambiente gratuito, test con Inspector, debug','Free tools, Inspector testing, debugging')
add(m,'a4.1','Preparare gli strumenti','Prepare the environment',10,
'Per comprendere un server non serve acquistare un LLM. Installeremo Python, uno strumento di gestione dell’ambiente (`uv`) e il pacchetto ufficiale `mcp[cli]`. L’Inspector permette di vedere Tools e risposte indipendentemente da una chat AI.',
'You do not need to buy an LLM to understand an MCP server. Install Python, the `uv` environment manager, and the official `mcp[cli]` package. The Inspector exposes tools and responses independently of an AI chat.',
'Crea una cartella isolata per il laboratorio e usa un ambiente virtuale. L’Inspector basato su Node richiede anche la disponibilità di `npx`; la procedura `uv run mcp dev server.py` è documentata dallo SDK Python v2.',
'Create an isolated lab folder and virtual environment. The Node-based Inspector also needs `npx`; the `uv run mcp dev server.py` workflow is documented by the Python SDK v2.',
'Prepara un ambiente per lavorare con dati BIM esemplificativi, senza Revit. In seguito la stessa architettura di Tool sarà riutilizzata nel modulo di sviluppo.',
'Prepare an environment to work with sample BIM data without Revit. The same tool-interface concepts will later be reused in the development module.',
'Esegui `python --version`, `uv --version`, `node --version` e `npx --version` da terminale, quindi registra i risultati.',
'Run `python --version`, `uv --version`, `node --version`, and `npx --version` in a terminal and record the outputs.',
'Python 3.10+ è il minimo dichiarato dallo SDK corrente; usa preferibilmente Python 3.11+ e versioni Node supportate.',
'The current SDK documents Python 3.10+; prefer Python 3.11+ and supported Node versions.',code_text='uv init mcp-lab\ncd mcp-lab\nuv add "mcp[cli]"')
add(m,'a4.2','Eseguire un Tool dimostrativo','Run a demo tool',20,
'Un server MCP Python può registrare funzioni con il decoratore `@mcp.tool()`. Il nome, la documentazione e le annotazioni dei tipi definiscono una parte importante del contratto del Tool. La funzione Python resta codice normale, quindi può essere verificata anche senza un modello AI.',
'A Python MCP server can register functions with `@mcp.tool()`. Function names, docstrings and type annotations contribute to the tool contract. The function remains ordinary Python code, so it can also be tested without a language model.',
'Il server demo espone `get_course_model_counts`, una funzione che legge uno snapshot statico di conteggi dell’IFC. Le quantità sono numeri osservati nell’esportazione allegata al corso, non risultati ottenuti direttamente da un MCP per Revit.',
'The demo server exposes `get_course_model_counts`, reading static counts from the course IFC snapshot. Those quantities were observed in the supplied IFC export; they are not the result of a live Revit MCP call.',
'Nel dataset didattico trovi 30 pareti, 15 porte e 7 finestre. Prima di eseguire il Tool, prevedi il risultato di una richiesta sulla categoria `IfcDoor`.',
'The learning dataset contains 30 walls, 15 doors and 7 windows. Before calling the tool, predict the outcome for `IfcDoor`.',
'Scarica il progetto demo dal pacchetto del Developer Lab, avvia `mcp dev`, richiama il Tool e confronta risultato e schema.',
'Download the demo project from the Developer Lab package, run `mcp dev`, call the tool and compare response with schema.',
'Il numero atteso nello snapshot per `IfcDoor` è 15. Un eventuale errore di importazione dipende dall’ambiente Python, non dal file RVT.',
'The expected IFC snapshot count for `IfcDoor` is 15. Python import errors belong to the development environment, not to the RVT file.',code_text='from mcp.server import MCPServer\nmcp = MCPServer("BIM Academy")\nCOUNTS = {"IfcWall":30,"IfcDoor":15,"IfcWindow":7}\n\n@mcp.tool()\ndef get_course_model_counts(category: str) -> int:\n    """Count a category in the static training snapshot."""\n    return COUNTS.get(category, 0)\n\nif __name__ == "__main__":\n    mcp.run(transport="stdio")',kind='ifc')
add(m,'a4.3','Inspector e debugging','Inspector and debugging',15,
'L’MCP Inspector è uno strumento di ispezione con cui esplorare gli strumenti annunciati da un server, verificarne gli schemi, invocare le funzioni e leggere risultati ed errori. Non richiede un abbonamento AI.',
'MCP Inspector lets you inspect a server’s advertised tools, verify their schemas, invoke functions, and review results and errors. It needs no paid AI subscription.',
'Per un server avviato via STDIO, evita `print()` su stdout: i log interferirebbero con i messaggi MCP. Se Inspector non trova il Tool, verifica ambiente virtuale, entrypoint, errori di avvio e nome della funzione.',
'With a STDIO-launched server, avoid `print()` on stdout: logs can interfere with MCP messages. If Inspector cannot find the tool, check the virtual environment, entrypoint, startup errors and the function name.',
'Testa prima la categoria corretta `IfcWindow`, poi una stringa inesistente. Una funzione dimostrativa può restituire zero, ma un server di produzione dovrebbe decidere se segnalare esplicitamente la categoria sconosciuta.',
'Test the valid `IfcWindow` category first, then an unknown string. A demo function might return zero, but a production server should decide whether an unknown category deserves an explicit validation error.',
'Annota: nome Tool, parametri, risposta, tempo di esecuzione, problemi e risoluzione.',
'Record: tool name, parameters, response, execution time, issues and resolution.',
'Completa la checklist del laboratorio; nel corso nessun quiz dipende da un abbonamento AI.',
'Complete the lab checklist; no course quiz depends on a paid AI plan.',code_text='uv run mcp dev server.py')
quiz(m,[
('A cosa serve MCP Inspector?','What is MCP Inspector for?',['Modellare muri','Testare Tools e risposte','Compilare Revit'],['Modelling walls','Testing tools and responses','Compiling Revit'],1,'Permette di provare server e Tools indipendentemente da un LLM.','It tests servers and tools independently from an LLM.'),
('Cosa registra `@mcp.tool()`?','What does `@mcp.tool()` register?',['Una funzione MCP richiamabile','Un materiale IFC','Una schermata Revit'],['A callable MCP function','An IFC material','A Revit screen'],0,'Il decoratore espone la funzione come Tool.','The decorator exposes the function as a tool.'),
('Quale comando è documentato per il testing dello SDK v2?','Which command is documented for SDK v2 testing?',['mcp sketch','uv run mcp dev server.py','revit /ifc'],['mcp sketch','uv run mcp dev server.py','revit /ifc'],1,'Il comando avvia l’ambiente di test Inspector.','The command launches the Inspector testing workflow.'),
('È indispensabile un abbonamento LLM per provare un Tool con Inspector?','Is a paid LLM required to test a tool with Inspector?',['Sì','Solo su Windows','No'],['Yes','Only on Windows','No'],2,'Inspector esegue chiamate di protocollo senza bisogno di un LLM.','Inspector makes protocol calls without needing an LLM.'),
('I conteggi nello snapshot demo indicano il numero attuale di oggetti RVT?','Do demo snapshot counts prove live RVT counts?',['No','Sì, sempre','Solo per le porte'],['No','Yes, always','Only for doors'],0,'I conteggi descrivono la versione IFC fornita, non lo stato corrente in Revit.','Counts describe the supplied IFC export, not the live Revit state.')])

m=mod('m5','MCP per Autodesk Revit','MCP for Autodesk Revit',40,'Revit API, server ufficiale, affidabilità','Revit API, official servers, reliability')
add(m,'a5.1','L’architettura Revit–MCP','The Revit–MCP architecture',10,
'Autodesk distribuisce un add-on MCP per Revit 2027. Il client compatibile usa un server locale STDIO, mentre Revit mantiene il documento e le proprie API. Per capire l’integrazione devi distinguere il modello RVT in memoria, il risultato delle API e la risposta elaborata dall’LLM.',
'Autodesk provides an MCP add-on for Revit 2027. A compatible client talks to a local STDIO server, while Revit owns the document and its APIs. Understand the distinction between live RVT data, API output, and the LLM-generated explanation.',
'Una richiesta in linguaggio naturale arriva all’host AI, che sceglie uno dei Tool esposti dal server. Il server implementa il proprio accesso a Revit e invia i risultati; l’utente deve poter verificare dati e operazioni.',
'A natural-language request reaches the AI host, which selects an exposed tool. The server implements access to Revit and returns results; the user must be able to verify values and operations.',
'Nel modello didattico fornito, il file IFC contiene 6 entità `IfcBuildingStorey`. Non è corretto dedurre automaticamente che il server Revit esponga esattamente 6 livelli senza una query reale.',
'The supplied course IFC contains six `IfcBuildingStorey` entities. That does not prove that the Revit server will report exactly six levels without a live query.',
'Segna nel diagramma la posizione del client AI, server Revit, add-in e documento. Individua dove avviene la conversione in linguaggio naturale.',
'Label the AI client, Revit server, add-in and document in the diagram. Identify where natural-language interpretation occurs.',
'La risposta dell’LLM non è l’origine dei dati BIM; deve essere collegata alle informazioni restituite dai Tools.',
'The LLM’s answer is not the BIM data origin; it must be grounded in tool results.',kind='flow')
add(m,'a5.2','Read, Write, Experimental','Read, Write, Experimental',15,
'Autodesk distingue i server Read, Write ed Experimental nella Technical Preview. Read espone operazioni di sola lettura; Write include anche Tools che modificano il modello; Experimental aggiunge funzionalità sperimentali. La disponibilità e i nomi precisi dei Tools possono cambiare con gli aggiornamenti.',
'Autodesk distinguishes Read, Write and Experimental servers in the Technical Preview. Read exposes non-mutating actions; Write adds model-changing tools; Experimental adds experimental functionality. Exact tool names and availability can change with updates.',
'Per ciascuna attività valuta il livello di permesso più basso che la renda possibile. Una ricerca di porte dovrebbe partire da Read. Una scrittura di parametro richiede capacità Write, il giusto contesto Revit e la conferma dell’utente dove prevista.',
'For every activity, choose the least powerful server necessary. Finding doors should start with Read. Editing a parameter requires write capabilities, an appropriate Revit context and user approval when requested.',
'Fra i flussi illustrati da Autodesk figurano ricerca elementi, parametri, report, navigazione viste ed esportazione viste. Non assumere che un comando inventato nella lezione esista nel catalogo effettivo.',
'Autodesk documents workflows such as searching elements, retrieving parameters, producing reports, navigating views and exporting views. Do not assume a tool name invented for a lesson is actually supported.',
'Classifica le richieste «conta finestre», «aggiorna commenti» e «crea geometrie sperimentali» scegliendo il livello di privilegio plausibile.',
'Classify “count windows”, “update comments” and “create experimental geometry” by plausible permission level.',
'Read per lettura; Write per modifica supportata; Experimental soltanto se la funzione richiesta è effettivamente esposta e verificata.',
'Read for non-mutating queries; Write for supported edits; Experimental only if the requested function is actually exposed and verified.')
add(m,'a5.3','Affidabilità, privacy e rischi','Reliability, privacy and risk',15,
'I risultati di una Tool call possono essere corretti mentre la sintesi dell’AI risulta incompleta, o viceversa. La verifica richiede controlli su categorie, unità, filtri, fasi, opzioni di progetto e natura del parametro (tipo/istanza). Il sistema AI non sostituisce un processo di validazione BIM.',
'A tool call can return accurate data while the AI summary is incomplete, or vice versa. Verification must account for categories, units, filters, phases, design options, and whether a parameter is type- or instance-based. AI does not replace BIM validation.',
'L’add-on ufficiale opera localmente, ma il client AI può trasmettere contenuti estratti a un servizio cloud. Usa un modello autorizzato e limita le informazioni condivise. Evita Tools di scrittura nei primi esercizi e lavora sempre su copie per le modifiche.',
'The official add-on runs locally, but the AI client may forward extracted content to a cloud service. Use an authorised model and limit exposed information. Start with read-only tools and use a project copy for changes.',
'Il file IFC didattico contiene metadati di esportazione. MCP Academy pubblica soltanto conteggi e valori necessari agli esercizi; i file RVT/IFC originali non sono inclusi automaticamente nel sito.',
'The course IFC includes export metadata. MCP Academy publishes only counts and values necessary for exercises; the original RVT/IFC files are not automatically included on the website.',
'Prepara una checklist di verifica per una tabella di porte: totali, elementi campionati, proprietà, unità e documentazione dei Tool effettivamente usati.',
'Prepare a validation checklist for a door schedule: totals, sampled elements, properties, units and the tools actually used.',
'Il prompt deve chiedere esplicitamente di segnalare l’assenza di Tool o dati, invece di inventare risultati.',
'The prompt should explicitly ask to report missing tools or data rather than fabricate outputs.',kind='ifc')
quiz(m,[
('Quale server privilegiare per una semplice interrogazione?','Which server should you prefer for a simple query?',['Write','Read','Experimental'],['Write','Read','Experimental'],1,'Applica il principio del privilegio minimo.','Use the least-privilege principle.'),
('MCP sostituisce la Revit API?','Does MCP replace the Revit API?',['No','Sì','Solo dal 2027'],['No','Yes','Only since 2027'],0,'MCP può esporre funzioni implementate tramite API.','MCP can expose functions implemented through APIs.'),
('Quale versione di Revit viene utilizzata nei laboratori MCP Academy?','Which Revit version is used in the MCP Academy labs?',['Revit 2020','Revit 2027.3','Unicamente IFC2x3'],['Revit 2020','Revit 2027.3','Only IFC2x3'],1,'Questa Academy adotta Revit 2027.3, con compatibilità confermata dall’autore.','This Academy targets Revit 2027.3, with compatibility confirmed by the author.'),
('Se l’LLM restituisce un conteggio senza evidenza...','If an LLM gives a count without evidence...',['va verificato sul modello','è definitivo','è sempre falso'],['verify it against the model','it is final','it is always false'],0,'Il risultato richiede tracciabilità dei dati e controlli.','Results need data traceability and checks.'),
('Un server Read può modificare parametri?','Can a Read server edit parameters?',['Sì, sempre','No, per definizione','Solo tramite screenshot'],['Yes, always','No, by design','Only through screenshots'],1,'Read espone operazioni che non modificano il modello.','Read exposes non-mutating operations.')])
m=mod('m6','Installazione e connessione a Revit','Installing and connecting to Revit',55,'Add-on Autodesk, Claude Desktop e test di connessione','Autodesk add-on, Claude Desktop and connection test')
add(m,'a6.1','Prerequisiti e compatibilità','Prerequisites and compatibility',15,
'Per i laboratori del corso utilizziamo Revit 2027.3, la cui compatibilità con il server MCP Autodesk è stata confermata dall’autore. Occorre installare l’add-on MCP corrispondente. Revit deve essere aperto con un documento caricato. Serve inoltre un client che supporti server locali STDIO: in questo corso il riferimento è Claude Desktop, senza richiedere un abbonamento a pagamento.',
'These labs use Revit 2027.3, with compatibility with the Autodesk MCP server confirmed by the course author. Install the corresponding MCP add-on. Revit must be running with a model open. You also need an AI client supporting local STDIO servers: this course uses Claude Desktop without requiring a paid subscription.',
'Il file IFC didattico riporta un’esportazione da Revit 27.3.0.28, coerente con la versione utilizzata per i laboratori. Se utilizzi un’altra build, verifica prima la compatibilità dell’add-on MCP e dei Tools.',
'The training IFC header reports an export from Revit 27.3.0.28, consistent with the lab version. For a different build, check MCP add-on and tool compatibility first.',
'Il file comune è un edificio residenziale unifamiliare. Se hai una copia RVT autorizzata, aprila in Revit e verificane la versione. Il sito non distribuisce per ora i file originali.',
'The shared case is a single-family house. If you have an authorised RVT copy, open it in Revit and check its version. The website does not currently distribute the original files.',
'Controlla Revit About, Autodesk Account, disponibilità dell’add-on Read e versione di Claude Desktop.',
'Check Revit About, Autodesk Account, the Read add-on availability and your Claude Desktop version.',
'In caso di dubbio sulla build, non passare a Write/Experimental: conferma prima la connessione Read.',
'If uncertain about your build, do not proceed to Write/Experimental: validate a Read connection first.',kind='ifc')
add(m,'a6.2','Installazione add-on e configurazione','Install the add-on and configure the client',20,
'Da Autodesk Account, nella sezione Revit 2027 Extensions, installa `Revit MCP Server Read-Tools Technical Preview` secondo la disponibilità del tuo account. Claude Desktop utilizza il file JSON di configurazione dei server MCP locali, accessibile da Settings → Developer → Edit Config.',
'From Autodesk Account, under Revit 2027 Extensions, install `Revit MCP Server Read-Tools Technical Preview` as available in your account. Claude Desktop reads local server definitions from a JSON config file opened via Settings → Developer → Edit Config.',
'Nel file, `command` punta all’eseguibile realmente installato e `args` contiene gli argomenti necessari. In JSON, i percorsi Windows richiedono due backslash. Non cancellare altre voci in `mcpServers` se usi già altri server.',
'In the file, `command` points at the actually installed executable and `args` contains required options. Windows paths in JSON use escaped backslashes. Do not erase other entries in `mcpServers` if other servers are already configured.',
'La configurazione riportata nell’esempio è quella Read pubblicata da Autodesk, non un Tool di scrittura. Dopo aver salvato il file, chiudi completamente e riavvia Claude Desktop.',
'The example configuration is Autodesk’s published Read setup, not a write tool. Save the file, fully quit Claude Desktop, then restart it.',
'Verifica il percorso `.exe` in Esplora File, poi confronta la configurazione con la documentazione ufficiale collegata nel corso.',
'Verify the executable path in File Explorer, then compare your configuration with the official documentation linked by the course.',
'Un backslash non escapato o una virgola finale rendono il file JSON invalido.',
'An unescaped backslash or a trailing comma makes the JSON invalid.',code_text=r'''{
  "mcpServers": {
    "Revit MCP Read-Tools Technical Preview": {
      "command": "C:\\Program Files\\Autodesk\\Revit 2027 MCP Server Read-Tools Technical Preview\\Autodesk.RevitMcpServer.Stdio.exe",
      "args": ["--ManageConfigurationWithAutodeskRevitPluginInstaller=true"]
    }
  }
}''')
add(m,'a6.3','Prima connessione e troubleshooting','First connection and troubleshooting',20,
'Apri Revit con un documento di prova, poi Claude Desktop e controlla la disponibilità del server. La prima richiesta deve essere non distruttiva: «Elenca i Tools Revit disponibili e i loro parametri». Solo dopo prova un’interrogazione limitata, citando il nome del Tool realmente trovato.',
'Open Revit with a training document, then Claude Desktop and verify server availability. The first request should be non-destructive: “List available Revit tools and their arguments.” Only then try a narrow data query, referring to an actually discovered tool.',
'Se il server non appare, ricontrolla build Revit, installazione add-on, percorso, sintassi JSON, riavvio completo del client e permessi. Se appare ma non restituisce dati, assicurati che un progetto sia aperto e che il Tool richiesto sia compatibile.',
'If the server does not appear, check the Revit build, add-on installation, executable path, JSON syntax, complete client restart and permissions. If it connects without results, confirm a project is open and the requested tool is supported.',
'Prompt di avvio consigliato: «List the available Revit MCP tools. For each, show its name, required arguments, whether it is read-only and its limitations. Do not modify the model.»',
'Recommended initial prompt: “List the available Revit MCP tools. For each, show its name, required arguments, whether it is read-only and its limitations. Do not modify the model.”',
'Conserva un breve log della connessione (versione, data, Tools visti) e verifica la prima risposta sul modello.',
'Keep a brief connection log (version, date, discovered tools) and validate the first answer against the model.',
'Quando il piano AI gratuito impone un limite, riprendi al reset del servizio o usa MCP Inspector per i test di protocollo disponibili; non acquistare crediti API per completare il corso.',
'If the free AI plan hits a limit, continue after its reset or use MCP Inspector for protocol-level tests where possible; no paid API credits are required for course completion.',kind='lab')
quiz(m,[
('Quale configurazione server è suggerita per iniziare?','Which server configuration is recommended for a first connection?',['Read','Experimental','Write obbligatorio'],['Read','Experimental','Mandatory Write'],0,'La lettura limita il rischio di modifiche involontarie.','Read limits the risk of accidental edits.'),
('Dove si configura un server locale in Claude Desktop?','Where is a local server configured in Claude Desktop?',['Solo in Revit Family Editor','Settings → Developer → Edit Config','Dentro IFC header'],['Only in Revit Family Editor','Settings → Developer → Edit Config','Inside the IFC header'],1,'Il file `claude_desktop_config.json` descrive i server.','`claude_desktop_config.json` lists local servers.'),
('In una stringa JSON il backslash Windows va...','In a JSON string a Windows backslash must be...',['escapato','rimosso sempre','sostituito con hashtag'],['escaped','always removed','replaced by a hashtag'],0,'Usa backslash doppi nelle stringhe di percorso JSON.','Use double backslashes in JSON path strings.'),
('Quale controllo fare prima di invocare un Tool specifico?','What should you do before requesting a specific tool?',['Scoprire i Tools disponibili','Modificare i file IFC','Disabilitare Revit'],['Discover available tools','Edit IFC files','Disable Revit'],0,'La Tool discovery evita nomi inventati.','Tool discovery avoids made-up tool names.'),
('La versione 27.3 nell’IFC prova la compatibilità del server MCP?','Does a 27.3 exporter version in IFC prove MCP server compatibility?',['Sì','No','Solo per gli IfcWall'],['Yes','No','Only for IfcWall'],1,'Le dichiarazioni di supporto e una prova reale sono fonti distinte.','Support statements and live testing are separate evidence.')])

m=mod('m7','Laboratori BIM sul modello comune','BIM labs using the shared model',95,'Esercizi Read verificabili e report informativi','Verifiable Read exercises and information reports')
add(m,'a7.1','Prima interrogazione BIM','First BIM query',15,
'Un laboratorio riproducibile inizia da un documento identificato e da una domanda limitata. Apri una copia del RVT didattico, verifica che il server Read sia collegato e chiedi al client di elencare la categoria interrogabile e gli strumenti effettivamente utilizzati.',
'A reproducible lab starts from a known document and a narrow question. Open a copy of the training RVT, verify the Read server connection, and ask the client to report the queried category and the tools actually used.',
'Il riferimento IFC4X3_ADD2 contiene 30 `IfcWall`, 15 `IfcDoor` e 7 `IfcWindow`. Le categorie di Revit possono avere conteggi differenti per via di esportazione, fasi, opzioni e mapping IFC. Annotare una differenza è un risultato didattico, non necessariamente un errore.',
'The IFC4X3_ADD2 reference contains 30 `IfcWall`, 15 `IfcDoor`, and 7 `IfcWindow`. Revit category counts may differ due to export scope, phases, design options and IFC mapping. Documenting a difference is a learning outcome, not necessarily a failure.',
'Prompt: «Utilizza soltanto i Tools Revit disponibili in modalità Read. Conta Walls, Doors e Windows nel documento aperto, indica gli strumenti usati e segnala eventuali filtri o limiti. Non modificare nulla.»',
'Prompt: “Use only available Read-mode Revit tools. Count Walls, Doors and Windows in the open document, list the tools used, and disclose filters or limitations. Do not modify anything.”',
'Confronta almeno un risultato con un abaco o una selezione verificabile in Revit. Registra la differenza rispetto allo snapshot IFC.',
'Cross-check at least one result using a Revit schedule or verifiable selection. Record any differences relative to the IFC snapshot.',
'La verifica è guidata: nessun caricamento automatico di report al sito.',
'This is a guided check; no report upload to the website is required.',kind='ifc')
add(m,'a7.2','Categorie, tipi e livelli','Categories, types and storeys',15,
'Un oggetto BIM va interpretato considerando categoria, tipologia, istanza, livello e identificativi. Nell’IFC fornito sono presenti sei `IfcBuildingStorey` chiamati `A_S_0`, `A_A_0`, `A_S_1`, `A_A_1`, `A_S_2` e `A_A_2`. Non ogni riferimento a un livello IFC deve coincidere con il nome di una vista Revit.',
'A BIM object must be interpreted through category, type, instance, level and identifiers. The supplied IFC contains six `IfcBuildingStorey` entities named `A_S_0`, `A_A_0`, `A_S_1`, `A_A_1`, `A_S_2`, and `A_A_2`. An IFC storey reference does not necessarily match a Revit view name.',
'Parti da un sottoinsieme, ad esempio le porte, e limita la richiesta a un livello. Chiedi al modello di indicare esattamente il criterio di filtro, non soltanto una tabella finale. Controlla poi uno o due ElementId/UniqueId nel progetto.',
'Start with a subset, such as doors, and filter by a level. Ask the model to disclose the exact filter criteria, not just the final table. Then cross-check one or two ElementId/UniqueIds in Revit.',
'Prompt: «Elenca fino a 10 porte associate al livello scelto. Riporta identificativo, nome/tipo e livello effettivamente recuperato. Se il Tool non può filtrare per livello, dichiaralo.»',
'Prompt: “List up to ten doors associated with the selected level. Include identifier, name/type and actual retrieved level. If the tool cannot filter by level, say so.”',
'Apri manualmente gli elementi in Revit e verifica che livello e tipologia siano coerenti. Se un GUID è solo del file IFC, non spacciarlo per ElementId di Revit.',
'Open the elements in Revit and confirm level and type information. Do not present an IFC GUID as though it were a Revit ElementId.',
'Il campo `GlobalId` IFC e `ElementId` Revit sono identificatori differenti.',
'IFC `GlobalId` and Revit `ElementId` are different identifier systems.',kind='ifc')
add(m,'a7.3','Parametri e quantità BIM','BIM parameters and quantities',20,
'Le proprietà BIM possono essere di istanza o di tipo, interne a Revit o esportate come pset IFC. Non assumere che un parametro esposto in Revit compaia automaticamente nell’IFC, né che le unità numeriche coincidano senza conversione. Nel file IFC sono presenti attributi `ThermalTransmittance` e `FireRating` in alcune proprietà.',
'BIM properties can be instance- or type-level, native to Revit or exported as IFC psets. A parameter present in Revit is not automatically present in IFC, and numeric units must not be assumed identical. The IFC file includes `ThermalTransmittance` and `FireRating` properties for some objects.',
'Il server Read potrebbe permettere di leggere parametri singoli o elenchi di parametri, in base al catalogo reale dei Tools. Per ogni valore registra identificativo, nome del parametro, contenuto, unità e origine. Gestisci con cura i valori nulli e non applicabili.',
'The Read server may allow retrieval of individual or multiple parameters depending on the actual tool catalogue. For each value record the identifier, parameter name, value, unit and origin. Handle null and not-applicable values carefully.',
'Prompt: «Per cinque pareti, elenca i parametri disponibili relativi ad area, volume e trasmittanza. Distingui tipo e istanza, non calcolare quantità assenti e segnala le unità.»',
'Prompt: “For five walls, list available parameters related to area, volume and thermal transmittance. Distinguish type and instance, do not invent missing quantities, and report units.”',
'Scegli una parete e confronta le proprietà con l’interfaccia Revit. Se l’IFC non ha quantità `IfcQuantityArea`/`IfcQuantityVolume`, non presentarle come già esportate.',
'Select one wall and compare properties with Revit. If the IFC lacks `IfcQuantityArea`/`IfcQuantityVolume`, do not claim they were exported.',
'In questo IFC non risultano entità `IfcQuantityArea` né `IfcQuantityVolume`; il risultato del laboratorio deve basarsi su Revit e sui Tools effettivamente disponibili.',
'This IFC contains no `IfcQuantityArea` or `IfcQuantityVolume` entities; the lab must use live Revit data and actual available tools.',kind='ifc')
add(m,'a7.4','Verifiche informative','Information completeness checks',20,
'Una verifica informativa deve definire il requisito prima di interrogare il modello. Un valore vuoto non equivale a un parametro inesistente; un valore di tipo può essere applicabile a molte istanze. Occorre quindi specificare categoria, ambito, parametro e regole per i valori nulli.',
'An information completeness check must define the requirement before querying the model. An empty value is not the same as a missing parameter; a type-level value can apply to many instances. Define category, scope, parameter and treatment of nulls.',
'Nel caso studio, il file IFC mostra alcune proprietà `FireRating` e `ThermalTransmittance`, ma la loro presenza non implica completezza per tutti gli oggetti. Gli strumenti potrebbero non esporre direttamente query complesse: in tal caso occorre recuperare un insieme e analizzarlo in modo dichiarato.',
'The IFC snapshot contains some `FireRating` and `ThermalTransmittance` properties, but their presence does not prove completeness across all objects. The server might not expose complex filters directly: if so, retrieve a subset and analyse it transparently.',
'Prompt: «Verifica quali porte non hanno un valore Fire Rating utilizzabile. Distingui valore mancante, campo vuoto e parametro non esposto dal Tool. Elenca gli identificativi senza modificare il modello.»',
'Prompt: “Check which doors lack a usable Fire Rating value. Distinguish missing value, empty field and parameter not exposed by the tool. List identifiers without changing the model.”',
'Verifica manualmente almeno due porte, specificando se il parametro è di tipo o di istanza.',
'Manually check at least two doors and document whether the parameter is type- or instance-based.',
'Una conclusione «tutte le porte conformi» richiederebbe prima la formalizzazione di un requisito, non soltanto la presenza della proprietà.',
'Claiming “all doors comply” requires a defined requirement, not merely a populated property.',kind='ifc')
add(m,'a7.5','Report BIM verificabili','Verifiable BIM reports',25,
'Un report prodotto con un LLM è utile quando collega ogni valore a una fonte identificabile. Usa la stessa copia del modello e uno schema tabellare fisso: categoria, numero di istanze, criteri di filtro, identificativi campionati, Tool usato e limitazioni. Il report non deve assumere che tutte le quantità siano affidabili.',
'An LLM-generated report is useful when every value has a traceable source. Use the same model copy and a fixed table schema: category, instance count, filter criteria, sampled IDs, tool used and limitations. Do not assume all quantities are trustworthy.',
'Lo snapshot IFC di riferimento include anche 11 `IfcSlab`, 21 `IfcColumn`, 14 `IfcBeam`, 2 `IfcRoof` e 13 `IfcSpace`. Usa tali conteggi solo per una seconda colonna di confronto IFC, mai come risultato fittizio di una chiamata Revit.',
'The IFC snapshot also contains 11 `IfcSlab`, 21 `IfcColumn`, 14 `IfcBeam`, 2 `IfcRoof` and 13 `IfcSpace`. Use these counts only as a separate IFC reference column, never as invented live Revit results.',
'Prompt: «Produci un report su Walls, Doors, Windows, Slabs, Columns e Beams. Se un numero non è verificabile con i Tools disponibili, scrivi non disponibile. Elenca strumenti e criteri.»',
'Prompt: “Produce a report for Walls, Doors, Windows, Slabs, Columns and Beams. If a figure cannot be verified with available tools, state unavailable. List tools and criteria.”',
'Salva il report e verifica manualmente almeno tre righe o tre identificativi. Aggiungi una nota che distingua l’IFC snapshot dal modello attualmente aperto.',
'Save the report and manually verify at least three rows or three IDs. Add a note distinguishing the IFC snapshot from the currently open model.',
'Un report replicabile include data, versione software e contesto del documento.',
'A reproducible report includes date, software version and document context.',kind='ifc')
quiz(m,[
('Quante entità IfcWall contiene lo snapshot IFC del corso?','How many IfcWall entities are in the course IFC snapshot?',['30','15','7'],['30','15','7'],0,'Conteggio delle istanze `IfcWall` nell’IFC allegato.','Count of `IfcWall` instances in the supplied IFC.'),
('GlobalId IFC ed ElementId Revit...','IFC GlobalId and Revit ElementId...',['sono sempre identici','sono identificativi diversi','sono unità di misura'],['are always identical','are different identifiers','are units of measure'],1,'Usano sistemi distinti; la corrispondenza va verificata.','They use distinct systems; mappings must be verified.'),
('Un valore FireRating vuoto equivale a parametro inesistente?','Is an empty FireRating equal to a missing parameter?',['Sì','Solo con IFC4x3','No'],['Yes','Only in IFC4x3','No'],2,'Distinguere valore assente e proprietà non definita.','Distinguish missing values from undefined properties.'),
('Quale controllo rende verificabile un report AI?','What makes an AI report verifiable?',['Tool, filtri e campioni verificati','Solo testo elegante','Nessuna informazione aggiuntiva'],['Tools, filters and verified samples','Elegant prose alone','No additional information'],0,'La tracciabilità permette un controllo indipendente.','Traceability supports independent validation.'),
('Se il Tool non espone una quantità...','If the tool does not expose a quantity...',['inventala dai colori','segnala la limitazione','cambiala senza permesso'],['invent it from colours','report the limitation','change it without approval'],1,'Non fabbricare numeri per completare il report.','Never fabricate values to fill the report.')])

m=mod('m8','Sviluppare MCP personalizzati','Developing custom MCP servers',70,'Python SDK, Inspector e architettura C#/Revit API','Python SDK, Inspector and C#/Revit API architecture')
add(m,'a8.1','Progettare un Tool BIM','Design a BIM tool',10,
'Il primo passo nello sviluppo non è scrivere codice ma definire uno scopo verificabile, input, output ed errori. Un Tool come `get_model_info` dovrebbe dichiarare origine dei dati, campi restituiti, condizioni di errore e semantica delle unità. Evita Tool generici che permettono di eseguire codice arbitrario sul modello.',
'The first development step is not coding but specifying verifiable purpose, inputs, outputs and errors. A tool such as `get_model_info` should document the data source, output fields, failure modes and units. Avoid generic tools that allow arbitrary code execution against the model.',
'In un progetto BIM è utile distinguere l’identità della sessione (file/documento attivo), l’identità degli oggetti (ID/GUID) e lo schema dei dati. Questa separazione riduce il rischio di modifiche accidentali e risultati ambigui.',
'In a BIM project, distinguish session identity (current file/document), object identity (ID/GUID) and data schema. Keeping these separate reduces accidental modifications and ambiguous results.',
'Progetta un Tool Read che restituisca `{category, count, source}` per un IFC snapshot, specificando esplicitamente che non interroga Revit.',
'Design a Read tool returning `{category, count, source}` for an IFC snapshot, explicitly stating that it does not query Revit.',
'Definisci almeno un caso di successo e uno di errore: per esempio categoria non supportata.',
'Define at least one success and one error case, such as unsupported category.',
'Non confondere demo offline e integrazione Autodesk.','Do not confuse an offline demo with Autodesk integration.')
add(m,'a8.2','Server Python con MCP SDK v2','Python server using MCP SDK v2',20,
'L’SDK Python MCP v2 espone la classe `MCPServer` e decoratori per Tools, Resources e Prompts. Una funzione è richiamabile tramite il protocollo se è stata registrata ed eseguita dentro il server. Per ambienti didattici conviene partire con dati statici e poi sostituire la sorgente.',
'The MCP Python SDK v2 exposes `MCPServer` and decorators for tools, resources and prompts. A function is callable through the protocol once registered and run by the server. For learning, start with static data before swapping in a real data source.',
'Installa `mcp[cli]` tramite uv, crea il file e usa `mcp.run(transport="stdio")` come entrypoint. La funzione demo usa conteggi estratti dall’IFC, validando la categoria richiesta. Non scrivere log su stdout.',
'Install `mcp[cli]` using uv, create the file and use `mcp.run(transport="stdio")` as an entrypoint. The demo function uses counts observed in IFC and validates the requested category. Avoid stdout logging.',
'Il codice di esempio nel pacchetto fornisce `get_course_model_counts` e `get_course_model_info`, così puoi controllare anche l’origine dei numeri e lo schema IFC4X3_ADD2.',
'The downloadable example offers `get_course_model_counts` and `get_course_model_info`, so you can inspect the source of numbers and the IFC4X3_ADD2 schema.',
'Rendi eseguibile il server e aggiungi una categoria supportata dello snapshot, per esempio `IfcSlab` con 11 elementi.',
'Run the server and add another supported snapshot category, such as `IfcSlab` with 11 elements.',
'Non cambiare il dato senza una nuova verifica: un numero dimostrativo non è un conteggio generato dal client AI.',
'Do not change the figure without verifying it: a demo number is not an AI-generated count.',code_text='from mcp.server import MCPServer\nmcp = MCPServer("MCP Academy BIM")\n\n@mcp.tool()\ndef get_course_model_counts(category: str) -> dict:\n    """Read the STATIC IFC course snapshot; does not query Revit."""\n    counts = {"IfcWall":30,"IfcDoor":15,"IfcWindow":7,"IfcSlab":11}\n    if category not in counts:\n        return {"error": "unsupported_category", "category": category}\n    return {"category":category,"count":counts[category],"source":"IFC snapshot"}\n\nif __name__ == "__main__":\n    mcp.run(transport="stdio")',kind='ifc')
add(m,'a8.3','Test indipendenti con Inspector','Independent testing with Inspector',15,
'Prima di collegare un LLM devi sapere se il tuo Tool funziona da solo. L’Inspector consente di ispezionare il catalogo, passare argomenti e registrare risposte. La validazione del codice Python può essere affiancata da unit test locali.',
'Before connecting an LLM, verify the tool works on its own. Inspector exposes the catalogue, lets you pass arguments and record responses. Python logic validation can be supplemented by local unit tests.',
'Testa casi positivi, categorie non supportate e condizioni anomale. Ogni test dovrebbe avere input, output atteso e controllo esplicito. La risposta corretta del Tool non garantisce automaticamente che il modello AI la riassuma bene.',
'Test successful requests, unsupported categories and unexpected conditions. Every test should identify input, expected output and validation. Correct tool output does not automatically guarantee an accurate AI summary.',
'Testa `IfcWall`, poi `UnknownCategory` e confronta struttura e significato dei risultati. Verifica l’assenza di scritture sul modello.',
'Test `IfcWall` and then `UnknownCategory`; compare response structures and meanings. Confirm that no writes occur.',
'Registra input e output in una checklist e correggi eventuali errori prima di passare al collegamento AI.',
'Record inputs and outputs in a checklist and fix issues before connecting an AI client.',
'Una categoria non supportata va documentata come tale; non sempre il conteggio zero è la scelta migliore.',
'An unsupported category should be reported as such; returning zero is not always ideal.',code_text='uv run mcp dev server.py')
add(m,'a8.4','Collegamento al client AI','Connect to an AI client',10,
'Per un server locale STDIO, un client compatibile deve conoscere l’interprete/command, il percorso dello script e gli argomenti di avvio. Claude Desktop utilizza `claude_desktop_config.json`; nel file non inserire token né credenziali nel repository.',
'For a local STDIO server, a compatible client needs the command/interpreter, script path and startup arguments. Claude Desktop uses `claude_desktop_config.json`; do not commit tokens or credentials to your repository.',
'Usa l’interprete Python dell’ambiente virtuale in modo che trovi il pacchetto `mcp`. Se il piano AI gratuito è limitato o temporaneamente esaurito, verifica comunque il server con Inspector, senza acquistare crediti API.',
'Use the virtual environment interpreter so the `mcp` dependency is found. If free AI usage is limited or exhausted, keep testing with Inspector rather than buying API credits.',
'Chiedi all’AI di elencare i Tools del server didattico e poi di chiamare `get_course_model_counts` sulla categoria `IfcDoor`, segnalando la fonte statica.',
'Ask the AI to list the demo server tools and then call `get_course_model_counts` for `IfcDoor`, disclosing the static source.',
'Confronta l’output di Claude con Inspector. La conversazione non deve attribuire al modello aperto in Revit i dati dello snapshot.',
'Compare Claude’s answer with Inspector. The chat must not attribute the snapshot data to a live open Revit model.',
'Se il client non è disponibile gratuitamente, il laboratorio resta verificabile tramite Inspector.',
'If the client is not available for free, the lab remains verifiable through Inspector.',code_text=r'''{
  "mcpServers": {
    "bim-academy": {
      "command": "C:\\PATH\\mcp-lab\\.venv\\Scripts\\python.exe",
      "args": ["C:\\PATH\\mcp-lab\\server.py"]
    }
  }
}''')
add(m,'a8.5','Architettura Revit API e C#','Revit API and C# architecture',15,
'Una chiamata proveniente da un processo MCP non può invocare arbitrariamente le API di Revit da un thread esterno. Un possibile progetto usa un add-in C# che riceve richieste tramite un bridge locale e ne pianifica l’esecuzione nel contesto autorizzato tramite `ExternalEvent`.',
'A request arriving at an MCP process cannot call the Revit API arbitrarily from an external thread. One architecture uses a C# add-in that receives messages from a local bridge and schedules them on an authorised context using `ExternalEvent`.',
'Per Revit 2027 Autodesk indica .NET 10 per lo sviluppo add-in. Occorrono quindi progetto C#, riferimenti alle API Revit, manifest `.addin`, gestione del ciclo di vita e comunicazione con Python. È una parte sostanzialmente più complessa del Tool statico.',
'For Revit 2027 Autodesk specifies .NET 10 for add-ins. You need a C# project, Revit API references, a `.addin` manifest, lifecycle handling and Python communication. This is substantially more complex than a static-data tool.',
'Il Developer Lab facoltativo fornisce un progetto iniziale: backend Python, add-in C#, bridge locale e check end-to-end. Il suo codice non va trattato come collaudato su Revit finché non viene compilato ed eseguito su una macchina Windows idonea.',
'The optional Developer Lab provides a starter: Python backend, C# add-in, local bridge and end-to-end checks. Its code must not be treated as validated on Revit until built and run on a suitable Windows machine.',
'Disegna il confine tra processo Python, listener, `ExternalEvent.Execute` e Revit Document. Individua dove vanno validati gli argomenti.',
'Draw the boundary between Python process, listener, `ExternalEvent.Execute` and the Revit Document. Identify where arguments should be validated.',
'Validazione prima del bridge e nel contesto Revit: mai fidarsi degli input solo perché arrivano da un client MCP.',
'Validate both before the bridge and in the Revit context: never blindly trust input because it came from an MCP client.',kind='flow')
quiz(m,[
('Quale SDK Python è presentato nel corso?','Which Python SDK is used in the course?',['MCP SDK v2','IfcOpenShell obbligatorio','Dynamo soltanto'],['MCP SDK v2','Mandatory IfcOpenShell','Dynamo only'],0,'Il codice usa `MCPServer` dello SDK v2.','The examples use `MCPServer` from SDK v2.'),
('Il server demo legge il modello RVT aperto?','Does the demo server query the open RVT?',['Sì','No, legge uno snapshot statico','Solo se Claude Pro'],['Yes','No, it reads a static snapshot','Only with Claude Pro'],1,'Il dato statico viene da un’analisi dell’IFC di riferimento.','The static numbers derive from analysis of the supplied IFC.'),
('Quale classe Revit aiuta a gestire chiamate esterne nel contesto API?','Which Revit mechanism can marshal requests into an API context?',['ExternalEvent','IfcQuantityArea','JSON.stringify'],['ExternalEvent','IfcQuantityArea','JSON.stringify'],0,'ExternalEvent permette di programmare operazioni in un contesto Revit previsto.','ExternalEvent schedules operations in an appropriate Revit context.'),
('Qual è il framework .NET per add-in Revit 2027?','What .NET target is specified for Revit 2027 add-ins?',['.NET Framework 4.8','.NET 10','.NET 5'],['.NET Framework 4.8','.NET 10','.NET 5'],1,'Autodesk ha aggiornato Revit 2027 a .NET 10.','Autodesk migrated Revit 2027 to .NET 10.'),
('Un server MCP Python deve stampare debug su stdout quando usa STDIO?','Should a Python MCP STDIO server print debug messages to stdout?',['Sì','Non importa','No'],['Yes','It does not matter','No'],2,'stdout è usato dal trasporto MCP.','stdout carries MCP transport messages.')])

extra={
 'optionalLabs':[
  {'id':'write','title':{'it':'Write Lab — Modifica controllata','en':'Write Lab — Controlled editing'},'mins':25,'it':'Facoltativo. Crea una copia del progetto, attiva solo i Tools Write disponibili e individua una proprietà scrivibile non critica su un singolo elemento. Prima di procedere chiedi al client di mostrare Tool, elemento, parametro, vecchio e nuovo valore. Approva soltanto una modifica verificabile, confronta in Revit e usa Undo se serve. I nomi dei Tools dipendono dalla tua build.', 'en':'Optional. Copy the project, enable only available Write tools and choose a non-critical writable property on one element. First ask the client to show the tool, element, parameter, old and proposed values. Approve only a verifiable change, cross-check in Revit and use Undo if needed. Exact tools depend on your build.'},
  {'id':'developer','title':{'it':'Developer Lab — Custom Revit MCP','en':'Developer Lab — Custom Revit MCP'},'mins':150,'it':'Facoltativo, 2–3 ore aggiuntive. Usa lo Starter Project Python/C# per implementare un bridge locale read-only tra MCPServer e la Revit API, compilare un add-in .NET 10 e verificarne il funzionamento sul modello aperto. Il codice è uno starter didattico da collaudare in un ambiente Revit reale. Non distribuire il modello originale senza autorizzazione.', 'en':'Optional, an additional 2–3 hours. Use the Python/C# Starter Project to implement a local read-only bridge between MCPServer and the Revit API, build a .NET 10 add-in and test it on the open model. The source is a learning starter requiring real Revit validation. Do not redistribute the original model without permission.'}
 ],
 'model':{'schema':'IFC4X3_ADD2','origin':'Autodesk Revit 27.3.0.28 (IFC export metadata)','classes':{'IfcWall':30,'IfcDoor':15,'IfcWindow':7,'IfcSlab':11,'IfcColumn':21,'IfcBeam':14,'IfcRoof':2,'IfcSpace':13,'IfcBuildingStorey':6,'IfcStair':1,'IfcRailing':5},'levels':['A_S_0','A_A_0','A_S_1','A_A_1','A_S_2','A_A_2'],'spaces':['Kitchen','Garage','Living Room','Bathroom','Single Bedroom','Boiler rooom','Master Bedroom','Corridor','Storage room','Anteroom','Attic'],'quantityNotes':{'it':'L’IFC non contiene IfcQuantityArea/IfcQuantityVolume; non confondere le quantità Revit con QTO IFC esportate.','en':'The IFC contains no IfcQuantityArea/IfcQuantityVolume; do not confuse live Revit quantities with exported IFC QTO.'}},
 'sources':[
  {'title':'Model Context Protocol — specification 2026-07-28','url':'https://modelcontextprotocol.io/specification/2026-07-28'},
  {'title':'Autodesk — Revit Public MCP Server','url':'https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_revit_mcp_server_html'},
  {'title':'Autodesk — Setting Up Revit MCP','url':'https://help.autodesk.com/view/ADSKMCP/ENU/?guid=ADSKMCP_RevitMcp_setting_up_revit_mcp_server_html'},
  {'title':'Official MCP Python SDK v2','url':'https://py.sdk.modelcontextprotocol.io/'},
  {'title':'Autodesk — Revit 2027 .NET 10','url':'https://help.autodesk.com/cloudhelp/2027/ITA/Revit-WhatsNew/files/GUID-8D7A4715-EAF8-4BD1-BE78-061F900D0BCE.htm'},
  {'title':'Autodesk — Revit API External Events','url':'https://help.autodesk.com/cloudhelp/2026/ENU/Revit-API/files/Revit_API_Developers_Guide/Advanced_Topics/Revit_API_Revit_API_Developers_Guide_Advanced_Topics_External_Events_html.html'}
 ]
}
allLessons=[l for m in MODULES for l in m['lessons']]
assert len(MODULES)==8 and len(allLessons)==28 and sum(m['mins'] for m in MODULES)==420,(len(allLessons),sum(m['mins'] for m in MODULES))
assert all(len(m['quiz'])==5 for m in MODULES)
assert all(sum(x['mins'] for x in m['lessons'])==m['mins'] for m in MODULES)
result={'version':'2.0.0','updated':'2026-10-14','author':'Ygor Fasanella','modules':MODULES,**extra}
(ROOT/'assets'/'advanced-data.js').write_text('window.MCP_ADVANCED_DATA = '+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
(ROOT/'assets'/'advanced-data.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print('Modules:',len(MODULES),'lessons:',len(allLessons),'quiz:',sum(len(m['quiz']) for m in MODULES),'bytes:',(ROOT/'assets'/'advanced-data.js').stat().st_size)