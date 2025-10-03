from src.agentPrograms import *
from src.agentClass import Agent

from src.rules import vacuumRules
from src.rules import actionList
from src.rules import table




'''Randomly choose one of the actions from the vacuum environment'''
def RandomVacuumAgent():
    return Agent(RandomAgentProgram(actionList))


def TableDrivenVacuumAgent():
     return Agent(TableDrivenAgentProgram(table))
 
 
def ReflexAgent() :
  return Agent(ReflexAgentProgram(vacuumRules,interpret_input,rule_match))


def ReflexAgentA2pro():
    from src.agentPrograms import ReflexAgentProgram, interpret_input_A2pro, rule_match_A2pro
    from src.rules import a2proRules
    return Agent(ReflexAgentProgram(a2proRules, interpret_input_A2pro, rule_match_A2pro))
  

