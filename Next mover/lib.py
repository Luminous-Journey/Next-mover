import csv
import math
import os
from time import sleep, time, ctime

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui
from PIL import Image
import io

selected = ''
Paused = False
pressed_keys = set()
first = True


def adjust_transparency(image, alpha):
    image = image.convert("RGBA")
    new_image = Image.new("RGBA", image.size)
    for x in range(image.width):
        for y in range(image.height):
            r, g, b, a = image.getpixel((x, y))
            new_image.putpixel((x, y), (r, g, b, int(alpha * a)))
    return new_image


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        if key != 'esc' and key not in pressed_keys:
            pressed_keys.add(key)


def get_all_paths(filePath):
    paths_to_get = []
    try:
        with open(filePath, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                paths_to_get.append(row)
    except FileNotFoundError:
        pass
    return paths_to_get


def store_path(path_to_store, file_path):
    if extension_remover(path_to_store) != '':
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([path_to_store])
    print("Path stored successfully.")


def window_event_handler(window, file_path, Paused, event, values):
    global selected
    global first

    if selected is None:
        selected = ''
        return selected

    if event == Psg.WIN_CLOSED:
        return 'exit'

    directory = values['Path']

    if extension_remover(directory) != '':
        window['Name'].update(values=extension_remover(directory))
        window['Name'].update(value=values['Name'])

    if event == 'Path':
        store_path(directory, file_path)
        print("Stored")
        if extension_remover(directory) == '':
            Psg.popup("There are no Valid Files is this directory", title='No Valid files')

    elif event == 'shortcut':
        if first:
            first = not first
            return "first"
        return "shortcut"

    elif event == 'Name':
        image_name = values['Name'] + '.png'
        selected = os.path.join(directory, image_name)
        print(directory)
        window['Pause'].update(disabled=False)
        original_image = Image.open(selected)
        new_width = int(original_image.width * 1.025)
        new_height = int(original_image.height * 1.025)
        resized_image = original_image.resize((new_width, new_height), Image.BILINEAR)
        img_byte_array = io.BytesIO()
        resized_image.save(img_byte_array, format='PNG')
        img_bytes = img_byte_array.getvalue()
        window['Image Text'].update(visible=True)
        window['Image'].update(data=img_bytes, visible=True)
        window['Name'].update(value=values['Name'])
        if not os.path.isfile(selected):
            print(f"Invalid file path: {selected}")
        else:
            print("Finding " + selected + " next button starting on: " + str(time()) + " aka " + str(ctime()))
            if selected != '':
                return selected

    if event == 'Pause':
        if Paused == False:
            Paused = True
            return Paused

        elif Paused == True:
            Paused = not Paused
            return Paused

    if Paused is False:
        window['Pause'].update(button_color=Psg.theme_button_color())


    elif Paused is True:
        window['Pause'].update(button_color=('#283b5b', "White"))


    return selected


def get_image_files_from_directory(path):
    global true
    image_files = []
    try:
        for file in os.listdir(path):
            if file.lower().endswith(('.png', '.jpg')):
                image_files.append(os.path.join(path, file))
        return image_files
    except FileNotFoundError:
        pass


    if not image_files:
        pass

    return image_files


def extension_remover(path):
    image_files = get_image_files_from_directory(path)
    names = [os.path.splitext(os.path.basename(file))[0] for file in image_files]
    if names:
        return names
    else:
        return ''


def color(text):
    os.system("")
    faded = ""
    for line in text.splitlines():
        green = 250
        blue = 250
        for character in line:
            green -= 5
            blue -= 5
            green = max(green, 0)
            blue = max(blue, 0)
            faded += f"\033[38;2;255;{blue};0m{character}\033[0m"
        faded += "\n"
    return faded


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def click(distance):
    if distance <= 15 and keyboard.is_pressed("right"):
        try:
            pygui.click()
            sleep(0.5)

        except Exception as e:
            print(f"An exception has occurred: {e}")


