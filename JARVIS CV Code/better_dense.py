# Example code for dense optical flow using openCV
#
# Original Source: https://docs.opencv.org/3.4/d4/dee/tutorial_optical_flow.html
# Pulled directly from openCV example materials
#
import re
import numpy as np
import ITH
import cv2 as cv
import time
import math
from itertools import chain
from skimage.measure import label
from skimage.measure import regionprops
import distanceFinder
from scipy import stats
from socket import *
import pickle

font = cv.FONT_HERSHEY_SIMPLEX
fontScale = .25
color = (255, 0, 0)
thickness = 1
thickness2 = 5
TRANSMITTING = False
LIMIT_FPS = False
#We're doing TCP over here now I guess

if(TRANSMITTING):
    serverPort = 42069
    serverName = "169.254.46.181" #Ip Address of rasberry Pi
    clientSocket = socket(AF_INET, SOCK_STREAM)
    ENDSTRING = "wake me up when september ends".encode()
    STARTSTRING = "ready".encode

def distance(a,b):
    return(pow(abs(a[0] - b[0]), 2) + pow(abs(a[1] - b[1]), 2))

def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    try:
        i = (np.abs(arr - input_value)).argmin()
        if (np.abs(arr[i] - input_value)) < 1:
            return i
        else:
            return -1
    except ValueError as e:
        return -1



def nearestCoordIndex(listOfCoords, currentCoord):
    try:
        nearest = min(listOfCoords, key=lambda x: distance(x, currentCoord))
        if(distance(nearest,currentCoord) < 20):
            #print(listOfCoords.index(nearest))
            return (listOfCoords.index(nearest))
        return -1
    except ValueError as e:
        return -1

def angleCorrection(ang):
    return (ang + 180)%360


#Generates linear relationsip between distance and pixel movement and returns speed of target in meters
def pixelsToMeters(pixelHeight, magnitude):
    return magnitude * (distanceFinder.real_target_height / pixelHeight)


def get_index_positions(list_of_elems, element):
    ''' Returns the indexes of all occurrences of give element in
    the list- listOfElements '''
    index_pos_list = []
    index_pos = 0
    while True:
        try:
            # Search for item in list from indexPos to the end of list
            index_pos = list_of_elems.index(element, index_pos)
            # Add the index position in list
            index_pos_list.append(index_pos)
            index_pos += 1
        except ValueError as e:
            break
    return index_pos_list

def regionEdge(matrix, value):
    ones = np.where(matrix == value, 1, 0)
    # print(ones)
    a = np.mean(ones, axis=1)  # rows
    # print(a)
    b = np.mean(ones, axis=0)  # columns
    # print(b)
    top = np.argmax(a > 0)
    left = np.argmax(b > 0)
    a = np.flip(a)
    b = np.flip(b)
    bottom = len(a) - np.argmax(a > 0) - 1
    right = len(b) - np.argmax(b > 0) - 1

    return (top, bottom, left, right)

def shakeFilter(matrix, uniqueVals):
    totalEntries = matrix.shape[0] * matrix.shape[1]
    for i in range(len(uniqueVals)):
        val = uniqueVals[i]
        if(val != 0):
            count = np.count_nonzero(matrix == val)
            if ((count / totalEntries) > .4):
                matrix = np.where(matrix == val, 0, matrix)
                print("Attempted to clean: ", val)
    return matrix


