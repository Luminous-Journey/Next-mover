from time import sleep, ctime, time
import os
import csv
import PySimpleGUI as psg
import numpy as np
import pyautogui as pygui
import keyboard
import cv2

FILE_PATH = "path_storage.txt"
os.system("title Next by Luminous_Journey")

def get_all_paths():
    paths = []
    try:
        with open(FILE_PATH, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                paths.append(row)
    except FileNotFoundError:
        pass
    return paths

def store_path(path):
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([path])

    print("Path stored successfully.")

def get_image_files_from_directory(path):
    '''parses file path for image files (.png and .jpg)'''
    image_files = []
    try:
        for file in os.listdir(path):
            if file.lower().endswith(('.png', '.jpg')):
                image_files.append(os.path.join(path, file))
    except FileNotFoundError:
        print('No image files (.png or .jpg) found in this directory')
        return []

    if not image_files:
        print('No image files (.png or .jpg) found in this directory')

    return image_files

def color(text):
    '''Adds color to banner'''
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
            faded += (f"\033[38;2;255;{blue};0m{character}\033[0m")
        faded += "\n"
    return faded

def extension_remover(path):
    image_files = get_image_files_from_directory(path)
    names = [os.path.splitext(os.path.basename(file))[0] for file in image_files]
    return names

print(color(r'''
       ___         ___  ___   ___   ___  ___   ___ 
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.' 
.'  |\|   | .'  |  ___ `.  | |  .'      |   |      
|   | |   | |   |=|_.'  .` |=| `.       |   |      
|   | |  .' |   |  ___ |   | |   |      `.  |      
|___| |.'   |___|=|_.' |___| |___|        `.|      
'''))

path = ''
paths = get_all_paths()
if paths:
    path = paths[0][0]

pygui.FAILSAFE = False
selected = None
psg.theme('black')

window_layout = [
    [psg.Text('Please select a directory')],
    [psg.Input(path, key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'), psg.FolderBrowse()],
    [psg.Combo(values=extension_remover(path), expand_x=True, enable_events=True, readonly=True, key='Name')]
]

window = psg.Window('Selection window', window_layout)

KILL_BOOL = False

while True:
    if KILL_BOOL:
        break
    event, values = window.read()
    directory = values['-FOLDER-']
    image_files = get_image_files_from_directory(directory)
    names = extension_remover(directory)
    store_path(directory)
    window['Name'].update(values=names)
    
    if event == psg.WIN_CLOSED:
        window.close()
        KILL_BOOL = True
    elif event == 'Name':
        selected = os.path.join(directory, values['Name'] + '.png')
        window['Name'].update(value=values['Name'])
        print("Finding " + selected + " next button starting on: " + str(time()) + " aka " + str(ctime()))

    template = cv2.imread(selected, cv2.IMREAD_GRAYSCALE)
    screenshot = pygui.screenshot()
    screenshot_np = np.array(screenshot)
    gray_screenshot = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    locations = np.where(cv2.matchTemplate(gray_screenshot, template, cv2.TM_CCOEFF_NORMED) >= 0.9)

    if len(locations[0]) > 0:
        top_left = (locations[1][0], locations[0][0])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        object_x = (top_left[0] + bottom_right[0]) // 2
        object_y = (top_left[1] + bottom_right[1]) // 2

        if pygui.position() != (object_x, object_y):
            pygui.moveTo(object_x, object_y)
            print("(x=" + str(object_x) + ", y=" + str(object_y) + ") at " + ctime())
            if selected.endswith('CyborgTL.png'):
                sleep(.5)

        if len(locations[0]) > 0 and pygui.position() == (object_x, object_y):
            if keyboard.read_key() == 'right':
                pygui.click()

    sleep(0.5)
