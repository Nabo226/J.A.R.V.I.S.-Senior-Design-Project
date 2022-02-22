# Main function code for JARVIS system
#
# Includes several test functions and serves as a "playground" for testing until final implementation
#
#

import numpy as np
import cv2
import time
import lucas_kanade_OF2
from socket import *
import pickle
from ITH import ITH
from better_dense import *


serverName = "169.254.46.181"
#serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)


def main():
    #lucas_kanade_OF2.lucas_kanade_method('people.mp4')
    imageName = "msTimerZoomedIn.PNG"
    storage1 = ITH("According to all known laws of aviation...", cv2.imread(imageName, cv2.IMREAD_COLOR),(2.55555, 4.7758),(187.5, 5.44))

    #print("Detecting Object at X:", storage.coordinates[0], "and Y:", storage.coordinates[1], "in Image:", imageName, "with vector radius:", storage.vector[0], "and magnitude:", storage.coordinates[1])

    message = pickle.dumps(storage1, pickle.DEFAULT_PROTOCOL)
    messageLength = len(message)/8
    print(messageLength)
    #print(message)
    storageVessel = message[0]
    print(storageVessel)
    storageVessel = message[1]
    print(storageVessel)
    storageVessel = message[0:10]
    #print(message)
    print(storageVessel)

    #for x in range():
    #    storageVessel = message[x-2047:x]


    #clientSocket.sendto(message, (serverName, serverPort))
    clientSocket.close()
    storage2 = pickle.loads(message)
    storage1.image = 'NULL'
    #print("Detecting Object at X:", storage2.coordinates[0], "and Y:", storage2.coordinates[1], "in Image:", imageName,
         # "with vector radius:", storage2.vector[0], "and magnitude:", storage2.coordinates[1])
    cv2.imshow("yeah", storage2.image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #main()
    startTime = time.time()
    betterDense("newtest_3fps.mp4")
    print("--- %s seconds ---" % (time.time() - startTime))
    startTime = time.time()
    betterDense("newtest_4fps.mp4")
    print("--- %s seconds ---" % (time.time() - startTime))
    startTime = time.time()
    betterDense("newtest_5fps.mp4")
    print("--- %s seconds ---" % (time.time() - startTime))
    startTime = time.time()
    betterDense("newtest_6fps.mp4")
    print("--- %s seconds ---" % (time.time() - startTime))