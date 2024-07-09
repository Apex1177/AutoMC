from pyautogui import *
import pyautogui, time, keyboard, random, win32api, win32con, os, sys, threading, customtkinter, multiprocessing, pydirectinput, signal
from PIL import Image, ImageGrab

def WaitingLoop(): #waits for a hotkey to be pressed
    print('Waiting Loop...')
    keyboard.add_hotkey(']', HoldM1)
    keyboard.add_hotkey('`', Condense)
    keyboard.add_hotkey("'", SellAll)
    keyboard.add_hotkey('=', AutoFish) 
    keyboard.add_hotkey('-', AutoFarm)
    keyboard.add_hotkey('esc+shift', RestartProgram)
    keyboard.wait()

def Condense(): #hotkey to run /condense cmd

    pyautogui.press('enter')
    pyautogui.write('/con', interval=random.uniform(0.01, 0.02))
    pyautogui.press('tab')   #presses tab to autocomplete 
    pyautogui.press('enter')   

def SellAll():
    pyautogui.press('enter')
    pyautogui.write('/se', interval=random.uniform(0.01, 0.02))
    pyautogui.press('tab')  
    pyautogui.press('tab')  
    pyautogui.press('enter') 

def AutoFarm(): #this function farms and replants each layer of the farm, dropping down at the end of each layer and switching direction 
    # Works, but could use some improvement and tweaking
    PartialLayers = 3
    FullLayers = 2

    PartialRowCount = 25 #1 less than to account for unused row
    FullRowCount = 32

    RowUsed = FullRowCount #Default for what row is used

    TimePerFarm = 5.5 #note this number needs to be changed based on how long it takes to run from one end of the farm to the other,I could have the program figure out this number through testing, but im lazy
    TimePerPlant = 6.6
    
    SellCounter = random.randint(0,1)

    Direction = 'd'

    for Layer in range(FullLayers+PartialLayers):
        if Layer == FullLayers:
            RowUsed = PartialRowCount
        pyautogui.keyDown(Direction)
        time.sleep(random.randint(2, 3))
        pyautogui.keyUp(Direction)
        if (Layer % 2) == 0:
            Direction = 'a'
        else:
            Direction = 'd'
        for Row in range(RowUsed):
            SellCounter+=1
            Farming(TimePerFarm)
            MovementAdjustment()
            Planting(TimePerPlant)
            pyautogui.keyDown(Direction)
            time.sleep(random.uniform(.065, .075))
            pyautogui.keyUp(Direction)
            if SellCounter == 8:
                SellAll()
                SellCounter = random.randint(0,1)
            

        #put change layer part here so it executes after all layers are farmed

def Farming(TimePerFarm):
    starttimer = time.time()
    pyautogui.press('3')
    time.sleep(random.uniform(0.05, 0.1))
    pyautogui.click(button='right')
    time.sleep(random.uniform(0.05, 0.1))
    pyautogui.keyDown('w')
    while 1:
        endtimer = time.time()
        if (endtimer-starttimer) > TimePerFarm: 
            break
        pyautogui.click()
        time.sleep(random.uniform(0.015, 0.02))
    pyautogui.keyUp('w')

def Planting(TimePerPlant):
    starttimer = time.time()
    pixel = ImageGrab.grab().load()
    color = pixel[893, 1005]
    print(color)
    if color == (194, 214, 80): #checks if the potatoe is poisonned, since you cant plant those
        pyautogui.press('5')
    else:
        pyautogui.press('4')
    time.sleep(random.uniform(0.05, 0.1))
    pyautogui.keyDown('s')
    while 1:
        endtimer = time.time()
        if (endtimer-starttimer) > TimePerPlant:
            break
        pyautogui.click(button='right')
        time.sleep(random.uniform(0.015, 0.02))
    pyautogui.keyUp('s')

def MovementAdjustment(): #looks for a certain color of pixel in tilled dirt then adjust its position to be closer to center based on the x coordinate of that pixel
    #this is required since you drift over time, and this could not be fixed by adjusting how far the player moves due to factors out of my control
    #if needed I can redesign this to adjust movement to any future functions, but im not sure if I will need to do that
    xstartcord = 820 #creating the search box
    ystartcord = 570
    xendcord = 1980
    yendcord = 600
    objcolor1 = 111, 111, 111 #RBG of pixel im searching for
    objcolor2 = objcolor1 #im searching for only 1 RBG
    while 1:
        RefPoint = FindObj(xstartcord, ystartcord, xendcord, yendcord, objcolor1, objcolor2)
        if RefPoint != None:
            xcord = RefPoint[0] 
            if xcord >= 990: #move right
                pyautogui.keyDown('d')
                pyautogui.keyUp('d')
                time.sleep(1)
            elif xcord <= 900: #move left
                pyautogui.keyDown('a')
                pyautogui.keyUp('a')
                time.sleep(1)
            else:
                break
        break

