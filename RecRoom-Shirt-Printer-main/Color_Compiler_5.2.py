name = 'Color Compiler'
version = '5.2'
#5.1 added more symbols, up to 113#
#5.2 removed # from HEX file and added some extra clicking for the new custom color change#

from tkinter import Tk
from tkinter.filedialog import askopenfilename
from time import sleep

try:
    from PIL import Image, ImageFilter, ImageOps, ImageEnhance #pip install pillow
except ModuleNotFoundError:
    print("")
    print("Pillow may not installed - type: 'pip install pillow' into command prompt")
    quit(10)
try:
    import pyautogui
except ModuleNotFoundError:
    print("")
    print("PyAutoGUI may not installed - type: 'pip install pyautogui' into command prompt")
    quit(10)
try:
    import win32api, win32con, win32gui
except ModuleNotFoundError:
    print("")
    print("Win32API may not installed - type: 'pip install pywin32' into command prompt")
    quit(10)
try:
    import pyperclip as pc
except ModuleNotFoundError:
    print("")
    print("PyperClip may not installed - type: 'pip install pyperclip' into command prompt")
    quit(10)

Sx, Sy = pyautogui.size()
if (Sy%Sx == Sy):
    pass
else:
    print("Screen ratio not supported - only 16:9 is supported")
    print("   Get the coordinates of the buttons and insert them manualy into the variables in the code")
    quit()
 
color = (int(0.55*Sx), int(0.45*Sy))
custom = (int(0.7*Sx), int(0.85*Sy))
text = (int(0.7*Sx), int(0.63*Sy))
symbols = ['!','','','#','','','$','','','%','','','&','','','(','','',')','','','*','','','+','','',',','','','.','','','/','','',':','','',';','','','<','','','=','','','>','','','?','','','@','','','[','','','Ñ','','',']','','','^','','','_','','','{','','','|','','','}','','','~','','','¢','','','£','','','¤','','','¥','','','¦','','','§','','','¨','','','©','','','ª','','','«','','','¬','','','Ö','','','®','','','¯','','','°','','','±','','','²','','','³','','','´','','','µ','','','¶','','','·','','','¸','','','¹','','','º','','','»','','','¼','','','½','','','¾','','','¿','','','À','','','È','','','ß','','','Ä','','','ê','','','ö','','','Ø','','','Ð','','','Ý','','','ä','','','î','','','Œ','','','Ç','','','Ž','','','ÿ','','','Ú','','','É','','','Ê','','','Æ','','','Ë','','','Ù','','','Ü','','','a','','','ƒ','','','ñ','','','å','','','Å','','','ë','','','Ï','','','ï','','','ù','','','ý','','','Ã','','','Â','','','ž','','','Á','','','Ò','','','Ì','','','Í','','','Ó','','','Ô','','','Õ','','','€','','','Š','','','†','','','‡','','','™','','','š','','','œ','','','Ÿ','','','Û','','','ã','','','â','','','ð','','','õ','','']


def getActiveWindow(window_title: str = "Rec Room") -> bool:
    if window_title not in (pyautogui.getActiveWindowTitle() or ""):
        print("Waiting for Rec Room to be the active window... ")
        while window_title not in (pyautogui.getActiveWindowTitle() or ""):
            sleep(0.1)
        sleep(0.5)
    return(True)

def rgbToHex(rgb):
    return('%02x%02x%02x' % rgb)

