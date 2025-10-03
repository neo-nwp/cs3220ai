import streamlit as st
import random

from src.agentClass import AgentCat
from src.foodClass import Milk, Sausage
from src.environment import CatFriendlyHouse


# --- Agent's program ---
def cat_program(percept):
    status, foods = percept
    if status == 'MilkHere' and foods:
        return 'Drink'
    elif status == 'SausageHere' and foods:
        return 'Eat'
    else:
        return random.choice(['MoveRight', 'MoveLeft'])


# --- Initialize session state ---
if "house" not in st.session_state:
    st.session_state.house = CatFriendlyHouse()
    st.session_state.agent = AgentCat(program=cat_program)
    st.session_state.agent.location = random.choice([0, 1])
    # Place food
    rooms = [0, 1]
    random.shuffle(rooms)
    st.session_state.house.place_food(Milk(), rooms[0])
    st.session_state.house.place_food(Sausage(), rooms[1])
    st.session_state.step = 0
    st.session_state.last_action = None


# --- Sidebar Controls ---
st.sidebar.title("Simulation Controls")
if st.sidebar.button("Reset Simulation"):
    st.session_state.house = CatFriendlyHouse()
    st.session_state.agent = AgentCat(program=cat_program)
    st.session_state.agent.location = random.choice([0, 1])
    rooms = [0, 1]
    random.shuffle(rooms)
    st.session_state.house.place_food(Milk(), rooms[0])
    st.session_state.house.place_food(Sausage(), rooms[1])
    st.session_state.step = 0
    st.session_state.last_action = None
    st.sidebar.success("Simulation reset!")


# --- Main Simulation Display ---
st.title("🐱 Cat Agent Simulation")

agent = st.session_state.agent
house = st.session_state.house

# Display house state
st.subheader("House State")
cols = st.columns(len(house.rooms))
for i, room in enumerate(house.rooms):
    with cols[i]:
        if i == agent.location:
            st.markdown(f"**Room {i} (Agent Here)**")
        else:
            st.markdown(f"Room {i}")
        st.write(f"Status: {room.status}")
        if room.foods:
            st.write("Foods: " + ", ".join([food.__class__.__name__ for food in room.foods]))
        else:
            st.write("Foods: None")

# Agent info
st.subheader("Agent State")
st.write(f"Performance: {agent.performance}")
if st.session_state.last_action:
    st.write(f"Last Action: {st.session_state.last_action}")


# --- Simulation Step Button ---
if st.button("Next Step"):
    st.session_state.step += 1
    percept = house.percept(agent)
    action = agent.program(percept)
    st.session_state.last_action = action

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

    if agent.performance <= 0:
        st.error("💀 The Agent is dead. Reset simulation to try again.")
