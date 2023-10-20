import os

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui

import lib

selected = ''
Paused = False
filePath = "path_storage.txt"
x = 0
path = ''
shortcut = 'ctrl+q'
pressed_keys = set()
paths = lib.get_all_paths(filePath)
paths = paths[0][0]
pygui.FAILSAFE = False
Psg.theme('DarkBlue3')
value = lib.extension_remover(paths)
percentage_threshold = 5
location = None
window_layout = [
    [Psg.Text('Please select a directory')],
    [Psg.Input(paths, key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'), Psg.FolderBrowse()],
    [Psg.Combo(values=value, expand_x=True, enable_events=True, readonly=True, key='Name', disabled=False)],
    [Psg.Text("Selected Image: ", visible=False, key='Image Text'), Psg.Image(key='Image',visible=False)],
    [Psg.Button(enable_events=True, key='Pause', button_text="Pause", button_color='White', disabled=True),
     Psg.Button(key='shortcut', enable_events=True, button_text="Set shortcut")]
]
window = Psg.Window('Selection window', window_layout)
displayText = r'''
       ___         ___  ___   ___   ___  ___   ___
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.'
.'  |\|   | .'  |  ___ `.  | |  .'      |   |
|   | |   | |   |=|_.'  .` |=| `.       |   |
|   | |  .' |   |  ___ |   | |   |      `.  |
|___| |.'   |___|=|_.' |___| |___|        `.|
'''

os.system("title Next by Luminous_Journey")
print(lib.color(displayText))


def toggle():
    global Paused
    Paused = not Paused


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        if key != 'esc' and key not in pressed_keys:
            pressed_keys.add(key)


if lib.extension_remover(paths) is []:
    Psg.popup("There are no Valid Files is this directory", title='No Valid files')

keyboard.add_hotkey(shortcut, toggle)

while True:
    selected = lib.window_event_handler(window, filePath, Paused)

    if Paused:
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

    elif selected is True:
        toggle()

    elif selected is False:
        pass

    elif selected == 'exit':
        window.close()
        break

    elif selected == "shortcut":
        popup = Psg.popup_non_blocking("Please enter a shortcut, Example: ctrl+q. Press Escape to stop recording")
        keyboard.hook(on_key_event)
        keyboard.wait('esc')
        # print("Escaped")
        shortcut = '+'.join(pressed_keys)
        # print(shortcut)
        window['shortcut'].update(text=shortcut)
        continue

    else:
        location = pygui.locateCenterOnScreen(selected, confidence=0.95, grayscale=False, limit=1, minSearchTime=0)

        if location is None:
            distance = 0
        else:
            distance = lib.euclidean_distance(pygui.position(), location)

        if location is not None and distance > 15:
            pygui.moveTo(location)

        keyboard.add_hotkey("right", lambda: lib.click(distance))
