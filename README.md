# 💰 Controle Financeiro (Streamlit + SQLite)

Aplicativo simples e eficiente para controlar o que você ganha (receitas) e o que você gasta (despesas), com categorias amplas, filtros, relatórios e exportação CSV.

## Funcionalidades

- Adicionar lançamentos de Receita e Despesa
- Categorias e subcategorias abrangentes (arquivo `categories.py`)
- Filtros por tipo, categoria, subcategoria, período e busca por texto
- Visão geral com indicadores e gráficos (fluxo mensal e por categoria)
- Listagem de transações com ordenação por data
- Exportação CSV com filtros aplicados
- Importação CSV básica
- Banco de dados local SQLite (`finance.db`)

## Requisitos

- Python 3.10+
- Pip

## Instalação (Windows PowerShell)

Recomendado usar ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Execução

```powershell
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`.

## Estrutura

- `app.py`: aplicação Streamlit e UI
- `db.py`: funções de banco (SQLite)
- `categories.py`: categorias e subcategorias
- `requirements.txt`: dependências
- `finance.db`: banco de dados criado automaticamente

## Importação CSV

- Colunas esperadas: `data,tipo,categoria,subcategoria,descricao,valor,conta,tags`
- O formato de `data` pode ser reconhecido automaticamente (ex: `2025-01-31`), caso contrário, ajuste antes de importar.

## Próximos Passos (Roadmap)

- Edição e exclusão de lançamentos na própria tabela
- Contas múltiplas e transferência entre contas
- Planejamento orçamentário (metas por categoria)
- Relatórios adicionais (tendências, comparação mês a mês)
- Backup/restauração do banco

## Observações

- O banco `finance.db` é criado na mesma pasta do projeto.
- Para começar do zero, basta excluir `finance.db` (isso apagará os dados).
