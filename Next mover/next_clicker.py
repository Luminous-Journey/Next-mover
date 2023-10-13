import os

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui

import lib

true = False
selected = ''
Paused = False
filePath = "path_storage.txt"
os.system("title Next by Luminous_Journey")
x = 0
path = ''
shortcut = "ctrl+q"

displayText = r'''
       ___         ___  ___   ___   ___  ___   ___
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.'
.'  |\|   | .'  |  ___ `.  | |  .'      |   |
|   | |   | |   |=|_.'  .` |=| `.       |   |
|   | |  .' |   |  ___ |   | |   |      `.  |
|___| |.'   |___|=|_.' |___| |___|        `.|
'''

print(lib.color(displayText))

paths = lib.get_all_paths(filePath)
if paths:
    path = paths[0][0]

pygui.FAILSAFE = False
Psg.theme('black')

if lib.extension_remover(path) is False:
    value = []
else:
    value = lib.extension_remover(path)

window_layout = [
    [Psg.Text('Please select a directory')],
    [Psg.Input(path, key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'), Psg.FolderBrowse()],
    [Psg.Combo(values=value, expand_x=True, enable_events=True, readonly=True, key='Name', disabled=True)],
    [Psg.Button(enable_events=True, key='Pause', button_text="Pause", button_color='White')]
]

window = Psg.Window('Selection window', window_layout)


def toggle():
    global Paused
    # global x
    Paused = not Paused
    if Paused is False:
        # x = 0
        pass
    # print("Pause state:", Paused)


keyboard.add_hotkey(shortcut, toggle)

if lib.extension_remover(path) is False:
    Psg.popup("There are no Valid Files is this directory", title='No Valid files')

percentage_threshold = 5
location = None

while True:

    selected = lib.window_event_handler(window, filePath, Paused)
    if Paused:
        # x += 1
        # print("waiting(" + f"{x})")
        # sleep(5)
        if selected == 'exit':
            exit('program closed')
        elif not selected:
            toggle()
        continue
    elif not Paused:
        # x = 0
        pass

    # print(selected)
    if selected is None:
        pass
    elif selected:
        toggle()
    elif selected is False:
        pass
    else:
        location = pygui.locateCenterOnScreen(selected, confidence=0.95, grayscale=False, limit=1, minSearchTime=0)
        # print(location)
        if location is None:
            distance = 0
        else:
            distance = lib.euclidean_distance(pygui.position(), location)

        if location is not None and distance > 15:
            pygui.moveTo(location)

        keyboard.add_hotkey("right", lambda: lib.click(distance))
