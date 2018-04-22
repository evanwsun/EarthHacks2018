import json
from math import sin,cos,atan2,sqrt,radians
import pandas as pd

walkDist = 0
driveDist = 0
bikeDist = 0
xCor = []
yCor = []
times = []
distance = 0
xDiff = 0
yDiff = 0
with open("history.json") as data:
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
    # print("cur:",curTime)
    # print("prev",prevTime)
    tDiff = abs(curTime-prevTime)/60.0/60.0/1000
    # print("time:", tDiff)
    a = (sin(yDiff / 2))**2 + cos(prevYCor)*cos(curYCor)*(sin(xDiff/2))**2
    if ((1-a) > 0 and 1-a < 1):
        c = 2*atan2(a**0.5, (1 - a)**0.5)
        dist = 3961 * c
        # print("Dist:",dist)
        speed = dist/tDiff
        # print("Speed:", speed)
        if (speed < 5):
            walkDist += dist
        elif(speed <15):
            bikeDist += dist
        else:
            driveDist += dist

print("walk:",walkDist)
print("bike:", bikeDist)
print("drive:",driveDist)
