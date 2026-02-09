# Lib Imports
import sys, pygame, csv, json

# Local Imports
from .settings import csv_state


class State:
    def __init__(self):
        # Setup
        self.unlocked_levels = 0
        self.current_level = 0

        self.max_health = 0
        self.current_health = 0

        self.total_coins = 0
        self.current_coins = 0

        self.in_game = False

    def __str__(self):
        state = {
            "unlocked_levels": self.unlocked_levels,
            "current_level": self.current_level,
            "max_health": self.max_health,
            "current_health": self.current_health,
            "total_coins": self.total_coins,
            "current_coins": self.current_coins,
        }

        return json.dumps(state)

    def load(self):
        try:
            with open(csv_state, "r") as raw:
                file = csv.DictReader(raw)
                state = next(file)

                self.unlocked_levels = int(state["unlocked_levels"])
                self.current_level = int(state["current_level"])
                self.max_health = int(state["max_health"])
                self.current_health = int(state["current_health"])
                self.total_coins = int(state["total_coins"])
                self.current_coins = int(state["current_coins"])
        except FileNotFoundError:
            self.make_state_file()
            self.load()

    def make_state_file(self):
        state = {
            "unlocked_levels": 0,
            "current_level": 0,
            "max_health": 100,
            "current_health": 100,
            "total_coins": 0,
            "current_coins": 0,
        }

        try:
            with open(csv_state, "w") as raw:
                file = csv.DictWriter(raw, fieldnames=state.keys())

                file.writeheader()
                file.writerow(state)
        except:
            print("\nUnable to find or create a game state.\n")
            pygame.quit()
            sys.exit()

    def save(self):
        state = json.loads(str(self))
        state["current_level"] = 0
        state["current_health"] = 0
        state["current_coins"] = 0

        with open(csv_state, "w") as raw:
            file = csv.DictWriter(raw, fieldnames=state.keys())

            file.writeheader()
            file.writerow(state)

    def reset(self):
        self.unlocked_levels = 0
        self.current_level = 0

        self.current_health = 100

        self.total_coins = 0
        self.current_coins = 0

    def reset_for_level(self):
        self.current_health = 100
        self.current_coins = 0

    def unlock_level(self):
        self.unlocked_levels += 1

    def change_level(self, by: int):
        self.current_level += by

    def change_health(self, by: int):
        self.current_health += by

    def save_coins(self):
        self.total_coins += self.current_coins

    def add_coin(self, coin):
        self.current_coins += coin.value

    def set_in_game(self, in_game=False):
        self.in_game = in_game
