
import json
import random
import copy
from sumo_simulation import SumoSimulation
from generators.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET
import utils as util
import tkinter as tk
import io
import contextlib
from arg_parser import create_parser

class BaseLineAlgorithm2:
    def __init__(self, dados, nSimulation, budget, vehicles, scala, trips):
        self.graph = dados
        self.simulation_number = nSimulation
        self.buget_number = budget
        self.vehicles = vehicles
        self.bestJson = copy.deepcopy(self.graph)
        self.scala = scala
        self.trips = trips

    def executar_algoritmo(self):
        
        # Criar janela e widget de texto para exibir os prints
        janela = tk.Tk()
        janela.title("Exemplo de Prints em Tempo Real")

        log_text = tk.Text(janela)
        log_text.pack()

        modifications = []
        arestas_criadas = []
        simulacoes = int(self.simulation_number)
        json_inicial = self.graph
        self.bestJson = json_inicial

        # Retorno da simulação da instância inicial
        simulador = SumoSimulation(json_str=self.graph, scala=self.scala, trips=self.trips, vehicles=self.vehicles)
        BestAvgTravelTime = simulador.run_simulation()

        simulation_number = 1
        while simulacoes > 0:
            json_mod = copy.deepcopy(json_inicial)
            vertices = json_mod['vertices']
            coordenadas = json_mod['coordenadas']
            arestas = json_mod['arestas']
            current_modification = []
            budget = float(self.buget_number)
            isBudget = True
            
            while isBudget:
                
                if random.random() < 0.5:
                    json_mod, current_modification, budget, isBudget = util.nova_lane(arestas, modifications, json_mod, current_modification, budget)
                
                else:
                    json_mod, current_modification, arestas_criadas, budget, isBudget = util.nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget)
            
            # Decrementar variável de critério de parada caso essa combinação não tiver sido feita
            #alternative_modification = [current_modification[1], current_modification[0]]
            if current_modification not in modifications: #and alternative_modification not in modifications:
                modifications.append(current_modification)
                simulacoes -= 1
                print(f"Simulação # {simulation_number}")
                print(f"Modificação: {current_modification}")
                
                simulation_number += 1

                # Simular modificação
                simulador = SumoSimulation(json_str=json_mod, scala=self.scala, trips=self.trips, vehicles=self.vehicles)
                AvgTravelTime = simulador.run_simulation()
                print(f"Tempo de simulação: {AvgTravelTime}")
                print("")

                # Verificar se a modificação resultou em uma melhora
                if AvgTravelTime < BestAvgTravelTime:
                    BestAvgTravelTime = AvgTravelTime
                    self.bestJson = json_mod

        # Printar a melhor melhora no final
        print(f"Modificações: {modifications}")
        print("")
        print(f'O melhor tempo de viagem foi: {BestAvgTravelTime}')

           

        return BestAvgTravelTime
    
def run(args):
    with open('data/' + args.ist, 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
    algoritm = BaseLineAlgorithm2(dados=data, budget= args.bd, nSimulation= args.it, vehicles= args.vc, trips=args.tntp, scala=args.scl)
    algoritm.executar_algoritmo()

if __name__ == "__main__":
    parser = create_parser()
    parser.description = 'Algorimo Baseline utilizando busca aleatória'
    parser.usage='python algoritm_baseline.py --ist grid/grid.json --tntp data/grid/grid_trips.tntp --scl 50 --bd 5 --it 3 --st 2'
    args = parser.parse_args()
    run(args)