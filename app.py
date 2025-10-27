import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from dateutil.relativedelta import relativedelta

import db
from categories import (
    CATEGORIES,
    get_categories,
    get_subcategories,
    get_income_categories,
    get_income_subcategories,
    get_all_categories,
    get_any_subcategories,
)

st.set_page_config(page_title="Controle Financeiro", page_icon="💰", layout="wide")

# Inicialização do banco
conn = db.get_connection()
db.init_db(conn)

# Estado inicial
if "filters" not in st.session_state:
    st.session_state.filters = {
        "tipo": "Todos",
        "categoria": "Todas",
        "subcategoria": "Todas",
        "data_inicio": date.today().replace(day=1) - relativedelta(months=5),
        "data_fim": date.today(),
        "busca": "",
    }

st.title("💰 Controle Financeiro - Ganhos e Gastos")

with st.sidebar:
    st.header("Adicionar Lançamento")
    tipo = st.radio("Tipo", ["Despesa", "Receita"], horizontal=True)
    # Categorias dependem do tipo selecionado
    if tipo == "Receita":
        categorias = ["Selecionar..."] + get_income_categories()
    else:
        categorias = ["Selecionar..."] + get_categories()
    categoria = st.selectbox("Categoria", categorias, index=0)
    if categoria == "Selecionar...":
        subcategorias = ["Selecionar..."]
    else:
        if tipo == "Receita":
            subcategorias = ["Selecionar..."] + get_income_subcategories(categoria)
        else:
            subcategorias = ["Selecionar..."] + get_subcategories(categoria)
    subcategoria = st.selectbox("Subcategoria", subcategorias, index=0)

    col1, col2 = st.columns(2)
    with col1:
        data_lanc = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
    with col2:
        valor = st.number_input("Valor", min_value=0.0, step=1.0, format="%.2f")

    conta = st.text_input("Conta/Carteira", placeholder="Ex.: Nubank, Itaú, Carteira")
    descricao = st.text_area("Descrição/Observações", placeholder="Opcional")
    tags = st.text_input("Tags", placeholder="Ex.: #trabalho #mercado")

    if st.button("Salvar lançamento", type="primary", use_container_width=True):
        if categoria == "Selecionar..." or subcategoria == "Selecionar...":
            st.warning("Selecione categoria e subcategoria.")
        elif valor <= 0:
            st.warning("Informe um valor maior que zero.")
        else:
            db.add_transaction(
                conn,
                data_lanc,
                tipo,
                categoria,
                subcategoria,
                descricao,
                float(valor) if tipo == "Despesa" else float(valor),
                conta,
                tags,
            )
            st.success("Lançamento salvo!")

    st.divider()
    st.header("Filtros")

    tipos = ["Todos", "Despesa", "Receita"]
    st.session_state.filters["tipo"] = st.selectbox("Tipo", tipos, index=0)

    # No filtro, mostrar categorias combinadas de despesas e receitas
    cat_filtro = ["Todas"] + get_all_categories()
    st.session_state.filters["categoria"] = st.selectbox("Categoria", cat_filtro, index=0)

    if st.session_state.filters["categoria"] == "Todas":
        subcat_filtro = ["Todas"]
    else:
        subcat_filtro = ["Todas"] + get_any_subcategories(st.session_state.filters["categoria"])
    st.session_state.filters["subcategoria"] = st.selectbox("Subcategoria", subcat_filtro, index=0)

    st.session_state.filters["data_inicio"] = st.date_input(
        "Data inicial",
        value=st.session_state.filters["data_inicio"],
        format="DD/MM/YYYY",
    )
    st.session_state.filters["data_fim"] = st.date_input(
        "Data final",
        value=st.session_state.filters["data_fim"],
        format="DD/MM/YYYY",
    )
    st.session_state.filters["busca"] = st.text_input("Buscar por descrição/conta/tags")

# Tabs principais
aba = st.tabs(["Visão geral", "Transações", "Relatórios", "Importar/Exportar"])

def carregar_transacoes():
    f = st.session_state.filters
    df = db.get_transactions(
        conn,
        tipo=None if f["tipo"] == "Todos" else f["tipo"],
        categoria=None if f["categoria"] == "Todas" else f["categoria"],
        subcategoria=None if f["subcategoria"] == "Todas" else f["subcategoria"],
        data_inicio=f["data_inicio"],
        data_fim=f["data_fim"],
        busca=f["busca"],
    )
    return df

