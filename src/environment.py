# environment.py
from src.foodClass import Milk, Sausage

class CatFriendlyHouse:
    def __init__(self):
        self.rooms = [Room(0), Room(1)]  # two rooms for simplicity

    def place_food(self, food, room_number):
        self.rooms[room_number].add_food(food)

    def percept(self, agent):
        room = self.rooms[agent.location]
        return (room.status, room.foods)


class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.status = 'Empty'
        self.foods = []

    def add_food(self, food):
        if food:
            if isinstance(food, Milk):
                self.status = 'MilkHere'
            elif isinstance(food, Sausage):
                self.status = 'SausageHere'
            self.foods.append(food)
        else:
            self.status = 'Empty'
