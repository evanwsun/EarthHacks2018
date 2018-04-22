import json
from math import sin,cos,atan2,sqrt,radians
import pandas as pd
import os

walkDist = 0
driveDist = 0
bikeDist = 0
xCor = []
yCor = []
times = []
distance = 0
xDiff = 0
yDiff = 0
global filename
fileName = "practice.json"

df = pd.DataFrame( columns=['Time', 'Distance', 'Type', 'Longitude', 'Latitude'])

def setFileName(x):
    global fileName
    fileName = x

def getData():
    global df
    global walkDist
    global driveDist
    global bikeDist
    with open(os.path.abspath(fileName)) as data:
        d = json.load(data)
        jData = d["locations"]
        for location in jData:
            xCor.append(location.get("latitudeE7") / 1E7)
            yCor.append(location.get("longitudeE7") / 1E7)
            times.append(location.get("timestampMs"))

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
                df.append([curTime, dist, "Walk", curYCor, curXCor])
            elif(speed < 15):
                bikeDist += dist
                df.append([curTime, dist, "Bike", curYCor, curXCor])
            else:
                driveDist += dist
                df.append([curTime, dist, "Drive", curYCor, curXCor])

def getTotalDistance():
    return walkDist+bikeDist+driveDist

def getWalkDistance():
    return walkDist

def getDriveDistance():
    return driveDist

def getBikeDistance():
    return bikeDist

def getDistance(month, type):
    epochHigh = month + 2628000
    epochLow = month
    return df[(int(df.Time) < epochHigh) & (int(df.Time) > epochLow) & (df.Type == type)].Distance.sum()

def getYear(year, type):
    epochLow = year
    months = {}
    for i in range(1,13):
        months.append(getDistance(epochLow,type))
        epochLow += 2628000000
    return months


def __init__(filename):
    setFileName(filename)
    getData()

getData()