with aba[0]:
    st.subheader("Resumo e Indicadores")
    df = carregar_transacoes()
    col1, col2, col3 = st.columns(3)
    total_receitas = df.loc[df.tipo == "Receita", "valor"].sum()
    total_despesas = df.loc[df.tipo == "Despesa", "valor"].sum()
    saldo = total_receitas - total_despesas

    col1.metric("Receitas", f"R$ {total_receitas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Despesas", f"R$ {total_despesas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col3.metric("Saldo", f"R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), delta=None)

    # Fluxo por mês
    fluxo = db.get_monthly_cashflow(conn, st.session_state.filters["data_inicio"], st.session_state.filters["data_fim"])
    if not fluxo.empty:
        c = alt.Chart(fluxo).mark_bar().encode(
            x=alt.X("mes:N", title="Mês"),
            y=alt.Y("valor:Q", title="Saldo"),
            color=alt.condition(alt.datum.valor >= 0, alt.value("#16a34a"), alt.value("#dc2626")),
            tooltip=["mes", "valor"],
        ).properties(height=300)
        st.altair_chart(c, use_container_width=True)

    # Comparativo mês a mês (Receitas, Despesas, Saldo)
    brkd = db.get_monthly_breakdown(conn, st.session_state.filters["data_inicio"], st.session_state.filters["data_fim"])
    if not brkd.empty and len(brkd) >= 2:
        # pegar mês atual do range (último) e anterior
        curr = brkd.iloc[-1]
        prev = brkd.iloc[-2]
        m1, m0 = st.columns(3)
        with m1:
            st.metric(
                label=f"Receitas ({curr['mes']})",
                value=f"R$ {curr['receitas']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                delta=f"{((curr['receitas'] - prev['receitas'])/prev['receitas']*100 if prev['receitas'] else 0):.1f}% vs {prev['mes']}",
                delta_color="normal",
            )
        with m0:
            st.metric(
                label=f"Despesas ({curr['mes']})",
                value=f"R$ {curr['despesas']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                delta=f"{((curr['despesas'] - prev['despesas'])/prev['despesas']*100 if prev['despesas'] else 0):.1f}% vs {prev['mes']}",
                delta_color="inverse",
            )
        with col3:
            st.metric(
                label=f"Saldo ({curr['mes']})",
                value=f"R$ {curr['saldo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                delta=f"{((curr['saldo'] - prev['saldo'])/abs(prev['saldo'])*100 if prev['saldo'] else 0):.1f}% vs {prev['mes']}",
                delta_color="normal",
            )

        # Avisos de especialista financeiro (guidelines simples)
        st.markdown("### Avisos e recomendações")
        receitas_m = float(curr["receitas"]) or 0.0
        despesas_m = float(curr["despesas"]) or 0.0
        saldo_m = float(curr["saldo"]) or 0.0

        # Percentuais recomendados (exemplos comuns)
        targets = {
            "Moradia": 0.30,
            "Alimentação": 0.15,
            "Transporte": 0.15,
            "Lazer": 0.10,
            "Dívidas/Crédito": 0.20,
        }

        # Filtrar apenas mês corrente para distribuição por categoria de despesas
        df_curr = df.copy()
        try:
            # Tentar detectar o ano-mês corrente em formato label e filtrar por data
            # Usamos ym do breakdown para precisão
            ym_curr = brkd.iloc[-1]["ym"]
            ano, mes = ym_curr.split("-")
            df_curr = df[(pd.to_datetime(df["data"]).dt.strftime('%Y-%m') == ym_curr)]
        except Exception:
            pass

        desp_cat = (
            df_curr[df_curr["tipo"] == "Despesa"].groupby("categoria")["valor"].sum().sort_values(ascending=False)
            if not df_curr.empty
            else pd.Series(dtype=float)
        )

        # Regra: poupar pelo menos 20% da renda
        save_target = 0.20
        if receitas_m > 0:
            if saldo_m >= receitas_m * save_target:
                st.success(f"Poupança/meta: OK — economia de {saldo_m/receitas_m*100:.1f}% (alvo: {save_target*100:.0f}%)")
            else:
                st.warning(f"Poupança/meta: Abaixo do recomendado — {saldo_m/receitas_m*100:.1f}% (alvo: {save_target*100:.0f}%)")
        else:
            st.info("Sem receitas no mês para avaliar poupança/meta.")

        # Regras por categoria
        if not desp_cat.empty and receitas_m > 0:
            for cat, pct in targets.items():
                val = float(desp_cat.get(cat, 0.0))
                share = val / receitas_m
                if share <= pct:
                    st.success(f"{cat}: {share*100:.1f}% da renda (alvo <= {pct*100:.0f}%)")
                else:
                    st.warning(f"{cat}: {share*100:.1f}% da renda — acima do recomendado (alvo <= {pct*100:.0f}%)")
        elif receitas_m == 0 and despesas_m > 0:
            st.warning("Há despesas, mas nenhuma receita registrada no mês corrente.")

    # Por categoria
    por_cat = db.get_sum_by_category(conn, st.session_state.filters)
    if not por_cat.empty:
        pie = alt.Chart(por_cat).mark_arc().encode(
            theta="valor:Q",
            color=alt.Color("categoria:N", legend=None),
            tooltip=["categoria", "valor"],
        ).properties(height=300)
        st.altair_chart(pie, use_container_width=True)

