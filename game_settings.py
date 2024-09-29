from turtle import *
from game_objects import *
from random import randint

# Constants
GAME_SPEED = 15
TOTAL_CARS_ON_SCREEN = 30
UP_KEY = "w"
DOWN_KEY = "s"
ROAD_LENGTH = 550
ROAD_WIDTH = 110
LINE_WIDTH = 10
LINE_LENGTH = 60
FINISH_LINE_Y = 360
SPAWN_POINT_OFFSET = 30
# Difficulty determines speed of cars
DEFAULT_DIFFICULTY = 5

class UI:
    # Initialize the game UI
    def __init__(self) -> None:
        self.game_window = Screen()
        self.game_window.setup(1024, 768)
        self.game_window.tracer(0)  # Adjust for FPS
        self.game_window.bgcolor("forest green")

        self.gameplay_turtle = Turtle()
        self.gameplay_turtle.pen(pendown=False, shown=False)

        self.text_turtle = Turtle()
        self.text_turtle.pen(pendown=False, shown=False)

        self.draw_finish_line()
        self.roads = Road_Builder()

    # Update the screen
    def update_screen(self) -> None:
        self.game_window.update()

    # Set up key listening for player movement
    def begin_listening(self, player: 'Player') -> None:
        self.game_window.listen()
        self.game_window.onkeypress(player.up, UP_KEY)
        self.game_window.onkeypress(player.down, DOWN_KEY)
        self.game_window.onkeyrelease(player.stop, UP_KEY)
        self.game_window.onkeyrelease(player.stop, DOWN_KEY)

    # Draw the finish line on the screen
    def draw_finish_line(self) -> None:
        self.gameplay_turtle.goto(-ROAD_LENGTH, FINISH_LINE_Y)
        self.gameplay_turtle.pen(pendown=True, pencolor="green2", pensize=10)
        self.gameplay_turtle.goto(ROAD_LENGTH, FINISH_LINE_Y)

    # Draw the main text and subtext on the screen
    def draw_words(self, string: str, sub_string: str) -> None:
        self.move_text_turtle(0, 170)
        self.text_turtle.write(f"{string}", align="center", font=("Courier", 32, "bold"))
        self.draw_sub_words(sub_string)

    # Draw the subtext on the screen
    def draw_sub_words(self, string: str) -> None:
        self.move_text_turtle(0, -5)
        self.text_turtle.write(f"{string}", align="center", font=("Courier", 24, "bold"))
    
    # Update the difficulty level on the screen
    def update_difficulty(self, difficulty: int) -> None:
        self.move_text_turtle(-450, -350)
        self.text_turtle.write(f"Difficulty: {difficulty}", align="left", font=("Courier", 24, "bold"))
    
    # Move the text turtle to a specific position
    def move_text_turtle(self, x: int, y: int) -> None:
        print(f"Moving to: {x}, {y}")
        self.text_turtle.pu()
        self.text_turtle.goto(x, y)
        self.text_turtle.pd()

    # Clear the text on the screen
    def clear_words(self) -> None:
        self.text_turtle.clear()

class Road_Builder:
    # Initialize the road builder
    def __init__(self) -> None:
        self.road_builder = Turtle()
        self.left_lane_spawn_points = []
        self.right_lane_spawn_points = []
        self.lane_spawn_points = [self.left_lane_spawn_points, self.right_lane_spawn_points]
        self.draw_roads()

    # Draw roads on the screen
    def draw_roads(self) -> None:
        roads_needed = 4
        road_y = 275
        while roads_needed > 0:
            self.draw_individual_road(0, road_y)
            road_y -= 175
            roads_needed -= 1
        self.road_builder.pen(pendown=False)

    # Draw a single road on the screen
    def draw_individual_road(self, x: int, y: int) -> None:
        self.road_builder.pen(pendown=False, pencolor="gray30", pensize=ROAD_WIDTH)
        self.road_builder.goto(x - ROAD_LENGTH, y)
        self.road_builder.pendown()
        self.road_builder.goto(x + ROAD_LENGTH, y)
        self.update_spawn_points(y)
        self.draw_lines()

    # Draw the road divider lines on the screen
    def draw_lines(self) -> None:
        self.road_builder.pen(pencolor="white", pensize=LINE_WIDTH)
        random_starting_x = self.road_builder.xcor() + randint(-40, 40)
        self.road_builder.goto(random_starting_x, self.road_builder.ycor())
        lines = 20
        draw = True
        while lines > 0:
            self.road_builder.pen(pendown=draw)
            draw = not draw
            new_x = self.road_builder.xcor() - LINE_LENGTH
            self.road_builder.goto(new_x, self.road_builder.ycor())
            lines -= 1

    # Update the spawn points for cars
    def update_spawn_points(self, spawn_point: int) -> None:
        self.left_lane_spawn_points.append(spawn_point - SPAWN_POINT_OFFSET)
        self.right_lane_spawn_points.append(spawn_point + SPAWN_POINT_OFFSET)