def AutoFish(): #Auto fishes moveto does not work currently
    FishCounter = random.randint(0, 2)
    TurnCounter = 0
    xstartcord = 900 #start and end cords are for making the box to search for the bobber
    ystartcord= 350 
    xendcord = 1000
    yendcord = 600
    objcolor1 = 211, 42, 42
    objcolor2 = 208, 41, 41
    while 1:
        FishCounter+=1
        print(FishCounter)
        if autosellbool == '1' or autosellbool == True:
            if FishCounter == 25: #autosells fish in emf shop
                time.sleep(.25)
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
                FishCounter = random.randint(0, 2)

        randomadd = random.randint(0, 6)

        TurnCounter+=1
        if TurnCounter < 4: 
            pyautogui.moveTo(1170+randomadd, 531, random.uniform(0.2, 0.25)) #960 x is center of the screen and 531 y is center when not in fullscreen
        if TurnCounter > 4: 
            pyautogui.moveTo(750+randomadd, 531, random.uniform(0.2, 0.25))
        if TurnCounter > 7:
            TurnCounter = 0
        
        time.sleep(random.uniform(0.2, 0.3))

        pyautogui.click(button='right')
        BobberCords = None
        while BobberCords == None:
            time.sleep(1.5)
            BobberCords=FindObj(xstartcord, ystartcord, xendcord, yendcord, objcolor1, objcolor2)
        print("THESE ARE BOBBER CORDS")
        print(BobberCords)
        xcord = BobberCords[0]
        ycord = BobberCords[1]
        confidencecounter = 0
        starttimer = time.time()
        while 1:
            endtimer = time.time()
            if (endtimer-starttimer) > 12: #if the program gets stuck it will timeout after x seconds and reset
                print("TIMEOUT RESET")
                break
            pix = pyautogui.pixel(xcord, ycord)
            #print(pix)
            if pix[2] >= 100 and pix[2] <=200:     #check if B value of RGB is between 100 and 200 if true fish detected
                print("MIGHT BE FISH")
                confidencecounter+=1
                if confidencecounter == 2:
                    print('FISH FOUND')
                    print(pix)
                    break
            else:
                confidencecounter = 0
            time.sleep(.15)
        pyautogui.click(button='right')
        time.sleep(.1)

def FindObj(xstartcord, ystartcord, xendcord, yendcord, objcolor1, objcolor2): #finds the bobber or obj and returns its locations
    xcounter = 0 #the counters are used to check through each line of pixels, starts at top left of the box finishes each row then moves down 3
    ycounter = 0
    pixel = ImageGrab.grab().load()
    pixelskip= 9 
    while 1:
        try:
            color = pixel[xstartcord+xcounter, ystartcord+ycounter] #returns the RGB color of the pixel checked in a tuple 
            xcounter+=pixelskip
            if xcounter+xstartcord>=xendcord: #When the y counter is above the end cord it resets to go to the next line
                xcounter = 0
                ycounter+=pixelskip
                if ycounter+ystartcord>=yendcord:#same as above but for x and when it reaches the end then the bobber isnt found
                    print("obj NOT FOUND, DECREASING SKIP")
                    pixelskip-=2
                    if pixelskip == 3:
                        print("obj NOT FOUND, RETURNING NONE")
                        ObjCords = None
                        return ObjCords
            print(color)
            print(xstartcord+xcounter, ystartcord+ycounter)
            if color == (objcolor1) or color == (objcolor2):#RBG of the bobber or obj 
                print('OBJ FOUND')
                ObjCords = (xstartcord+xcounter+2, ystartcord+ycounter-2)
                return ObjCords
        except:
            print("obj NOT FOUND+EXCEPTION, DECREASING SKIP")
            pixelskip-=2
            if pixelskip == 3:
                print("obj NOT FOUND+EXCEPTION, RETURNING NONE")
                ObjCords = None
                return ObjCords