with aba[1]:
    st.subheader("Transações")
    df = carregar_transacoes()
    if df.empty:
        st.info("Nenhum lançamento encontrado para os filtros selecionados.")
    else:
        st.dataframe(
            df[["data", "tipo", "categoria", "subcategoria", "descricao", "valor", "conta", "tags"]]
            .sort_values("data", ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )

with aba[2]:
    st.subheader("Relatórios")
    st.caption("Relatórios básicos. Em breve: exportações detalhadas e gráficos adicionais.")
    df = carregar_transacoes()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Gastos por Categoria")
        por_cat = (
            df[df["tipo"] == "Despesa"].groupby(["categoria"], as_index=False)["valor"].sum()
        )
        if not por_cat.empty:
            bar = alt.Chart(por_cat).mark_bar().encode(x="categoria:N", y="valor:Q", tooltip=["categoria", "valor"]).properties(height=300)
            st.altair_chart(bar, use_container_width=True)
        else:
            st.info("Sem dados de despesas para o período.")
    with col2:
        st.markdown("### Receitas por Categoria")
        por_cat_r = (
            df[df["tipo"] == "Receita"].groupby(["categoria"], as_index=False)["valor"].sum()
        )
        if not por_cat_r.empty:
            bar2 = alt.Chart(por_cat_r).mark_bar(color="#16a34a").encode(x="categoria:N", y="valor:Q", tooltip=["categoria", "valor"]).properties(height=300)
            st.altair_chart(bar2, use_container_width=True)
        else:
            st.info("Sem dados de receitas para o período.")

with aba[3]:
    st.subheader("Importar/Exportar")
    st.caption("Funcionalidades básicas de exportação. Importação CSV mínima.")

    df = carregar_transacoes()
    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("Exportar CSV (filtros aplicados)", csv, file_name="transacoes.csv", mime="text/csv")
    else:
        st.info("Sem dados para exportar.")

    st.markdown("#### Importar CSV")
    up = st.file_uploader("Selecione um arquivo CSV com colunas: data,tipo,categoria,subcategoria,descricao,valor,conta,tags", type=["csv"])
    if up is not None:
        try:
            imp = pd.read_csv(up)
            required = {"data", "tipo", "categoria", "subcategoria", "descricao", "valor", "conta", "tags"}
            if not required.issubset(set(imp.columns)):
                st.error("Arquivo CSV inválido. Colunas obrigatórias ausentes.")
            else:
                linhas = 0
                for _, row in imp.iterrows():
                    dt = pd.to_datetime(row["data"]).date()
                    db.add_transaction(
                        conn,
                        dt,
                        str(row["tipo"]),
                        str(row["categoria"]),
                        str(row["subcategoria"]),
                        str(row.get("descricao", "")),
                        float(row["valor"]),
                        str(row.get("conta", "")),
                        str(row.get("tags", "")),
                    )
                    linhas += 1
                st.success(f"Importação concluída: {linhas} linhas.")
        except Exception as e:
            st.error(f"Erro ao importar: {e}")
