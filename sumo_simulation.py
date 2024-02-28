import os
import subprocess
import time
import sys
import shutil
from generators.sumo_router import convert_router
from generators.sumo_xml_demand_generator import SumoXmlDemandGenerator
from generators.sumo_xml_generator import SumoFilesGenerator
from generators.sumo_xml_trips_generator import generate_trip_file
import sumolib

# Classe responsável pela realização da simulação.
# json_str - arquivo em json na estrutura do grafo
# trips - Representa a matriz OD que deverá ser passada, e que será convertida no conjunto de rotas. Se não passado será gerado uma rota
# aleatória.
# vehicles - representa a quantidade de veiculos que serão gerados na rota aleatória. Só será considerado caso não seja passado uma rota.
class SumoSimulation:
    def __init__(self, json_str, trips, scala = 1, vehicles = 50):
        sumo_path = shutil.which('sumo')
        self.sumo_dir = os.path.dirname(sumo_path)

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        self.sumoBinary = os.path.join(self.sumo_dir, "sumo")
        self.sumoCmd = [self.sumoBinary, "-c", "sumo_data/config.sumocfg"]
        self.json_str = json_str
        self.trips = trips
        self.scala = scala
        self.vehicles = vehicles
    
    def gerarRotas(self):
        print('Gerando novas rotas')
        if self.trips is None:
            self.__gerarRotasAleatoria()
        else:
            self.__gerarDemandAsOD()

    # Gera a demanda a partir de uma quantidade de veículos passado como parâmetro.
    def __gerarRotasAleatoria(self):
        network_file = "sumo_data/network.net.xml"
        output_file = "sumo_data/routes.rou.xml"
        num_trips = self.vehicles
        trip_depart_period = 1
        random_seed = 42

        demand_generator = SumoXmlDemandGenerator(network_file, output_file)

        # Gera a demanda de maneira aleatória mas com um seed randomico
        demand_generator.generateDemand(num_trips, trip_depart_period, random_seed)
    
    def __gerarDemandAsOD(self):
        outputFile = "sumo_data/routes.rou.xml"
        net_file = "sumo_data/network.net.xml"
        convert_router(file_net=net_file, file_od= self.trips, destination=outputFile, scala=self.scala)

    def __average_speed(self):
        speedSum = 0.0
        edgeCount = 0
        try:
            for edge in sumolib.xml.parse('sumo_data/output.xml', ['edge']):
                speedSum += float(edge.traveltime)
                edgeCount += 1
        except Exception:
            return float("inf")
        
        avgSpeed = speedSum / edgeCount
        #A velocidade média na borda/faixa dentro do intervalo relatado.
        print('Velocidade média da simulação:', avgSpeed)
        return avgSpeed

    def __run_sumo(self):
        output_file = "sumo_data/output.xml"
        command = self.sumoCmd + ["--edgedata-output", output_file]

        try:
            start_time = time.time()
            process = subprocess.Popen(command)
            
            # Wait for the process to finish or timeout after 5 seconds
            while process.poll() is None and time.time() - start_time < 5:
                time.sleep(0.1)
            
            if process.poll() is None:
                process.terminate()  # Cancel the operation if it exceeds 5 seconds
            
        except subprocess.CalledProcessError as e:
            # Handle any error that occurred during the subprocess execution
            print("Error: ", e)

    def run_simulation(self):
        grafoFile = SumoFilesGenerator(self.json_str)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
        self.gerarRotas()
        self.__run_sumo()
        return self.__average_speed()



