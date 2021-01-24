import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import math

# This program creates an object using the corners by applying it to the linear equation ax+by+c=0
# Then, using the min/max values for x and y aswell as the direction, it is able to determine which side
# a point in space is from the line. If the point is to the left of the line and within the bounds of
# y, a counter will be incremented. If this counter is odd, then we know the point is within the object
# In order to prevent a rare corner case, I had to calculate the number of lines to the right of the
# point as well. If both of those values are odd, then the program will return true meaning the point is
# inside the object. If those values don't match then we ran into the corner case and will return false,
# if they are both even or zero then the point is outside of the object.

# if the point is outside of the object, this program is also able to determine how far away the
# closest boundary of the object is to the point. This is done by converting the ax+by+c=0 into
# the form of y=mx+b. From there, the program can convert that into an equation perpendicular to
# the object boundary that will pass through the point. This is the shortest distance to that line.
# After that, it is as simple as finding the closest line to determine how far away the object is.
# (further notes about how this is done will be in the program)

# I also set up a testing environment that will display a graph of the object aswell as the point
# this is to aid in debuging and can visually show the program working.
# The output is whether the point is inside or outside the object, if it is outside then the program
# will print the coordinates of intersection as well as the distance to the intersection so we can know
# where and how far the closest point is

# The line class defines a line in space, each object will be made up of at least 3 of these
# It contains the start point and end point (p1 and p2) as well as the values for the linear equation,
# the min/max of x and y, and the direction of the line
class Line:
    def __init__(self, p1, p2, a, b, c, xMin, xMax, yMin, yMax, direction):
        self.p1 = p1
        self.p2 = p2
        self.a = a
        self.b = b
        self.c = c
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.direction = direction
    def print_line(self, home):
        print('p1:', self.p1, 'p2:', self.p2, 
        '\na:', self.a, 'b', self.b, 'c', self.c, 
        '\nxMin:', self.xMin, 'xMax:', self.xMax, 'yMin:', self.yMin, 'yMax:', self.yMax, 
        '\nax + by + c=', (self.a*home[0] + self.b*home[1] + self.c),
        '\ndirection:', self.direction, '\n')

# This will simply display the object on a graph with the point
def display_plot(x, y, home):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(home[0], home[1], "-bo")

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("test.png")
    plt.show()

# Home is the point the user is testing, a custom object can be defined by entering the x and y values of each point
def custom_test():
    points=[]
    x = []
    y = []

    home = [2,1]
    x = [4,4]
    y = [0,-2]

    for i in range(len(x)):
        points.append([x[i], y[i]])
    points.append([x[0], y[0]])
    x.append(x[0])
    y.append(y[0])
    N = len(x)
    obj = create_object(x, y)
    if(is_inside(obj, home)):
        print('Inside')
    else:
        print('Outside')
        distance_to_object(obj, home)
    display_plot(x, y, home)
    return obj

# this will create a randomly generated object. The size can be expanded by changing the value of size
# this will determine the scale of the plane the program is operating in.
# The first value of N is the minimum number of points used to create the object, the second value is the maximum
# make sure N is at least three otherwise the program may not be able to make an object
def auto_test():
    size = 10
    points=[]
    x = []
    y = []
    N = random.randint(3,5)
    home = [random.randint(-size, size),random.randint(-size, size)]
   
    for i in range(N):
        x.append(random.randint(-size, size))
        y.append(random.randint(-size, size))
        points.append([x[i], y[i]])
    points.append([x[0], y[0]])
    x.append(x[0])
    y.append(y[0])
    obj = create_object(x, y)
    # print(is_inside(obj, home))
    if(is_inside(obj, home)):
        print('Inside')
    else:
        print('Outside')
        distance_to_object(obj, home)
    display_plot(x, y, home)
    return obj

# create_object will take the location of the points defined in the test functions
# It will group each index into a single point and pass sequential points to the create_line
# function that will define the values that make up the line between those two points
# upon completion, create_object will return an object that is made up of a list of lines
def create_object(x, y):
    obj = []
    p1 = []
    p2 = []

    for i in range(len(x) - 1):
        p1 = [x[i], y[i]]
        p2 = [x[i+1], y[i+1]]
        obj.append(create_line(p1, p2))
    return obj

