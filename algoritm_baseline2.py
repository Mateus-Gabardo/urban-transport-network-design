import copy
import random
import itertools
import json
from arg_parser import create_parser
from sumo_simulation import SumoSimulation

def searchBestNeighbor(network, budget, estrategia, vehicles, trips, scala):
    no1, no2 = getTwoRandomNodes(network)
    arestas_relacionadas = getRelatedEdges(network, no1, no2)
    modificacoes = generateValidCombinations(network, arestas_relacionadas, budget)

    min_tmax = float("inf")
    best_network = network
    primeira_melhoria = True

    for conjunto_arestas in modificacoes:
        new_network = applyChanges(network, conjunto_arestas)

        simulador = SumoSimulation(new_network, scala=scala, trips=trips, vehicles=vehicles)
        avgTravelTime = simulador.run_simulation()

        if min_tmax > avgTravelTime:
            best_network = new_network
            min_tmax = avgTravelTime
            if not primeira_melhoria and estrategia == 2:
                return best_network, min_tmax

            primeira_melhoria = False

    return best_network, min_tmax

def getTwoRandomNodes(network):
    nodes = list(network['vertices'])
    return random.sample(nodes, 2)

def getRelatedEdges(network, no1, no2):
    arestas_relacionadas = []

    for aresta, dados in network["arestas"].items():
        extremos = aresta.split("-")
        if no1 in extremos or no2 in extremos:
            arestas_relacionadas.append(aresta)

    return arestas_relacionadas

def generateValidCombinations(network, arestas_relacionadas, budget):
    modificacoes = []

    for r in range(1, len(arestas_relacionadas) + 1):
        combinacoes = list(itertools.combinations(arestas_relacionadas, r))
        

        for combinacao in combinacoes:
            comprimento_total = sum(network['arestas'][aresta]['length'] for aresta in combinacao)
            if comprimento_total <= budget:
                modificacoes.append(combinacao)

    return modificacoes

def applyChanges(network, conjunto_arestas):
    new_network = copy.deepcopy(network)

    for id_aresta in conjunto_arestas:
        json_aresta = new_network['arestas'][id_aresta]
        json_aresta["numLanes"] += 1
        new_network['arestas'][id_aresta] = json_aresta

    return new_network

def initialSolution(network, budget, vehicles, trips, scala):
    new_network = network
    tentativas = len(network['arestas'])
    best_modificacoes = []

    while not best_modificacoes and tentativas > 0:
        arestas = list(network['arestas'].keys())
        aresta1, aresta2 = random.sample(arestas, 2)
        arestas_candidatas = [(aresta1), (aresta2)]

        modificacoes = generateValidCombinations(network, arestas_candidatas, budget)

        if modificacoes:
            best_modificacoes = max(modificacoes, key=len)

        tentativas -= 1
        if tentativas == 0:
            break

    if best_modificacoes:
        new_network = applyChanges(network, best_modificacoes)
        simulador = SumoSimulation(json_str=network, scala=scala, trips=trips, vehicles=vehicles)
        avgTravelTime = simulador.run_simulation()
    else:
        avgTravelTime = None

    return new_network, avgTravelTime

def localSearch(grafo, budget, trips, scala, interacoes=50, estrategia=2, vehicles = 50 ):
    best_network, best_temp = initialSolution(grafo, budget, vehicles, trips, scala)

    qtd_iteracoes = interacoes

    while int(qtd_iteracoes) > 0:
        network_curent, temp_curent = searchBestNeighbor(grafo, budget, estrategia, vehicles, trips, scala)
        if temp_curent < best_temp:
            best_temp = temp_curent
            best_network = network_curent
        qtd_iteracoes = qtd_iteracoes - 1

    return best_network, best_temp

def run(args):
    with open('data/' + args.ist, 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)

    localSearch(grafo= data, budget= args.bd, estrategia= args.st, interacoes=args.it, vehicles= args.vc, trips=args.tntp, scala=args.scl)

if __name__ == "__main__":
    parser = create_parser()
    parser.description = 'Algorimo baseline melhorado'
    parser.usage='python algoritm_baseline2.py --ist grid/grid.json --tntp data/grid/grid_trips.tntp --scl 50 --bd 20 --it 3 --st 2'
    args = parser.parse_args()
    run(args)

