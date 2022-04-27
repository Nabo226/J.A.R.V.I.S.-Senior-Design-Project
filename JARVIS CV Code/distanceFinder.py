

Focal_Length = 632.3529411764706;
real_distance_to_target = 2.54; #meters
real_target_height = 1.7272; #meters
pixel_of_real_target = 430; #pixel coords

#pixelWidth is calculates for each object
def Distance_finder(pixelWidth):
    distance = (real_target_height * Focal_Length) / pixelWidth
    # return the distance
    return distance

def Focal_Length_Finder():
    # finding the focal length
    focal_length = (pixel_of_real_target * real_distance_to_target) / real_target_height
    return focal_length