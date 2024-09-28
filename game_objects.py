from turtle import *
from random import *

# Constants
CAR_SPEED = 5
CAR_COLORS = ["red", "blue", "green", "orange", "purple", "pink", "cyan", "magenta", "brown", "gray", "lime"]
PLAYER_STARTING_Y = -350
PLAYER_SPEED = 2
PLAYER_SIZE = 1.5

class Car():
    def __init__(self) -> None:
        self.car_obj = Turtle()
        self.current_y = 0
        self.direction = ""

        self.collision_min_x = 0
        self.collision_min_y = 0

        self.design_car()

    def design_car(self) -> None:
        self.car_obj.shape("square")
        self.car_obj.shapesize(1, 2)
        self.car_obj.pu()
        self.car_obj.color(choice(CAR_COLORS))

    def update_collision(self) -> None:
        self.collision_min_x = self.car_obj.xcor() - 20
        self.collision_min_y = self.car_obj.ycor() - 10

    def determine_spawn(self, screen, spawn_points) -> None:
        lane = choice(spawn_points)
        self.current_y = choice(lane)

        if lane[0] == 245:
            self.direction = "right"
            spawn_x = -screen.window_width() / 2 - 40

        elif lane[0] == 305:
            self.direction = "left"
            spawn_x = screen.window_width() / 2 + 40
            
        self.car_obj.goto(spawn_x, self.current_y)

    def car_move(self, screen) -> bool:
        new_x = 0

        if self.direction == "right":
            new_x = self.car_obj.xcor() + CAR_SPEED
            if(self.car_obj.xcor() > screen.window_width() / 2 + 40):
                print(f"{self.car_obj} deleted.")
                return True

        elif self.direction == "left":
            new_x = self.car_obj.xcor() - CAR_SPEED
            if(self.car_obj.xcor() < -screen.window_width() / 2 - 40):
                print(f"{self.car_obj} deleted.")
                return True

        self.car_obj.goto(new_x, self.current_y)
        self.update_collision()
        return False


class Player():
    def __init__(self) -> None:
        self.initialize_player()
        self.y_velocity = 0

        self.update_collision()

    def initialize_player(self) -> None:
        self.player_obj = Turtle()
        self.player_obj.shape("turtle")
        self.player_obj.color("green3")
        self.player_obj.pu()
        self.player_obj.lt(90)
        self.player_obj.shapesize(PLAYER_SIZE, PLAYER_SIZE)
        self.player_obj.goto(0, PLAYER_STARTING_Y)

    def up(self) -> None:
        self.y_velocity = PLAYER_SPEED
    
    def down(self) -> None:
        self.y_velocity = -PLAYER_SPEED

    def stop(self) -> None:
        self.y_velocity = 0

    def move(self) -> None:
        new_y = self.player_obj.ycor() + self.y_velocity
        self.player_obj.goto(0, new_y)

        self.update_collision()

    def update_collision(self) -> None:
        self.player_min_y = self.player_obj.ycor() - (PLAYER_SIZE * 10)
        self.player_min_x = self.player_obj.xcor() - (PLAYER_SIZE * 10)

    def check_for_collision(self, current_cars) -> bool:
        for car in current_cars:
            if abs(self.player_obj.xcor() - car.car_obj.xcor() < 50):
                within_x_range = self.player_min_x <= (car.collision_min_x+40) and (self.player_min_x+30) >= car.collision_min_x
                within_y_range = self.player_min_y <= (car.collision_min_y+20) and (self.player_min_y+30) >= car.collision_min_y

                if within_x_range and within_y_range:
                    print("Collision detected!")
                    self.player_obj.color("red")
                    return True
        return False

    def check_for_finish(self, finish_line_y) -> bool:
        if self.player_obj.ycor() >= finish_line_y:
            print(f"DEBUG: Win Detected!")
            return True
        return False