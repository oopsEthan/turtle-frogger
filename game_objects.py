from turtle import *
from random import *

# Constants
CAR_SPEED = 3
CAR_COLORS = ["red", "blue", "green", "orange", "purple", "pink", "cyan", "magenta", "brown", "gray", "lime"]
PLAYER_STARTING_Y = -275
PLAYER_SPEED = 4

class Car():
    def __init__(self) -> None:
        self.car_obj = Turtle()
        self.current_y = 0

        self.collision_x = 20
        self.collision_y = 10

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
        self.initialize_player()
        self.y_velocity = 0

    def initialize_player(self):
        self.player_obj = Turtle()
        self.player_obj.shape("turtle")
        self.player_obj.pu()
        self.player_obj.lt(90)
        self.player_obj.shapesize(1.5, 1.5)
        self.player_obj.goto(0, PLAYER_STARTING_Y)

    def up(self):
        self.y_velocity = PLAYER_SPEED
    
    def down(self):
        self.y_velocity = -PLAYER_SPEED

    def stop(self):
        self.y_velocity = 0

    def move(self):
        new_y = self.player_obj.ycor() + self.y_velocity
        self.player_obj.goto(0, new_y)