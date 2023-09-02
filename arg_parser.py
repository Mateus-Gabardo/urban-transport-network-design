import argparse

def create_parser():
    parser = argparse.ArgumentParser(
        usage="python algoritmo.py --ist CAMINHO_DA_INSTÂNCIA [opções]",
    )
    parser.add_argument("--ist", type=str, required=True, help="Caminho da instância que será rodada. Esta contida a partir de data/. Exemplo: --ist sioux_falls/siouxFalls.json")
    parser.add_argument("--bd", type=float, default=50, help="Quantidade de budget")
    parser.add_argument("--it", type=int, default=10, help="Número de iterações")
    parser.add_argument("--st", type=int, default=2, help="Estratégia de melhoria. 1 - Melhor melhoria, 2 - Primeira melhoria")
    parser.add_argument("--vc", type=int, default=50, help="Número de Veículos")
    return parser