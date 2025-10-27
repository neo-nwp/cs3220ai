from src.pacman_environment import PacmanEnvironment
from src.environmentClass import Environment
from src.pacman_agentSMART import PacmanProblemSolvingAgentSMART
import copy

def main():

    #  Generate ONE random environment
    base_env = PacmanEnvironment(seed=None)

    print("\n==== Running A* MULTI-GOAL ====\n")
    envA = copy.deepcopy(base_env)   #  A* gets its own independent copy
    agentA = PacmanProblemSolvingAgentSMART(envA.start, envA, envA.goal, use_ida=False)
    worldA = Environment(envA, use_ida=False)
    worldA.add_thing(agentA)
    worldA.run()

    print("\n==== Running IDA* MULTI-GOAL ====\n")
    envB = copy.deepcopy(base_env)   #  IDA* gets the SAME map, untouched
    agentB = PacmanProblemSolvingAgentSMART(envB.start, envB, envB.goal, use_ida=True)
    worldB = Environment(envB, use_ida=True)
    worldB.add_thing(agentB)
    worldB.run()

if __name__ == "__main__":
    main()
