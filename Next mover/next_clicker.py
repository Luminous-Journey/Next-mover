'''moves my mouse and clicks for me'''
from time import sleep, ctime, time
import os
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard


os.system("title Next by Luminous_Journey")
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

psg.theme('Black')
psg.set_options(font=('Times New Roman', 14))
lst = psg.Combo([], expand_x=True, enable_events=True, readonly=True, key='Name')
layout = [
    [psg.Text('Please select a directory')],
    [psg.Input(key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'),
     psg.FolderBrowse()], [lst]
]

window = psg.Window('Selection window', layout)
KILL_BOOL = False
while True:
    event, values = window.read()

    if event == psg.WIN_CLOSED:
        window.close()
        KILL_BOOL = True
    elif event == "-FOLDER-":
        directory = values['-FOLDER-'] + "/"
        png_list = get_png_files_from_directory(directory)
        names = [sub.replace(directory, '') for sub in png_list]
        names = [sub.replace('.png', '') for sub in names]
        window['Name'].update(values=names)
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
res = 0.9
if selected == 'C:/Users/tebre/source/repos/Next mover/Next mover/templates/SalmonLatte.png':
        res = 1
        print(res)
while True:
    if KILL_BOOL:
        break
    image = np.array(pygui.screenshot().convert('L'))
    result = match_template(image, template)
    
    locations = np.where(result >= res)
    if len(locations[0]) > 0:
        top_left = (locations[1][0], locations[0][0])
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])

        object_x = (top_left[0] + bottom_right[0]) // 2
        object_y = (top_left[1] + bottom_right[1]) // 2

        if pygui.position() != (object_x, object_y):
            pygui.moveTo(object_x, object_y)
            print("(x=" + str(object_x) + ", y=" + str(object_y)+ ") at " + ctime())
            if selected == png_list[2]:
                sleep(.5)

        if len(locations[0])>0 and pygui.position()==(object_x,object_y):
            if keyboard.read_key()=='right':
                pygui.click()