# prints out all the values for the lines that define the object
# used for debugging
def print_object(obj, home):
    for i in range(len(obj)):
        obj[i].print_line(home)

# create_line works by taking two points and defining the values that will make up the line between them
# in the form ax+by+c=0. a=(y1-y2), b=(x2-x1), and c=(x1*y2 + x2*y1).
# the min/max values are simply the minimum and maximum values of x and y that are within the bounds of the line
# without them the line would run out to infinity in both directions
# finally, it will return all of these as a line object and make a call to get the direction of the line
# based off the two points
def create_line(p1, p2):
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = (p1[0]*p2[1])-(p1[1] * p2[0])

    xMax = max(p1[0], p2[0])
    xMin = min(p1[0], p2[0])
    
    yMax = max(p1[1], p2[1])
    yMin = min(p1[1], p2[1])

    return Line(p1, p2, a, b, c, xMin, xMax, yMin, yMax, get_direction(p1, p2))

# get_direction will use the values in p1 and p2 to determine the direction the line is going
# the actual direction is irrelevent but it needs to be uniform in order to define the corners of the
# object correctly. Otherwise, if the point is parallel with a corner, the program will not be able to
# determine if the point is inside or outside the object.
# the return values are as follows:

#    0 - horizontal line
#    1 - diagonal left to right and lower to higher
#    2 - diagonal left to right and higher to lower
#    3 - diagonal right to left and lower to higher
#    4 - diagonal right to left and higher to lower
#    5 - vertical line running down
#    6 - vertical line running up

def get_direction(p1, p2):
    if p1[0] < p2[0]:
        if p1[1] < p2[1]:
            return 1
        elif p1[1] > p2[1]:
            return 2
        else:
            return 0
    elif p1[0] > p2[0]:
        if p1[1] < p2[1]:
            return 3
        elif p1[1] > p2[1]:
            return 4
        else:
            return 0
    else:
        if p1[1] > p2[1]:
            return 5
        if p1[1] < p2[1]:
            return 6
    
# is_inside can determine if the point home is within the object.
# the values of tmp1 and tmp2 are the counters for determining how many lines the point is
# to the left of and right of respectively
# The process of determining left and right is the same, just the inequalities are flipped
# Left side:
# loop through all the lines defined in obj
# determine if the x coordinate for the point is less than the maximum value of x for the current line
# use the direction to determine which inequality to use, if the line is running lower to higher the value
# of ax+by+c needs to be greater than or equal to 0 to determine if the point is to the left,
# if the line runs higher to lower then the inequality flips to less than or equal to
# if either of this is true then tmp1 is incremented
# 
# The right side is determined the same
# if both tmp1 and tmp2 are odd, is_inside returns true indicating the point is inside the object
# if they are unequal, zero or even then the point is outside the object
def is_inside(obj, home):
    tmp1 = 0
    tmp2 = 0

    x = home[0]
    y = home[1]
    # left side
    for i in range(len(obj)):
        a = obj[i].a
        b = obj[i].b
        c = obj[i].c
        if(x < obj[i].xMax):
            if (obj[i].direction == 1 or obj[i].direction == 3 or obj[i].direction == 6):
                if(y <= obj[i].yMax and y > obj[i].yMin):
                    if((a * x + b * y + c) >= 0):
                        tmp1 = tmp1 + 1
            elif (obj[i].direction == 2 or obj[i].direction == 4 or obj[i].direction == 5):
                if(y < obj[i].yMax and y >= obj[i].yMin):
                    if((a * x + b * y + c) <= 0):
                        tmp1 = tmp1 + 1

    # right side
    for i in range(len(obj)):
        a = obj[i].a
        b = obj[i].b
        c = obj[i].c
        if(x > obj[i].xMin):
            if (obj[i].direction == 1 or obj[i].direction == 3 or obj[i].direction == 6):               
                if(y <= obj[i].yMax and y > obj[i].yMin):
                    if((a * x + b * y + c) <= 0):
                        tmp2 = tmp2 + 1
            elif (obj[i].direction == 2 or obj[i].direction == 4 or obj[i].direction == 5):
                if(y < obj[i].yMax and y >= obj[i].yMin):
                    if((a * x + b * y + c) >= 0):
                        tmp2 = tmp2 + 1

    # determine if tmp1 and tmp2 are odd
    tmp1 = tmp1 % 2
    tmp2 = tmp2 % 2

    if(tmp1 == 1 and tmp2 == 1):
        return True
    else:
        return False

