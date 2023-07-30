import time as lIIIlIIlIlIlIlI
import PySimpleGUI as IIIIlIIlIlIIIlI
import numpy as IIIIlIIlIlIIIll
from PIL import Image as lIlIlIIlIlIlIlI
from skimage.feature import match_template as IIlIlIIlIlIlIlI
import pyautogui as llIIlIIlIlIIIlI
import keyboard as llIIlIIlIlIlIlI
IIIIlIIlIlIIIlI.theme('Black')
lIIIlIIlIIIIIlI = ["Asurascans", "Reaperscans", "Cyborg", "Suzeriantrans", "thatguywhosthere"]
IIlIIlllllllllIlI = IIIIlIIlIlIIIlI.Combo(lIIIlIIlIIIIIlI, font=('CC Wild Words', 14),  expand_x=True, enable_events=True,  readonly=True, key='lIIIlIIlIlIIIlI')
lIIllIIllI = [[IIlIIlllllllllIlI]]
lIIllllIllIlIllIIII = IIIIlIIlIlIIIlI.Window('Selection window', lIIllIIllI, size=(250, 100), icon=r"C:\Users\tebre\source\repos\Next mover\Next mover\Group_1.ico")
lIllIlllIlllIIIlll, lllIIIIlIIIIIll = lIIllllIllIlIllIIII.read()
while True:
    if lIllIlllIlllIIIlll == IIIIlIIlIlIIIlI.WIN_CLOSED:
        lIIllllIllIlIllIIII.close()
        exit("The selection window was closed")
    if lllIIIIlIIIIIll['lIIIlIIlIlIIIlI'] == lIIIlIIlIIIIIlI[0]:
        lIlIlIlllIIlI = lIIIlIIlIIIIIlI[0]
    elif lllIIIIlIIIIIll['lIIIlIIlIlIIIlI'] == lIIIlIIlIIIIIlI[1]:
        lIlIlIlllIIlI = lIIIlIIlIIIIIlI[1]
    elif lllIIIIlIIIIIll['lIIIlIIlIlIIIlI'] == lIIIlIIlIIIIIlI[2]:
        lIlIlIlllIIlI = lIIIlIIlIIIIIlI[2]
    elif lllIIIIlIIIIIll['lIIIlIIlIlIIIlI'] == lIIIlIIlIIIIIlI[3]:
        lIlIlIlllIIlI = lIIIlIIlIIIIIlI[3]
    elif lllIIIIlIIIIIll['lIIIlIIlIlIIIlI'] == lIIIlIIlIIIIIlI[4]:
        lIlIlIlllIIlI = lIIIlIIlIIIIIlI[4]
    print("Finding " + lIlIlIlllIIlI + " next button starting on: " + str(lIIIlIIlIlIlIlI.time()) + " aka " + str(lIIIlIIlIlIlIlI.ctime()))
    break
lIIllllIllIlIllIIII.close()
lIIlllIllIllIll = IIIIlIIlIlIIIll.array(lIlIlIIlIlIlIlI.open(r'C:\Users\tebre\source\repos\Next mover\Next mover\templates\\' + lIlIlIlllIIlI.lower() + 'nexlIIIlIIlIlIlIlI.png').convert('L'))
while True:
    IIIlIIlllllI = IIIIlIIlIlIIIll.array(llIIlIIlIlIIIlI.screenshot().convert('L'))
    IIlllllIIl = IIlIlIIlIlIlIlI(IIIlIIlllllI, lIIlllIllIllIll)
    IllIIIlIIIlI = IIIIlIIlIlIIIll.where(IIlllllIIl >= 0.9)
    if len(IllIIIlIIIlI[0]) > 0:
        IlIIIIllllIIllll = (IllIIIlIIIlI[1][0], IllIIIlIIIlI[0][0])
        lIIIllIIllIIl = (IlIIIIllllIIllll[0] + lIIlllIllIllIll.shape[1], IlIIIIllllIIllll[1] + lIIlllIllIllIll.shape[0])
        IllIIllIll = (IlIIIIllllIIllll[0] + lIIIllIIllIIl[0]) // 2
        llllllIlIlIIlIII = (IlIIIIllllIIllll[1] + lIIIllIIllIIl[1]) // 2
        if llIIlIIlIlIIIlI.position() != (IllIIllIll, llllllIlIlIIlIII):
            llIIlIIlIlIIIlI.moveTo(IllIIllIll, llllllIlIlIIlIII)
            print("(x=" + str(IllIIllIll) + ", y=" + str(llllllIlIlIIlIII)+ ") at " + lIIIlIIlIlIlIlI.ctime())
        if lIlIlIlllIIlI == lIIIlIIlIIIIIlI[2]:
            lIIIlIIlIlIlIlI.sleep(.5)
        if len(IllIIIlIIIlI[0]) > 0 and llIIlIIlIlIIIlI.position() == (IllIIllIll, llllllIlIlIIlIII) and llIIlIIlIlIlIlI.read_key() == 'right':
             llIIlIIlIlIIIlI.click()