from turtle import *
from random import *

# Constants for Car
CAR_SPEED = 5
CAR_COLORS = [
    "blue", "red", "white", "black", 
    "#6495ED", "#FF6347", "#FFF5EE", 
    "#9370DB", "#FFD700", "#FF4500", 
    "#87CEEB", "#FF69B4", "#E6E6FA", 
    "#F5DEB3", "#000000"
]

# Constants for Player
PLAYER_STARTING_Y = -375
PLAYER_SPEED = 2
PLAYER_SIZE = 1.5
PLAYER_COLLISION_THRESHOLD = 25

class Car(Turtle):
    # Initialize the car object
    def __init__(self, prev_y: float, car_speed: int = CAR_SPEED) -> None:
        super().__init__()
        self.current_y = 0
        self.prev_y = prev_y
        self.direction = ""
        self.car_speed = car_speed

        self.design_car()

    # Design the car with random color and attributes
    def design_car(self) -> None:
        self.shape("square")
        self.shapesize(1, 2)
        self.pu()
        self.color(choice(CAR_COLORS))

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

        self.goto(spawn_x, self.current_y)
        return kickback_y_before_randomizing

    # Move the car across the screen and return True if it goes off-screen
    def car_move(self, screen: Screen) -> bool:
        if self.direction == "right":
            new_x = self.xcor() + self.car_speed
            if self.xcor() > screen.window_width() / 2 + 40:
                return True
        elif self.direction == "left":
            new_x = self.xcor() - self.car_speed
            if self.xcor() < -screen.window_width() / 2 - 40:
                return True

        self.goto(new_x, self.current_y)
        self.update_collision()
        return False

class Player(Turtle):
    # Initialize the player object
    def __init__(self) -> None:
        super().__init__()
        self.initialize_player()

    # Set up the player's starting attributes
    def initialize_player(self) -> None:
        self.y_velocity = 0
        self.shape("turtle")
        self.color("green3")
        self.lt(90)
        self.shapesize(PLAYER_SIZE, PLAYER_SIZE)
        self.teleport(0, PLAYER_STARTING_Y)

    # Move the player up
    def up(self) -> None:
        self.y_velocity = PLAYER_SPEED
    
    # Move the player down
    def down(self) -> None:
        self.y_velocity = -PLAYER_SPEED

    # Stop the player's movement
    def stop(self) -> None:
        self.y_velocity = 0

    # Reset the player's position
    def reset_player(self) -> None:
        self.teleport(0, PLAYER_STARTING_Y)

    # Move the player based on the velocity
    def move(self) -> None:
        new_y = self.ycor() + self.y_velocity
        self.teleport(0, new_y)

    # Check for collisions between the player and any cars
    def check_for_collision(self, current_cars: list) -> bool:
        for car in current_cars:
            if self.distance(car) < PLAYER_COLLISION_THRESHOLD:
                return True
        return False

    # Check if the player has reached the finish line
    def check_for_finish(self, finish_line_y: float) -> bool:
        if self.ycor() >= finish_line_y:
            return True
        return False