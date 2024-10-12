from turtle import *
from random import randint
from game_objects import *

# Constants for Game Settings
GAME_SPEED = 15
DEFAULT_DIFFICULTY = 5
UP_KEY = "w"
DOWN_KEY = "s"

# Constants for Car Controls
CAR_SPAWN_TIMER = 450
TOTAL_CARS_ON_SCREEN = 30
SPAWN_POINT_OFFSET = 30

# Constants for UI
ROAD_LENGTH = 550
ROAD_WIDTH = 110
LINE_WIDTH = 10
LINE_LENGTH = 60
FINISH_LINE_Y = 360

class UI(Turtle):
    # Initialize the game UI
    def __init__(self) -> None:
        super().__init__()
        self.game_window = Screen()
        self.game_window.setup(1024, 768)
        self.game_window.tracer(0)  # or tracer(8) based on performance

        self.graphics = Graphics_Drawer()
        self.graphics.draw_finish_line()
        self.graphics.draw_roads()

        self.pen(pendown=False, shown=False)

    # Update the game screen
    def update_screen(self) -> None:
        self.game_window.update()

    # Set up key listening for player controls
    def begin_listening(self, player: 'Player') -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)

    # Draw the main text on the screen
    def draw_words(self, string: str, sub_string: str) -> None:
        self.teleport(0, 170)
        self.write(f"{string}", align="center", font=("Courier", 32, "bold"))
        self.draw_sub_words(sub_string)

    # Draw the subtext on the screen
    def draw_sub_words(self, string: str) -> None:
        self.teleport(0, -5)
        self.write(f"{string}", align="center", font=("Courier", 24, "bold"))

    # Clear the text from the screen
    def clear_words(self) -> None:
        self.clear()

class Graphics_Drawer(Turtle):
    # Initialize the graphics drawer for roads and lines
    def __init__(self) -> None:
        super().__init__()
        self.left_lane_spawn_points = []
        self.right_lane_spawn_points = []
        self.lane_spawn_points = [self.left_lane_spawn_points, self.right_lane_spawn_points]
        self.hideturtle()

    # Draw multiple roads on the screen
    def draw_roads(self) -> None:
        roads_needed = 4
        road_y = 275
        while roads_needed > 0:
            self.draw_individual_road(0, road_y)
            road_y -= 175
            roads_needed -= 1
    
    # Draw an individual road
    def draw_individual_road(self, x: int, y: int) -> None:
        self.teleport(x-ROAD_LENGTH, y)
        self.pen(pencolor="gray30", pensize=ROAD_WIDTH)
        self.goto(x+ROAD_LENGTH, y)
        self.update_spawn_points(y)
        self.draw_lines()

    # Draw the lane divider lines on the roads
    def draw_lines(self) -> None:
        self.pen(pencolor="white", pensize=LINE_WIDTH)
        random_starting_x = self.xcor() + randint(-40, 40)
        self.goto(random_starting_x, self.ycor())
        lines = 19
        draw = True
        while lines > 0:
            print(draw)
            self.pen(pendown=draw)
            draw = not draw
            new_x = self.xcor() - LINE_LENGTH
            self.goto(new_x, self.ycor())
            lines -= 1
            
    # Update the spawn points for cars
    def update_spawn_points(self, spawn_point: int) -> None:
        self.left_lane_spawn_points.append(spawn_point - SPAWN_POINT_OFFSET)
        self.right_lane_spawn_points.append(spawn_point + SPAWN_POINT_OFFSET)

    # Draw the finish line at the top of the screen
    def draw_finish_line(self) -> None:
        self.teleport(-ROAD_LENGTH, FINISH_LINE_Y)
        self.pen(pencolor="green2", pensize=10)
        self.goto(ROAD_LENGTH, FINISH_LINE_Y)

class Game():
    # Initialize the game
    def __init__(self) -> None:
        self.ui = UI()
        self.current_cars = []
        self.cars_to_be_removed = []
        self.prev_y = 0
        self.car_timer = CAR_SPAWN_TIMER
        self.difficulty = DEFAULT_DIFFICULTY
        self.ui.update_screen()  # for initial setup

        self.player = Player()
        self.ui.begin_listening(self.player)

        self.game_loop()
        self.spawn_car()

    # Main game loop to control movement, collisions, and screen updates
    def game_loop(self) -> None:
        if not self.player.check_for_finish(FINISH_LINE_Y) and not self.player.check_for_collision(self.current_cars):
            self.cars_to_be_removed = [car for car in self.current_cars if car.car_move(self.ui.game_window)]

            self.player.move()
            self.ui.update_screen()

            if len(self.cars_to_be_removed) >= 1:
                self.clean_cars()

            self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)
        elif self.player.check_for_finish(FINISH_LINE_Y):
            self.reached_end()
        elif self.player.check_for_collision(self.current_cars):
            self.hit_by_car()

    # Spawn new cars if below the limit
    def spawn_car(self) -> None:
        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car(self.prev_y, self.difficulty)
            self.prev_y = car.determine_spawn(self.ui.game_window, self.ui.graphics.lane_spawn_points)
            self.current_cars.append(car)
            self.car_timer += 10
        self.ui.game_window.ontimer(self.spawn_car, self.car_timer)

    # Remove cars that have gone off-screen
    def clean_cars(self) -> None:
        for car in self.cars_to_be_removed:
            self.current_cars.remove(car)
            car.hideturtle()
            del car
        self.cars_to_be_removed.clear()

    # Display "You Win!" when the player reaches the finish line
    def reached_end(self) -> None:
        self.ui.draw_words("You Win!", "Click to continue")
        self.ui.game_window.onclick(self.reset_screen)

    # Display "Game Over" when the player hits a car
    def hit_by_car(self) -> None:
        self.ui.draw_words("Game Over!", "Click to restart")
        self.ui.game_window.onclick(self.reset_screen)

    # Reset the game state after win or loss
    def reset_screen(self, x: int = None, y: int = None) -> None:
        self.ui.clear_words()
        for car in self.current_cars:
            self.cars_to_be_removed.append(car)
        self.clean_cars()
        self.car_timer = CAR_SPAWN_TIMER
        self.player.reset_player()
        self.ui.update_screen()
        self.game_loop()

    # Run the game loop
    def run(self) -> None:
        self.ui.game_window.mainloop()