from time import sleep, ctime, time
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard
import os

os.system("title Next by Luminous_Journey")

print(f'''       ___         ___  ___   ___   ___  ___   ___ 
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.' 
.'  |\|   | .'  |  ___ `.  | |  .'      |   |      
|   | |   | |   |=|_.'  .` |=| `.       |   |      
|   | |  .' |   |  ___ |   | |   |      `.  |      
|___| |.'   |___|=|_.' |___| |___|        `.|      
''')
psg.theme('Black')
names = ["Asurascans", "Reaperscans", "Cyborg", "Suzeriantrans", "ThatGuyOverThere"]
lst = psg.Combo(names, font=('CC Wild Words', 14),  expand_x=True, enable_events=False,  readonly=False, key='Name')
layout = [[lst], [psg.Button('Ok')]], #psg.Button('Add', key='Add')]]
window = psg.Window('Selection window', layout, size=(250, 100), icon=r"C:\Users\tebre\source\repos\Next mover\Next mover\Group_1.ico")
event, values = window.read()

while True:
    if event == psg.WIN_CLOSED:
        window.close()
        exit("The selection window was closed")
    if event == 'Ok':
        for x in range(0, len(names)):
            if values['Name'] == names[int(x)]:
                next = names[int(x)]
        print("Finding " + next + " next button starting on: " + str(time()) + " aka " + str(ctime()))
        break
    elif event == "Open Folder":
        window['Name'].update(values=names)
        sleep(1)
        


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
            print("(x=" + str(object_x) + ", y=" + str(object_y)+ ") at " + ctime())
    
        if next == names[2]:
            sleep(.5)

        if len(locations[0]) > 0 and pygui.position() == (object_x, object_y) and keyboard.read_key() == 'right':
             pygui.click()
        