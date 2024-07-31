import os
import sys
import optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options

""" < Define TraCI control loop > """
def run(sim_time):
    step = 0
    while step < sim_time:
        traci.simulationStep()
        step += 1
        
        # if step % 100 == 0:
        #     print(f"Time = {step}")
    traci.close()
    sys.stdout.flush()

# To obtain sim_time
import xml.etree.ElementTree as ET

def simulationStart(sumocfg_path):
    options = get_options()

    # if options.nogui:
    #     sumoBinary = checkBinary('sumo')
    # else:
    #     sumoBinary = checkBinary('sumo-gui')
    sumoBinary = 'sumo'

    sumoCmd = [sumoBinary, "-c", sumocfg_path, "--start", "--quit-on-end"]
    traci.start(sumoCmd)

    # To obtain sim_time
    sumo_xml = ET.parse(sumocfg_path)
    configuration = sumo_xml.getroot()
    sim_time = int(configuration.find('time/end').get('value'))

    run(sim_time)

if __name__ == '__main__':
    simulationStart("test.sumocfg")