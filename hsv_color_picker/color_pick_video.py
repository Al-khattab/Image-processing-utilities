import argparse
import cv2
import numpy as np
import sys


class color_pick():
	kernal = (7,7)
	blur =(5,5)
	pixel = (0,0,0)


	def __init__(self,path,video):
		self.path = path
		self.video = video
		self.image = cv2.imread(self.path)
		self.cap = cv2.VideoCapture(self.video)

	def pick_color(self,event,x,y,flags,param):
		global up, down
		if event == cv2.EVENT_LBUTTONDOWN:
			pixel = self.hsv[y,x]
        #tolerance adjustable values
			Tolerance_1 = 15 
			Tolerance_2 = 45
        #HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
			up =  np.array([pixel[0] + Tolerance_1, pixel[1] + Tolerance_1, pixel[2] + Tolerance_2])
			down =  np.array([pixel[0] - Tolerance_1, pixel[1] - Tolerance_1, pixel[2] - Tolerance_2])
        #changing the the trackbars values 
			cv2.setTrackbarPos("L - H", "Trackbars",down[0])
			cv2.setTrackbarPos("L - S", "Trackbars",down[1])
			cv2.setTrackbarPos("L - V", "Trackbars",down[2])
			cv2.setTrackbarPos("U - H", "Trackbars",up[0])
			cv2.setTrackbarPos("U - S", "Trackbars",up[1])
			cv2.setTrackbarPos("U - V", "Trackbars",up[2])

	def nothing(self,x):
		pass

	def main(self):
		mat = np.zeros((300,300,3), np.uint8)
		cv2.imshow("HSV",mat)
		cv2.setMouseCallback("HSV", self.pick_color)
		cv2.namedWindow("Trackbars")
		cv2.createTrackbar("L - H", "Trackbars", 0, 179, self.nothing)
		cv2.createTrackbar("L - S", "Trackbars", 0, 255, self.nothing)
		cv2.createTrackbar("L - V", "Trackbars", 0, 255, self.nothing)
		cv2.createTrackbar("U - H", "Trackbars", 0, 179, self.nothing)
		cv2.createTrackbar("U - S", "Trackbars", 0, 255, self.nothing)
		cv2.createTrackbar("U - V", "Trackbars", 0, 255, self.nothing)
		while True:
        			#loading image from the user path
			_,frame = self.cap.read()
       			#adding a blure to inhance the color detection
			frame = cv2.GaussianBlur(frame,self.blur,0)

			ref = cv2.imread('circle.jpg')
			ref = cv2.resize(ref,(300,300))
			ref = cv2.GaussianBlur(ref,self.blur,0)

       			# converting to HSV color space
			self.hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			self.refhsv = cv2.cvtColor(ref, cv2.COLOR_BGR2HSV)
			l_h = cv2.getTrackbarPos("L - H", "Trackbars")
			l_s = cv2.getTrackbarPos("L - S", "Trackbars")
			l_v = cv2.getTrackbarPos("L - V", "Trackbars")
			u_h = cv2.getTrackbarPos("U - H", "Trackbars")
			u_s = cv2.getTrackbarPos("U - S", "Trackbars")
			u_v = cv2.getTrackbarPos("U - V", "Trackbars")

			lower= np.array([l_h, l_s, l_v])
			upper = np.array([u_h, u_s, u_v])
			mask = cv2.inRange(self.hsv, lower, upper)
			maskref = cv2.inRange(self.refhsv, lower, upper)
        	#cleaning the mask
			mask = cv2.erode(mask,self.kernal)
			mask = cv2.dilate(mask,self.kernal)
			last = cv2.bitwise_or(frame, frame, mask = mask)
			maskref = cv2.erode(maskref,self.kernal)
			maskref = cv2.dilate(maskref,self.kernal)
			inv = cv2.bitwise_or(ref,ref,mask = maskref)

       		#Show results 
			cv2.imshow("frame", last)
			cv2.imshow("HSV",self.hsv)
			cv2.imshow("Trackbars", inv)
			if cv2.waitKey(1) & 0xFF == ord('s'):
				break





if __name__ == '__main__':
	parser = argparse.ArgumentParser('Hsv color picker')
	parser.add_argument('-p', '--path', help ='add the location of the picture')
	args = parser.parse_args()
	path = args.path
	pick = color_pick(path,1)
	pick.main()
	cv2.destroyAllWindows()



