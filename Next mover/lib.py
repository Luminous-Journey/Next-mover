import csv
import math
import os
from time import sleep, time, ctime

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui

true = False
selected = ''
Paused = False


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


def store_path(path_to_store, filePath):
    if extension_remover(path_to_store) is not False:
        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([path_to_store])
    print("Path stored successfully.")


def window_event_handler(window, filePath, Paused):
    global selected
    if selected is None:
        selected = ''
    event, values = window.read(timeout=50)
    if event == Psg.WIN_CLOSED:
        window.close()
        selected = 'exit'
        return selected
        # exit('program closed')
    directory = values['-FOLDER-']
    # image_files = get_image_files_from_directory(directory)
    names = extension_remover(directory)

    if extension_remover(directory) is not False:
        window['Name'].update(values=names)

    if event == '-FOLDER-':
        store_path(directory, filePath)
        if extension_remover(directory) is False:
            Psg.popup("There are no Valid Files is this directory", title='No Valid files')

    elif event == 'Name':
        image_name = values['Name'] + '.png'
        selected = os.path.join(directory, image_name)
        if not os.path.isfile(selected):
            print(f"Invalid file path: {selected}")
        else:
            print("Finding " + selected + " next button starting on: " + str(time()) + " aka " + str(ctime()))

    elif event == 'Pause':
        if Paused == False:
            Paused = True
            window['Pause'].update(button_color='Gray')
            window['Name'].update(value=values['Name'])
            window['Name'].update(disabled=True)
            return Paused
        elif Paused == True:
            Paused = not Paused
            window['Pause'].update(button_color='White')
            window['Name'].update(value=values['Name'])
            window['Name'].update(disabled=False)
            return Paused

    window['Name'].update(value=values['Name'])

    if selected != '':
        return selected


def get_image_files_from_directory(path):
    global true
    image_files = []
    try:
        for file in os.listdir(path):
            if file.lower().endswith(('.png', '.jpg')):
                image_files.append(os.path.join(path, file))
    except FileNotFoundError:
        if not true:
            print('Error: No image files (.png or .jpg) found in this directory')
            true = not true

    if not image_files:
        pass

    return image_files


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


def extension_remover(path):
    image_files = get_image_files_from_directory(path)
    names = [os.path.splitext(os.path.basename(file))[0] for file in image_files]
    if names:
        return names
    else:
        return False


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def click(distance):
    if distance <= 15 and keyboard.is_pressed("right"):
        try:
            pygui.click()
            sleep(0.5)

        except Exception as e:
            print(f"An exception has occurred: {e}")
