/* Shared Academy progress overview; independent track state, no external requests. */
window.MCPAcademyProgress = (() => {
  'use strict';
  const ESSENTIALS_KEY = 'mcp-academy-progress-v1';
  const ADVANCED_KEY = 'mcp-academy-advanced-v2';
  const ESSENTIALS_LESSONS = ['e1','e2','e3','e4','e5'];
  const ADVANCED_MODULES = [{"id":"m1","title":{"it":"Fondamenti MCP","en":"MCP foundations"},"lessons":["a1.1","a1.2","a1.3"]},{"id":"m2","title":{"it":"Architettura MCP","en":"MCP architecture"},"lessons":["a2.1","a2.2","a2.3"]},{"id":"m3","title":{"it":"Tools, Resources e Prompts","en":"Tools, Resources and Prompts"},"lessons":["a3.1","a3.2","a3.3"]},{"id":"m4","title":{"it":"Primo server MCP","en":"Your first MCP server"},"lessons":["a4.1","a4.2","a4.3"]},{"id":"m5","title":{"it":"MCP per Autodesk Revit","en":"MCP for Autodesk Revit"},"lessons":["a5.1","a5.2","a5.3"]},{"id":"m6","title":{"it":"Installazione e connessione a Revit","en":"Installing and connecting to Revit"},"lessons":["a6.1","a6.2","a6.3"]},{"id":"m7","title":{"it":"Laboratori BIM sul modello comune","en":"BIM labs using the shared model"},"lessons":["a7.1","a7.2","a7.3","a7.4","a7.5"]},{"id":"m8","title":{"it":"Sviluppare MCP personalizzati","en":"Developing custom MCP servers"},"lessons":["a8.1","a8.2","a8.3","a8.4","a8.5"]}];
  const ADVANCED_IDS = ADVANCED_MODULES.flatMap(module => module.lessons);
  function read(key) {
    try { const value = JSON.parse(localStorage.getItem(key) || 'null');
      return value && typeof value === 'object' ? value : {};
    } catch (_) { return {}; }
  }
  function validCompleted(value, ids) {
    if (!Array.isArray(value)) return [];
    const valid = new Set(ids);
    return [...new Set(value.filter(id => typeof id === 'string' && valid.has(id)))];
  }
  function snapshot() {
    const e = read(ESSENTIALS_KEY);
    const a = read(ADVANCED_KEY);
    const essentials = validCompleted(e.completed, ESSENTIALS_LESSONS);
    // Optional labs are deliberately excluded: only module lessons count.
    const advanced = validCompleted(a.completed, ADVANCED_IDS);
    const quizzes = a.quizzes && typeof a.quizzes === 'object' ? a.quizzes : {};
    return {
      essentials: {
        completed: essentials.length, total: ESSENTIALS_LESSONS.length,
        percent: Math.round(essentials.length / ESSENTIALS_LESSONS.length * 100),
        best: Number.isFinite(Number(e.best)) ? Math.min(100,Math.max(0,Number(e.best))) : 0,
        lessonIds: essentials
      },
      advanced: {
        completed: advanced.length, total: ADVANCED_IDS.length,
        percent: Math.round(advanced.length / ADVANCED_IDS.length * 100),
        lessonIds: advanced,
        passed: ADVANCED_MODULES.filter(m => Number(quizzes[m.id]) >= 80).length,
        totalQuizzes: ADVANCED_MODULES.length,
        modules: ADVANCED_MODULES.map(m => ({
          id: m.id, title: m.title,
          completed: m.lessons.filter(id => advanced.includes(id)).length,
          total: m.lessons.length
        }))
      }
    };
  }
  function cards(language = 'it') {
    const it = language !== 'en';
    const all = snapshot();
    const entries = [
      {id:'essentials', name:'Essentials', number:'01', href:'./index.html', info: it?'Quiz finale migliore':'Best final quiz', extra: all.essentials.best + '%', course:all.essentials},
      {id:'advanced', name:'Advanced', number:'02', href:'./advanced.html', info: it?'Quiz dei moduli superati':'Module quizzes passed', extra:all.advanced.passed + '/' + all.advanced.totalQuizzes, course:all.advanced}
    ];
    return '<section class="academy-progress-grid" aria-label="' + (it?'Progressi dei percorsi':'Course progress') + '">' + entries.map(entry =>
      '<article class="academy-progress-card" data-course="'+entry.id+'">' +
        '<div class="academy-progress-head"><div><span class="academy-progress-overline">'+entry.number+' / '+(it?'PERCORSO':'TRACK')+'</span><h2>MCP '+entry.name+'</h2></div><strong>'+entry.course.percent+'%</strong></div>' +
        '<div class="academy-course-meter" role="progressbar" aria-label="MCP '+entry.name+'" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+entry.course.percent+'"><span style="width:'+entry.course.percent+'%"></span></div>' +
        '<div class="academy-progress-foot"><span>'+entry.course.completed+' / '+entry.course.total+' '+(it?'lezioni completate':'lessons completed')+'</span><span>'+entry.info+': <b>'+entry.extra+'</b></span></div>' +
        (entry.id==='advanced'?'<p class="academy-progress-note">'+(it?'I laboratori facoltativi non influenzano questa percentuale.':'Optional labs do not affect this percentage.')+'</p>':'') +
      '</article>'
    ).join('') + '</section>';
  }
  return {snapshot, cards};
})();