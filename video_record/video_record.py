import cv2
import argparse as ap
from datetime import datetime
now = datetime.now().time() # time object
hour = str(now.hour)
minute = str(now.minute)
time = "{}_{}.avi".format(hour,minute)



class video_record():

	def __init__(self,cap,choice):
		self.cap = cap
		self.choice = choice
		self.video = cv2.VideoCapture(self.cap)
		self.create_video = False

		self.fps = 24

		if (self.choice == 'yes'):
			self.create_video = True

		if (self.video.isOpened() == False):
			print("video captureing error")

		_, tframe = self.video.read()
		self.size = (tframe.shape[1],tframe.shape[0])


	def record(self):
		self.result = cv2.VideoWriter(time,cv2.VideoWriter_fourcc(*'MJPG'),self.fps, self.size)
		while(True):
			ret,frame = self.video.read()

			if ret == True:
				if self.create_video == True:
					self.result.write(frame)

				cv2.imshow("Frame",frame)
				if cv2.waitKey(1) & 0xFF == ord('s'):
					break

			else:
				break



if __name__ == '__main__':
	parser = ap.ArgumentParser(description="Recording vision output")
	parser.add_argument('--record', choices=['yes', 'no'], default='no')
	args = parser.parse_args()
	choice = args.record
	video = video_record(1,choice)
	video.record()
	video.video.release()
	cv2.destroyAllWindows()
