import pyautogui

Debugging = False  # Отладка для просмотра областей поиска
window = []
fishingON = 0

def view_area(area, newScr = 0):
    if Debugging:
        if newScr:
            pyautogui.screenshot('Pictures/screenshot.png', region = window.box)
        from PIL import Image, ImageDraw
        screen = Image.open('Pictures/screenshot.png')
        pencil = ImageDraw.Draw(screen)
        pencil.rectangle((area[0], area[1], area[0] + area[2], area[1] + area[3]), fill='green')
        screen.show()
        screen.save('Pictures/screenshot.png')

def fishing_rod_in_hand(in_h=0):
    import time
    if in_h:
        return 1
    for i in range(10):
        pyautogui.keyDown(f'{i}')
        time.sleep(0.1)
        pyautogui.keyUp(f'{i}')
        in_hand = pyautogui.locateOnScreen('Pictures/fishing_rod_in_hand.png', grayscale=True, confidence=.7, region = window.box)
        if in_hand != None:
            view_area(in_hand)
            return 1
    return 0

def fishing():
    import math, time
    global window
    countX = 0
    countY = 0
    countNone = 0
    R = 0
    while True:
        pyautogui.moveTo(window.box[0] + int(window.box[2] // 2) - 37, window.box[1] + int(window.box[3] // 2) + 40)
        CFloat = pyautogui.locateOnScreen('Pictures/float.png', confidence=.79, region=window.box)
        if R == 0:
            pyautogui.mouseDown()
            time.sleep(0.1)
            pyautogui.mouseUp()
            time.sleep(1.5)
            R = 1
        if CFloat == None:
            countNone += 1
        if CFloat != None:
            if (1 <= math.fabs(CFloat[0] - countX) <= 25 or 1 <= math.fabs(CFloat[1] - countY) <= 25) and countNone >= 2:
                print(CFloat[0], countX, CFloat[1], countY)
                if R == 1:
                    pyautogui.mouseDown()
                    time.sleep(0.1)
                    pyautogui.mouseUp()
                    time.sleep(1.5)
                    R = 0
            countNone = 0
            countX = CFloat[0]
            countY = CFloat[1]

def Terraria():
    global fishingON, window
    TerrariaON = pyautogui.locateOnScreen('Pictures/Terraria.png', grayscale=True, confidence=.7)  # Поиск окна террарии
    if TerrariaON == None:
        TerrariaON = pyautogui.locateOnScreen('Pictures/ico.png', grayscale=True, confidence=.9)
    if TerrariaON == None:
        exit("Terraria window not found")
    else:
        print("Terraria window found")
        pyautogui.moveTo(TerrariaON[0]+int(TerrariaON[2]//2), TerrariaON[1]+int(TerrariaON[3]//2))
        pyautogui.click()
        window = pyautogui.getActiveWindow()
        print(window.box)
        view_area(TerrariaON, 1)
        fishing_rod = pyautogui.locateOnScreen('Pictures/fishing_rod.png', grayscale=True, confidence=.55, region = window.box) # Поиск золотой удочки
        in_hand = pyautogui.locateOnScreen('Pictures/fishing_rod_in_hand.png', grayscale=True, confidence=.7, region = window.box)
        no_bait = pyautogui.locateOnScreen('Pictures/no_bait.png', grayscale=True, confidence=.55, region = window.box)  # Поиск наживки
        if fishing_rod == None and in_hand == None:
            exit("Fishing rod not found")
        elif not(no_bait == None):
            exit("Baits not found")
        else:
            print("Fishing rod and baits found")
            view_area(fishing_rod)
            if in_hand != None:
                fishingON = fishing_rod_in_hand(1)
            else:
                fishingON = fishing_rod_in_hand()

    if fishingON:
        fishing()

Terraria()
