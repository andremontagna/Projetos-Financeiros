# carteira.py
from collections import deque
import pandas as pd


class Carteira:

    def __init__(self):
        self.lotes = {}              # codigo → fila de lotes
        self.registros_venda = []    # vendas realizadas

    def _fila(self, codigo):
        if codigo not in self.lotes:
            self.lotes[codigo] = deque()
        return self.lotes[codigo]

    # -------------------------
    # COMPRA
    # -------------------------

    def comprar(self, codigo, qtd, preco, data):

        self._fila(codigo).append({
            "qtd": qtd,
            "preco": preco,
            "data": data
        })

    # -------------------------
    # VENDA (FIFO)
    # -------------------------

    def vender(self, codigo, qtd, preco, data, tipo):

        fila = self._fila(codigo)

        posicao = sum(l["qtd"] for l in fila)

        if posicao < qtd:
            raise ValueError(
                f"Venda maior que posição disponível: {codigo} "
                f"(pos={posicao}, venda={qtd})"
            )

        restante = qtd
        custo = 0

        while restante > 0:

            lote = fila[0]

            if lote["qtd"] <= restante:
                custo += lote["qtd"] * lote["preco"]
                restante -= lote["qtd"]
                fila.popleft()

            else:
                custo += restante * lote["preco"]
                lote["qtd"] -= restante
                restante = 0

        valor_venda = qtd * preco
        resultado = valor_venda - custo

        self.registros_venda.append({
            "Código": codigo,
            "Data": data,
            "Quantidade": qtd,
            "Preço_Venda": preco,
            "Valor_Venda": valor_venda,
            "Custo_FIFO": custo,
            "Resultado": resultado,
            "Tipo": tipo
        })

    # -------------------------
    # PROCESSAMENTO DO DF
    # -------------------------

    def processar(self, df):

        for _, r in df.iterrows():

            if r["C/V"] == "C":

                self.comprar(
                    r["Código"],
                    r["Quantidade"],
                    r["Preço"],
                    r["Data"]
                )

            elif r["C/V"] == "V":

                tipo = r["Tipo"] if "Tipo" in r else "s"

                self.vender(
                    r["Código"],
                    r["Quantidade"],
                    r["Preço"],
                    r["Data"],
                    tipo
                )

            else:
                raise ValueError(f"Valor inválido em C/V: {r['C/V']}")

    # -------------------------
    # CARTEIRA ATUAL
    # -------------------------

    def carteira_atual(self):

        dados = []

        for codigo, fila in self.lotes.items():

            qtd_total = sum(l["qtd"] for l in fila)

            if qtd_total == 0:
                continue

            custo_total = sum(l["qtd"] * l["preco"] for l in fila)
            pm = custo_total / qtd_total

            dados.append({
                "Código": codigo,
                "Quantidade": qtd_total,
                "Custo_Total": custo_total,
                "Preço_Médio_FIFO": pm
            })

        if not dados:
            return pd.DataFrame()

        return pd.DataFrame(dados).sort_values("Código")

    # -------------------------
    # DATAFRAME VENDAS
    # -------------------------

    def vendas_df(self):

        if not self.registros_venda:
            return pd.DataFrame()

        return pd.DataFrame(self.registros_venda)
