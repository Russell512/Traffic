import os
import sys
import optparse
import traci
# from sumolib import checkBinary

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


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
    traci.close()
    sys.stdout.flush()

def simulationStart(sumocfg_path, sim_time):
    # options = get_options()

    sumoBinary = 'sumo'
    # if options.nogui:
    #     sumoBinary = checkBinary('sumo')
    # else:
    #     sumoBinary = checkBinary('sumo-gui')

    sumoCmd = [sumoBinary, "-c", sumocfg_path, "--start", "--quit-on-end"]
    traci.start(sumoCmd)
    
    run(sim_time)