/* A single shared toolbar for every MCP4BIM Academy page. */
window.MCPAcademyToolbar = (()=>{
  'use strict';
  const icons={
    search:'<circle cx="11" cy="11" r="7"/><path d="m16 16 5 5"/>',
    glossary:'<path d="M4 19.5A2.5 2.5 0 016.5 17H20V4a1 1 0 00-1-1H6.5A2 2 0 004 5.5z"/><path d="M4 19.5V5.5A2.5 2.5 0 016.5 3"/>',
    progress:'<circle cx="12" cy="8" r="5"/><path d="m8 12-2 9 6-3 6 3-2-9"/>',
    menu:'<path d="M4 6h16M4 12h16M4 18h16"/>'
  };
  const icon=(kind)=>`<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${icons[kind]}</svg>`;
  function render(language='it'){
    const it=language!=='en';
    const search=it?'Cerca':'Search', glossary=it?'Glossario':'Glossary', progress=it?'Progressi':'Progress';
    return `<header class="topbar"><div class="top-inner"><a class="brand" href="./index.html" aria-label="MCP4BIM Academy — Home"><span class="brand-mark">M<span>.</span></span><span class="brand-text">MCP4BIM <strong>Academy</strong><small>LEARNING PLATFORM</small></span></a><div class="top-right"><a class="nav-min" href="./index.html">Home</a><button class="nav-min" type="button" data-academy-nav="search" aria-label="${search}">${icon('search')}<span>${search}</span></button><button class="nav-min" type="button" data-academy-nav="glossary" aria-label="${glossary}">${icon('glossary')}<span>${glossary}</span></button><button class="nav-min" type="button" data-academy-nav="progress" aria-label="${progress}">${icon('progress')}<span>${progress}</span></button><div class="lang-switch" role="group" aria-label="Language"><button type="button" data-academy-nav="language" data-lang="it" class="${it?'on':''}" aria-pressed="${it}">IT</button><button type="button" data-academy-nav="language" data-lang="en" class="${it?'':'on'}" aria-pressed="${!it}">EN</button></div><button class="mobile-menu" type="button" data-academy-nav="menu" aria-label="${it?'Apri il menu':'Open menu'}">${icon('menu')}</button></div></div></header>`;
  }
  return {render};
})();