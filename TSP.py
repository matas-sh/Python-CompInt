import math
import itertools
import random
import copy

def getCostOfRoute(route, cityList) :
        subRoutes=[]
        cost=0
        for index in range(len(route)) :
            if index > 0 : 
                subRoutes.append([route[index - 1], route[index]])
        
        subRoutes.append([route[len(route) - 1], route[0]])
        for route in subRoutes :
            cost+= distanceToCost(cityList[route[0]], cityList[route[1]])
        return cost

def distanceToCost(aSet, bSet) :
    cost = math.sqrt(
        math.pow((bSet[0] - aSet[0]), 2) +
        math.pow((bSet[1] - aSet[1]), 2)
    )
    return cost

def readCSV() :
    file = open('ulysses9.csv', 'r')
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

def intilializer(cityList) :
    print('cityList : ', cityList)
    random.shuffle(cityList)
    return cityList

def neighbourhood(route) :
    neighbourhood = []
    for index1, cityA in enumerate(route) :
        for index2, cityB in enumerate(route) :
            if (index1 != index2) :   
                clone = copy.deepcopy(route)
                clone[index1] = cityA
                clone[index2] = cityB
                print('clone: ', clone)
                neighbourhood.append(clone)
    print('neighbourhood : ', neighbourhood)
    return neighbourhood

def permuteRoutes(cityList) :
    return list(itertools.permutations(range(len(cityList))))

def runTSP_2(graph) :
     cityList = list(range(len(graph)))
     route = intilializer(cityList)
     print('route: ', route)
     neighbourhood(route)

def runTSP_1(routes, cityList) : 
    bestRoute = []
    bestCost = 100
    for route in routes :
        routeCost = getCostOfRoute(route, cityList)
        print('Route ', route, ' cost: ', routeCost)
        if (routeCost < bestCost) :
            bestCost = routeCost
            bestRoute = route
    print('best route - ', bestRoute, ' cost: ', bestCost)

graph = readCSV()
routes = permuteRoutes(graph)
# runTSP_1(routes, graph)
runTSP_2(graph)