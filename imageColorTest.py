import numpy as np
import cv2
import math

#konstansok
SIZEX = 500
SIZEY = 500
START = 30
STEPS = 10
PATH = '/home/pi/rPi/overAllColor/orangeM.jpeg'

#atvaltas fgv
def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h,s*100,v*100

#szintombok
colorNames = ["black", "white", "grey", "red", "pink", "orange", "brown", "yellow", "green", "cyan", "blue", "pruple", "magenta"]
colorCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#kep betolt
img=cv2.imread(PATH, -1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#vizsgalat
for y in range (START,SIZEY-START+1,STEPS):
    for x in range (START,SIZEX-START+1, STEPS):
    
        #konvertaltas
        pixel=img[y,x]
        px = rgb2hsv(pixel[2], pixel[1], pixel[0])

        #megjeleno pontok
        img[y,x]=[255,0,0]
        
        #fekete?
        if px[2] < 9:
            colorCount[0] += 1
        #feher vagy szurke?
        elif px[1] < 22:
            if px[2] > 91:
                colorCount[1] += 1
            else:
                colorCount[2] += 1
        #piros vagy rozsaszin?
        elif px[0] < 11:
            if px[1] > 73:
                colorCount[3] += 1
            else:
                colorCount[4] += 1
        #narancs vagy barna?
        elif px[0] < 39:
            if px[2] > 68:
                colorCount[5] += 1
            else:
                colorCount[6] += 1
        #sarga?
        elif px[0] < 72:
            colorCount[7] += 1
        #zold?
        elif px[0] < 152:
            colorCount[8] += 1
        #cian?
        elif px[0] < 185:
            colorCount[9] += 1
        #kek?
        elif px[0] < 263:
            colorCount[10] += 1
        #lila?
        elif px[0] < 287:
            colorCount[11] += 1
        #magenta?
        elif px[0] < 352:
            colorCount[12] += 1
        #masik piros vagy rozsaszin?
        else:
            if px[1] > 73:
                colorCount[3] += 1
            else:
                colorCount[4] += 1

       
#vizsgalt pixelek szama
pixNum = ((SIZEX - START*2) / STEPS + 1) * ((SIZEY - START*2) / STEPS + 1)

#lista kiiras
for i in range (0,13):
    print(colorNames[i], ": ", colorCount[i] * 100 / pixNum, "%")
print(pixNum)

#konkluzio kiiras
colorful = True
for j in range (0,13):
    if colorCount[j] > pixNum / 2:
        print(colorNames[j])
        colorful = False
if colorful:
    print("colorful")

#kepmegjelenites    
cv2.imshow('imageWindow',img)
cv2.waitKey(0)
