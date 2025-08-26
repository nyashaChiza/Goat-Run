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

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/predator-vs-goat.git
cd Goat-Run
