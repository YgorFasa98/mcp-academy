"""Build a self-contained, file://-compatible static website from editable sources."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
src = ROOT / 'src'
out = ROOT / 'index.html'
html = (src/'template.html').read_text(encoding='utf-8')
html = html.replace('/* INLINE_CSS */', (src/'style.css').read_text(encoding='utf-8'))
html = html.replace('/* INLINE_DATA */', (src/'data.js').read_text(encoding='utf-8'))
html = html.replace('/* INLINE_APP */', (src/'app.js').read_text(encoding='utf-8'))
out.write_text(html,encoding='utf-8')
(ROOT/'.nojekyll').touch()
print(f'Built {out}: {out.stat().st_size:,} bytes')
