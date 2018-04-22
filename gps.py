import json
from math import sin,cos,atan2,sqrt,radians
import pandas as pd

global walkDist
walkDist = 0
global driveDist
driveDist = 0
global bikeDist
bikeDist = 0
xCor = []
yCor = []
times = []
distance = 0
xDiff = 0
yDiff = 0
fileName = "history.json"

def setFileName(x):
    fileName = x

def getData():
    with open(fileName) as data:
        d = json.load(data)
        jData = d["locations"]
        for location in jData:
            xCor.append(location.get("latitudeE7") / 1E7)
            yCor.append(location.get("longitudeE7") / 1E7)
            times.append(location.get("timestampMs"))
        df = pd.DataFrame({'Longitude': xCor, 'Latitude': yCor, 'Time': times})
        print(df)

    for i in range(1,len(xCor)):
        curXCor = radians(xCor[i])
        prevXCor = radians(xCor[i-1])
        curYCor = radians(yCor[i])
        prevYCor = radians(yCor[i-1])
        yDiff = abs(curXCor-prevXCor)
        xDiff = abs(curYCor - prevYCor)
        curTime = int(times[i])
        prevTime = int(times[i-1])
        tDiff = abs(curTime-prevTime)/60.0/60.0/1000
        a = (sin(yDiff / 2))**2 + cos(prevYCor)*cos(curYCor)*(sin(xDiff/2))**2
        if ((1-a) > 0 and 1-a < 1):
            c = 2*atan2(a**0.5, (1 - a)**0.5)
            dist = 3961 * c
            speed = dist/tDiff
            if (speed < 5):
                walkDist += dist
            elif(speed <15):
                bikeDist += dist
            else:
                driveDist += dist

def getTotalDistance():
    return walkDist+bikeDist+driveDist

def getWalkDistance():
    return walkDist

def getDriveDistance():
    return driveDist

def getBikeDistance():
    return bikeDist

getData()