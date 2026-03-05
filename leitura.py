# leitura.py
import pandas as pd
from tkinter import Tk, filedialog


COLUNAS_OBRIGATORIAS = [
    "Data", "Código", "C/V", "Quantidade", "Preço"
]

# ✅ mapa nome → código
MAPA_ATIVOS = {
    "ABC BRASIL": "ABCB4",
    "ALUPAR": "ALUP11",
    "BRASIL": "BBAS3",
    "BRADESCO": "BBDC4",
    "BBSEGURIDADE": "BBSE3",
    "BRADESPAR": "BRAP4",
    "CURY S/A": "CURY3",
    "CAIXA SEGURI": "CXSE3",
    "CYRELA REALT": "CYRE3",
    "DIRECIONAL": "DIRR3",
    "ECORODOVIAS": "ECOR3",
    "IGUATEMI S.A": "IGTI11",
    "ISA ENERGIA": "ISAE4",
    "ITAUSA": "ITSA4",
    "ITAUUNIBANCO": "ITUB4",
    "JHSF PART": "JHSF3",
    "MARFRIG": "MRFG3",
    "PETROBRAS": "PETR4",
    "MARCOPOLO": "POMO4",
    "PORTO SEGURO": "PSSA3",
    "PETRORECSA": "RECV3",
    "SANEPAR": "SAPR11",
    "TIM": "TIMS3",
    "VALE": "VALE3",
    "TELEF BRASIL": "VIVT3",
}


def selecionar_arquivo():
    Tk().withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha de operações",
        filetypes=[("Excel", "*.xlsx *.xls")]
    )
    if not caminho:
        raise ValueError("Nenhum arquivo selecionado.")
    return caminho


def carregar_dados():
    caminho = selecionar_arquivo()
    return pd.read_excel(caminho)


def validar_colunas(df):
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas obrigatórias ausentes: {faltando}")


def normalizar_codigo(valor):

    if pd.isna(valor):
        return valor

    v = str(valor).strip().upper()

    # se já parece ticker → mantém
    if any(c.isdigit() for c in v):
        return v

    # tenta mapear nome → código
    if v in MAPA_ATIVOS:
        print(f"🔄 Convertido nome → ticker: {v} → {MAPA_ATIVOS[v]}")
        return MAPA_ATIVOS[v]

    print(f"⚠ Nome não mapeado mantido: {v}")
    return v


def tratar_dados(df):

    df = df.copy()

    mapa = {
        "Ticket": "Código",
        "Ticker": "Código",
        "Posição": "Quantidade"
    }

    df = df.rename(columns=mapa)

    validar_colunas(df)

    # ✅ conversão nome → código
    df["Código"] = df["Código"].apply(normalizar_codigo)

    df["C/V"] = df["C/V"].astype(str).str.strip().str.upper()

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce")

    if df["Data"].isna().any():
        raise ValueError("Existem datas inválidas.")

    df["Quantidade"] = df["Quantidade"].astype(int)
    df["Preço"] = df["Preço"].astype(float)

    df["Valor Total"] = df["Quantidade"] * df["Preço"]

    if "Tipo" not in df.columns:
        df["Tipo"] = "s"

    df["Tipo"] = df["Tipo"].astype(str).str.lower().str.strip()

    df = df.sort_values(["Data", "Código"]).reset_index(drop=True)

    return df
