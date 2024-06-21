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
    #while 1:
        #if pyautogui.locateOnScreen('MinecraftBobber.png', confidence=.4) != None:
            #print('I see it')
            #time.sleep(.5)
        #else:
            #print("I cant see it")
            #time.sleep(.5)
    
def FindBobber(): #need to make more efficient / search smaller area
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