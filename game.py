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
          if answer in ["y", "yes"]:
            print("The figure moves aside for you to sit with them")
            print("I don't expect you to stay long, they never do... But thank you for staying longer than most.")
            print("I must warn you, there are dangerous entities from the north, you should be wary on your travels... To the east, there is an inn you can stay in {self.name}.")
            return True            
          elif answer in ["n", "no"]:
             print("That is alright, I wouldn't have expected such a weary soul such as yourself to accept such offers...")
             print("But I must warn you... There are hostile entities around here, to the north. There is an inn to the east you can stay in.")
             return False
          else:
            print("Sorry, can you repeat that?")


player = Player()
player.intro()

