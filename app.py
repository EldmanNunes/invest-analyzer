# -*- coding: utf-8 -*-

import streamlit as st

st.set_page_config(
    page_title="INVEST ANALYZER",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("INVEST ANALYZER")

st.subheader("Analise e comparacao inteligente de investimentos")

st.markdown("---")

st.markdown("""
### Bem-vindo ao INVEST ANALYZER!

Uma plataforma para simular, analisar e comparar investimentos
do mercado financeiro brasileiro.

O objetivo e apresentar resultados considerando rentabilidade,
tributacao, custos e indicadores economicos.
""")

st.markdown("### Modulos planejados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Tesouro Direto")
    st.write("Simulacao e comparacao de titulos publicos.")

    st.markdown("#### Renda Fixa")
    st.write("Analise de CDB, LCI, LCA e outros produtos.")

with col2:
    st.markdown("#### Indicadores economicos")
    st.write("Acompanhamento de Selic, CDI, IPCA e outros indicadores.")

    st.markdown("#### Comparador")
    st.write("Comparacao de rentabilidade liquida e tributacao.")

st.markdown("---")

st.caption("INVEST ANALYZER | Versao 0.1.0 | Em desenvolvimento")