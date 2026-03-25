# list of locations, actions, exits, and description.
# will update into a dictionary soon once mini text-game is fully fleshed out and complete as to make transition less mentally distressing.
locations = {
    "The Village of Pithon": {
        "description": "A small, quiet village, secluded from the rest of the world. The Fountain of Youth waits patiently in the village square.",
        "exits": ["The Dark Forest", "The Fountain of Youth"],
        "actions": ["talk", "rest", "investigate", "leave", "go to fountain"]
},

    "The Dark Forest": {
        "description": "The dark trees shade you from the once bright sun, and only stark contrast remains.",
        "exits": ["The Village of Pithon", "The Fountain of Youth", "The Dark Cave"],
        "actions": ["investigate", "call", "investigate cave", "leave"]
},

    "The Dark Cave": {
        "description": "A dark and damp cave. The drops of water echo throughout. Something within growls low.",
        "exits": ["The Dark Forest"],
        "actions": ["investigate", "fight", "calm", "investigate cave", "leave", "eat herb"]
    },
    "The Fountain of Youth": {
        "description": "A fountain glowing ethereal white. It's rich water begs you to take a sip.",
        "exits": ["The Village of Pithon", "The Dark Forest"],
        "actions": ["sip", "examine", "pee in"]
    }
}

class GameState:
    def __init__(self):
        self.location = "The Village of Pithon"
        self.health = 150
        self.inventory = []
        self.flags = {
            "bear_attacked": False,
            "bear_calmed": False,
            "talked_to_elder": False,
            "peed_in_fountain": False,
            "found_herb": False,
            "gained_immortality": False,
            "eaten_herb": False
        }

def game_loop():
    self = GameState()
    print("Welcome to your adventure!\nType 'save' to save, 'load' to load your previous game, 'restart' to start from the beginning again, 'quit' to exit the game, or type an action on screen to start!")

    while True:
        show_location(self)
        cmd = input("\n>").strip().lower()

        if cmd == "restart":
            confirm = input("Restart from the beginning? (y/n) :")
            if confirm.lower() == "y":
                self = GameState()
                print("Game has been restarted!")
            continue

        elif cmd == "load":
            result = load_game()
            if result is not None:
                self = result
            continue

        elif cmd == "save":
            save_game(self)
            continue

        elif cmd == "quit":
            confirm = input("Are you sure you want to quit? (y/n): ").lower()
            if confirm == "y":
                print("Goodbye.")
            break

        process_cmd(self, cmd)

import json

# currently creates a successful .json file. unsure if it can create duplicates. will look into further.
def save_game(self):
    data = {
        "location": self.location,
        "health": self.health,
        "inventory": self.inventory,
        "flags": self.flags,
    }

    with open("save.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\n[ Game saved successfully. ]")

def load_game():
    try:
        with open("save.json", "r") as f:
            data = json.load(f)

        new_self = GameState()

        new_self = GameState()
        new_self.location = data["location"]
        new_self.health = data["health"]
        new_self.inventory = data["inventory"]
        new_self.flags = data["flags"]

        print("\n[ Game loaded successfully. ]")
        return new_self

    except FileNotFoundError:
            print("\n[ No save data found. ]")
            return None

def handle_death(self):
    print("\n------G A M E  O V E R------")
    choice = input("Would you like to restart from the last state? (y/n): ").lower().strip()

    if choice == "y":
        self = GameState()
    elif choice == "n":
        print("Goodbye.")
        exit()

# simple def that displays location, actions, exits, etc. 
def show_location(self):
    loc = locations[self.location]

    print("\nLocation:", self.location)
    print(f"Health: {self.health}")
    
    print("\nExits:")
    for e in loc["exits"]:
        print("-", e)

    print("\nActions:")
    for a in loc["actions"]:
        print("-", a)

def process_cmd(self, cmd):
    loc = locations[self.location]
    cmd = cmd.lower() 

    if cmd in [e.lower() for e in loc["exits"]]:
        self.location = cmd
        return
    if cmd in loc["exits"]:
        self.location = cmd
        return
    if cmd == "save":
        save_game(self)
        return
    if cmd == "load":
        new_self = load_game()
        self.location = new_self.location
        self.health = new_self.health
        self.inventory = new_self.inventory
        self.flags = new_self.flags
        return
    
    if cmd == "fight":
        fight_bear(self)
        return
    if cmd == "calm":
        calm_bear(self)
        return
    if cmd in [a.lower() for a in loc["actions"]]:
        interact(self, cmd)
        return
    else:
        print("Unknown command.")

