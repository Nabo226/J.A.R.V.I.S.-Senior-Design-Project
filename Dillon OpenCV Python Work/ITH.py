# Custom class to handle transfering data between two rasberry pis.
# Class is condensed into byte stream using the pickle library and sent via UDP sockets
# Class can easily be expanded to accomodate additional data structures as necessary
#
#

class ITH:
    def __init__(self, header, image, coordinates, vector):
        self.header = header #description of type of data being transmitted
        self.image = image #stores the actual image
        self.coordinates = coordinates #stores pixel coordinates of a tracked object
        self.vector = vector #stores the calculated movement vector