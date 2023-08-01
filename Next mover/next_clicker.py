'''moves my mouse and clicks for me'''
from time import sleep, ctime, time
import os
import csv
from tkinter import BOTTOM
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard

FILE_PATH = r"path_storage.txt"
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
    # Wipe the previous content and write the new path
    with open(FILE_PATH, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([path])

    print("Path stored successfully.")

def get_png_files_from_directory(path):
    '''parses file path for files'''
    png_files = []
    try:
        for file in os.listdir(path):
            if file.lower().endswith(('.png', '.jpg')):
                png_files.append(os.path.join(path, file))
    except FileNotFoundError:
        # Handle the case when the path is not found
        print('No .png files found in this directory, please select a different directory')
        return []
    
    if not png_files:
        print('No .png files found in this directory, please select a different directory')
    
    return png_files

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
 
def extension_remover(path):
    png_list = get_png_files_from_directory(path) 
    names = [sub.replace(path, '') for sub in png_list]
    names = [sub.replace('.png', '') for sub in names]
    names = [sub.replace('.jpg', '') for sub in names]
    names = [sub.replace('\\','') for sub in names]
    return names

psg.theme('Black')
psg.set_options(font=('Times New Roman', 14))
lst = psg.Combo(values=extension_remover(path), expand_x=True, enable_events=True, readonly=True, key='Name')  # Use values=extension_remover(path)  # Use values=extension_remover() here
layout = [
    [psg.Text('Please select a directory')],
    [psg.Input(path ,key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'),
     psg.FolderBrowse()], [lst]
]

window = psg.Window('Selection window', layout)
KILL_BOOL = False
while True:
    event, values = window.read()
    directory = values['-FOLDER-'] + "/"
    png_list = get_png_files_from_directory(directory)
    names = extension_remover(png_list)
    store_path(directory)
    window['Name'].update(values=names)

    if event == psg.WIN_CLOSED:
        window.close()
        KILL_BOOL = True
    elif event == 'Name':
        for x in range(0, len(names)):
            if values['Name'] == names[int(x)]:
                selected = png_list[int(x)]
        print("Finding "+selected+" next button starting on: "+str(time())+" aka "+str(ctime()))
        break
    if KILL_BOOL:
        break
window.close()

if  not KILL_BOOL:
    template = np.array(Image.open(selected).convert('L'))

del selected, path, paths, x, names, png_list, directory, event, values, window, layout, lst
object_x = None
object_y = None
top_left = None
bottom_right = None
result = None
while True:
    if KILL_BOOL:
        break
    image = np.array(pygui.screenshot().convert('L'))
    result = match_template(image, template)
    
    locations = np.where(result >= 0.9)
    if len(locations[0]) > 0:
        top_left = (locations[1][0], locations[0][0])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])

        object_x = (top_left[0] + bottom_right[0]) // 2
        object_y = (top_left[1] + bottom_right[1]) // 2

        if pygui.position() != (object_x, object_y):
            pygui.moveTo(object_x, object_y)
            print("(x=" + str(object_x) + ", y=" + str(object_y)+ ") at " + ctime())
            if selected == r"C:\Users\tebre\source\repos\Next mover\Next mover\templates\CyborgTL.png":
                sleep(.5)

        if len(locations[0])>0 and pygui.position()==(object_x,object_y):
            if keyboard.read_key()=='right':
                pygui.click()

    del image, result, object_x, object_y, top_left, bottom_right, locations, result
