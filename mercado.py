# mercado.py
import yfinance as yf
import pandas as pd


def preco_atual(ticker):

    try:
        t = yf.Ticker(f"{ticker}.SA")
        hist = t.history(period="1d")

        if hist.empty:
            return None

        return float(hist["Close"].iloc[-1])

    except:
        return None


def precos_carteira(df_carteira):

    precos = {}

    for cod in df_carteira["Código"]:
        p = preco_atual(cod)
        precos[cod] = p

    return precos


def enriquecer_carteira_mercado(df_carteira):

    df = df_carteira.copy()

    precos = precos_carteira(df)

    df["Preco_Mercado"] = df["Código"].map(precos)

    df["Valor_Mercado"] = (
        df["Quantidade"] * df["Preco_Mercado"]
    )

    df["PL_Nao_Realizado"] = (
        df["Valor_Mercado"] - df["Custo_Total"]
    )

    return df
