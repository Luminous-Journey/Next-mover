import csv
import math
import os
from time import sleep, time, ctime

import PySimpleGUI as Psg
import keyboard
import pyautogui as pygui
from PIL import Image, ImageDraw
import io

selected = ''
Paused = False
pressed_keys = set()
first = True


def on_key_event(e):
    if e.event_type == keyboard.KEY_DOWN:
        key = e.name
        if key != 'esc' and key not in pressed_keys:
            pressed_keys.add(key)


def get_all_paths(filePath):
    paths_to_get = []
    try:
        with open(filePath, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                paths_to_get.append(row)
    except FileNotFoundError:
        pass
    return paths_to_get


def store_path(path_to_store, file_path):
    if extension_remover(path_to_store) != '':
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([path_to_store])
    print("Path stored successfully.")


def create_rounded_gradient(width, height, corner_radius):
    gradient = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(gradient)

    # Create the gradient
    for y in range(height):
        r = int(194 - (194 - 32) * ((height - y) / height))  # Red component
        g = int(36 + (107 - 36) * ((height - y) / height))  # Green component
        b = int(255 - (255 - 191) * ((height - y) / height))  # Blue component
        color = (r, g, b)
        draw.line([(0, y), (width, y)], fill=color)

    # Create the mask for rounded corners
    mask = Image.new("L", (width, height), 255)
    draw_mask = ImageDraw.Draw(mask)

    x0, y0 = 0, height - 2 * corner_radius
    x1, y1 = 2 * corner_radius, height

    draw_mask.rectangle((0, 0, width, height), fill=0)
    draw_mask.pieslice((x0, y0, x1, y1), 90, 180, fill=255)

    x0, y0 = width - 2 * corner_radius, height - 2 * corner_radius
    x1, y1 = width, height

    draw_mask.pieslice((x0, y0, x1, y1), 0, 90, fill=255)
    draw_mask.rectangle((8, 0, width-corner_radius, y1), fill=255)
    draw_mask.rectangle((0, 0, width, height-corner_radius), fill=255)

    gradient.putalpha(mask)
    return gradient


def window_event_handler(window, window_background, file_path, Paused, event, values):
    global selected
    global first

    if selected is None:
        selected = ''
        return selected
    elif not os.path.isfile(selected):
        selected = ''


    if event == Psg.WIN_CLOSED:
        return 'exit'

    directory = values['Path']

    if extension_remover(directory) != '':
        window['Name'].update(values=extension_remover(directory))
        window['Name'].update(value=values['Name'])

    if event == 'Path':
        store_path(directory, file_path)
        print("Stored")
        if extension_remover(directory) == '':
            Psg.popup("There are no Valid Files is this directory", title='No Valid files')

    elif event == 'shortcut':
        return "shortcut"

    elif event == 'trigger':
        return "trigger"

    elif event == 'Name':
        image_name = values['Name'] + '.png'
        selected = os.path.join(directory, image_name)
        print(directory)
        window['Pause'].update(disabled=False)
        original_image = Image.open(selected)
        new_width = int(original_image.width * 1.025)
        new_height = int(original_image.height * 1.025)
        resized_image = original_image.resize((new_width, new_height), Image.BILINEAR)
        resized_image_array = io.BytesIO()
        resized_image.save(resized_image_array, format='PNG')
        img_bytes = resized_image_array.getvalue()
        width, height = 425, new_height+130
        rounded_gradient = create_rounded_gradient(width, height+5, 8)
        gradient_data = io.BytesIO()
        rounded_gradient.save(gradient_data, format="PNG")
        gradient_data.seek(0)
        window_background['canvas'].update(data=gradient_data.read())
        window.size = (425, 130 + new_height)
        window_background.size = width, height + 5
        window['Image Text'].update(visible=True)
        window['Image'].update(data=img_bytes, visible=True)
        window['Name'].update(value=values['Name'])
        if not os.path.isfile(selected):
            print(f"Invalid file path: {selected}")
        else:
            print("Finding " + selected + " next button starting on: " + str(time()) + " aka " + str(ctime()))
            if selected != '':
                return selected

    if event == 'Pause':
        if Paused == False:
            Paused = True
            return Paused

        elif Paused == True:
            Paused = not Paused
            return Paused

    if Paused is False:
        window['Pause'].update(button_color=Psg.theme_button_color())


    elif Paused is True:
        window['Pause'].update(button_color=('#283b5b', "White"))


    return selected


def get_image_files_from_directory(path):
    global true
    image_files = []
    try:
        for file in os.listdir(path):
            if file.lower().endswith(('.png', '.jpg')):
                image_files.append(os.path.join(path, file))
        return image_files
    except FileNotFoundError:
        pass


    if not image_files:
        pass

    return image_files


def extension_remover(path):
    image_files = get_image_files_from_directory(path)
    names = [os.path.splitext(os.path.basename(file))[0] for file in image_files]
    if names:
        return names
    else:
        return ''


def color(text):
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
            faded += f"\033[38;2;255;{blue};0m{character}\033[0m"
        faded += "\n"
    return faded


def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def click(distance):
    if distance <= 15 and keyboard.is_pressed("right"):
        try:
            pygui.click()
            sleep(0.5)

        except Exception as e:
            print(f"An exception has occurred: {e}")

