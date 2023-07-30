from time import sleep, ctime, time
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard
import os

os.system("title Next by Luminous_Journey")
def color(text):
    os.system(""); faded = ""
    for line in text.splitlines():
        green = 250
        blue = 250
        for character in line:
            green -= 5
            blue -= 5
            if green < 0:
                green = 0
            if blue < 0:
                blue = 0 
            faded += (f"\033[38;2;255;{blue};0m{character}\033[0m")
        faded += "\n"
    return faded

print(color(f'''
       ___         ___  ___   ___   ___  ___   ___ 
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.' 
.'  |\|   | .'  |  ___ `.  | |  .'      |   |      
|   | |   | |   |=|_.'  .` |=| `.       |   |      
|   | |  .' |   |  ___ |   | |   |      `.  |      
|___| |.'   |___|=|_.' |___| |___|        `.|      
'''))

def get_png_files_from_directory(directory):
    png_files = []
    for file in os.listdir(directory):
        if file.lower().endswith('.png'):
            png_files.append(os.path.join(directory, file))
    return png_files

psg.theme('Black')
lst = psg.Combo([], font=('CC Wild Words', 14), expand_x=True, enable_events=True, readonly=True, key='Name')
layout = [
    [psg.Text('Please select a directory')],
    [psg.Input(key='-FOLDER-', readonly=True, enable_events=True), psg.FolderBrowse()], 
    [lst], 
]

window = psg.Window('Selection window', layout)

while True:
    event, values = window.read()

    if event == psg.WIN_CLOSED:
        window.close()
        exit("The selection window was closed")
    elif event == "-FOLDER-":
        directory = values['-FOLDER-'] + "//"
        png_files = get_png_files_from_directory(directory)
        names = [sub.replace(directory, '') for sub in png_files]
        names = [sub.replace('.png', '') for sub in names]
        window['Name'].update(values=names)
        
    elif event == 'Name':
        for x in range(0, len(names)):
            if values['Name'] == names[int(x)]:
                next = png_files[int(x)]

        print("Finding " + next + " next button starting on: " + str(time()) + " aka " + str(ctime()))
        break
        

window.close()
template = np.array(Image.open(next).convert('L'))

while True:
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
    
        if next == png_files[2]:
            sleep(.5)

        if len(locations[0]) > 0 and pygui.position() == (object_x, object_y) and keyboard.read_key() == 'right':
             pygui.click()
        
