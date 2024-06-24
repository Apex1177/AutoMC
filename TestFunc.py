import pyautogui, time, cv2, multiprocessing
import numpy as np
from PIL import Image, ImageGrab


# !!!!! This file is for testing functions and is not used in the actual program !!!!


print(pyautogui.displayMousePosition())

#1500, 550

# x start 930 
# x end 1000
# y start 500
# y end 1000

#208, 41, 41

#1015, 490
time.sleep(3)

    #pix = pyautogui.pixel(100, 200)
    #print(pix)
    #screenshot = pyautogui.screenshot()

#im1 = pyautogui.screenshot(region=(900,390, 125, 250)) #900, 390 is starting x and y values and 125, 250 is how many pixels you go out from 900, 390
#im1 = cv2.cvtColor(np.array(im1), cv2.COLOR_RGB2BGR)




xstartcord = 0
ystartcord= 0

xcounter =0 
ycounter = 0

pixel = ImageGrab.grab().load()
while 1:
        color = pixel[xstartcord+xcounter, ystartcord+ycounter]
        xcounter+=3
        if xcounter>=1920: #X END CORD
            xcounter = 0
            ycounter+=3
            if ycounter>=1080:#Y END CORD
                print("BOBBER NOT FOUND")
                break
        print(color)
        if color == (211, 42, 42):#THIS WORKS FINALLY
            print('BOBBER FOUND')
            print(xstartcord+xcounter, ystartcord+ycounter)
            break

#cv2.imwrite("screenshot.png", im1)
    #print(screenshot.width)
    #print(screenshot.height)
    #pyautogui.position()
    #time.sleep(20)
    #960, 540 center of screen
    #211, 42, 42 RBG of bobber
    # x - 875, 1025
    #y - 380, 630