class Game:
    # Initialize the game
    def __init__(self) -> None:
        self.ui = UI()
        self.current_cars = []
        self.cars_to_be_removed = []
        self.prev_y = 0
        self.car_timer = 300
        self.difficulty = DEFAULT_DIFFICULTY
        self.ui.update_difficulty(int((self.difficulty - 3) / 2))
        self.spawn_car()

        self.win = False
        self.collision_detected = False
        self.player = Player()

        self.ui.begin_listening(self.player)
        self.game_loop()

    # Main game loop
    def game_loop(self) -> None:
        if not self.win and not self.collision_detected:
            for car in self.current_cars:
                if car.car_move(self.ui.game_window):
                    self.cars_to_be_removed.append(car)

            self.player.move()
            self.collision_detected = self.player.check_for_collision(self.current_cars)
            self.win = self.player.check_for_finish(FINISH_LINE_Y)

            if len(self.cars_to_be_removed) >= 1:
                self.clean_cars()

            self.ui.update_screen()

            self.ui.game_window.ontimer(self.game_loop, GAME_SPEED)

        elif self.collision_detected:
            self.hit_by_car()

        elif self.win:
            self.reached_end()

    # Spawn cars on the screen
    def spawn_car(self) -> None:
        if len(self.current_cars) < TOTAL_CARS_ON_SCREEN:
            car = Car(self.prev_y, self.difficulty)
            self.prev_y = car.determine_spawn(self.ui.game_window, self.ui.roads.lane_spawn_points)
            self.current_cars.append(car)
            self.car_timer += 10
        self.ui.game_window.ontimer(self.spawn_car, self.car_timer)

    # Clean up cars that are no longer on the screen
    def clean_cars(self) -> None:
        for car in self.cars_to_be_removed:
            self.current_cars.remove(car)
            car.car_obj.hideturtle()
            car.car_obj.clear()
            self.car_timer -= 10
            del car
        self.cars_to_be_removed.clear()

    # Handle reaching the end of the game (winning)
    def reached_end(self) -> None:
        self.ui.draw_words("You Win!", "Click to continue")
        self.ui.game_window.listen()
        self.win = False
        self.difficulty += 2
        self.ui.game_window.onclick(self.reset_screen)

    # Handle losing the game (colliding with a car)
    def hit_by_car(self) -> None:
        self.ui.draw_words("Game Over!", "Click to restart")
        self.ui.game_window.listen()
        self.collision_detected = False
        self.difficulty = DEFAULT_DIFFICULTY
        self.ui.game_window.onclick(self.reset_screen)
    
    # Reset the game screen after a win or loss
    def reset_screen(self, x: int = None, y: int = None) -> None:
        self.ui.clear_words()
        self.ui.update_difficulty(int((self.difficulty - 3) / 2))
        for car in self.current_cars:
            self.cars_to_be_removed.append(car)
        self.clean_cars()
        self.car_timer = 300
        self.player.reset_player()
        self.ui.update_screen()
        self.game_loop()

    # Run the game
    def run(self) -> None:
        self.ui.game_window.mainloop()