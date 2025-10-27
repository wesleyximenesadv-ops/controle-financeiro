# Product Roadmap

## Phase 1: MVP Dinâmico

**Goal:** Tornar possível gerar matrizes completas a partir de CSVs, com exportação fiel à UI.
**Success Criteria:** Usuário gera ao menos 1 matriz por curso com Extensão/TCC/Estágio e exporta CSV/DOC idênticos à UI.

### Features
- [x] Modelo genérico lê Catálogo/EAD e monta matriz `matrizes/matriz_modelo_generico.html` `M`
- [x] Similaridade com badges e metadados nas exportações `M`
- [x] Extensão 10% 1x por semestre (Trimestral B) `S`
- [x] TCC/Estágio via parâmetros e posicionamento no último semestre B `S`
- [x] Regra fim → início para ajuste de carga (preservando Extensão/TCC/Estágio) `M`
- [x] Exportações CSV/DOC fiéis ao que é exibido `S`

### Dependencies
- `catalogo_cncst.csv`, `estruturas_ead.csv` disponíveis e servidos via HTTP.

## Phase 2: Usabilidade e Operação

**Goal:** Facilitar uso por não técnicos e operação em lote.
**Success Criteria:** Usuário não técnico gera links por UI e operação gera lote para 100% dos cursos.

### Features
- [x] Gerador de Links `matrizes/gerador_de_links.html` `S`
- [x] Script em lote `produto/gerar_links_matrizes.py` `S`
- [ ] Fallback de upload de CSVs na UI (sem servidor) `S`
- [ ] Parametrização de percentuais e limiares na UI `M`

### Dependencies
- Navegador moderno e/ou Python 3.8+.

## Phase 3: Escala e Empacotamento

**Goal:** Padronizar implantação e melhorar robustez.
**Success Criteria:** Repositório com docs de produto, empacote pronto e validações de CSV/encoding.

### Features
- [x] Documentação de produto (`.agent-os/product/*`) `S`
- [ ] README unificado com instruções de hospedagem estática e troubleshooting `S`
- [ ] Validação de encoding/headers dos CSVs com mensagens amigáveis `M`
- [ ] Configuração opcional via `config.json` por curso `M`

### Dependencies
- Host estático (Netlify/GitHub Pages/S3) ou servidor local.
