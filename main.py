from leitura import carregar_dados, tratar_dados
from carteira import Carteira
from tributacao import (
    consolidar_resultado_mensal,
    calcular_ir_mensal,
    resultado_por_tipo
)
from relatorios import salvar_relatorio


def main():

    df = carregar_dados()
    df = tratar_dados(df)

    cart = Carteira()
    cart.processar(df)

    vendas = cart.vendas_df()
    carteira = cart.carteira_atual()

    mensal = consolidar_resultado_mensal(vendas)
    ir = calcular_ir_mensal(vendas)
    por_tipo = resultado_por_tipo(vendas)

    salvar_relatorio(carteira, vendas, mensal, ir, por_tipo)


if __name__ == "__main__":
    main()
