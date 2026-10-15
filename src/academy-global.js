/* MCP4BIM Academy global navigation: one Search, Glossary, and Progress experience across both tracks. */
(() => {
  'use strict';
  const EKEY = 'mcp-academy-progress-v1';
  const AKEY = 'mcp-academy-advanced-v2';
  const essentials = typeof ACADEMY_DATA !== 'undefined' ? ACADEMY_DATA : null;
  const advanced = window.MCP_ADVANCED_DATA || null;
  if (!essentials || !advanced || !window.MCPAcademyProgress) {
    console.warn('MCP4BIM Academy: global tools require both course data sets.');
    return;
  }
  const currentTrack = document.getElementById('adv-root') ? 'advanced' : 'essentials';
  const ADVANCED_GLOSSARY = [
    ['MCP','Protocollo che collega applicazioni AI a Tools, Resources e Prompts.','Protocol connecting AI applications to tools, resources and prompts.'],
    ['Host','Applicazione che gestisce l’esperienza AI e i collegamenti MCP.','Application managing the AI experience and MCP connections.'],
    ['Client','Componente che comunica con un server MCP.','Component that communicates with an MCP server.'],
    ['Server','Programma che espone strumenti e dati mediante MCP.','Program exposing tools and data through MCP.'],
    ['STDIO','Trasporto MCP tramite input/output standard del processo.','MCP transport over a process standard input/output.'],
    ['Streamable HTTP','Trasporto MCP su endpoint HTTP.','MCP transport over HTTP endpoints.'],
    ['Tool','Operazione richiamabile tramite nome e argomenti.','Callable operation with a name and arguments.'],
    ['Resource','Contenuto consultabile identificato da URI.','Readable content addressed by a URI.'],
    ['Prompt','Template di istruzioni riutilizzabile.','Reusable instruction template.'],
    ['IfcWall','Entità IFC che rappresenta una parete.','IFC entity representing a wall.'],
    ['ExternalEvent','Meccanismo della Revit API per eseguire operazioni dal contesto appropriato.','Revit API mechanism to execute operations within an appropriate context.'],
    ['JSON-RPC','Formato strutturato per messaggi di richiesta e risposta.','Structured request/response message format.']
  ];
  const entries = new Map();
  for (const term of essentials.glossary) entries.set(term.term.toLocaleLowerCase(), { ...term });
  for (const [term,it,en] of ADVANCED_GLOSSARY) {
    if (!entries.has(term.toLocaleLowerCase())) entries.set(term.toLocaleLowerCase(),{term,it,en});
  }
  const glossary = [...entries.values()].sort((a,b)=>a.term.localeCompare(b.term));
  const allAdvanced = advanced.modules.flatMap(m => m.lessons);
  const allEssential = essentials.lessons;
  const validIds = {
    essentials: new Set(allEssential.map(l=>l.id)),
    advanced: new Set(allAdvanced.map(l=>l.id))
  };
  const state = { view:null, tab:currentTrack, search:'', term:'', scroll:0, notice:'', modalParent:null, modalParentScroll:0 };
  const esc = value => String(value ?? '').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const language = () => {
    try {
      const key = currentTrack === 'advanced' ? AKEY : EKEY;
      const item = JSON.parse(localStorage.getItem(key) || 'null');
      if (item && ['it','en'].includes(item.lang)) return item.lang;
    } catch (_) {}
    return document.documentElement.lang === 'en' ? 'en' : 'it';
  };
  const tr = (it,en) => language()==='it' ? it : en;
  const loc = x => typeof x === 'string' ? x : x?.[language()] || '';
  const read = key => {try {const x=JSON.parse(localStorage.getItem(key)||'null');return x && typeof x==='object'?x:{};}catch(_){return {};}};
  const icon = name => {
    const a = name==='search' ? '<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>' : name==='close' ? '<path d="M5 5l14 14M19 5 5 19"/>' : name==='back' ? '<path d="m19 12-14 0m6 6-6-6 6-6"/>' : '<path d="m5 12 14 0m-6-6 6 6-6 6"/>';
    return `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${a}</svg>`;
  };
  function baseSearch() {
    const records=[];
    for (const l of essentials.lessons) {
      for (let i=0;i<l.steps.length;i++) {
        const s=l.steps[i];const text=s.blocks[language()].filter(b=>b.type==='p'||b.type==='note'||b.type==='bullets').flatMap(b=>b.text?[b.text]:b.items||[]).join(' ');
        records.push({course:'essentials',lesson:l.id,step:i,module:tr('MCP Essentials','MCP Essentials'),title:loc(l.title),stepTitle:loc(s.title),description:text});
      }
    }
    for (const m of advanced.modules)for(const l of m.lessons)for(let i=0;i<l.steps.length;i++){
      const s=l.steps[i];records.push({course:'advanced',lesson:l.id,step:i,module:loc(m.title),title:loc(l.title),stepTitle:loc(s.title),description:loc(s.text)});
    }
    for(const lab of advanced.optionalLabs||[]){
      records.push({course:'advanced',optional:lab.id,lesson:lab.id,step:0,module:tr('Laboratorio facoltativo','Optional lab'),title:loc(lab.title),stepTitle:loc(lab.title),description:lab[language()]||''});
    }
    return records;
  }
  function resultHref(x) {
    const base=x.course==='advanced' ? './advanced.html' : './index.html';
    return x.optional ? `${base}?optional=${encodeURIComponent(x.optional)}` : `${base}?lesson=${encodeURIComponent(x.lesson)}&step=${x.step}`;
  }
  function searchResults() {
    const q=state.search.trim().toLocaleLowerCase();
    const grouped=new Map();
    for(const rec of baseSearch()) {
      const content=[rec.module,rec.title,rec.stepTitle,rec.description].join(' ').toLocaleLowerCase();
      if(!q || content.includes(q)){
        const key=rec.course+'-'+rec.lesson;
        if(!grouped.has(key) || q) {
          // With a query, the first matching step of a lesson is the destination.
          if (!grouped.has(key)) grouped.set(key,rec);
        }
      }
    }
    return [...grouped.values()];
  }
  function searchPage() {
    const results=searchResults();
    return `<main class="ag-utility-page ag-search-page"><button class="ag-back" data-academy="back">${icon('back')} ${tr('Torna alla pagina precedente','Back to previous page')}</button><div class="ag-utility-head"><span class="ag-overline">INDEX / SEARCH · MCP4BIM ACADEMY</span><h1>${tr('Cerca','Search')}</h1><p>${tr('Cerca in tutte le lezioni di Essentials e Advanced. Seleziona un risultato per aprire direttamente l’argomento.','Search every lesson in Essentials and Advanced. Select a result to open its topic directly.')}</p></div><label class="ag-search-wrap">${icon('search')}<input id="ag-search-field" type="search" autocomplete="off" placeholder="${tr('Cerca tra lezioni, moduli e argomenti…','Search lessons, modules and topics…')}" value="${esc(state.search)}" aria-label="${tr('Cerca in tutta l’Academy','Search the entire Academy')}"></label><p class="ag-result-count">${results.length} ${tr('risultati in entrambi i corsi','results across both courses')}</p><div class="ag-search-results">${results.length?results.map(x=>`<a class="ag-search-result" href="${resultHref(x)}"><div class="ag-result-meta"><span class="ag-course-chip">MCP ${x.course==='advanced'?'Advanced':'Essentials'}</span><span>${esc(x.module)}${x.optional?' · OPTIONAL':''}</span></div><strong>${esc(x.title)} / ${esc(x.stepTitle)}</strong><p>${esc(x.description.replace(/\*\*/g,'').slice(0,175))}${x.description.length>175?'…':''}</p><span class="ag-result-arrow">${icon('arrow')}</span></a>`).join(''):`<p class="ag-empty">${tr('Nessun contenuto corrispondente.','No matching content.')}</p>`}</div></main>`;
  }
  function glossaryModal() {
    const q=state.term.trim().toLocaleLowerCase();
    const matches=glossary.filter(x=>!q || (x.term+' '+x[language()]).toLocaleLowerCase().includes(q));
    return `<div class="ag-backdrop" id="ag-glossary-backdrop" data-academy="backdrop"><div class="ag-modal-panel" role="dialog" aria-modal="true" aria-labelledby="ag-glossary-title"><div class="ag-modal-head"><div><span class="ag-overline">REFERENCE · MCP4BIM ACADEMY</span><h2 id="ag-glossary-title">${tr('Glossario','Glossary')}</h2><p>${tr('Definizioni condivise di Essentials e Advanced, disponibili in entrambe le lingue.','Definitions from Essentials and Advanced in both languages.')}</p></div><button class="ag-modal-close" data-academy="close" aria-label="${tr('Chiudi il glossario','Close glossary')}">${icon('close')}</button></div><label class="ag-search-wrap">${icon('search')}<input id="ag-glossary-field" type="search" autocomplete="off" value="${esc(state.term)}" placeholder="${tr('Cerca un termine…','Search for a term…')}" aria-label="${tr('Cerca nel glossario','Search glossary')}"></label><div class="ag-glossary-list">${matches.length?matches.map(x=>`<div class="ag-term"><h3>${esc(x.term)}</h3><p>${esc(x[language()])}</p></div>`).join(''):`<p class="ag-empty">${tr('Nessun termine trovato.','No term found.')}</p>`}</div></div></div>`;
  }
  // The two course cards are the tab controls; no Academy-wide aggregate is displayed.
  function tabs() {
    const snapshot=window.MCPAcademyProgress.snapshot();
    return `<div class="ag-course-tabs" role="tablist" aria-label="${tr('Percorsi formativi','Learning tracks')}">${['essentials','advanced'].map((course,index)=>{
      const data=snapshot[course], active=state.tab===course;
      const quiz=course==='essentials'?`${tr('Miglior quiz finale','Best final quiz')}: <b>${data.best}%</b>`:`${tr('Quiz dei moduli superati','Module quizzes passed')}: <b>${data.passed}/${data.totalQuizzes}</b>`;
      return `<button id="ag-tab-${course}" class="ag-course-tab${active?' is-active':''}" role="tab" aria-selected="${active}" tabindex="${active?0:-1}" data-academy="tab" data-tab="${course}" aria-controls="ag-tabpanel"><div class="ag-course-head"><div><span class="ag-course-overline">0${index+1} / ${tr('PERCORSO','TRACK')}</span><h2>MCP ${course==='essentials'?'Essentials':'Advanced'}</h2></div><strong class="ag-course-percent">${data.percent}%</strong></div><div class="ag-course-meter" role="progressbar" aria-label="MCP ${course} ${tr('completamento','completion')}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${data.percent}"><span style="width:${data.percent}%"></span></div><div class="ag-course-foot"><span>${data.completed} / ${data.total} ${tr('lezioni completate','lessons completed')}</span><span>${quiz}</span></div>${course==='advanced'?`<p class="ag-course-note">${tr('I laboratori facoltativi non influenzano questa percentuale.','Optional labs do not affect this percentage.')}</p>`:''}</button>`;
    }).join('')}</div>`;
  }
  function progressDetail() {
    const snapshot=window.MCPAcademyProgress.snapshot();
    const e=read(EKEY),a=read(AKEY);
    const isAdvanced=state.tab==='advanced';
    const x=isAdvanced?snapshot.advanced:snapshot.essentials;
    const completed=new Set(x.lessonIds);
    const stats=isAdvanced?[
      [x.completed+'/'+x.total,tr('lezioni principali completate','core lessons completed')],
      [x.passed+'/'+x.totalQuizzes,tr('quiz superati','module quizzes passed')],
      [(Array.isArray(a.optional)?a.optional.filter(s=>advanced.optionalLabs.some(o=>o.id===s)):[]).length+'/'+advanced.optionalLabs.length,tr('laboratori facoltativi (separati)','optional labs (separate)')]
    ]:[
      [x.completed+'/'+x.total,tr('lezioni completate','lessons completed')],
      [x.best+'%',tr('miglior risultato del quiz finale','best final quiz score')],
      [x.best>=80?tr('Superato','Passed'):tr('Non superato','Not passed'),tr('quiz conclusivo (soglia 80%)','final quiz (80% to pass)')]
    ];
    const modules=isAdvanced?advanced.modules.map((m,i)=>{
      const done=m.lessons.filter(l=>completed.has(l.id)).length;
      const grade=Number(a.quizzes?.[m.id]||0);
      return `<a class="ag-progress-module" href="./advanced.html?module=${encodeURIComponent(m.id)}"><b>${esc(loc(m.title))} — ${Math.round(done/m.lessons.length*100)}%</b><small>${done}/${m.lessons.length} ${tr('lezioni','lessons')} · ${tr('Miglior quiz','Best quiz')}: ${grade}%</small></a>`;
    }).join(''):
      essentials.lessons.map((l,i)=>`<a class="ag-progress-module" href="./index.html?lesson=${encodeURIComponent(l.id)}&step=0"><b>${completed.has(l.id)?'✓ ':''}${esc(loc(l.title))}</b><small>${tr('Lezione','Lesson')} ${i+1} · ${completed.has(l.id)?tr('Completata','Completed'):tr('Non ancora completata','Not yet completed')}</small></a>`).join('');
    return `<div id="ag-tabpanel" role="tabpanel" aria-labelledby="ag-tab-${state.tab}"><h2 class="ag-detail-heading">${isAdvanced?tr('Dettaglio Advanced','Advanced details'):tr('Dettaglio Essentials','Essentials details')}</h2><div class="ag-progress-grid">${stats.map(([value,desc])=>`<div class="ag-progress-stat"><b>${esc(value)}</b><span>${esc(desc)}</span></div>`).join('')}</div><div class="ag-util-card"><h2>${tr('Backup dei progressi','Progress backup')} ${isAdvanced?'Advanced':'Essentials'}</h2><p class="ag-helper">${tr('I progressi dei due percorsi sono conservati separatamente nello stesso browser. Questi comandi agiscono soltanto su','Both tracks are stored separately in this browser. These controls affect only')} ${isAdvanced?'Advanced':'Essentials'}.</p><div class="ag-actions"><button data-academy="export" class="ag-button light">${tr('Esporta JSON','Export JSON')}</button><button data-academy="import" class="ag-button light">${tr('Importa JSON','Import JSON')}</button><button data-academy="reset" class="ag-button light">${tr('Azzera','Reset')} ${isAdvanced?'Advanced':'Essentials'}</button></div><input id="ag-import-input" type="file" accept=".json,application/json" hidden></div><div class="ag-util-card"><h2>${isAdvanced?tr('Moduli Advanced','Advanced modules'):tr('Lezioni Essentials','Essentials lessons')}</h2>${modules}</div></div>`;
  }
  function progressPage() {
    return `<main class="ag-advanced-utility"><span class="ag-overline">MY LEARNING</span><h1>${tr('Progressi Academy','Academy progress')}</h1><p class="ag-progress-intro">${tr('Le percentuali considerano le lezioni dei percorsi principali. I laboratori facoltativi non contano nel completamento di Advanced.','Percentages cover lessons in the core tracks. Optional labs do not count toward Advanced completion.')}</p>${tabs()}${progressDetail()}${state.notice?`<p class="ag-notice" role="status">${esc(state.notice)}</p>`:''}</main>`;
  }
  function removeSurface() {document.getElementById('academy-global-ui')?.remove();document.body.classList.remove('academy-global-page','academy-global-dialog');}
  function render(focusId=null) {
    if(!state.view)return;
    removeSurface();
    if(state.view==='glossary') {
      document.body.classList.add('academy-global-dialog');
      if(state.modalParent) document.body.classList.add('academy-global-page');
    } else document.body.classList.add('academy-global-page');
    const el=document.createElement('div');el.id='academy-global-ui';
    const previous=state.modalParent==='progress'?progressPage():state.modalParent==='search'?searchPage():'';
    el.innerHTML=state.view==='glossary'?previous+glossaryModal():state.view==='search'?searchPage():progressPage();
    document.body.appendChild(el);
    if(focusId) {
      const input=document.getElementById(focusId);input?.focus();
      const caret= input?.value.length || 0;
      try {input?.setSelectionRange(caret,caret);}catch(_){}
    }
  }
  function open(view) {
    if(!state.view)state.scroll=window.scrollY;
    if(view==='glossary' && state.view && state.view!=='glossary') {
      state.modalParent=state.view;
      state.modalParentScroll=window.scrollY;
    } else if(view!=='glossary') state.modalParent=null;
    state.view=view;state.notice='';
    if(view==='search')state.search='';
    if(view==='glossary')state.term='';
    render(view==='glossary'?'ag-glossary-field':view==='search'?'ag-search-field':null);
    if(view!=='glossary')window.scrollTo(0,0);
  }
  function close() {
    if(!state.view)return;
    if(state.view==='glossary' && state.modalParent){
      const prior=state.modalParent, scroll=state.modalParentScroll;
      state.modalParent=null;state.view=prior;render();window.scrollTo(0,scroll);return;
    }
    removeSurface();state.view=null;state.modalParent=null;state.notice='';
    window.scrollTo(0,state.scroll);
  }
  function download(data,name) {
    const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
    const a=document.createElement('a');a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),1500);
  }
  function exportState() {
    if(state.tab==='advanced') {
      const a=read(AKEY);download({format:'MCP_Academy_Advanced_Progress',schema:2,lang:a.lang||language(),lesson:a.lesson||'a1.1',step:a.step||0,completed:a.completed||[],quizzes:a.quizzes||{},checks:a.checks||{},optional:a.optional||[],view:'home'},'mcp-academy-advanced-progress.json');
    }else {
      const e=read(EKEY);download({format:'MCP_Academy_Progress',schema:1,lang:e.lang||language(),lessonId:e.lessonId||'e1',step:e.step||0,completed:e.completed||[],best:e.best||0,exportedAt:new Date().toISOString()},'mcp-academy-progress.json');
    }
  }
  function refreshAfterChange() {
    try { sessionStorage.setItem('mcp-academy-global-return',JSON.stringify({view:'progress',tab:state.tab})); }catch(_){}
    window.location.reload();
  }
  async function importState(file) {
    try {
      const x=JSON.parse(await file.text());
      if(state.tab==='advanced'){
        if(x.format!=='MCP_Academy_Advanced_Progress'||x.schema!==2||!Array.isArray(x.completed)||!x.completed.every(v=>validIds.advanced.has(v)))throw Error('invalid');
        const prior=read(AKEY);
        const data={...prior,...x,completed:[...new Set(x.completed)],lang:prior.lang||language(),view:'home'};
        localStorage.setItem(AKEY,JSON.stringify(data));
      }else{
        if(x.format!=='MCP_Academy_Progress'||x.schema!==1||!Array.isArray(x.completed)||!x.completed.every(v=>validIds.essentials.has(v))||!validIds.essentials.has(x.lessonId)||!Number.isFinite(x.best)||x.best<0||x.best>100||!Number.isInteger(x.step))throw Error('invalid');
        const prior=read(EKEY);
        const data={...prior,...x,completed:[...new Set(x.completed)],lang:prior.lang||language(),view:'home'};
        localStorage.setItem(EKEY,JSON.stringify(data));
      }
      refreshAfterChange();
    }catch(_) {state.notice=tr('Il file non è un backup valido di questo percorso.','This file is not a valid backup for this track.');render();}
  }
  function resetState() {
    const target=state.tab==='advanced'?'Advanced':'Essentials';
    if(!window.confirm(tr(`Vuoi azzerare soltanto ${target}? L’altro percorso non sarà modificato.`,`Reset only ${target}? The other track will be unaffected.`)))return;
    const key=state.tab==='advanced'?AKEY:EKEY;
    const lang=language();
    const zero=state.tab==='advanced'?{lang,view:'home',lesson:'a1.1',step:0,completed:[],quizzes:{},checks:{},optional:[]}:{lang,view:'home',lessonId:'e1',step:0,completed:[],best:0};
    localStorage.setItem(key,JSON.stringify(zero));
    refreshAfterChange();
  }
  function action(name,element) {
    switch(name) {
      case 'close':case 'back':close();break;
      case 'tab': state.tab=element.dataset.tab;state.notice='';render();document.getElementById('ag-tab-'+state.tab)?.focus();break;
      case 'export':exportState();break;
      case 'import':document.getElementById('ag-import-input')?.click();break;
      case 'reset':resetState();break;
    }
  }
  // Capture global header commands before the individual course's legacy router.
  document.addEventListener('click',event=>{
    // Global tools work from the header, the home hero and either course sidebar.
    const navButton=event.target.closest('[data-academy-nav]');
    if(navButton){
      const nav=navButton.dataset.academyNav;
      if(nav==='search'||nav==='glossary'||nav==='progress'){event.preventDefault();event.stopImmediatePropagation();open(nav);return;}
      if(nav==='language'){
        event.preventDefault();event.stopImmediatePropagation();
        const requested=navButton.dataset.lang;
        if(!['it','en'].includes(requested))return;
        window.MCPAcademySetLanguage?.(requested);
        for(const key of [EKEY,AKEY]){try{const item=JSON.parse(localStorage.getItem(key)||'null');if(item&&typeof item==='object'){item.lang=requested;localStorage.setItem(key,JSON.stringify(item));}}catch(_){}}
        if(state.view)render(state.view==='search'?'ag-search-field':state.view==='glossary'?'ag-glossary-field':null);
        return;
      }
      if(nav==='menu'){event.preventDefault();event.stopImmediatePropagation();window.MCPAcademyToggleMenu?.();return;}
    }
    const toolButton=event.target.closest('[data-action="search"], [data-action="glossary"], [data-action="progress"], [data-act="search"], [data-act="glossary"], [data-act="progress"]');
    if(toolButton){
      event.preventDefault();event.stopPropagation();
      open(toolButton.dataset.action || toolButton.dataset.act);return;
    }
    const headerButton=event.target.closest('.topbar [data-action], .topbar [data-act]');
    const headerAction=headerButton?.dataset.action||headerButton?.dataset.act;
    if(headerAction==='lang'||headerAction==='language') {
      queueMicrotask(()=>{if(state.view)render();});
    }
    if(headerAction==='home' && state.view)close();
    const within=event.target.closest('#academy-global-ui');
    if(within){
      const btn=event.target.closest('[data-academy]');
      if(btn) {
        if(btn.dataset.academy==='backdrop' && btn!==event.target)return;
        event.preventDefault();event.stopPropagation();action(btn.dataset.academy,btn);
      }
    }
  },true);
  document.addEventListener('input',event=>{
    if(event.target.id==='ag-search-field'){state.search=event.target.value;render('ag-search-field');}
    if(event.target.id==='ag-glossary-field'){state.term=event.target.value;render('ag-glossary-field');}
  },true);
  document.addEventListener('change',event=>{
    if(event.target.id==='ag-import-input'&&event.target.files?.[0])importState(event.target.files[0]);
  },true);
  document.addEventListener('keydown',event=>{
    if(state.view && event.key==='Escape') {event.preventDefault();event.stopPropagation();close();return;}
    const tab=event.target.closest?.('.ag-course-tabs [role="tab"]');
    if(tab && (event.key==='ArrowLeft'||event.key==='ArrowRight')){
      event.preventDefault();state.tab=state.tab==='advanced'?'essentials':'advanced';render();document.getElementById('ag-tab-'+state.tab)?.focus();
    }
  },true);
  window.addEventListener('storage',event=>{if(state.view && (event.key===EKEY||event.key===AKEY))render();});
  const pending=(()=>{try{const x=JSON.parse(sessionStorage.getItem('mcp-academy-global-return')||'null');sessionStorage.removeItem('mcp-academy-global-return');return x;}catch(_){return null;}})();
  if(pending?.view==='progress') {state.tab=pending.tab==='essentials'?'essentials':'advanced';open('progress');}
})();