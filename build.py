"""Rebuild standalone Essentials after editing /src (Python standard library)."""
from pathlib import Path
root=Path(__file__).resolve().parent
html=(root/'src/template.html').read_text(encoding='utf-8')
for token,file in [('INLINE_CSS','style.css'),('INLINE_PROGRESS_CSS','shared-progress.css'),('INLINE_DATA','data.js'),('INLINE_PROGRESS_JS','shared-progress.js'),('INLINE_HEADER_JS','academy-header.js'),('INLINE_APP','app.js'),('INLINE_GLOBAL_CSS','academy-global.css'),('INLINE_SHARED_HEADER_CSS','shared-header.css'),('INLINE_ADVANCED_DATA','../assets/advanced-data.js'),('INLINE_GLOBAL_JS','academy-global.js')]:
    html=html.replace('/* '+token+' */',(root/'src'/file).read_text(encoding='utf-8'))
(root/'index.html').write_text(html,encoding='utf-8')
print('Rebuilt index.html')