import os
import json
import time
import random
import rich

class Player:
    def __init__(self):
        self.name = input("Lost one.. Do you have a name? ").strip().title()
        self.health = 100
    def intro(self):
        print(f"What a wonderful name... {self.name}.")
        self.backstory = input("Where did you come from? Not often we have visitors here in the void...")
        print(f"Ah... {self.backstory}, I am yet to visit... But it is much beautiful from what I have heard")
        print(f"You must have came such a long way from {self.backstory}...")
        while True:
          print(f"You surely much be tired after such a journey...")
          answer = input("Please come sit with me?: ").strip().lower()
          if answer in ["y", "yes", "Yeah", "Yes", "sure", "yeah" "Sure", "Of course", "ofcourse"]:
            print("The figure moves aside for you to sit with them")
            print("I don't expect you to stay long, they never do... But thank you for staying longer than most.")
            print("I must warn you, there are dangerous entities from the north, you should be wary on your travels... To the east, there is an inn you can stay in {self.name}.")
            return True            
          elif answer in ["n", "no", "No", "Nah", "nah", "Nope", "nope"]:
             print("That is alright, I wouldn't have expected such a weary soul such as yourself to accept such offers...")
             print("But I must warn you... There are hostile entities around here, to the north. There is an inn to the east you can stay in.")
             return False
          else:
            print("Sorry, can you repeat that?")

#after intro

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

def battle(player, enemy):
    print(f"\nA {enemy.name} wanders out from the shadows")
    while player.health > 0 and enemy.health > 0:
        input("Press Enter to strike...")
        damage = random.randint(10, 20)
        enemy.health -= damage
        print(f"You hit the {enemy.name} for {damage} damage. Enemy HP: {enemy.health}")

        if enemy.health <= 0:
            print(f"The {enemy.name} dissapears into the darkness...")
            return

        enemy_damage = random.randint(5, enemy.attack)
        player.health -= enemy_damage
        print(f"The {enemy.name} lashes out for {enemy_damage} damage. Your HP: {player.health}")

        if player.health <= 0:
            print("You have been felled... The {enemy.name} takes its victory.")
            exit()

def direction(player):
    print("You give your thanks to the figure, and continue on the trail")
    print("~---------~")
    print("North\nNortheast\nEast\nSoutheast\nSouth\nSouthwest\nWest\nNorthwest")
    print("~---------~")
    choice = input("Where to now? ").strip().lower()

    directions = {
        "north", "North", "N", "n", "NORTH": "You head northwards",
        "northeast", "Northeast", "NE" "ne", "NORTHEAST": "You head Northeast",
        "east", "East" "E" "e", "EAST": "You head Eastwards",
        "southeast", "Southeast" "SE" "se", "SOUTHEAST": "You head Southeast",
        "south", "South" "S" "s", "SOUTH": "You head Southwards",
        "southwest", "Southwest" "SW" "sw", "SOUTHWEST": "You head Southwest",
        "west", "West", "w" "W", "WEST": "You head Westwards",
        "northwest", "NW", "nw", "Northwest", "NORTHWEST": "You head Northwest"
    }

    if choice in directions:
        print(directions[choice])
        # Random encounter chance
        if random.random() < 0.5:
            enemy_pool = [
                Enemy("Shadow", 40, 15),
                Enemy("Silloete", 60, 20),
                Enemy("Figure", 30, 10)
            ]
            enemy = random.choice(enemy_pool)
            battle(player, enemy)
        else:
            print("The ground has gone silent...")
    else:
        print("That is not a valid direction...")

#gamestufflolz
player = Player()
player.intro()
while True:
    direction(player)