# this is a WIP and very barebones. there will be a randomizer that will either inflict or deflect damage.
# will add a sword to game for this scenario.
def fight_bear(self):
    if self.flags["bear_calmed"]:
        print("The beast stares at you with a soft gaze. He does not intend to hurt you.")
        return

    if not self.flags["bear_attacked"]:
        print("The beast slashes you, dealing -5 damage!")
        self.health -= 5
        self.flags["bear_attacked"] = True
    else:
        print("The beast slashes you once again, dealing -10 damage!")
        self.health -= 10
    if self.health <= 0:
        print("The beast has defeated you...")
        exit()
    else:
        print(f"Your health is now {self.health}")

# this is a WIP and very barebones. there will be a randomizer that will make the flag True or False.
def calm_bear(self):
    if self.flags.get("bear_calmed"):
        print("The beast is already calm.")
        return
    elif self.flags.get("bear_attacked"):
        print("You coo and show yourself to not be a threat. The beast sits and stares at you with soft eyes.")
        self.flags["bear_calmed"] = True
        self.flags["bear_attacked"] = False
    else:
        print("The bear is not aggressive yet. There is no need to calm it.")


# choices player can choose and what they do.
# still very incomplete and some commands do not function as intended.
def interact(self, cmd):
    if cmd == "talk":
        if self.location == "The Village of Pithon":
            print("You speak to the village elder. He warns you of dangers in the forest and begs you not to investigate the sounds.")
            self.flags["talked_to_elder"] = True
        elif self.flags["talked_to_elder"] == True:
            print("There is nobody here to speak to...")
        else:
            print("Invalid command.")

    if cmd == "rest":
        print("You rest and regain 10 health")
        self.health = min(self.health + 10, 150)
    else:
        print("You are at full health.")

    if cmd == "leave":
        if self.location == "The Village of Pithon":
            print("Your curiosity overtakes you and you step outside the village's safe walls and into the darkness before you...")
            self.location = "The Dark Forest"
        elif self.location == "The Dark Cave":
            print("You leave the dark cave and find yourself oddly satisfied with your small adventure. You return to the village elder and tell him of your encounter with a bear, which is then passed down for generations.")
            print("THE END.")
            choice = input("\n Would you like to play again? (y/n): ")
            if choice == "y":
                self .__init__()
                print("\n" + "="*20)
                print("RESTARTING ADVENTURE...")
                print("="*20 + "\n")
            else:
                print("Thanks for playing!")
                exit()

    if cmd == "call":
        if self.location == "The Dark Forest":
            print("Your words bounce off the once bright bark of the alders and into the wild. Nothing returns your call except your own echo...")
        else:
            print("You cannot do that here.")

    if cmd == "investigate cave":
        if self.location == "The Dark Forest":
            print("You wander inside the dark a mouldy cave, cautious of the dangers that await you...")
            self.location = "The Dark Cave"
        elif self.location == "The Dark Cave" and not self.flags["bear_calmed"]:
            print("A large and terrifying Grizzly Bear springs out from the darkness and attacks you!")
            self.flags["bear_attacked"] = True

    if cmd == "go to fountain":
        if self.location == "The Village of Pithon":
            print("You make your way to the fountain in the village square.")
            self.location = "The Fountain of Youth"

    if cmd == "investigate":
        if self.location == "The Dark Forest":
            print("You search the ground and find a healing herb in the shrubs.")
            self.inventory.append("healing herb")
            self.flags["found_herb"] = True
        elif self.location == "The Dark Cave" and not self.flags["bear_calmed"]:
            print("Growls low and threatening ring through the cave. Be cautious.")
        elif self.location == "The Village of Pithon":
            print("The forest noises draw you closer, almost beckoning you to step inside...")
        else:
            print("You may not perform that action right now.")

if __name__ == "__main__":
    game_loop()