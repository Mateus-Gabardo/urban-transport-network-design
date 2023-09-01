import argparse
from grafo_grid_generator import gerar_intancia_grid
from grafo_sioux_falls_generator import gerar_intancia_sioux_falls

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=float, default=1.0, help="Scale parameter")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    gerar_intancia_grid()
    gerar_intancia_sioux_falls()