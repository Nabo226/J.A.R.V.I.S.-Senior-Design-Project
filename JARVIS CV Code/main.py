# Main function code for JARVIS system
#
# Includes several test functions and serves as a "playground" for testing until final implementation
#
#
import better_dense
import numpy
import sys
import cv2
from socket import *
import pickle
from ITH import ITH
from better_dense import *
import time
import scipy
import math
import distanceFinder
from itertools import chain
#from skimage.measure import label
import skimage
import os
filename = 'outsideTest4.mp4'
frames_per_second = 5.0
res = '480p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    '.avi': cv2.VideoWriter_fourcc(*'XVID'),
    '.mp4': cv2.VideoWriter_fourcc(*'H264'),
    #'.mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']




def main():
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    takingVid = False
    #print(distanceFinder.Focal_Length_Finder())
    numpy.set_printoptions(threshold=sys.maxsize)
    print(skimage.__version__)
    print(sys.version)
    print(scipy.__version__)
    print(cv2.__version__)
    print(numpy.__version__)

    if(takingVid):
        main()
    else:
        startTime = time.time()
        numFrames = betterDense("outsideTest3_Trim.mp4")
        print("MWCV Runtime:")
        print("--- %s seconds ---" % (time.time() - startTime))
        print("Total frames:", numFrames, "Average framerate:", numFrames/(time.time() - startTime))

    #cap = cv2.VideoCapture(0)

    #Check if the webcam is opened correctly
    '''
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=1, fy=1, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break
        elif c == ord('s'):
            cv.imwrite('NoahMeasure.png', frame)

    cap.release()
    cv2.destroyAllWindows()
    '''


