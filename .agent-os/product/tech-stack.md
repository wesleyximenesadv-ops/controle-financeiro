# Technical Stack

- application_framework: Static HTML + Vanilla JavaScript (ES2020+)
- database_system: N/A (arquivos CSV locais: `catalogo_cncst.csv`, `estruturas_ead.csv`)
- javascript_framework: N/A (Vanilla JS)
- import_strategy: importmaps
- css_framework: Utilitário leve custom (CSS próprio)
- ui_component_library: N/A (componentes simples em HTML/CSS)
- fonts_provider: Sistema (Segoe UI, Roboto, Arial)
- icon_library: N/A
- application_hosting: Qualquer host estático (GitHub Pages, Netlify, S3) — ou servidor local simples
- database_hosting: Armazenamento de arquivos (CSV) lado do cliente
- asset_hosting: Mesmo host estático do app
- deployment_solution: Upload de arquivos estáticos (drag-and-drop) ou integração CI/CD com host estático
- code_repository_url: [definir]

Observações:
- Para uso local, é necessário servir via HTTP (ex.: `npx serve -p 8000`), pois `fetch()` não funciona com `file://` por CORS.
- Em produção, recomenda-se hospedagem estática que sirva `text/csv` corretamente.
