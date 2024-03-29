import math
import random

'''
    Travelling Salesman Problem represententation and it's common methods
'''


def randomRouteGenerator(cityList) :
    random.shuffle(cityList)
    return cityList

def getSubRoutes(route) :
    subRoutes = []
    for index in range(len(route)) :
            if index > 0 : 
                subRoutes.append([route[index - 1], route[index]])
    
    subRoutes.append([route[len(route) - 1], route[0]])
    return subRoutes

def getCostOfRoute(route, cityList) :
        # print('cityList: ', cityList, 'route: ', route)
        cost=0
        subRoutes = getSubRoutes(route)

        for subRoute in subRoutes :
            cost+= distanceToCost(cityList[subRoute[0]], cityList[subRoute[1]])
        return cost

def distanceToCost(aSet, bSet) :
    cost = math.sqrt(
        math.pow((bSet[0] - aSet[0]), 2) +
        math.pow((bSet[1] - aSet[1]), 2)
    )
    return cost

def readCSV(short = False) :
    if short :
        file = open('ulysses9.csv', 'r')
    else :
        file = open('ulysses16.csv', 'r')
    cityPositions = []
    contents = file.readlines()
    for index, line in enumerate(contents) :
        if (index > 1 ) :
            lineContents = line.strip().split(',')
            length = len(lineContents)
            # get the city x and y coords
            cityPositions.append(
                [float(lineContents[length - 2]),
                float(lineContents[length - 1])]
            )
    return cityPositions
