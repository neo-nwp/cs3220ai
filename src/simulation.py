# simulation.py
import sys
import os
import random

# Ensure src is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agentClass import AgentCat
from src.foodClass import Milk, Sausage
from src.environment import CatFriendlyHouse


# --- Agent's brain ---
def cat_program(percept):
    status, foods = percept
    if status == 'MilkHere' and foods:
        return 'Drink'
    elif status == 'SausageHere' and foods:
        return 'Eat'
    else:
        # No food, move randomly
        return random.choice(['MoveRight', 'MoveLeft'])


# --- Setup environment ---
def place_food_in_random_room(house):
    milk = Milk()
    sausage = Sausage()
    rooms = [0, 1]
    random.shuffle(rooms)
    house.place_food(milk, rooms[0])
    house.place_food(sausage, rooms[1])


house = CatFriendlyHouse()
place_food_in_random_room(house)

agent_cat = AgentCat(program=cat_program)
agent_cat.location = random.choice([0, 1])  # start randomly


# --- Simulation loop ---
def run_simulation(house, agent):
    steps = 10
    for step in range(steps):
        percept = house.percept(agent)
        action = agent.program(percept)
        print(f"\nStep {step+1}: Agent at room {agent.location}, Percept: {percept}, Action: {action}")

        if action == 'MoveRight' and agent.location < len(house.rooms) - 1:
            agent.location += 1
            agent.performance -= 1
        elif action == 'MoveLeft' and agent.location > 0:
            agent.location -= 1
            agent.performance -= 1
        elif action in ['Drink', 'Eat']:
            food = next((food for food in house.rooms[agent.location].foods), None)
            if food:
                agent.eat(food)
                house.rooms[agent.location].foods.remove(food)
                house.rooms[agent.location].status = 'Empty' if not house.rooms[agent.location].foods else house.rooms[agent.location].status

        print(f"Agent performance: {agent.performance}")

        if agent.performance <= 0:
            print("Agent is dead.")
            break


if __name__ == "__main__":
    run_simulation(house, agent_cat)
