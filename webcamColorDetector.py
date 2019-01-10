import numpy as np
import cv2
import math

#constants
SIZEX = 640
SIZEY = 480
STARTX = SIZEX / 2 - 30
STARTY = SIZEY / 2 - 30
STEPS = 3
TRIGGERHELP = 30

#conversion function
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

#color arrays
colorNames = ['black', 'white', 'grey', 'red', 'pink', 'orange', 'brown', 'yellow', 'green', 'cyan', 'blue', 'pruple', 'magenta']
colorCount = [0] * 13

#start video capture
cap=cv2.VideoCapture(-1)

while (True):
	#capture frame-by-frame
	ret, frame=cap.read()
	
	colorCount = [0] * 13
	
	#analyse pixel-by-pixel
	for y in range (STARTY, SIZEY-STARTY, STEPS):
		for x in range (STARTX, SIZEX-STARTX, STEPS):
			
		
			#convert current pixel
			pixel = frame[y,x]
			px = rgb2hsv(pixel[2], pixel[1], pixel[0])

			#points on display
			frame[y,x]=[255,0,0]
			
			#black?
			if px[2] < 29:
				colorCount[0] += 1
			#white or grey?
			elif px[1] < 10:
				if px[2] > 91:
					colorCount[1] += 1
				else:
					colorCount[2] += 1
			#red (or brown) or pink?
			elif px[0] < 11:
				if px[2] < 94:
					if px[0] < 21 and px[2] > 80:
						colorCount[6] += 1
					else:
						colorCount[3] += 1
				else:
					colorCount[4] += 1
			#orange or brown?
			elif px[0] < 39:
				if px[2] > 80 and (px[2] < 96 or px[1] > 70):
					colorCount[5] += 1
				else:
					colorCount[6] += 1
			#yellow?
			elif px[0] < 82:
				colorCount[7] += 1
			#green?
			elif px[0] < 152:
				colorCount[8] += 1
			#cyan?
			elif px[0] < 185:
				colorCount[9] += 1
			#blue?
			elif px[0] < 273:
				colorCount[10] += 1
			#purple?
			elif px[0] < 315:
				colorCount[11] += 1
			#magenta?
			elif px[0] < 345:
				colorCount[12] += 1
			#the other red (or brown) or pink?
			else:
				if px[2] < 94:
					if px[0] < 21 and px[2] > 80:
						colorCount[6] += 1
					else:
						colorCount[3] += 1
				else:
					colorCount[4] += 1
					
					
	#number of pixels monitored
	pixNum = ((SIZEX - STARTX*2) / STEPS + 1) * ((SIZEY - STARTY*2) / STEPS + 1)

	#output conclusion
	colorful = True
	largest = 0
	#finding largest
	for i in range (1,13):
		if colorCount[largest] < colorCount[i]:
			largest = i
	for j in range (0,13):
		if (colorCount[j] > (pixNum / 2) * 100 / (100 + TRIGGERHELP)) and j == largest:
			cv2.putText(img = frame, text = colorNames[j], org = (int(20),int(SIZEY-20)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.7, color = (0, 255, 0))
			colorful = False
	if colorful:
		cv2.putText(img = frame, text = 'colorful', org = (int(20),int(SIZEY-20)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.8, color = (0, 255, 0))

	#display exit option
	cv2.putText(img = frame, text = 'Q - exit', org = (int(SIZEX-80),int(SIZEY-20)), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 0.5, color = (0, 255, 0))
	
	#display the frame
	cv2.imshow('frame', frame)
	
	#exit option
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

#closing
cap.release()
cv2.destroyAllWindows()
