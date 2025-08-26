
# Goat Run

**Predator vs. Goat** is a turn-based survival game written in Python. You control a goat and must consume all the food on a 15×15 board while avoiding predators. The game uses **loguru** for detailed event logging, including movement, attacks, defenses, and food consumption.

---

## Features

- **15×15 grid board** visualized in the console.
- **Player-controlled goat** with keyboard input (`w`, `a`, `s`, `d`).
- **Predators** that move randomly and attack goats within range.
- **Other goats** that move randomly and consume food.
- **Food items** placed randomly on the board, providing health when consumed.
- **Event logging** for movement, attacks, defense, and food consumption.
- **Win/Lose conditions**:
  - **Win:** Player goat consumes all food.
  - **Lose:** Player goat is killed by predators.
- **Color-coded logs** for clear visualization:
  - **Red:** Attacks
  - **Blue:** Defense
  - **Green:** Food consumption / victory
  - **Yellow:** Other events

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/goat-run.git
cd goat-run
````

2. Install Python 3.8+ if you don’t have it already.

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Game

### Linux/macOS

1. Make the launcher script executable:

```bash
chmod +x play.sh
```

2. Run the game:

```bash
./play.sh
```

### Windows

1. Double-click `play.bat`, or run it from Command Prompt:

```bat
play.bat
```

The batch file will automatically check for Python and required packages.

---

## Controls

* **w** = Move up
* **s** = Move down
* **a** = Move left
* **d** = Move right

Your goal: consume all the food while avoiding predators.

---

## Notes

* Avoid choosing `G`, `P`, or `F` as your goat symbol—it may conflict with other board markers.
* The game logs the last 10 events on the console for easy tracking.
* Player stats are always visible above the board.

---

## License

This project is licensed under the MIT License.

```
