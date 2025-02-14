import pyautogui
from string import ascii_letters
import random
from time import sleep
from pyautogui import moveTo, dragTo

# -- I used this to automatically save images i was drawing as input before seeing that the quickdraw dataset was online

#automatically capture images when ran so i dont have to manually do it every time
MENU_COORDS = (33,62)
SAVEAS_COORDS = (109,392)
IMAGE_COORDS = (129,298)
NAME_COORDS = (195,412)
SAVE_COORDS = (746,550)
ERASER_COORDS = (750,270)
ERASE_POINTS = ((223,495),(432,527),(424,780),(224,761),(223,495))
PENCIL_COORDS = (900,200)
CANVAS_COORDS = (300,650)

def click(coords):
    pyautogui.click(x=coords[0], y=coords[1])

#while True:
#    print(pyautogui.position())


if __name__ == '__main__':
    click(MENU_COORDS)
    sleep(0.1)
    click(SAVEAS_COORDS)
    click(IMAGE_COORDS)
    click(NAME_COORDS)
    name = ''.join(random.sample(ascii_letters,16))+'.png'
    sleep(0.1)
    pyautogui.write(name,interval=0.025)
    click(SAVE_COORDS)
    click(ERASER_COORDS)
    moveTo(ERASE_POINTS[0][0],ERASE_POINTS[0][1])
    for point in ERASE_POINTS[1:]:
        dragTo(point[0],point[1])
    click(PENCIL_COORDS)
    moveTo(CANVAS_COORDS[0],CANVAS_COORDS[1])