def hexToRGB(hex):
    hex = str(hex)
    hex = hex.replace('#','')
    return(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

def printBreak(number):
    for i in range(number):
        print("")

def hexinsert(list,delay):
    getActiveWindow()
    sleep(1)
    win32api.SetCursorPos((0,0))
    (x,y) = color
    (xx,yy) = custom
    (xxx,yyy) = text
    for i in enumerate(list):
        (index,string) = i
        getActiveWindow()
        sleep(delay)
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(.5)
        win32api.SetCursorPos((xx, yy))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(.5)        
        win32api.SetCursorPos((xxx,yyy))
        sleep(delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(delay)
        pc.copy(string)
        sleep(delay)
        pyautogui.hotkey('ctrl','v')
        sleep(delay)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        sleep(delay)
        pyautogui.keyDown('f')
        pyautogui.keyUp('f')
        sleep(delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        sleep(delay)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        sleep(delay)
        pyautogui.keyDown('f')
        pyautogui.keyUp('f')
        sleep(delay)

def dilate(cycles, image):
    for i in range(cycles):
        image = image.filter(ImageFilter.MaxFilter(3))
        return image

def erode(cycles, image):
    for i in range(cycles):
        image = image.filter(ImageFilter.MinFilter(3))
        return image

print("")
Tk().withdraw()
print(str(name) + " " + str(version))
print("   'i' to import a HEX file")
print("   'c' to compile a image into RGB and HEX files")
selection = str(input("Enter value: "))
if (selection == 'c'):
    print("  Select image file to compile")
elif (selection == 'i'):
    print("  Select text file to import")
    strings = askopenfilename()
    strings = open(strings, "r")
    try:
        try:
            segments = strings.readlines()
        except:
            print("")
            print("Invalid file type - only use text files")
            print("")
            quit()
    except AttributeError:
        print("Error - file window closed")
        print("")
        quit()
    print("")
    print("File found.")
    print("")
    print("Colors obtained, " + str(len(segments)) + " colors found.")
    print("")
    delay = float(input("Enter import delay in seconds from 0 to 1 second: "))
    print("Delay set to " + str(delay) + " seconds")
    print("")
    print("  Import will begin three seconds after you press enter and will check if 'Rec Room' is the active window")
    input("Press enter to start the import process: ")
    sleep(3)
    hexinsert(segments,delay)
    print("")
    quit()
else:
    print("Enter valid option")
    print("")
    quit()

fileName = askopenfilename()
try: #File error detection
    try:
        img = Image.open(fileName)
    except:
        print("")
        print("Invalid image type - only use PNG, JPEG, or JFIF")
        print("")
        quit()
except AttributeError:
    print("Error - file window closed")
    print("")
    quit()

img = img.convert('RGB')
FileName = str(fileName)
FileName = FileName.split('/')
FileName = FileName[len(FileName)-1]
try:
    FileName = FileName.replace('.png','')
except:
    try:
        FileName = FileName.replace('.jpg','')
    except:
        try:
            FileName = FileName.replace('.jfif','')
        except:
            try:
                FileName = FileName.replace('.jpeg','')
            except:
                pass

print("  1 marker is minmum 113 is maximum")
img.load()
coloramount = int(input("Enter amount of colors: "))
if (coloramount < 1):
    print("")
    print("Color amount too small - 1 is minmum amount")
    print("")
    quit()
elif (coloramount > 113):
    print("")
    print("Color amount too large - 113 is maximum amount")
    print("")
    quit()
else:
    pass
print("   0 = Median Cut - Has best color detection")
print("   1 = Maximum Coverage - Use for special circumstances")
print("   2 = Fast Octree - Use this method it works the best")
colortype = int(input("Enter type of quantization: "))
try:
    quant = img.quantize(colors=coloramount,method=colortype)
except ValueError:
    print("")
    print("Quantization method not recognized - enter valid integer")
    print("")
    quit()

count = coloramount*3
palette = (quant.getpalette()[:count])
maximum = int(len(palette)-2)
hexcolors = []
rgbcolors = []
i = 0
if (coloramount > 0 and coloramount <= 113):
    for i in (range(maximum)):
        if (i%3 == 0):
            rgb = palette[i],palette[i+1],palette[i+2]
            hexcolor = str(rgbToHex(rgb))
            rgbcolors.append(str(rgb) + ': "' + str(symbols[i]) + '",')
            hexcolors.append(hexcolor)
            i += 1
        else:
            i += 1
else:
    for i in (range(maximum)):
        if (i%3 == 0):
            rgb = palette[i],palette[i+1],palette[i+2]
            hexcolor = str(rgbToHex(rgb))
            rgbcolors.append(str(rgb))
            hexcolors.append(hexcolor)
            i += 1
        else:
            i += 1
print(str(coloramount) + " colors compiled")
print("")
hexFileName = FileName + "-Hex.txt"
with open(hexFileName, 'w') as file1:
    file1.write('\n'.join(hexcolors))
RGBfileName = FileName + "-RGB.txt"
with open(RGBfileName, 'w') as file2:
    file2.write('\n'.join(rgbcolors))
print("Text files written")
print("  Run program again to import colors")