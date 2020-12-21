#Color picker uitility 
#this tool alows you to pick the right HSV values for each color


#How it works

#1) take the path to the desired image from the terminal by adding the argument -p then the full path
#2) import the image
#3) create track bars for the HSV upper and lower
#4) create mosue callback
#5) the feedback loop takes the left click and get the HSV pixel value of that postion
#6) those HSV values adjust the Track bars values
#7) create a mask from the ranges

#########Important note######
#PLEASE MAKE SURE THAT YOU ARE USING THE SAME MASKING METHOD BEFORE TRYING THE VALUES IN OTHER PROJECTS 
#BY DEFUALT THE FOLLOWING IS USED 
#GaussinBlure (15,15)
#erode (7,7)
#deilate(7,7)

import argparse
import cv2
import numpy as np
import sys
# defult values 
pixel = (0,0,0)

#pass argument 
def nothing(x):
    pass


#mouse callback 
def pick_color(event,x,y,flags,param):
    global up, down
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y,x]
        #tolerance adjustable values
        Tolerance_1 = 15 
        Tolerance_2 = 45
        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        up =  np.array([pixel[0] + Tolerance_1, pixel[1] + Tolerance_1, pixel[2] + Tolerance_2])
        down =  np.array([pixel[0] - Tolerance_1, pixel[1] - Tolerance_1, pixel[2] - Tolerance_2])
        print(down, up)
        #changing the the trackbars values 
        cv2.setTrackbarPos("L - H", "Trackbars",down[0])
        cv2.setTrackbarPos("L - S", "Trackbars",down[1])
        cv2.setTrackbarPos("L - V", "Trackbars",down[2])
        cv2.setTrackbarPos("U - H", "Trackbars",up[0])
        cv2.setTrackbarPos("U - S", "Trackbars",up[1])
        cv2.setTrackbarPos("U - V", "Trackbars",up[2])


def main():
    global hsv, pixel
    #adjustable kernal size for mask cleaning
    kernal = (7,7)
    #user argument definition
    parser = argparse.ArgumentParser('Hsv color picker')
    parser.add_argument('-p', '--path', help ='add the location of the picture')
    args = parser.parse_args()
    path = args.path

    #create a window for trackbars
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("U - S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("U - V", "Trackbars", 0, 255, nothing)

    #a defult mat just for avoiding null errors
    mat = np.zeros((300,300,3), np.uint8)
    cv2.imshow("HSV",mat)
    cv2.setMouseCallback("HSV", pick_color)

    while True:
        #loading image from the user path
        image = cv2.imread(path)
        ref = cv2.imread('circle.jpg')
        image = cv2.resize(image,((300,300)))
        #adding a blure to inhance the color detection
        image = cv2.GaussianBlur(image,(5,5),0)
        #ref = cv2.GaussianBlur(ref,(5,5),0)

        # converting to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        refhsv = cv2.cvtColor(ref, cv2.COLOR_BGR2HSV)
        l_h = cv2.getTrackbarPos("L - H", "Trackbars")
        l_s = cv2.getTrackbarPos("L - S", "Trackbars")
        l_v = cv2.getTrackbarPos("L - V", "Trackbars")
        u_h = cv2.getTrackbarPos("U - H", "Trackbars")
        u_s = cv2.getTrackbarPos("U - S", "Trackbars")
        u_v = cv2.getTrackbarPos("U - V", "Trackbars")
        lower= np.array([l_h, l_s, l_v])
        upper = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower, upper)
        maskref = cv2.inRange(refhsv, lower, upper)

        #cleaning the mask
        mask = cv2.erode(mask,kernal)
        mask = cv2.dilate(mask,kernal)
        last = cv2.bitwise_or(image, image, mask = mask)

        maskref = cv2.erode(maskref,kernal)
        maskref = cv2.dilate(maskref,kernal)
        inv = cv2.bitwise_or(ref,ref,mask = maskref)
        #Show results 
        cv2.imshow("frame", last)
        cv2.imshow("HSV",hsv)
        cv2.imshow("Trackbars", inv)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break

    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