def betterDense(videoName):
    #cap = cv.VideoCapture(0)
    readyToTransmit = True
    prepared = False
    messageList = list()
    lastTransmittedTime = 2147483647
    distanceList = list()
    timeOutList = list()
    cap = cv.VideoCapture(cv.samples.findFile(videoName))
    ret, frame1 = cap.read()
    prvs = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
    timeBetweenFrames = .25
    numFrames = 1
    #hsv = np.zeros_like(frame1)
    #print(hsv)
    #hsv[..., 1] = 255
    if(TRANSMITTING):
        clientSocket.connect((serverName, serverPort))
    while(1):
        ret, frame2 = cap.read()
        startTime = time.time()
        if not ret:
            print('No frames grabbed!')
            break
        #print(frame2.shape[1], frame2.shape[0])
        next = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        flow = cv.calcOpticalFlowFarneback(prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        mag, ang = cv.cartToPolar(flow[:,:, 0], flow[:,:, 1], angleInDegrees = True)
        #ang = np.degrees(ang)
        #uniqueVals = list(set(chain(*mag)))
        #mag2 = shakeFilter(mag, uniqueVals)
        mag = np.where(mag < 1, 0, mag)
        mag2 = np.where(mag < 1, 0, 1)
        mag2 = mag2.astype('uint8')

        morph = cv.morphologyEx(mag2, cv.MORPH_OPEN, np.ones((3,3),dtype = np.uint8))
        morph = cv.morphologyEx(morph, cv.MORPH_CLOSE, np.ones((3, 3), dtype=np.uint8))
        morph = label(morph, connectivity =1)
        Object = 0
        for r in regionprops(morph):
                coordString = ('({},{}),({},{})'.format(*r.bbox))
                s = [float(s) for s in re.findall(r'-?\d+\.?\d*', coordString)]
                s = np.array(s)
                s = s.astype('int')
                y1 = s[0]
                x1 = s[1]
                y2 = s[2]
                x2 = s[3]
                cropImage = frame2[y1:y2,x1:x2].copy()
                if((cropImage.shape[0] > 15) and (cropImage.shape[1] > 15)):
                    if ((cropImage.shape[0] < 440) and (cropImage.shape[1] < 600)):
                        if( ((cropImage.shape[1] * 1.2) < cropImage.shape[0]) ):
                            mag3 = mag[y1:y2,x1:x2]
                            ang2 = ang[y1:y2,x1:x2]
                            ang2 = ang2 - 180
                            height = y2 - y1
                            distanceToTarget = distanceFinder.Distance_finder(height)
                            distanceToTarget = round(distanceToTarget, 2)
                            mag3[mag3 == 0] = np.nan
                            AvgMag = np.nanmean(mag3)
                            if(AvgMag == np.inf):
                                AvgMag = 0
                            AvgAng = stats.circmean(ang2, high=360)
                            AvgAng = angleCorrection(AvgAng)
                            #cv.imshow('Crop', cropImage)
                            frame2 = cv.rectangle(frame2, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            string = "Object:" + str(Object)
                            org1 = (x1, y1 - 5)
                            org2 = (x1, y2 -50)
                            frame2 = cv.putText(frame2, string, org1, font, fontScale, color, thickness, cv.LINE_AA)
                            midX = int((x1 + x2) / 2)
                            midY = int((y1 + y2) / 2)
                            xPixelDisp = AvgMag * np.cos(AvgAng)
                            xPixelDisp = xPixelDisp/timeBetweenFrames
                            xAngleDisp = .078 * xPixelDisp

                            AvgMag = pixelsToMeters(height, AvgMag)
                            AvgMag = (AvgMag/timeBetweenFrames)


                            xComp = AvgMag * np.cos(AvgAng)
                            yComp = AvgMag * np.sin(AvgAng)

                            AvgMag = round(AvgMag, 2)
                            AvgAng = round(AvgAng, 2)
                            xComp = round(xComp, 2)
                            yComp = round(yComp, 2)

                            print("X Component of object: ",Object, xComp)
                            print("Y Component of object: ",Object, yComp)
                            print("Distance to Object: ", Object, distanceToTarget)
                            #nextX = int(midX + AvgMag * np.cos(AvgAng))
                            #nextY = int(midY + AvgMag * np.sin(AvgAng))
                            #frame2 = cv.arrowedLine(frame2, (midX, midY), (nextX, nextY), color, thickness2)
                            string = "M/s: " + str(AvgMag) + " Angle: " + str(AvgAng) + " Distance: " + str(distanceToTarget)
                            frame2 = cv.putText(frame2, string, org2, font, fontScale, color, thickness, cv.LINE_AA)
                            Object = Object + 1
                            #print("Time between frames:",timeBetweenFrames)
                            distanceIndex = closest_value(distanceList,distanceToTarget)
                            if(distanceIndex == -1):
                                distanceList.append(distanceToTarget)
                                timeOutList.append(3)
                                zComp = 0
                                print("Distance Unidentified, adding:", distanceToTarget, "to list")
                            else:
                                zComp = (distanceToTarget - distanceList[distanceIndex])/timeBetweenFrames
                                print("Distance identified, distance:", distanceToTarget, "is close to distance:",distanceList[distanceIndex])
                                distanceList[distanceIndex] = distanceToTarget
                                timeOutList[distanceIndex] = 5
                            print("zComp of Object:", Object, "is" ,zComp)
                            if(TRANSMITTING):
                                if(readyToTransmit):
                                    #Transmission
                                    print("Writing Transmission---------------------")
                                    storage = ITH.ITH(Object,cropImage,(y1,x1,y2,x2),(xComp,yComp,zComp), distanceToTarget, xAngleDisp, (AvgAng, AvgMag))
                                    message = pickle.dumps(storage, pickle.DEFAULT_PROTOCOL)
                                    messageList.append(message)
                                    prepared = True
        if(TRANSMITTING):
            if(readyToTransmit & prepared):
                returnedMessage = clientSocket.recv(1024)
                print(returnedMessage.decode())
                print("TRANSMITTING------------------------")
                size = len(messageList)
                clientSocket.send(str(size).encode())
                time.sleep(.5)
                for i in range(len(messageList)):
                    #clientSocket.connect((serverName, serverPort))
                    print("Sending object ", i)
                    #print("Contains:", messageList[i])
                    message = messageList[i]
                    clientSocket.sendto(message, (serverName, serverPort))
                    #clientSocket.close()
                    time.sleep(.25)
                    clientSocket.send(ENDSTRING)
                    print("Waiting on confirm")
                    returnedMessage = clientSocket.recv(1024) #waits for a return message, anything
                    print(returnedMessage.decode())
                    print("Confirm recievd")
                prepared = False
                readyToTransmit = False
                lastTransmittedTime = time.time()
                #clientSocket.close()
                messageList.clear()

        if (timeOutList != []):
            timeOutList = [x - 1 for x in timeOutList]
            print(timeOutList)
            listOfTimedOutDistances = np.where((np.asarray(timeOutList)) == 0)[0]
            print(listOfTimedOutDistances)
            count = 0
            for x in listOfTimedOutDistances:
                print("Deleting index:", x)
                del timeOutList[x-count]
                del distanceList[x-count]
                count = count + 1
        #listOfTimedOutDistances = np.empty(listOfTimedOutDistances)
        #print(time.time())
        #print(lastTransmittedTime)
        #print(time.time() - lastTransmittedTime)
        if(TRANSMITTING):
            if(time.time() - lastTransmittedTime > 5):
                readyToTransmit = True
                print("Ready to Transmit--------------------------------------------------")
            #hsv[..., 0] = ang*180/np.pi/2
            #hsv[..., 2] = cv.normalize(mag2, None, 0, 255, cv.NORM_MINMAX)

        #bgr = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
        timeBetweenFrames = time.time() - startTime
        if(LIMIT_FPS):
            if(timeBetweenFrames < .25):
                time.sleep(.25-timeBetweenFrames)
                timeBetweenFrames = time.time()-startTime
        numFrames = numFrames + 1
        cv.imshow('frame2', frame2)
        k = cv.waitKey(30) & 0xff
        #time.sleep(.5)
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite('opticalfb.png', frame2)
            #cv.imwrite('opticalhsv.png', bgr)
        prvs = next
        #time.sleep(5)
    cv.destroyAllWindows()
    if(TRANSMITTING):
        clientSocket.close()
    return numFrames