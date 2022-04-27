# Custom class to handle transfering data between two rasberry pis.
# Class is condensed into byte stream using the pickle library and sent via TCP sockets
# Class can easily be expanded to accomodate additional data structures as necessary
#
#

class ITH:
    def __init__(self, header, image, coordinates, vector, distance, xAngleDisp, motion):
        self.header = header #description of type of data being transmitted, string
        self.image = image #stores the actual cropped image being sent
        self.coordinates = coordinates #stores pixel coordinates of a tracked object, tuple of coords, format: y1,x1,y2,x2
        self.vector = vector #stores the calculated movement vector, three elements, X,Y,Z movement vectors. Assembled they form a 3d vector
        self.distance = distance #distance to tagre
        self.xAngleDisp = xAngleDisp #x angular displacement in degrees per second used for collision calculations
        self.motion = motion #tuple of average mag/ang values used, for motion speech