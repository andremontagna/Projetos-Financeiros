# relatorios.py
import pandas as pd
from tkinter import Tk, filedialog
from io import BytesIO

def gerar_excel_bytes(carteira, vendas, mensal, ir, por_tipo, por_ano):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:

        carteira.to_excel(writer, sheet_name="Carteira", index=False)
        vendas.to_excel(writer, sheet_name="Vendas_FIFO", index=False)
        mensal.to_excel(writer, sheet_name="Resultado_Mensal", index=False)
        ir.to_excel(writer, sheet_name="IR_Mensal", index=False)
        por_tipo.to_excel(writer, sheet_name="Resultado_por_Tipo", index=False)
        por_ano.to_excel(writer, sheet_name="PL_por_Ano", index=False)


    return output.getvalue()

def salvar_relatorio(carteira, vendas, mensal, ir, por_tipo):

    Tk().withdraw()

    caminho = filedialog.asksaveasfilename(
        title="Salvar relatório",
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")]
    )

    if not caminho:
        print("Relatório cancelado.")
        return

    with pd.ExcelWriter(caminho, engine="xlsxwriter") as writer:

        carteira.to_excel(writer, sheet_name="Carteira", index=False)
        vendas.to_excel(writer, sheet_name="Vendas_FIFO", index=False)
        mensal.to_excel(writer, sheet_name="Resultado_Mensal", index=False)
        ir.to_excel(writer, sheet_name="IR_Mensal", index=False)
        por_tipo.to_excel(writer, sheet_name="Resultado_por_Tipo", index=False)

    print("Relatório salvo com sucesso.")
