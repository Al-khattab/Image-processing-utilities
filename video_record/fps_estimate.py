import time
import cv2

video = cv2.VideoCapture(1)
num_frames = 240; # Number of frames to capture

print "Capturing {0} frames".format(num_frames)

start = time.time()# Start time

# Grab a few frames
for i in xrange(0, num_frames) :
    ret, frame = video.read()

end = time.time() # End time

seconds = end - start # Time elapsed
print "Time taken : {0} seconds".format(seconds)

# Calculate frames per second
fps  = num_frames / seconds;
print "Estimated frames per second : {0}".format(fps);
