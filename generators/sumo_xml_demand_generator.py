import argparse
import subprocess
import shutil
import os

class SumoXmlDemandGenerator:
    def __init__(self, net_file, rou_file):
        self.net_file = net_file
        self.rou_file = rou_file
        sumo_path = shutil.which('sumo')
        self.sumo_dir = os.path.dirname(sumo_path)
        self.duarouter_path = os.path.join(self.sumo_dir, "duarouter")
    
    def generateDemand(self, num_vehicles, probability, seed):
        command = ["python", "generators/randomTrips.py", "-n", self.net_file, "-r", self.rou_file, "-e", str(num_vehicles), "-p", str(probability), "-s", str(seed), "-o" "sumo_data/trips.trips.xml"]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        error_output = result.stderr
        if(error_output):
            print("Erro:", error_output)

    def generateDemandByTaz(self, taz_file):
        command = [self.duarouter_path, "-n", self.net_file, "-r", taz_file, "-o", self.rou_file]
        subprocess.call(command)
    
    def generateDemandByTrips(self, trips_file):
        command = [self.duarouter_path, "-n", self.net_file, "-t", trips_file, "-o", self.rou_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        error_output = result.stderr
        if(error_output):
            print("Erro:", error_output)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            usage="python generators/sumo_xml_demand_generator.py -n ./sumo_data/network.net.xml -t ./data/sioux_falls/SiouxFalls_trips.xml",
        )
    parser.add_argument("-n", type=str, required= True, help="Caminho de rotas")
    parser.add_argument("-t", type=str, required= True, help="Caminho do arquivo de trips a ser convertido.")
    parser.add_argument("-o", type=str, default="rou.xml", help="Arquivo onde será salvo as rotas")
    args = parser.parse_args()
    generator = SumoXmlDemandGenerator(net_file=args.n, rou_file=args.o)
    generator.generateDemandByTrips(trips_file=args.t)