from time import sleep, ctime, time
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard
import os
os.system("title Next by Luminous_Journey")
print(f'''
       ___         ___  ___   ___   ___  ___   ___ 
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.' 
.'  |\|   | .'  |  ___ `.  | |  .'      |   |      
|   | |   | |   |=|_.'  .` |=| `.       |   |      
|   | |  .' |   |  ___ |   | |   |      `.  |      
|___| |.'   |___|=|_.' |___| |___|        `.|      
''')
def llIlIIIIlIIIll(IllIIlIIlIlIlIlllI):
    llIlIIllIllIII = []
    for lIIlIIIlllIIIll in os.listdir(IllIIlIIlIlIlIlllI):
        if lIIlIIIlllIIIll.lower().endswith('.png'):
            llIlIIllIllIII.append(os.path.join(IllIIlIIlIlIlIlllI, lIIlIIIlllIIIll))
    return llIlIIllIllIII
IIIIIllllIlIllIllIll = psg.Combo([], font=('CC Wild Words', 14), expand_x=True, enable_events=True, readonly=True, key='Name')
IIIIlIIIlIIIlIlIl = [
    [psg.Input(key='-FOLDER-'), psg.FolderBrowse()], 
    [IIIIIllllIlIllIllIll], 
    [psg.Button('Open Folder'), psg.Button('Okay')]
]
lIIlllIllIIlIllI = psg.Window('Selection window', IIIIlIIIlIIIlIlIl)
while True:
    IlIllIlIIIIlllIIl, IIlIllIIIlI = lIIlllIllIIlIllI.read()
    if IlIllIlIIIIlllIIl == psg.WIN_CLOSED:
        lIIlllIllIIlIllI.close()
        exit("The selection window was closed")
    elif IlIllIlIIIIlllIIl == "Open Folder":
        IllIIlIIlIlIlIlllI = IIlIllIIIlI['-FOLDER-'] + "//"
        llIlIIllIllIII = llIlIIIIlIIIll(IllIIlIIlIlIlIlllI)
        lIIIIIIllIII = [IIIllIlIlIIIIll.replace(IllIIlIIlIlIlIlllI, '') for IIIllIlIlIIIIll in llIlIIllIllIII]
        lIIIIIIllIII = [IIIllIlIlIIIIll.replace('.png', '') for IIIllIlIlIIIIll in lIIIIIIllIII]
        lIIlllIllIIlIllI['Name'].update(IIlIllIIIlI=lIIIIIIllIII)
    elif IlIllIlIIIIlllIIl == 'Okay':
        for lIIllIllllllIIlllIIl in range(0, len(lIIIIIIllIII)):
            if IIlIllIIIlI['Name'] == lIIIIIIllIII[int(lIIllIllllllIIlllIIl)]:
                IIIlIIIlIlII = llIlIIllIllIII[int(lIIllIllllllIIlllIIl)]
        print("Finding " + IIIlIIIlIlII + " next button starting on: " + str(time()) + " aka " + str(ctime()))
        break
lIIlllIllIIlIllI.close()
lIllllIIlIllIllIIII = np.array(Image.open(IIIlIIIlIlII).convert('L'))
while True:
    llIllIlll = np.array(pygui.screenshot().convert('L'))
    IllIllIIlIIIIIlllIII = match_template(llIllIlll, lIllllIIlIllIllIIII)
    lIlIIIIIllIlIIIlIlI = np.where(IllIllIIlIIIIIlllIII >= 0.9)
    if len(lIlIIIIIllIlIIIlIlI[0]) > 0:
        lIlIIlIIlIlI = (lIlIIIIIllIlIIIlIlI[1][0], lIlIIIIIllIlIIIlIlI[0][0])
        IlIllIlIlllIIII = (lIlIIlIIlIlI[0] + lIllllIIlIllIllIIII.shape[1], lIlIIlIIlIlI[1] + lIllllIIlIllIllIIII.shape[0])
        lIIIIlIIllllIIl = (lIlIIlIIlIlI[0] + IlIllIlIlllIIII[0]) // 2
        lIllIlIlIIllIll = (lIlIIlIIlIlI[1] + IlIllIlIlllIIII[1]) // 2
        if pygui.position() != (lIIIIlIIllllIIl, lIllIlIlIIllIll):
            pygui.moveTo(lIIIIlIIllllIIl, lIllIlIlIIllIll)
            print("(x=" + str(lIIIIlIIllllIIl) + ", y=" + str(lIllIlIlIIllIll)+ ") at " + ctime())
        if IIIlIIIlIlII == llIlIIllIllIII[2]:
            sleep(.5)
        if len(lIlIIIIIllIlIIIlIlI[0]) > 0 and pygui.position() == (lIIIIlIIllllIIl, lIllIlIlIIllIll) and keyboard.read_key() == 'right':
             pygui.click()