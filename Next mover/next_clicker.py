import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui

import lib

dead = False
path = ''
Paused = False
filePath = "path_storage.txt"
shortcut = None
pressed_keys = set()
paths = lib.get_all_paths(filePath)
if len(paths) > 0:
    path = paths[0][0]
pygui.FAILSAFE = False
# Psg.theme('DarkBlue3')
value = lib.extension_remover(path)
if value is bool:
    value = ''
percentage_threshold = 5
location = None
icon = "Next-page-256.ico"
count = 0
window_layout = [
    [Psg.Text('Please select a directory')],
    [Psg.Input(path, key='Path', readonly=True, enable_events=True, text_color='Black'), Psg.FolderBrowse()],
    [Psg.Combo(values=value, expand_x=True, enable_events=True, readonly=True, key='Name', disabled=False,
               background_color='white', text_color='light_blue')],
    [Psg.Text("Selected Image: ", visible=False, key='Image Text'), Psg.Image(key='Image', visible=False)],
    [Psg.Button(enable_events=True, key='Pause', button_text="Pause", disabled=True),
     Psg.Button(key='shortcut', enable_events=True, button_text="Set Pause shortcut",
                tooltip="Press to record a shortcut \nPress Esc to stop recording \nExample: ctrl+q")]
]
width, initial_height = 425, 200
gradient_height = initial_height
background_layout = [[Psg.Canvas(size=(width, gradient_height), background_color='white', key='canvas', pad=(0, 0), expand_y=True)]]
window = Psg.Window('Selection window', window_layout, finalize=True, no_titlebar=False, grab_anywhere=False,
                    transparent_color=Psg.theme_background_color(), icon="Next-page-256.ico", size=(425, 125))
init_x, init_y = window.current_location()
window_background = Psg.Window('Background', background_layout, no_titlebar=True, finalize=True, grab_anywhere=False,
                               margins=(0, 0), element_padding=(0, 0), size=(424, 125+5), location=(init_x + 8, init_y + 25), background_color='white')

x1, y1 = window_background.current_location()
x2, y2 = window.current_location()


# displayText = r'''
#        ___         ___  ___   ___   ___  ___   ___
#   .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.'
# .'  |\|   | .'  |  ___ `.  | |  .'      |   |
# |   | |   | |   |=|_.'  .` |=| `.       |   |
# |   | |  .' |   |  ___ |   | |   |      `.  |
# |___| |.'   |___|=|_.' |___| |___|        `.|
# '''

# os.system("title Next by Luminous_Journey")
# print(lib.color(displayText))


def configure(event):
    global x1, x2, y1, y2
    if not dead:
        try:
            x, y = window.current_location()
            dx, dy = x - x2, y - y2
            x1, y1 = x1 + dx, y1 + dy
            window_background.move(x1, y1)
            x2, y2 = x, y

        except TypeError as e:
            print(f"probably the program closing: {e}")


def toggle():
    global Paused
    Paused = not Paused


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        if key != 'esc' and key not in pressed_keys:
            pressed_keys.add(key)
        if key == 'esc':
            print("unhooking")
            keyboard.unhook(on_key_event)


if lib.extension_remover(path) is []:
    Psg.popup("There are no Valid Files is this directory", title='No Valid files')

window.bring_to_front()
window.make_modal()
window.bind('<FocusIn>', 'FocusIn')
window_background.TKroot.bind('<Configure>', configure)

width, height = window.size
canvas_elem = window_background['canvas']
canvas_widget = canvas_elem.Widget
lib.draw_gradient(canvas_widget, width, height+5)

while True:
    event, values = window.read(timeout=50)
    selected = lib.window_event_handler(window=window, window_background=window_background, file_path=filePath,
                                        Paused=Paused, event=event, values=values)

    if selected == 'exit':
        dead = True
        window_background.TKroot.unbind('<Configure>')
        window_background.close()
        window_background, x2, y2 = None, None, None
        window.close()
        exit()

    if event in 'FocusIn':
        window_background.bring_to_front()
        window.bring_to_front()

    if Paused:
        if selected == 'exit':
            exit('program closed')
        elif not selected:
            toggle()
        continue

    elif selected == '' or selected is False:
        continue

    elif selected is True:
        toggle()
        continue

    elif selected == 'first' or selected == "shortcut":
        window['shortcut'].update(disabled=True)
        print('setting shortcut')
        # window.refresh()
        print('refreshed')
        keyboard.hook(on_key_event)
        keyboard.wait('esc')
        shortcut = '+'.join(pressed_keys)
        if shortcut != '':
            window['shortcut'].update(text=shortcut)
        if selected == 'first' and shortcut != '':
            keyboard.add_hotkey(shortcut, toggle)
        window['shortcut'].update(disabled=False)
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
