# Python program to save a video using OpenCV 

#imports
import cv2
import argparse as ap
from datetime import datetime
now = datetime.now().time() # time object
hour = str(now.hour)
minute = str(now.minute)
time = "{}_{}.avi".format(hour,minute)

create_video = False


#using built in camera, to change it just put the directory to the video
video = cv2.VideoCapture(1)
_, tframe = video.read()
size = (tframe.shape[1],tframe.shape[0])
print(tframe.shape)

#user input argument to save or not
parser = ap.ArgumentParser(description="Recording vision output")
parser.add_argument('--record', choices=['yes', 'no'], default='no')

args = parser.parse_args()
if args.record == 'yes':
	create_video =True


if (video.isOpened() == False):  
    print("Error reading video file")
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
   
#size = (frame_width, frame_height) 

#output format of the video   
result = cv2.VideoWriter(time,cv2.VideoWriter_fourcc(*'MJPG'), 27, size)

while(True): 
    ret, frame = video.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #print('{}'.format(gray.shape) + 'gray')
    #print('{}'.format(frame.shape) + 'frame')
  
    if ret == True:

    	if create_video == True:
    		result.write(frame)

        cv2.imshow('Frame', frame)
        #cv2.imshow('gray',gray) 
  
        # Press S on keyboard  
        # to stop the process 
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
  
    # Break the loop 
    else: 
        break
  
# When everything done, release  
# the video capture and video  
# write objects 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 
