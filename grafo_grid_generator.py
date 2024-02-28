import json
from generators.grafo_generator import GrafoJsonWriter
from generators.sumo_xml_generator import SumoFilesGenerator
from generators.sumo_xml_trips_generator import generate_trip_file

def __gerar_instancia_grid():
    grafo = GrafoJsonWriter()

    atributos = {
        1: {"length": 0.2, "maxSpeed": 80, "numLanes": 1, "priority": 100},
        2: {"length": 0.3, "maxSpeed": 60, "numLanes": 1, "priority": 80}
    }

    arestas = [
        ("1", "2", atributos[1]),
        ("1", "5", atributos[1]),
        ("2", "1", atributos[1]),
        ("2", "6", atributos[1]),
        ("2", "3", atributos[1]),
        ("3", "2", atributos[1]),
        ("3", "7", atributos[1]),
        ("3", "4", atributos[1]),
        ("4", "3", atributos[1]),
        ("4", "8", atributos[1]),
        ("5", "1", atributos[1]),
        ("5", "6", atributos[1]),
        ("5", "9", atributos[2]),
        ("6", "5", atributos[1]),
        ("6", "2", atributos[1]),
        ("6", "10", atributos[2]),
        ("6", "7", atributos[1]),
        ("7", "6", atributos[1]),
        ("7", "3", atributos[1]),
        ("7", "11", atributos[2]),
        ("7", "8", atributos[1]),
        ("8", "7", atributos[1]),
        ("8", "4", atributos[1]),
        ("8", "12", atributos[2]),
        ("9", "5", atributos[2]),
        ("9", "13", atributos[2]),
        ("9", "10", atributos[1]),
        ("10", "9", atributos[1]),
        ("10", "6", atributos[2]),
        ("10", "14", atributos[2]),
        ("10", "11", atributos[1]),
        ("11", "10", atributos[1]),
        ("11", "7", atributos[2]),
        ("11", "15", atributos[2]),
        ("11", "12", atributos[1]),
        ("12", "11", atributos[1]),
        ("12", "8", atributos[2]),
        ("12", "16", atributos[2]),
        ("13", "9", atributos[2]),
        ("13", "14", atributos[1]),
        ("14", "10", atributos[2]),
        ("14", "15", atributos[1]),
        ("15", "11", atributos[2]),
        ("15", "16", atributos[1]),
        ("16", "15", atributos[1]),
        ("16", "12", atributos[2])
    ]

    for origem, destino, atributo in arestas:
        grafo.adicionar_aresta(origem, destino, atributo)


    # Definindo as coordenadas dos vértices
    grafo.adicionar_coordenadas("1", "-150.00", "150.00")
    grafo.adicionar_coordenadas("2", "-50.00", "150.00")
    grafo.adicionar_coordenadas("3", "50.00", "150.00")
    grafo.adicionar_coordenadas("4", "150.00", "150.00")

    grafo.adicionar_coordenadas("5", "-150.00", "50.00")
    grafo.adicionar_coordenadas("6", "-50.00", "50.00")
    grafo.adicionar_coordenadas("7", "50.00", "50.00")
    grafo.adicionar_coordenadas("8", "150.00", "50.00")

    grafo.adicionar_coordenadas("9", "-150.00", "-50.00")
    grafo.adicionar_coordenadas("10", "-50.00", "-50.00")
    grafo.adicionar_coordenadas("11", "50.00", "-50.00")
    grafo.adicionar_coordenadas("12", "150.00", "-50.00")

    grafo.adicionar_coordenadas("13", "-150.00", "-150.00")
    grafo.adicionar_coordenadas("14", "-50.00", "-150.00")
    grafo.adicionar_coordenadas("15", "50.00", "-150.00")
    grafo.adicionar_coordenadas("16", "150.00", "-150.00")

    grafo.salvar_arquivo_json("grid.json", "data/grid")

def __gerarIntanciaSumo():
    with open('data/grid/grid.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
        
    grafoFile = SumoFilesGenerator(data)
    grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
    
def __gerarInstanciaTrips():
    generate_trip_file(origin_dest_data="data/grid/grid_trips.tntp", destination="data/grid/grid_trips.xml", scala=50)
    
def gerar_intancia_grid():
    __gerar_instancia_grid()
    __gerarIntanciaSumo()
    #__gerarInstanciaTrips()

if __name__ == "__main__":
    gerar_intancia_grid()