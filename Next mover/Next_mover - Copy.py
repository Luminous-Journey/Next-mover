import time as t
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard

psg.theme('Black')
names = ["Asurascans", "Reaperscans", "Cyborg", "Suzeriantrans", "thatguywhosthere"]
lst = psg.Combo(names, font=('CC Wild Words', 14),  expand_x=True, enable_events=True,  readonly=True, key='-COMBO-')
layout = [[lst]]
window = psg.Window('Selection window', layout, size=(250, 100), icon=r"C:\Users\tebre\source\repos\Next mover\Next mover\Group_1.ico")
event, values = window.read()

while True:
    if event == psg.WIN_CLOSED:
        window.close()
        exit("The selection window was closed")
    if values['-COMBO-'] == names[0]:
        next = names[0]
    elif values['-COMBO-'] == names[1]:
        next = names[1]
    elif values['-COMBO-'] == names[2]:
        next = names[2]
    elif values['-COMBO-'] == names[3]:
        next = names[3]
    elif values['-COMBO-'] == names[4]:
        next = names[4]
    print("Finding " + next + " next button starting on: " + str(t.time()) + " aka " + str(t.ctime()))
    break
window.close()
template = np.array(Image.open(r'C:\Users\tebre\source\repos\Next mover\Next mover\templates\\' + next.lower() + 'next.png').convert('L'))

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
            print("(x=" + str(object_x) + ", y=" + str(object_y)+ ") at " + t.ctime())
    
        if next == names[2]:
            t.sleep(.5)

        if len(locations[0]) > 0 and pygui.position() == (object_x, object_y) and keyboard.read_key() == 'right':
             pygui.click()
        