import argparse

def generate_trip_file(destination, origin_dest_data, scala= 1):

    with open(origin_dest_data, 'r') as data:
        tntp = data.readlines()

    dataTntp = []
    for line in tntp:
        line = line.strip().replace(" ", "")
        if line and not line.startswith("<"):
            dataTntp.append(line)

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
                        for car in range(flow):
                            f.write(f'    <trip id="{trip_id}" depart="{depart_time}" from="{origin}" to="{dest_id}"/>\n')
                            trip_id = trip_id + 1

        f.write('</routes>\n')


def create_parser():
    parser = argparse.ArgumentParser(
        usage="python generators/sumo_xml_trips_generator.py --inst ./data/sioux_falls/SiouxFalls_trips.tntp --o ./data/sioux_falls/siouxFalls_trips.xml --scl 2",
    )
    parser.add_argument("--inst", type=str, required= True, help="Caminho do arquivo tntp a ser convertido.")
    parser.add_argument("--scl", type=int, default= 1, help="Escala que serão considerados na criação das rotas na matriz OD")
    parser.add_argument("--o", type=str, default="data/trips.xml", help="Arquivo onde será salvo as rotas")
    return parser.parse_args()

def run():
    args = create_parser()
    generate_trip_file(destination=args.o, origin_dest_data=args.inst, scala=args.scl)

if __name__ == "__main__":
    run ()
