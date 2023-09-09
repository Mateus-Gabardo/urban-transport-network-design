import argparse
import sumolib
import xml.etree.ElementTree as ET
import numpy as np

# Algoritmo de busca em profundidade
# Algoritmo de busca em profundidade
# Encontra todas as vias possíveis de se chegar de um ponto a outro.
def find_all_paths(adj_matrix, nodes, origin, destination):
    # Criar um mapeamento de IDs de nós para índices na matriz
    map_nos_indices = {id_no: indice for indice, id_no in enumerate(nodes)}

    def dfs(current_node, path):
        if current_node == destination:
            paths.append(path)
            return
        for neighbor, connected in enumerate(adj_matrix[map_nos_indices[current_node]]):
            if connected == 1 and nodes[neighbor] not in path:
                dfs(nodes[neighbor], path + [nodes[neighbor]])

    paths = []
    dfs(origin, [origin])
    return paths

def convert_matrix(file_net):
    net = sumolib.net.readNet(file_net)
    edges_html = net.getEdges(False)

    edges = []
    nodes = set()
    for edge in edges_html:
        from_node = edge.getFromNode().getID()
        to_node = edge.getToNode().getID()
        edges.append((from_node, to_node))
        nodes.add(from_node)
        nodes.add(to_node)

    nodes = list(nodes)
    num_nodes = len(nodes)
    od_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    for edge in edges:
        from_node = nodes.index(edge[0])
        to_node = nodes.index(edge[1])
        od_matrix[from_node][to_node] += 1
    
    return od_matrix, nodes

# Prepara a matriz OD proveniente do arquivo tntp, retirando todos os espacos
# O resultado sera uma lista de String, cusjas linhas estarao todos os dados sem espaços.
def od_prepare(txt_tntp):
    dataTntp = []
    for line in txt_tntp:
        line = line.strip().replace(" ", "")
        if line and not line.startswith("<"):
            dataTntp.append(line)
    return dataTntp

def convert_router(file_net, file_od, destination, scala=1):
    matriz_adj, nodes = convert_matrix(file_net)

    with open(file_od, 'r') as data:
        tntp = data.readlines()
    dataTntp = od_prepare(tntp)

    with open(destination, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')
        origin = 0
        trip_id = 0
        for line in dataTntp:
            if line.startswith('Origin'):
                origin = line.split("\t")[1]
            else:
                destinies = line.split(";")
                destinies = [dest.rstrip() for dest in destinies if dest.rstrip()]
                depart_time = origin
                for destiny in destinies:
                    flows = destiny.split(":")
                    dest_id = flows[0]
                    flow = float(flows[1]) / scala
                    flow = round(flow)

                    if flow != 0.0:
                        all_paths = find_all_paths(matriz_adj, nodes, origin, dest_id)
                        next_path = 0
                        if len(all_paths) > 0:
                            for _ in range(flow):
                                choice_path = all_paths[next_path]
                                choice_path = ' '.join([f"{choice_path[i]}-{choice_path[i+1]}" for i in range(len(choice_path)-1)])
                                f.write(f'    <vehicle id="{trip_id}" depart="{depart_time}">\n')
                                f.write(f'        <route edges="{choice_path}"/>\n')
                                f.write(f'    </vehicle>\n')
                                trip_id = trip_id + 1
                                next_path = (next_path + 1) % len(all_paths)

        f.write('</routes>\n')

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=str, required= True, help="Caminho do arquivo de rede (network)")
    parser.add_argument("--od", type=str, required= True, help="Caminho do arquivo da matriz OD")
    parser.add_argument("--scl", type=int, default= 1, help="Escala que serão considerados na criação das rotas na matriz OD")
    parser.add_argument("--o", type=str, default="data/sumo.rou.xml", help="Arquivo onde será salvo as rotas")
    return parser.parse_args()

def run():
    args = create_parser()
    convert_router(file_net=args.n, file_od= args.od, destination=args.o, scala=args.scl)

if __name__ == "__main__":
    run ()