# tributacao.py
import pandas as pd


def consolidar_resultado_mensal(vendas):

    df = vendas.copy()
    df["Mes"] = df["Data"].dt.to_period("M")

    return (
        df.groupby("Mes")
        .agg(
            Total_Vendido=("Valor_Venda", "sum"),
            Resultado=("Resultado", "sum")
        )
        .reset_index()
        .sort_values("Mes")
    )

def resultado_por_tipo(vendas):

    df = vendas.copy()

    df["Tipo"] = df["Tipo"].astype(str).str.lower().str.strip()

    resumo = (
        df.groupby("Tipo")
        .agg(
            Qtde_Vendas=("Resultado", "count"),
            Total_Vendido=("Valor_Venda", "sum"),
            Custo_Total=("Custo_FIFO", "sum"),
            Resultado_Total=("Resultado", "sum"),
            Resultado_Medio=("Resultado", "mean")
        )
        .reset_index()
        .sort_values("Resultado_Total", ascending=False)
    )

    return resumo


def resultado_por_ativo(vendas):

    df = vendas.copy()

    resumo = (
        df.groupby("Código")
        .agg(
            Qtde=("Resultado", "count"),
            Total_Vendido=("Valor_Venda", "sum"),
            Custo=("Custo_FIFO", "sum"),
            Resultado=("Resultado", "sum")
        )
        .reset_index()
        .sort_values("Resultado", ascending=False)
    )

    return resumo


def pl_realizado_por_ano(vendas):

    df = vendas.copy()

    df["Ano"] = df["Data"].dt.year

    resumo = (
        df.groupby("Ano")
        .agg(
            Qtde_Vendas=("Resultado", "count"),
            Resultado_Realizado=("Resultado", "sum"),
            Total_Vendido=("Valor_Venda", "sum")
        )
        .reset_index()
        .sort_values("Ano")
    )

    return resumo



def calcular_ir_mensal(vendas):

    df = vendas.copy()

    df["Tipo"] = df["Tipo"].astype(str).str.lower().str.strip()

    df["Classe"] = df["Tipo"].apply(
        lambda x: "DAY_TRADE" if x == "dt" else "SWING"
    )

    df["Mes"] = df["Data"].dt.to_period("M")

    resumo = (
        df.groupby(["Mes", "Classe"])
        .agg(
            Total_Vendido=("Valor_Venda", "sum"),
            Resultado=("Resultado", "sum")
        )
        .reset_index()
        .sort_values("Mes")
    )

    prejuizo = {"SWING": 0, "DAY_TRADE": 0}
    linhas = []

    for _, r in resumo.iterrows():

        classe = r["Classe"]
        total = r["Total_Vendido"]
        resultado = r["Resultado"]

        base = resultado + prejuizo[classe]

        if classe == "SWING":
            ir = base * 0.15 if base > 0 and total > 20000 else 0
        else:
            ir = base * 0.20 if base > 0 else 0

        prejuizo[classe] = 0 if base > 0 else base

        linhas.append({
            "Mes": r["Mes"],
            "Classe": classe,
            "Total_Vendido": total,
            "Resultado": resultado,
            "Base_Calculo": base,
            "IR_Devido": ir,
            "Prejuizo_Acumulado": prejuizo[classe]
        })

    return pd.DataFrame(linhas)

