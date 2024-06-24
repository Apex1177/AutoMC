from pyautogui import *
import pyautogui, time, keyboard, random, win32api, win32con, os, sys, threading, customtkinter, multiprocessing, pydirectinput
from PIL import Image, ImageGrab

def WaitingLoop(): #waits for a hotkey to be pressed
    #HoldM1_thread = threading.Thread(target=HoldM1, daemon=True)
    print('Waiting Loop...')
    keyboard.add_hotkey(']', HoldM1)
    keyboard.add_hotkey('-', Condense)
    keyboard.add_hotkey('=', AutoFish) 
    keyboard.add_hotkey('esc+shift', RestartProgram)
    keyboard.wait()

def Condense(): #hotkey to run /condense cmd
    pyautogui.press('enter')
    pyautogui.write('/condense', interval=random.uniform(0.025, 0.04))
    pyautogui.press('enter')   



def AutoFish(): #Auto fishes moveto does not work currently
    FishCounter = random.randint(0, 3)
    TurnCounter = 0
    while keyboard.is_pressed('esc') == False:
        if autosellbool == '1':
            if FishCounter >= 30: #untested autosell
                pyautogui.press('enter')
                pyautogui.write('/emf shop', interval=random.uniform(0.025, 0.04))
                pyautogui.press('enter')
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.moveTo(1015, 0, random.uniform(0.4, 0.8))
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.click()
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.click()
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.press('esc')
                time.sleep(random.uniform(0.05, 0.1))
                FishCounter = random.randint(0, 3)
        if TurnCounter <= 3:
            pydirectinput.moveTo(1300, 0)
        if TurnCounter<=6:
            pydirectinput.moveTo(700, 0)
        TurnCounter+=1
        if TurnCounter == 7:
            TurnCounter = 0
        time.sleep(random.uniform(0.05, 0.1))
        pyautogui.click(button='right')
        time.sleep(2.2)
        BobberCords=FindBobber()
        print("THESE ARE BOBBER CORDS")
        print(BobberCords)
        xcord = BobberCords[0]
        ycord = BobberCords[1]
        confidencecounter = 0
        while 1:
            pix = pyautogui.pixel(xcord, ycord)
            print(pix)
            if pix[2] >= 100 and pix[2] <=200:     #check if B value of RGB is between 100 and 200 if true fish detected
                print("MIGHT BE FISH")
                confidencecounter+=1
                time.sleep(.05)
                if confidencecounter == 2:
                    FishCounter+=1
                    print('FISH FOUND')
                    print(pix)
                    pyautogui.click(button='right')
                    time.sleep(.1)
                    break
            else:
                confidencecounter = 0
            time.sleep(.3)

def FindBobber(): #finds the bobber and returns its locations
    xstartcord = 900 #start and end cords are for making the box to search for the bobber
    ystartcord= 350 
    xendcord = 1000
    yendcord = 600
    xcounter = 0 #the counters are used to check through each line of pixels, starts at top left of the box finishes each row then moves down 3
    ycounter = 0
    pixel = ImageGrab.grab().load()

    while 1:
        try:
            color = pixel[xstartcord+xcounter, ystartcord+ycounter] #returns the RGB color of the pixel checked in a tuple 
            xcounter+=3 #at the distance viewed "minecraft pixels" are 3x3 of pixels, so we can skip 3 at a time for efficiency, same for y below
            if xcounter+xstartcord>=xendcord: #When the y counter is above the end cord it resets to go to the next line
                xcounter = 0
                ycounter+=3
                if ycounter+ystartcord>=yendcord:#same as above but for x and when it reaches the end then the bobber isnt found
                    print("BOBBER NOT FOUND")
                    pyautogui.click(button='right')
                    AutoFish()
            print(color)
            print(xstartcord+xcounter, ystartcord+ycounter)
            if color == (211, 42, 42) or color == (208, 41, 41):#RBG of the bobber 
                print('BOBBER FOUND')
                BobberCords = (xstartcord+xcounter, ystartcord+ycounter)
                return BobberCords
        except:
            print("BOBBER NOT FOUND + EXCEPTION")
            pyautogui.click(button='right')
            AutoFish()

def AutoMiner():
    pass

def AutoChatGame():
    pass

def AutoSell():
    while keyboard.is_pressed('esc') == False:
        print('Autosell is on')
        pyautogui.keyUp('w')
        pyautogui.mouseUp()     
        time.sleep(random.uniform(.6, 1.1))
        pyautogui.press('enter')
        pyautogui.write('/condense', interval=random.uniform(0.025, 0.04)) # issue where it types slower than its supposed to... why did threading break this?
        pyautogui.press('enter')
        time.sleep(random.uniform(.6, 1.1))
        pyautogui.press('enter')
        pyautogui.write('/sellall', interval=random.uniform(0.025, 0.04))
        pyautogui.press('enter')
        pyautogui.keyDown('w')
        pyautogui.mouseDown()
        time.sleep(random.randint(55, 65)) 
        AutoSell()
        

def HoldM1(): #holds M1 and w until esc is pressed on the keyboard
    print('Holding M1')
    if autosellbool == '1':
        TimerThread = threading.Timer(50, AutoSell, args=[]) # added a timer thread to fix issue where you could not escape the program during a time.sleep()
        TimerThread.start()
    pyautogui.keyDown('w')
    pyautogui.mouseDown()
    while keyboard.is_pressed('esc') == False: #This is bad, really not good, temp solution as keyboard.wait() and similar cause unexpected issues... fix later 
        continue
    pyautogui.keyUp('w')
    pyautogui.mouseUp()
    TimerThread.cancel()
    print('Not holding M1')


def RestartProgram():
    print('program ended')
    python = sys.executable
    os.execl(python, python, *sys.argv)




customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("1000x700") #size of application

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="AutoTrappedMC alpha", font=("Roboto", 24))
label.pack(pady=12, padx=10)


#buttonyes = customtkinter.CTkButton(master=frame, text="Yes", autosellbool = True)
#buttonyes.pack(pady=12, padx=10)
#buttonno = customtkinter.CTkButton(master=frame, text="No", autosellbool = False)
#buttonno.pack(pady=12, padx=10)

# below is the checkbox for setting autosell to true or false
autosellbool=False
def on_checkbox_toggle():
    global autosellbool
    autosellbool = check_var.get()
    print(autosellbool)
check_var = customtkinter.StringVar(value="on")
autosellcheckbox = customtkinter.CTkCheckBox(master=frame, text="Auto-Sell", command=on_checkbox_toggle, variable=check_var, onvalue=True, offvalue=False)
autosellcheckbox.pack(pady=12, padx=10)



if __name__ == '__main__':
    root.mainloop()
    print('Progam started')
    WaitingLoop()