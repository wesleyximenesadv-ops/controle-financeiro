# Product Mission

## Pitch

Curriculum Matrix Dynamic Integration é um gerador dinâmico de matrizes curriculares que ajuda instituições de ensino a montar, ajustar e exportar matrizes completas a partir do Catálogo CNCST e de estruturas EAD, com correspondências exatas/similares, regras automáticas de carga horária e exportações consistentes.

## Users

### Primary Customers
- Faculdades e Centros Universitários: equipes de NDE/coordenação que definem e atualizam matrizes curriculares.
- Polos EAD e Operação Acadêmica: times responsáveis por padronizar e replicar matrizes.

### User Personas
**Coordenador de Curso** (28-55 anos)
- **Role:** Coordenação/NDE
- **Context:** Pressionado por prazos de regulação e implantação de cursos.
- **Pain Points:** trabalho manual repetitivo, inconsistências entre UI e exportações, dificuldade de aproveitar catálogos e bases existentes.
- **Goals:** reduzir tempo de montagem, manter consistência, garantir aderência ao Catálogo/CBO.

**Analista Acadêmico** (22-40 anos)
- **Role:** Operação/Backoffice
- **Context:** Necessidade de gerar muitas matrizes em lote, com variações de TCC/Estágio.
- **Pain Points:** planilhas manuais, erro humano, refação.
- **Goals:** automação, rastreabilidade, exportações fiéis à interface.

## The Problem

### Montagem manual e inconsistente de matrizes
A montagem de matrizes consome tempo e gera inconsistências entre interface, CSV e documentos. Impacto: atrasos, retrabalho e erros em submissões regulatórias.

**Our Solution:** motor dinâmico com regras e exportações fiéis ao que é exibido em tela.

### Baixo reaproveitamento de bases existentes
As instituições possuem Catálogo CNCST e estruturas EAD, mas não os conectam automaticamente às matrizes. Impacto: perda de eficiência e qualidade.

**Our Solution:** integração direta aos CSVs do Catálogo e EAD, com matching exato/similaridade.

### Ajustes trabalhosos de carga horária
Incluir TCC/Estágio e extensão sem quebrar a carga exige ajustes manuais. Impacto: tempo elevado e risco de erro.

**Our Solution:** regras automáticas (fim → início), preservando Extensão/TCC/Estágio e respeitando percentuais.

## Differentiators

### Exportações que refletem exatamente a UI
Diferente de planilhas manuais, as exportações CSV/DOC reproduzem fielmente o que é renderizado, reduzindo discrepâncias e auditorias.

### Matching híbrido e metadados visíveis
Além de correspondência exata, aplicamos similaridade (Jaccard + Levenshtein + boost), com badges e metadados por disciplina (código, origem, oferta).

### Parametrização por URL e operação em lote
É possível ajustar curso/TCC/Estágio via query na UI e gerar lotes via script Python, acelerando a implantação.

## Key Features

### Core Features
- **Leitura automática do Catálogo:** Perfil, Infra, CBOs, carga mínima e semestres, direto de `catalogo_cncst.csv`.
- **Sugestão de disciplinas:** Matching exato/similaridade com `estruturas_ead.csv`, com badges e metadados.
- **Distribuição por semestres/trimestres:** Extensão 10% (1 por semestre em B), TCC/Estágio no último semestre B.
- **Regra fim → início:** Ajuste automático ao exceder carga, preservando Extensão e TCC/Estágio.
- **Exportações fidedignas:** CSV e DOC idênticos ao conteúdo da UI.

### Collaboration Features
- **Gerador de Links:** UI simples para compor URLs por curso/TCC/Estágio e exportar lista CSV.
- **Script em lote:** `produto/gerar_links_matrizes.py` para gerar links para todos os cursos do catálogo.
- **Modelo reutilizável:** `matrizes/matriz_modelo_generico.html` e variantes específicas (ex.: Negócios Imobiliários).
