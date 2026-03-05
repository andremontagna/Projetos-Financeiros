import streamlit as st
import pandas as pd

from leitura import tratar_dados
from carteira import Carteira
from tributacao import pl_realizado_por_ano
from tributacao import (
    consolidar_resultado_mensal,
    calcular_ir_mensal,
    resultado_por_tipo,
    resultado_por_ativo
)
from mercado import enriquecer_carteira_mercado
from relatorios import gerar_excel_bytes


st.set_page_config(layout="wide")

st.title("📊 Carteira B3 — Dashboard Analítico")

arquivo = st.file_uploader(
    "Upload planilha de operações",
    type=["xlsx"]
)

if arquivo:

    df = pd.read_excel(arquivo)
    df = tratar_dados(df)

    cart = Carteira()
    cart.processar(df)

    vendas = cart.vendas_df()
    carteira = cart.carteira_atual()

    mensal = consolidar_resultado_mensal(vendas)
    ir = calcular_ir_mensal(vendas)
    por_tipo = resultado_por_tipo(vendas)
    por_ativo = resultado_por_ativo(vendas)
    por_ano = pl_realizado_por_ano(vendas)

    carteira_mkt = enriquecer_carteira_mercado(carteira)
    


    # =========================
    # MÉTRICAS GERAIS
    # =========================

    custo_total = carteira_mkt["Custo_Total"].sum()
    valor_mercado = carteira_mkt["Valor_Mercado"].sum()
    pl_aberto = carteira_mkt["PL_Nao_Realizado"].sum()
    pl_realizado = vendas["Resultado"].sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💼 Valor Mercado", f"R$ {valor_mercado:,.2f}")
    col2.metric("💰 Custo", f"R$ {custo_total:,.2f}")
    col3.metric("📈 P/L Aberto", f"R$ {pl_aberto:,.2f}")
    col4.metric("🏁 P/L Realizado", f"R$ {pl_realizado:,.2f}")

    # =========================
    # PL POR ANO
    # =========================

    st.header("📅 P/L Realizado por Ano")

    st.bar_chart(
        por_ano.set_index("Ano")["Resultado_Realizado"]
    )

    st.dataframe(por_ano)


    # =========================
    # CARTEIRA
    # =========================

    st.header("📦 Carteira (valor de compra e posição atual de mercado)")
    st.dataframe(carteira_mkt)

    # composição carteira
    st.subheader("Composição por Valor de Mercado")

    comp = carteira_mkt.set_index("Código")["Valor_Mercado"]
    st.bar_chart(comp)

    # =========================
    # RESULTADO MENSAL — gráfico correto
    # =========================

    st.header("📈 Resultado Mensal")

    mensal_plot = mensal.copy()
    mensal_plot["Mes"] = mensal_plot["Mes"].astype(str)
    mensal_plot = mensal_plot.set_index("Mes")

    st.line_chart(mensal_plot["Resultado"])

    st.dataframe(mensal)

    # =========================
    # RESULTADO POR TIPO
    # =========================

    st.header("📊 Resultado por Tipo de Carteira")

    st.bar_chart(
        por_tipo.set_index("Tipo")["Resultado_Total"]
    )

    st.dataframe(por_tipo)

    # =========================
    # RESULTADO POR ATIVO
    # =========================

    st.header("🏷 Resultado por Ativo")

    st.bar_chart(
        por_ativo.set_index("Código")["Resultado"]
    )

    st.dataframe(por_ativo)

    # =========================
    # IR
    # =========================

    st.header("🧾 IR Mensal")

    st.dataframe(ir)

    # =========================
    # VENDAS
    # =========================

    st.header("🔁 Relatório de Vendas")

    st.dataframe(vendas)

    # =========================
    # DOWNLOAD EXCEL
    # =========================

    excel_bytes = gerar_excel_bytes(
        carteira_mkt,
        vendas,
        mensal,
        ir,
        por_tipo,
        por_ano
)



    st.download_button(
        label="⬇️ Download Relatório Excel",
        data=excel_bytes,
        file_name="relatorio_carteira.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
