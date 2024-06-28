from pyautogui import *
import pyautogui, time, keyboard, random, win32api, win32con, os, sys, threading, customtkinter, multiprocessing, pydirectinput
from PIL import Image, ImageGrab

def WaitingLoop(): #waits for a hotkey to be pressed
    print('Waiting Loop...')
    keyboard.add_hotkey(']', HoldM1)
    keyboard.add_hotkey('tab', Condense)
    keyboard.add_hotkey("'", SellAll)
    keyboard.add_hotkey('=', AutoFish) 
    keyboard.add_hotkey('esc+shift', RestartProgram)
    keyboard.wait()

def Condense(): #hotkey to run /condense cmd
    pyautogui.press('enter')
    pyautogui.write('/con', interval=random.uniform(0.025, 0.04))
    pyautogui.press('tab')   #presses tab to autocomplete 
    pyautogui.press('enter')   
def SellAll():
    pyautogui.press('enter')
    pyautogui.write('/se', interval=random.uniform(0.025, 0.04))
    pyautogui.press('tab')  
    pyautogui.press('tab')  
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
                pyautogui.moveTo(1015, 490, random.uniform(0.4, 0.8))
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.click()
                time.sleep(random.uniform(0.05, 0.1))
                pyautogui.click()
                time.sleep(random.uniform(0.05, 0.1))
                FishCounter = random.randint(0, 3)

        randomadd = random.randint(0, 6)

        TurnCounter+=1
        if TurnCounter < 3: 
            pyautogui.moveTo(1170+randomadd, 531, random.uniform(0.2, 0.25)) #960 x is center of the screen and 531 y is center when not in fullscreen
        if TurnCounter > 3: 
            pyautogui.moveTo(750+randomadd, 531, random.uniform(0.2, 0.25))
        if TurnCounter > 6:
            TurnCounter = 0
        
        time.sleep(random.uniform(0.2, 0.3))

        pyautogui.click(button='right')
        time.sleep(2.5)
        BobberCords=FindBobber()
        print("THESE ARE BOBBER CORDS")
        print(BobberCords)
        xcord = BobberCords[0]
        ycord = BobberCords[1]
        confidencecounter = 0
        starttimer = time.time()
        while 1:
            endtimer = time.time()
            if (endtimer-starttimer) > 20: #if the program gets stuck it will timeout after x seconds and reset
                print("TIMEOUT RESET")
                break
            pix = pyautogui.pixel(xcord, ycord)
            #print(pix)
            if pix[2] >= 100 and pix[2] <=200:     #check if B value of RGB is between 100 and 200 if true fish detected
                print("MIGHT BE FISH")
                confidencecounter+=1
                time.sleep(.15)
                if confidencecounter == 2:
                    FishCounter+=1
                    print('FISH FOUND')
                    print(pix)
                    break
            else:
                confidencecounter = 0
            time.sleep(.25)
        pyautogui.click(button='right')
        time.sleep(.1)

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
                BobberCords = (xstartcord+xcounter+2, ystartcord+ycounter-2)
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
        print('Autoselling')
        pyautogui.keyUp('w')
        pyautogui.mouseUp()     
        time.sleep(random.uniform(.6, 1.1))
        Condense() # issue where it types slower than its supposed to... why did threading break this? #update I believe its an issue with multithreading in python and made it press tab to autocomplete
        time.sleep(random.uniform(.6, 1.1))
        SellAll()
        pyautogui.click(button='right')
        pyautogui.keyDown('w')
        pyautogui.mouseDown()
        time.sleep(random.randint(55, 65)) 
        AutoSell()
        

def HoldM1(): #holds M1 and w until esc is pressed on the keyboard
    print('Holding M1')
    if autosellbool == '1':
        print('Autosell is on')
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
    RestartProgram()


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

label = customtkinter.CTkLabel(master=frame, text="AutoTrappedMC alpha", font=("Roboto", 36))
label.pack(pady=12, padx=10)
label1 = customtkinter.CTkLabel(master=frame, text="Hotkeys Below", font=("Roboto", 30))
label1.pack(pady=6, padx=10)

label2 = customtkinter.CTkLabel(master=frame, text="Condense ' tab '", font=("Roboto", 24))
label2.pack(pady=6, padx=10)
label3 = customtkinter.CTkLabel(master=frame, text="Sellall ' ' '", font=("Roboto", 24))
label3.pack(pady=6, padx=10)
label4 = customtkinter.CTkLabel(master=frame, text="Hold M1 & W ' ] '", font=("Roboto", 24))
label4.pack(pady=6, padx=10)
label5 = customtkinter.CTkLabel(master=frame, text="Autofish - can't be fullscreen' = '", font=("Roboto", 24))
label5.pack(pady=6, padx=10)
label6 = customtkinter.CTkLabel(master=frame, text="Restart Program ' esc+shift '", font=("Roboto", 24))
label6.pack(pady=6, padx=10)


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
    root.mainloop() # need to add something to show which hotkeys do what
    print('Progam started')
    WaitingLoop()