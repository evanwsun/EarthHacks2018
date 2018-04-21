import json
import math

walkDist = 0
driveDist = 0
bikeDist = 0
xCor = 0
yCor = 0
prevXCor = 0
prevYCor = 0
distance = 0
xDiff = 0
yDiff = 0
walkConf = 0
bikeConf = 0
driveConf = 0
with open("practice.json") as data:
    d = json.load(data)
    jData = d["locations"]
    for location in jData:
        xCor = location.get("latitudeE7") / 1E7
        yCor = location.get("longitudeE7") / 1E7
        xDiff = abs(xCor-prevXCor)
        yDiff = abs(yCor - prevYCor)
        a = (math.sin(yDiff / 2))**2 + math.cos(prevYCor) * math.cos(yCor) * (math.sin(xDiff / 2))**2
        c = 2 * math.atan2(a**0.5, (1 - a)**0.5)
        d = 3961*c
        print d
        prevXCor = xCor
        prevYCor = yCor
        activities = location.get("activity")
        print activities
        for act in activities:
            print act
        # act = activities["activity"]
        # print act
        # for obj in act:
        #     type = obj.get("type")
        #     if (type == "ON_FOOT"):
        #         walkConf = walkConf + obj.get("confidence")
        #     elif (type == "IN_VEHICLE"):
        #         driveConf = driveConf + obj.get("confidence")
        # if (walkConf > driveConf):
        #     walkDist += d
        # else:
        #     driveDist +=d
        # print "Walk:",walkDist
        # print "Drive:",driveDist


