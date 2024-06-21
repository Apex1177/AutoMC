from pyautogui import *
import pyautogui, time, keyboard, random, win32api, win32con, os, sys, threading, customtkinter, multiprocessing
from PIL import Image, ImageGrab

def WaitingLoop(): #waits for a hotkey to be pressed
    #HoldM1_thread = threading.Thread(target=HoldM1, daemon=True)
    keyboard.add_hotkey(']', HoldM1)
    keyboard.add_hotkey('-', Condense)
    keyboard.add_hotkey('=', AutoFish) 
    keyboard.add_hotkey('esc+shift', RestartProgram)
    keyboard.wait()

def Condense():
    pyautogui.press('enter')
    pyautogui.write('/condense', interval=random.uniform(0.025, 0.04))
    pyautogui.press('enter')   

def AutoFish():#DOES NOT WORK / NOT ACCURATE
    FindBobber()
    
def FindBobber(): #finds the bobber and returns its locations
    xstartcord = 900 #start and end cords are for making the box to search for the bobber
    ystartcord= 350 
    xendcord = 1000
    yendcord = 600
    xcounter = 0 
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
                    break
            print(color)
            print(xstartcord+xcounter, ystartcord+ycounter)
            if color == (211, 42, 42):#RBG of the bobber 
                print('BOBBER FOUND')
                print(xstartcord+xcounter, ystartcord+ycounter)
                break
        except:
            print("BOBBER NOT FOUND + EXCEPTION")
            break

def AutoMiner():
    pass

def AutoChatGame():
    pass

def Reset_Configs(WDownbool, M1Downbool):
    if WDownbool == True:
        pyautogui.keyUp('w')
        WDownbool = False
    if M1Downbool == True:
        pyautogui.mouseUp()
        M1Downbool = False

def AutoSell(prev_func, WDownbool, M1Downbool):
    while keyboard.is_pressed('esc') == False:
        print('Autosell is on')
        time.sleep(random.randint(55, 65)) #bug where you cannot exit while program is sleeping with esc key
        print('Autoselling')
        Reset_Configs(WDownbool, M1Downbool)     
        time.sleep(random.uniform(.8, 1.6))
        pyautogui.press('enter')
        pyautogui.write('/condense', interval=random.uniform(0.025, 0.04))
        pyautogui.press('enter')
        time.sleep(random.uniform(.8, 1.6))
        pyautogui.press('enter')
        pyautogui.write('/sellall', interval=random.uniform(0.025, 0.04))
        pyautogui.press('enter')
        prev_func()

def HoldM1(): #holds M1 and w until esc is pressed on the keyboard
    prev_func = HoldM1
    print('Holding M1')
    while keyboard.is_pressed('esc') == False:
        pyautogui.keyDown('w')
        pyautogui.mouseDown()
        WDownbool = True
        M1Downbool = True
        if autosellbool == '1':
            #IDK multiprocess = multiprocessing.Process(target=AutoSell(prev_func, WDownbool, M1Downbool)) 
            #multiprocess.start()
            AutoSell(prev_func, WDownbool,M1Downbool)
    print('Not holding M1')
    pyautogui.keyUp('w')
    pyautogui.mouseUp()

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


root.mainloop()


print('Progam started')
WaitingLoop()