import random
import os
from loguru import logger

# --- Logger setup ---
logger.remove()
log_buffer = []
MAX_LOG_LINES = 10

def log_message(message, color="yellow"):
    logger.remove()
    color_format = {"red": "<red>{message}</red>",
                    "green": "<green>{message}</green>",
                    "blue": "<blue>{message}</blue>",
                    "yellow": "<yellow>{message}</yellow>"}
    logger.add(lambda msg: log_buffer.append(msg), colorize=True, format=color_format.get(color, "<yellow>{message}</yellow>"))
    logger.info(message)

# --- Classes ---
class Food:
    def __init__(self, value, position, defense):
        self.value = value
        self.defense = defense
        self.position = position

    def __str__(self):
        return f"Food(value={self.value}, position={self.position}, defense={self.defense})"

class Animal:
    def __init__(self, name, symbol=None):
        self.name = name
        self.symbol = symbol
        self.health = 100
        self.defence = 100
        self.position = (random.randint(0, 14), random.randint(0, 14))
        self.under_attack = False

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

    def radius(self):
        x, y = self.position
        return [(x-1,y), (x+1,y), (x,y-1), (x,y+1),self.position]

    def is_in_radius(self, target):
        return target.position in self.radius()

    def attack(self, target, damage):
        if isinstance(target, Animal):
            target.under_attack = True
            if self.is_in_radius(target):
                target.health -= damage
                if target.symbol:
                    log_message(f"YOU HAVE BEEN ATTACKED by {self.name}! with {damage:.1f} damage.", "red")
                else:
                    log_message(f"{self.name} attacks {target.name} for {damage:.1f} damage!", "red")
            else:
                log_message(f"{self.name} tried to attack {target.name} but target is out of range", "yellow")

    def defend(self, incoming_damage):
        if self.defence > 0:
            # Decide how much of the damage is absorbed by defence
            absorbed = random.uniform(0.4, 0.7) * incoming_damage
            absorbed = min(absorbed, self.defence)  # can’t absorb more than available defence

            # Reduce defence and apply remaining damage to health
            self.defence -= absorbed
            self.health -= max(0, incoming_damage - absorbed)

            log_message(
                f"{self.name} defends! Defence absorbed {absorbed:.1f} damage. "
                f"Took {max(0, incoming_damage - absorbed):.1f} damage to health. "
                f"Remaining Defence: {self.defence:.1f}, Health: {self.health:.1f}",
                "blue"
            )
        else:
            # No defence left → full damage goes to health
            self.health -= incoming_damage
            log_message(
                f"{self.name} has no defence left! Took {incoming_damage:.1f} damage directly to health.",
                "red"
            )

        self.under_attack = False


    def consume_food(self, foods):
        for food in foods[:]:
            if food.position in self.radius():
                self.health += food.value
                self.defence += food.defense
                foods.remove(food)
                if self.symbol:
                    log_message(f"YOU CONSUMED {food}! Gained {food.value} health. Total health: {self.health:.1f}", "green")
                else:
                    log_message(f"{self.name} consumed {food}.", "green")

    def __str__(self):
        return f"{self.name}(H:{self.health:.1f}, D:{self.defence:.1f}, Pos:{self.position})"

# --- Helper functions ---
def end_game(player, win: bool):
    status = "🏆 YOU WIN!" if win else "☠️ GAME OVER!"
    logger.opt(colors=True).success(
        f"\n\n<green>{status}</green>\n"
        f"<green>Final Stats:</green>\n"
        f"<green>Name:</green> {player.name}\n"
        f"<green>Health:</green> {player.health:.1f}\n"
        f"<green>Defence:</green> {player.defence:.1f}\n"
        f"<green>Position:</green> {player.position}\n"
    )
    input()


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
    # Display logs
    print("---- Game Log ----")
    for line in log_buffer[-MAX_LOG_LINES:]:
        print(line, end="")
    print("------------------\n")
    # Player stats
    print(f"Player Stats: Name: {player_goat.name} | Health: {player_goat.health:.1f} | Defence: {player_goat.defence:.1f} | Position: {player_goat.position}\n")
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
        if symbol.upper() not in {"G","P","F"} and len(symbol) == 1:
            return symbol
        print("Invalid symbol. Choose a single character not G, P, or F.")

# Predator AI helpers
def manhattan_distance(pos1,pos2):
    return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

def predator_decide_move(predator, goats, foods):
    target_goat = None
    guard_radius = 2
    for food in foods:
        for goat in goats:
            if manhattan_distance(food.position, goat.position) <= guard_radius:
                target_goat = goat
                break
        if target_goat:
            break
    if not target_goat and goats:
        target_goat = min(goats, key=lambda g: manhattan_distance(predator.position, g.position))
    if target_goat:
        dx = target_goat.position[0]-predator.position[0]
        dy = target_goat.position[1]-predator.position[1]
        if abs(dx)>abs(dy):
            predator.move("right" if dx>0 else "left")
        elif dy!=0:
            predator.move("up" if dy>0 else "down")
    else:
        predator.move(random.choice(["up","down","left","right"]))

# --- Main Game ---
def main():
    # Setup
    foods = [Food(random.randint(5,30),(random.randint(0,14),random.randint(0,14)), random.randint(5,15)) for _ in range(8)]
    predators = [Animal(f"Predator{i+1}") for i in range(4)]
    player_symbol = choose_player_symbol()
    player_goat = Animal("PlayerGoat", symbol=player_symbol)
    other_goats = [Animal(f"Goat{i+1}") for i in range(2)]
    all_animals = predators + [player_goat] + other_goats
    turn = 0

    # Game loop
    while True:
        turn +=1
        print(f"--- Turn {turn} ---")
        draw_board(all_animals, foods, player_goat)

        # Player move
        move = None
        while move is None:
            move = get_player_move()
        player_goat.move(move)
        player_goat.consume_food(foods)

        if player_goat.health <=0:
            end_game(player_goat, win=False)
            break

        # Other goats move
        for goat in other_goats[:]:
            move = random.choice(["up","down","left","right"])
            goat.move(move)
            goat.consume_food(foods)
            if goat.health<=0:
                log_message(f"{goat.name} has been defeated!", "red")
                all_animals.remove(goat)
                other_goats.remove(goat)

        # Predators move
        for predator in predators:
            predator_decide_move(predator, [player_goat]+other_goats, foods)
            for goat in [player_goat]+other_goats:
                if predator.is_in_radius(goat):
                    damage = random.randint(5,10)
                    predator.attack(goat, damage)
                    goat.defend(damage)
                    if goat.health<=0:
                        log_message(f"{goat.name} has been defeated!", "red")
                        if goat==player_goat:
                            end_game(player_goat, win=False)
                            return
                        all_animals.remove(goat)
                        if goat in other_goats:
                            other_goats.remove(goat)

        # Win/Lose check
        if not foods:
            end_game(player_goat, win=True)
            break
        if player_goat.health<=0:
            end_game(player_goat, win=False)
            break

if __name__=="__main__":
    main()
    input("Press Enter to exit...")
