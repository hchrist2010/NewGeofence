import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random
import math

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

def display_plot(x, y, home):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.plot(home[0], home[1], "-bo")

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("test.png")
    plt.show()

def custom_test():
    points=[]
    x = []
    y = []

    home = [0,0]
    x = [-1,5,5,-1]
    y = [5,5,-5,-5]

    for i in range(len(x)):
        points.append([x[i], y[i]])
    points.append([x[0], y[0]])
    x.append(x[0])
    y.append(y[0])
    N = len(x)
    obj = create_object(x, y, N, home)
    print(isInside(obj, N, home))
    display_plot(x, y, home)
    return obj

def auto_test():
    points=[]
    x = []
    y = []
    N = random.randint(3,100)
    home = [random.randint(-100, 100),random.randint(-100, 100)]
   
    for i in range(N):
        x.append(random.randint(-100, 100))
        y.append(random.randint(-100, 100))
        points.append([x[i], y[i]])
    points.append([x[0], y[0]])
    x.append(x[0])
    y.append(y[0])
    obj = create_object(x, y, N, home)
    #print(isInside(obj, N, home))
    if(isInside(obj, N, home)):
        print('Inside')
    else:
        print('Outside')
        distance_to_object(obj, home)
    display_plot(x, y, home)
    return obj

def create_object(x, y, N, home):
    obj = []
    p1 = []
    p2 = []

    for i in range(len(x) - 1):
        p1 = [x[i], y[i]]
        p2 = [x[i+1], y[i+1]]
        obj.append(create_line(p1, p2))
    return obj

def print_object(obj, home):
    for i in range(len(obj)):
        obj[i].print_line(home)

def create_line(p1, p2):
    a = p1[1] - p2[1]
    b = p2[0] - p1[0]
    c = (p1[0]*p2[1])-(p1[1] * p2[0])

    xMax = max(p1[0], p2[0])
    xMin = min(p1[0], p2[0])
    
    yMax = max(p1[1], p2[1])
    yMin = min(p1[1], p2[1])

    return Line(p1, p2, a, b, c, xMin, xMax, yMin, yMax, get_direction(p1, p2))

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
    

def isInside(obj, n, home):
    tmp1 = 0
    tmp2 = 0

    #print_object(obj, home)
    x = home[0]
    y = home[1]
    for i in range(len(obj)):
        a = obj[i].a
        b = obj[i].b
        c = obj[i].c
        if(x < obj[i].xMax):
            if (obj[i].direction == 1 or obj[i].direction == 3 or obj[i].direction == 6):
                if(y <= obj[i].yMax and y > obj[i].yMin):
                    if((a * x + b * y + c) >= 0):
                        #obj[i].print_line(home)
                        tmp1 = tmp1 + 1
            elif (obj[i].direction == 2 or obj[i].direction == 4 or obj[i].direction == 5):
                if(y < obj[i].yMax and y >= obj[i].yMin):
                    if((a * x + b * y + c) <= 0):
                        tmp1 = tmp1 + 1
                        #obj[i].print_line(home)

    for i in range(len(obj)):
        a = obj[i].a
        b = obj[i].b
        c = obj[i].c
        if(x > obj[i].xMin):
            if (obj[i].direction == 1 or obj[i].direction == 3 or obj[i].direction == 6):               
                if(y <= obj[i].yMax and y > obj[i].yMin):
                    if((a * x + b * y + c) <= 0):
                        #obj[i].print_line(home)
                        tmp2 = tmp2 + 1
            elif (obj[i].direction == 2 or obj[i].direction == 4 or obj[i].direction == 5):
                if(y < obj[i].yMax and y >= obj[i].yMin):
                    if((a * x + b * y + c) >= 0):
                        tmp2 = tmp2 + 1
                        #obj[i].print_line(home)

    tmp1 = tmp1 % 2
    tmp2 = tmp2 % 2

    if(tmp1 == 1 and tmp2 == 1):
        return True
    else:
        return False

def distance_to_object(obj, point):
    tmp = []
    for i in range(len(obj)):
        tmp.append(distance(obj[i], point))
    print(tmp)
    print(tmp.index(min(tmp)),':', min(tmp))
    obj[tmp.index(min(tmp))].print_line(point)

def distance(line, point):
    #return (abs((line.p2[0] - line.p1[0]) * (line.p1[1] - point[1]) - (line.p1[0] - point[0]) * (line.p2[1] - line.p1[1]))/(math.sqrt(((line.p2[0] - line.p1[0])**2) + ((line.p2[1] - line.p1[1]) ** 2))))
    
    return (abs((line.a * point[0]) + (line.b * point[1]) + line.c)) / (math.sqrt((line.a ** 2) + (line.b ** 2)))


#custom_test()
auto_test()
#closest_line(auto_test(), [0,0])
#distance_to_object(custom_test(), [0,0])