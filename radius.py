import math
import random

home = [random.randint(0,10),random.randint(0,10)]
points = []
for i in range(random.randint(1,10)):
    points.append([random.randint(0,10),random.randint(0,10)])

def closest():
    tempc = []
    for i in range(len(points)):
        temp = distance([0,0], points[i][0], points[i][1])
        print(temp)
        tempc.append(temp)
    return tempc.index(min(tempc))

def distance(p1, p2, p3):
    return math.sqrt(((p2-p1[0])**2) + ((p3-p1[1])**2))


print('Welcome, points are:')
print("home: ", home, "Points: ", points)
print(closest())