def StoreEmeralds():
    pyautogui.press('enter')
    pyautogui.write('/ec', interval=random.uniform(0.025, 0.04))
    pyautogui.press('enter')
    xstartcord = 730 #start and end is the minecraft inventory
    ystartcord = 550
    xendcord = 1190
    yendcord = 730
    objcolor1 = 23, 218, 97 #emerald rbg
    objcolor2 = 15, 142, 63 #emerald block rbg
    for x in range(2): #looks for block and emeralds
        EmeraldCords = FindObj(xstartcord, ystartcord, xendcord, yendcord, objcolor1, objcolor2)
        print(EmeraldCords)
        if EmeraldCords == None:
            print("Not found")
            break
        xcord = EmeraldCords[0]
        ycord = EmeraldCords[1]
        pyautogui.moveTo(xcord, ycord)
        with pyautogui.hold('shift'):
            pyautogui.click()
    pyautogui.press('esc')

def AutoMiner():
    pass

def AutoChatGame():
    pass

def AutoSell():
    print('Autoselling')
    pyautogui.keyUp('w')
    pyautogui.mouseUp()     
    time.sleep(random.uniform(.2, .3))
    Condense() 
    if emeraldstorebool == '1' or emeraldstorebool == True:
        time.sleep(random.uniform(.2, .3))
        StoreEmeralds() 
    time.sleep(random.uniform(.2, .3))
    SellAll()
    pyautogui.click(button='right') # for superbreaker ability 
    pyautogui.keyDown('w')
    pyautogui.mouseDown()
    time.sleep(random.randint(48, 54)) 
    AutoSell()
        
def HoldM1(): #holds M1 and w until esc is pressed on the keyboard
    print('Holding M1')
    pyautogui.keyDown('w')
    pyautogui.mouseDown()
    if autosellbool == '1' or autosellbool == True:
        print('Autosell is on')
        time.sleep(60)
        AutoSell()

def CheckForRestart():
    while keyboard.is_pressed('esc') == False:
        time.sleep(.1)
    RestartProgram()
    sys.exit()
    
def RestartProgram():
    print('program ended')
    os.kill(os.getppid(), signal.SIGTERM)
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

label2 = customtkinter.CTkLabel(master=frame, text="Condense ' ` '", font=("Roboto", 24))
label2.pack(pady=6, padx=10)
label3 = customtkinter.CTkLabel(master=frame, text="Sellall ' ' '", font=("Roboto", 24))
label3.pack(pady=6, padx=10)
label4 = customtkinter.CTkLabel(master=frame, text="Hold M1 & W ' ] '", font=("Roboto", 24))
label4.pack(pady=6, padx=10)
label5 = customtkinter.CTkLabel(master=frame, text="Autofish - can't be fullscreen' = '", font=("Roboto", 24))
label5.pack(pady=6, padx=10)
label6 = customtkinter.CTkLabel(master=frame, text="Restart Program ' esc '", font=("Roboto", 24))
label6.pack(pady=6, padx=10)

#buttonyes = customtkinter.CTkButton(master=frame, text="Yes", autosellbool = True)
#buttonyes.pack(pady=12, padx=10)
#buttonno = customtkinter.CTkButton(master=frame, text="No", autosellbool = False)
#buttonno.pack(pady=12, padx=10)

# below is the checkbox for setting autosell to true or false
autosellbool=True
emeraldstorebool=True
def on_checkbox_toggle():
    global autosellbool
    global emeraldstorebool
    autosellbool = check_autosell.get()
    emeraldstorebool = check_storeemerald.get()
    print("Autosell : ")
    print(autosellbool)
    print("Emerald store : ")
    print(emeraldstorebool)

check_autosell = customtkinter.StringVar(value="on")
check_storeemerald = customtkinter.StringVar(value="on")
autosellcheckbox = customtkinter.CTkCheckBox(master=frame, text="Turn Off Auto-Sell?", command=on_checkbox_toggle, variable=check_autosell, onvalue=False, offvalue=True)
autosellcheckbox.pack(pady=12, padx=10)
autosellcheckbox = customtkinter.CTkCheckBox(master=frame, text="Turn Off Storing Emeralds?", command=on_checkbox_toggle, variable=check_storeemerald, onvalue=False, offvalue=True)
autosellcheckbox.pack(pady=12, padx=10)

if __name__ == '__main__':
    root.mainloop() # need to add something to show which hotkeys do what
    print('Progam started')
    print("Autosell : ")
    print(autosellbool)
    print("Emerald store : ")
    print(emeraldstorebool)
    CheckRestart = multiprocessing.Process(target=CheckForRestart) #If esc is ever pressed the program will restart
    CheckRestart.start()
    WaitingLoop()