# distance_to_object will loop through all of the lines that define the object and
# get the closest point of that line to the point
# finally it will send the information for the closest point
def distance_to_object(obj, point):
    tmp = []
    minI = 0
    for i in range(len(obj)):
        tmp.append(line_distance(obj[i], point))
        if(tmp[i][2] < tmp[minI][2]):
            minI = i
    print('closest point: \n\tx:', tmp[minI][0], 'y:', tmp[minI][1], 'distance:', tmp[minI][2])
    print('\nclosest point to all lines:')
    for i in range(len(tmp)):
        print('\tp1:', obj[i].p1, '\tp2:', obj[i].p2, '\tx:', tmp[i][0], '\ty:', tmp[i][1], '\tdistance:', tmp[i][2], '\n')
    return tmp[minI]
    
# A line is defined by the equation ax+by+c=0. This can be changed into y=mx+b by
# using the form y=(a/-b)*x + (c/-b). A perpendicular line can be created using y=(b/a)*x + p.
# p is defined as y-(b/a)*x and then applying the x and y coordinates of the point to it.
# The x value of the point of intersection can be calculated by solving (a/-b)*x + (c/-b) = (b/a)*x + p for x.
# When solved for x this takes the form of x=(p + (c/b)) / ((a^2 + b^2) / (-b * a)) 
# From there, the y value can be calculated by plugging x into any of these y=mx+b functions.
# if the values of x and y that were calculated are within the bounds of the line then line_distance
# will pass the values of x and y along with the coordinates stored in point to the point_distance function
# in order to determine how far away the point is 
# 
# There are some corner cases here that need to be solved. If the lines are vertical or horizontal
# there would be a divide by zero error using the above method. Fortunately, the closest point of a vertical and
# horizontal line is easy to calculate. The closest point of a horizontal line is directly above or below the point
# so the x value is that of the point and the y value is that of the line
# a vertical line is the y value of the point and the x value of the line
# 
# One problem with the top method of finding the closest point is the line the equations define will stretch out to
# infinity in either direction. There could be a point on the line closer to point that is beyond the max/min values that
# define the line. If this happens then the closest point would be one of the ends of the line so line_distance will send each
# end of the line as well as point to the point_distance function.
#
# finally, line_distance will return the closest coordinates in the line to the point. If the corners are the same distance then this will
# just send the info for the first corner
def line_distance(line, point):
    p1 = line.p1
    p2 = line.p2
    p3 = point

    a = line.a
    b = line.b
    c = line.c
    # calculate the values of x and y that are closest to point as long as the line isn't vertical or horizontal
    if(a != 0 and b != 0):
        p = p3[1] - (b/a)*p3[0]
        x = (p + (c/b))/(((a**2) + (b**2))/(-b*a))
        y = (b/a)*x + p
    
    # vertical and horizontal lines
    else:
        if(a == 0):     # horizontal line
            x = point[0]
            y = line.p1[1]
        if(b == 0):     # vertical line
            x = line.p1[0]
            y = point[1]

    # if the closest point is inside the bounds of x and y, calculate the distance from point to the line and return the
    # coordinates along with the distance
    if(y <= line.yMax and y >= line.yMin):
        if(x <= line.xMax and x >= line.xMin):
            return [x, y, point_distance([x,y], point)]

    # If the nearest x and y are outside the bounds of the line, then calculate the distance to each end and return the closest 
    p1dist = point_distance(line.p1, point)
    p2dist = point_distance(line.p2, point)

    if(p1dist < p2dist):
        return [line.p1[0], line.p1[1], p1dist]
    elif(p1dist > p2dist):
        return [line.p2[0], line.p2[1], p2dist]
    elif(p1dist == p2dist):
        return [line.p1[0], line.p1[1], p1dist]

# point_distance calculates the distance between two points using the pythagorean theorem
def point_distance(p1, p2):
    return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))


# custom_test()
auto_test()