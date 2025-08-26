import random
import os
from loguru import logger

# Configure logger to print to console only
logger.remove()
logger.add(lambda msg: log_buffer.append(msg), colorize=True, format="<green>{message}</green>")

# --- Global log buffer ---
log_buffer = []
MAX_LOG_LINES = 10  # Number of log lines to display

# --- Classes ---
class Food:
    def __init__(self, value, position):
        self.value = value
        self.position = position

    def __str__(self):
        return f"Food(value={self.value}, position={self.position})"


class Animal:
    def __init__(self, name, symbol=None):
        self.name = name
        self.under_attack = False
        self.health = 100
        self.defence = 100
        self.position = (random.randint(0, 14), random.randint(0, 14))
        self.symbol = symbol  # Player custom symbol or None

    def move(self, direction):
        x, y = self.position
        if direction == "up" and y < 14:
            self.position = (x, y + 1)
        elif direction == "down" and y > 0:
            self.position = (x, y - 1)
        elif direction == "left" and x > 0:
            self.position = (x - 1, y)
        elif direction == "right" and x < 14:
            self.position = (x + 1, y)
        self._log(f"{self.name} moved {direction} to {self.position}", "info")

    def radius(self):
        x, y = self.position
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    def is_in_radius(self, target):
        return target.position in self.radius()

    def attack(self, target, damage):
        if isinstance(target, Animal):
            target.under_attack = True
            if self.is_in_radius(target):
                target.health -= damage
                color = "red" if target.symbol else "yellow"
                self._log(f"{self.name} attacks {target.name} for {damage:.1f} damage!", color)
                if target.symbol:
                    self._log(f"YOU HAVE BEEN ATTACKED! Lost {damage:.1f} health.", "red")
            else:
                self._log(f"{self.name} tried to attack {target.name}, but target is out of range", "yellow")

    def defend(self):
        if self.under_attack:
            loss = self.defence / 4
            self.health -= loss
            self.defence -= loss
            self.under_attack = False
            if self.symbol:
                self._log(f"YOU DEFENDED! Lost {loss:.1f} health/defence. Health: {self.health:.1f}, Defence: {self.defence:.1f}", "blue")
            else:
                self._log(f"{self.name} defends and loses {loss:.1f} health/defence.", "yellow")

    def consume_food(self, foods):
        for food in foods[:]:
            if food.position in self.radius():
                self.health += food.value
                foods.remove(food)
                if self.symbol:
                    self._log(f"YOU CONSUMED {food}! Gained {food.value} health. Total health: {self.health:.1f}", "green")
                else:
                    self._log(f"{self.name} consumed {food}.", "yellow")

    def _log(self, message, color="yellow"):
        if color == "red":
            logger.remove()
            logger.add(lambda msg: log_buffer.append(msg), colorize=True, format="<red>{message}</red>")
        elif color == "green":
            logger.remove()
            logger.add(lambda msg: log_buffer.append(msg), colorize=True, format="<green>{message}</green>")
        elif color == "blue":
            logger.remove()
            logger.add(lambda msg: log_buffer.append(msg), colorize=True, format="<blue>{message}</blue>")
        else:
            logger.remove()
            logger.add(lambda msg: log_buffer.append(msg), colorize=True, format="<yellow>{message}</yellow>")
        logger.info(message)

    def __str__(self):
        return f"{self.name}(H:{self.health:.1f}, D:{self.defence:.1f}, Pos:{self.position})"


# --- Helper functions ---
def draw_board(animals, foods, player_goat, size=15):
    board = [["." for _ in range(size)] for _ in range(size)]

    # Place food
    for food in foods:
        x, y = food.position
        board[y][x] = "F"

    # Place animals
    for animal in animals:
        x, y = animal.position
        mark = animal.symbol or ("P" if "Predator" in animal.name else "G")
        board[y][x] = mark if board[y][x] == "." else board[y][x] + mark

    os.system("cls" if os.name == "nt" else "clear")

    # Display last logs
    print("---- Game Log ----")
    for line in log_buffer[-MAX_LOG_LINES:]:
        print(line, end="")  # loguru adds newlines
    print("------------------\n")

    # Display player stats
    print(f"Player Stats: Name: {player_goat.name} | Health: {player_goat.health:.1f} | "
          f"Defence: {player_goat.defence:.1f} | Position: {player_goat.position}\n")

    # Print board
    for row in reversed(board):
        print(" ".join(row))
    print("\n")


def get_player_move():
    move = input("Move your goat (w/a/s/d): ").strip().lower()
    mapping = {"w": "up", "s": "down", "a": "left", "d": "right"}
    return mapping.get(move, None)


def choose_player_symbol():
    while True:
        symbol = input("Choose a symbol for your goat (avoid G, P, F): ").strip()
        if symbol.upper() not in {"G", "P", "F"} and len(symbol) == 1:
            return symbol
        print("Invalid symbol. Please choose a single character not G, P, or F.")


# --- Game setup ---
foods = [Food(random.randint(5, 30), (random.randint(0, 14), random.randint(0, 14))) for _ in range(8)]
predators = [Animal(f"Predator{i+1}") for i in range(4)]
player_symbol = choose_player_symbol()
player_goat = Animal("PlayerGoat", symbol=player_symbol)
other_goats = [Animal(f"Goat{i+1}") for i in range(2)]
all_animals = predators + [player_goat] + other_goats

# --- Game loop ---
turn = 0
while True:
    turn += 1
    print(f"--- Turn {turn} ---")

    # Draw board and logs
    draw_board(all_animals, foods, player_goat)

    # Player move
    move = None
    while move is None:
        move = get_player_move()
    player_goat.move(move)
    player_goat.consume_food(foods)
    if player_goat.health <= 0:
        player_goat._log("You have been defeated! Game over.", "red")
        break

    # Other goats move randomly
    for goat in other_goats[:]:
        move = random.choice(["up", "down", "left", "right"])
        goat.move(move)
        goat.consume_food(foods)
        if goat.health <= 0:
            goat._log(f"{goat.name} has been defeated!", "red")
            all_animals.remove(goat)
            other_goats.remove(goat)

    # Predators move randomly and attack goats
    for predator in predators:
        move = random.choice(["up", "down", "left", "right"])
        predator.move(move)
        for goat in [player_goat] + other_goats:
            if predator.is_in_radius(goat):
                damage = random.randint(5, 20)
                predator.attack(goat, damage)
                goat.defend()
                if goat.health <= 0:
                    goat._log(f"{goat.name} has been defeated!", "red")
                    if goat == player_goat:
                        break
                    all_animals.remove(goat)
                    if goat in other_goats:
                        other_goats.remove(goat)

    # Check win/lose
    if not foods:
        player_goat._log("Congratulations! You consumed all the food. You win!", "green")
        break
    if player_goat.health <= 0:
        player_goat._log("You have been killed by predators. Game over.", "red")
        break
