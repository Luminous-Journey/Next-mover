from time import sleep, ctime, time
import os
import PySimpleGUI as psg
import numpy as np
from PIL import Image
from skimage.feature import match_template
import pyautogui as pygui
import keyboard
os.system("title Next by Luminous_Journey")
def lIlIIlllllIIl(IIIIllIIIllIlIllll):
    os.system("")
    IlIIIIlll = ""
    for lIlIIIIIIIIIIIlIlI in IIIIllIIIllIlIllll.splitlines():
        IIIllllIlIIII = 250
        IIlIllIlI = 250
        for lllIIlIIIIIII in lIlIIIIIIIIIIIlIlI:
            IIIllllIlIIII -= 5
            IIlIllIlI -= 5
            IIIllllIlIIII = max(IIIllllIlIIII, 0)
            IIlIllIlI = max(IIlIllIlI, 0)
            IlIIIIlll += (f"\033[38;2;255;{IIlIllIlI};0m{lllIIlIIIIIII}\033[0m")
        IlIIIIlll += "\n"
    return IlIIIIlll
print(lIlIIlllllIIl(r'''
       ___         ___  ___   ___   ___  ___   ___ 
  .'| |   |   .'|=|_.' |   | |   | `._|=|   |=|_.' 
.'  |\|   | .'  |  ___ `.  | |  .'      |   |      
|   | |   | |   |=|_.'  .` |=| `.       |   |      
|   | |  .' |   |  ___ |   | |   |      `.  |      
|___| |.'   |___|=|_.' |___| |___|        `.|      
'''))
def IlIlIIlIl(lllllllIllIIIIllllI):
    llIIlllIIIllIIll = []
    for IIllllllIl in os.listdir(lllllllIllIIIIllllI):
        if IIllllllIl.lower().endswith('.png'):
            llIIlllIIIllIIll.append(os.lllllllIllIIIIllllI.join(lllllllIllIIIIllllI, IIllllllIl))
    return llIIlllIIIllIIll
psg.theme('Black')
psg.set_options(font=('Times New Roman', 14))
IlllIlIlll = psg.Combo([], expand_x=True, enable_events=True, readonly=True, key='Name')
IIIIlIllIIIllI = [
    [psg.Text('Please select a directory')],
    [psg.Input(key='-FOLDER-', readonly=True, enable_events=True, text_color='Black'),
     psg.FolderBrowse()], [IlllIlIlll]
]
IllIIIlIllIlIllI = psg.Window('Selection window', IIIIlIllIIIllI)
lIllIlIIIlIlIllIlIlI = False
while True:
    IIllllIlIllIIIlI, IIIlIIIIll = IllIIIlIllIlIllI.read()
    if IIllllIlIllIIIlI == psg.WIN_CLOSED:
        IllIIIlIllIlIllI.close()
        lIllIlIIIlIlIllIlIlI = True
    elif IIllllIlIllIIIlI == "-FOLDER-":
        IIIIlIIl = IIIlIIIIll['-FOLDER-'] + "//"
        IIlIlIlIIlllIIlIII = IlIlIIlIl(IIIIlIIl)
        llllIIllIllIIll = [llllIIllIIl.replace(IIIIlIIl, '') for llllIIllIIl in IIlIlIlIIlllIIlIII]
        llllIIllIllIIll = [llllIIllIIl.replace('.png', '') for llllIIllIIl in llllIIllIllIIll]
        IllIIIlIllIlIllI['Name'].update(IIIlIIIIll=llllIIllIllIIll)
    elif IIllllIlIllIIIlI == 'Name':
        for IIIIIIlIllI in range(0, len(llllIIllIllIIll)):
            if IIIlIIIIll['Name'] == llllIIllIllIIll[int(IIIIIIlIllI)]:
                llllIlIllI = IIlIlIlIIlllIIlIII[int(IIIIIIlIllI)]
        print("Finding "+llllIlIllI+" next button starting on: "+str(time())+" aka "+str(ctime()))
        break
    if lIllIlIIIlIlIllIlIlI:
        break
IllIIIlIllIlIllI.close()
if  not lIllIlIIIlIlIllIlIlI:
    IIlllIIIlllIllII = np.array(Image.open(llllIlIllI).convert('L'))
while True:
    if lIllIlIIIlIlIllIlIlI:
        break
    IIllIIllIIl = np.array(pygui.screenshot().convert('L'))
    IIIIllIlllIIIIIll = match_template(IIllIIllIIl, IIlllIIIlllIllII)
    llllIIlllllllIlII = np.where(IIIIllIlllIIIIIll >= 0.9)
    if len(llllIIlllllllIlII[0]) > 0:
        IllIlIIIIIlllIllI = (llllIIlllllllIlII[1][0], llllIIlllllllIlII[0][0])
        lIIlIlIl = (IllIlIIIIIlllIllI[0] + IIlllIIIlllIllII.shape[1], IllIlIIIIIlllIllI[1] + IIlllIIIlllIllII.shape[0])
        IIllllIlllllIllllI = (IllIlIIIIIlllIllI[0] + lIIlIlIl[0]) // 2
        lllIlIllllll = (IllIlIIIIIlllIllI[1] + lIIlIlIl[1]) // 2
        if pygui.position() != (IIllllIlllllIllllI, lllIlIllllll):
            pygui.moveTo(IIllllIlllllIllllI, lllIlIllllll)
            print("(x=" + str(IIllllIlllllIllllI) + ", y=" + str(lllIlIllllll)+ ") at " + ctime())
            if llllIlIllI == IIlIlIlIIlllIIlIII[2]:
                sleep(.5)
        if len(llllIIlllllllIlII[0])>0 and pygui.position()==(IIllllIlllllIllllI,lllIlIllllll):
            if keyboard.read_key()=='right':
                pygui.click()