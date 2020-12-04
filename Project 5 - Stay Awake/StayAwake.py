import pyautogui
import time
import sys
from datetime import datetime

pyautogui.FAILSAFE = False
numMin = None

if ((len(sys.argv) < 2) or sys.argv[1].isalpha() or int(sys.argv[1]) < 1):
    numMin = 1.5
else:
    numMin = int(sys.argv[1])

print("Time Set: ", numMin)
print(f'Computer will stay awake by moving the mouse every {numMin} minutes.')

while(True):
    x = 0
    while(x < numMin):
        time.sleep(30)
        x += 0.5
    for i in range(2):
        pyautogui.moveRel(1, 0, duration=0.1)
        pyautogui.moveRel(-1, 0, duration=0.1)

    for i in range(0, 2):
        pyautogui.press("shift")
    print("Movement made at {}".format(datetime.now().time()))
