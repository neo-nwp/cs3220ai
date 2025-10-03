# foodClass.py
class Food:
    def __init__(self, weight, calories):
        self.weight = weight
        self.calories = calories


class Milk(Food):
    def __init__(self):
        super().__init__(weight=1, calories=100)


class Sausage(Food):
    def __init__(self):
        super().__init__(weight=1, calories=200)
