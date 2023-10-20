import os

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui

import lib

path = ''
Paused = False
filePath = "path_storage.txt"
shortcut = None
pressed_keys = set()
paths = lib.get_all_paths(filePath)
if paths is list:
    path = paths[0][0]
pygui.FAILSAFE = False
Psg.theme('DarkBlue3')
value = lib.extension_remover(path)
if value is bool:
    value = ''
percentage_threshold = 5
location = None
window_layout = [
    [Psg.Text('Please select a directory')],
    [Psg.Input(path, key='Path', readonly=True, enable_events=True, text_color='Black'),
     Psg.FolderBrowse(tooltip="Select a folder to choose from", key='-FOLDER-'),],
    [Psg.Combo(values=value, expand_x=True, enable_events=True, readonly=True, key='Name', disabled=False)],
    [Psg.Text("Selected Image: ", visible=False, key='Image Text'), Psg.Image(key='Image', visible=False)],
    [Psg.Button(enable_events=True, key='Pause', button_text="Pause", disabled=False),
     Psg.Button(key='shortcut', enable_events=True, button_text="Set shortcut")]
]
popup_layout = [
    [Psg.Text("Please enter a shortcut, Example: ctrl+q. Press Escape to stop recording")],
    [Psg.Text()]

]
window = Psg.Window('Selection window', window_layout)
popup = Psg.Window("Popup", popup_layout)
displayText = r'''
       ___         ___  ___   ___   ___  ___   ___
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.'
.'  |\|   | .'  |  ___ `.  | |  .'      |   |
|   | |   | |   |=|_.'  .` |=| `.       |   |
|   | |  .' |   |  ___ |   | |   |      `.  |
|___| |.'   |___|=|_.' |___| |___|        `.|
'''

# os.system("title Next by Luminous_Journey")
# print(lib.color(displayText))


def toggle():
    global Paused
    Paused = not Paused


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        if key != 'esc' and key not in pressed_keys:
            pressed_keys.add(key)


if lib.extension_remover(path) is []:
    Psg.popup("There are no Valid Files is this directory", title='No Valid files')

while True:
    selected = lib.window_event_handler(window, filePath, Paused)

    if Paused:
        if selected == 'exit':
            exit('program closed')
        elif not selected:
            toggle()
        continue

    # print(selected)
    if selected == '' or selected is False:
        continue

    elif selected is True:
        toggle()
        continue

    elif selected == 'exit':
        window.close()
        break

    elif selected == 'first' or selected == "shortcut":
        popup.read(timeout=25)
        keyboard.hook(on_key_event)
        keyboard.wait('esc')
        shortcut = '+'.join(pressed_keys)
        if shortcut != '':
            window['shortcut'].update(text=shortcut)
        if selected == 'first' and shortcut != '':
            keyboard.add_hotkey(shortcut, toggle)
        popup.close()
        continue

    else:
        location = pygui.locateCenterOnScreen(selected, confidence=0.99, grayscale=False, limit=1, minSearchTime=0)

        if location is None:
            distance = 0
        else:
            distance = lib.euclidean_distance(pygui.position(), location)

        if location is not None and distance > 15:
            pygui.moveTo(location)

        keyboard.add_hotkey("right", lambda: lib.click(distance))
