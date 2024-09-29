from turtle import *
from random import *

# Constants
CAR_COLORS = [
    "blue", "red", "white", "black", 
    "#6495ED", "#FF6347", "#FFF5EE", 
    "#9370DB", "#FFD700", "#FF4500", 
    "#87CEEB", "#FF69B4", "#E6E6FA", 
    "#F5DEB3", "#000000"
]
PLAYER_STARTING_Y = -350
PLAYER_SPEED = 2
PLAYER_SIZE = 1.5

class Car:
    # Initialize the car object
    def __init__(self, prev_y: float, car_speed: int) -> None:
        self.car_obj = Turtle()
        self.current_y = 0
        self.prev_y = prev_y
        self.direction = ""
        self.car_speed = car_speed

        self.collision_min_x = 0
        self.collision_min_y = 0

        self.design_car()

    # Design the car with random color and attributes
    def design_car(self) -> None:
        self.car_obj.shape("square")
        self.car_obj.shapesize(1, 2)
        self.car_obj.pu()
        self.car_obj.color(choice(CAR_COLORS))

    # Update the collision boundaries of the car
    def update_collision(self) -> None:
        self.collision_min_x = self.car_obj.xcor() - 20
        self.collision_min_y = self.car_obj.ycor() - 10

    # Determine the spawn location for the car, ensuring it doesn't spawn in the same lane as the previous one
    def determine_spawn(self, screen: Screen, spawn_points: list) -> float:
        lane = choice(spawn_points)
        
        self.current_y = choice(lane)
        while self.current_y == self.prev_y:
            self.current_y = choice(lane)
        kickback_y_before_randomizing = self.current_y
        self.current_y += randint(1, 10)

        if lane[0] == 245:
            self.direction = "right"
            spawn_x = -screen.window_width() / 2 - 40
        elif lane[0] == 305:
            self.direction = "left"
            spawn_x = screen.window_width() / 2 + 40

        self.car_obj.goto(spawn_x, self.current_y)
        return kickback_y_before_randomizing

    # Move the car across the screen and return True if it goes off-screen
    def car_move(self, screen: Screen) -> bool:
        if self.direction == "right":
            new_x = self.car_obj.xcor() + self.car_speed
            if self.car_obj.xcor() > screen.window_width() / 2 + 40:
                return True
        elif self.direction == "left":
            new_x = self.car_obj.xcor() - self.car_speed
            if self.car_obj.xcor() < -screen.window_width() / 2 - 40:
                return True

        self.car_obj.goto(new_x, self.current_y)
        self.update_collision()
        return False
    
class Player:
    # Initialize the player object
    def __init__(self) -> None:
        self.initialize_player()
        self.y_velocity = 0
        self.update_collision()

    # Set up the player's starting attributes
    def initialize_player(self) -> None:
        self.player_obj = Turtle()
        self.player_obj.shape("turtle")
        self.player_obj.color("green3")
        self.player_obj.pu()
        self.player_obj.lt(90)
        self.player_obj.shapesize(PLAYER_SIZE, PLAYER_SIZE)
        self.player_obj.goto(0, PLAYER_STARTING_Y)

    # Reset the player's position
    def reset_player(self) -> None:
        self.player_obj.goto(0, PLAYER_STARTING_Y)

    # Move the player up
    def up(self) -> None:
        self.y_velocity = PLAYER_SPEED
    
    # Move the player down
    def down(self) -> None:
        self.y_velocity = -PLAYER_SPEED

    # Stop the player's movement
    def stop(self) -> None:
        self.y_velocity = 0

    # Move the player based on the velocity
    def move(self) -> None:
        new_y = self.player_obj.ycor() + self.y_velocity
        self.player_obj.goto(0, new_y)
        self.update_collision()

    # Update the collision boundaries of the player
    def update_collision(self) -> None:
        self.player_min_y = self.player_obj.ycor() - (PLAYER_SIZE * 10)
        self.player_min_x = self.player_obj.xcor() - (PLAYER_SIZE * 10)

    # Check for collisions between the player and any cars
    def check_for_collision(self, current_cars: list) -> bool:
        for car in current_cars:
            if abs(self.player_obj.xcor() - car.car_obj.xcor()) < 50:
                within_x_range = self.player_min_x <= (car.collision_min_x + 40) and (self.player_min_x + 30) >= car.collision_min_x
                within_y_range = self.player_min_y <= (car.collision_min_y + 20) and (self.player_min_y + 30) >= car.collision_min_y

                if within_x_range and within_y_range:
                    return True
        return False

    # Check if the player has reached the finish line
    def check_for_finish(self, finish_line_y: float) -> bool:
        if self.player_obj.ycor() >= finish_line_y:
            return True
        return False