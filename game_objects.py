from turtle import *
from random import *

# Constants
CAR_SPEED = 3
CAR_COLORS = ["red", "blue", "green", "orange", "purple", "pink", "yellow", "cyan", "magenta", "brown", "gray", "lime"]

class Car():
    def __init__(self) -> None:
        self.car_obj = Turtle()
        self.current_y = 0

        self.design_car()
        self.determine_spawn()
    
    def design_car(self) -> None:
        self.car_obj.shape("square")
        self.car_obj.shapesize(1, 2)
        self.car_obj.pu()
        self.car_obj.color(choice(CAR_COLORS))

    def determine_spawn(self) -> None:
        self.current_y = randrange(-300, 300)
        self.car_obj.goto(-400, self.current_y)

    def car_move(self) -> bool:
        new_x = self.car_obj.xcor() + CAR_SPEED
        self.car_obj.goto(new_x, self.current_y)

        if(self.car_obj.xcor() > 400):
            return True
        return False


class Player():
    def __init__(self) -> None:
        pass