import math
import itertools
import random
import time

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

def intilializer(cityList) :
    random.shuffle(cityList)
    return cityList

def generateNeighbourhood(route) :
    neighbourhood = []
    clone = []
    for index1, cityA in enumerate(route) :
        for index2, cityB in enumerate(route) :
            if (index1 != index2) :   
                clone = route[:]
                # print('clean_clone: ', clone)
                clone[index1] = cityB
                clone[index2] = cityA
                # print('clone: ', clone, index1, index2)
                if clone not in neighbourhood :
                    neighbourhood.append(clone)
    # print('neighbourhood : ', neighbourhood)
    return neighbourhood

def permuteRoutes(cityList) :
    return list(itertools.permutations(range(len(cityList))))

def runTSP_2(graph) :
    cityList = list(range(len(graph)))
    route = intilializer(cityList)
    print('route: ', route)
    startTime = time.time()
    currentTime = time.time()
    TERMINATION_TIME = 10
    bestCost = getCostOfRoute(route, graph)
    bestRoute = []

    while (currentTime - startTime) < TERMINATION_TIME:
        neighbourhood = generateNeighbourhood(route)
        print('NEW ROUTE: ', route)

        previousCost = bestCost
        for neighbour in neighbourhood : 
            neigbourCost = getCostOfRoute(neighbour, graph) 
            print('neigbour: ', neighbour, ' cost', neigbourCost)
            if neigbourCost < bestCost :
                bestCost = neigbourCost
                bestRoute = neighbour
                route = neighbour
                print('route: ', route , ' cost: ', bestCost )
        # print('bestCost: ', bestCost , ' previousCost: ', previousCost )
        if bestCost == previousCost :
            route = intilializer(cityList)
        currentTime = time.time()
        print('time left', TERMINATION_TIME - (currentTime - startTime))
        print('bestRoute: ', bestRoute , ' bestCost: ', bestCost )

def stepFunction(route, cityList,  previousCost) : 
    neighbourhood = generateNeighbourhood(route)
    nextRoute = []
    bestCost = getCostOfRoute(route, cityList)
    
    for neighbour in neighbourhood : 
            neigbourCost = getCostOfRoute(neighbour, cityList)
            if neigbourCost < bestCost :
                nextRoute = neighbour
    
    if bestCost == previousCost :
        return [nextRoute, bestCost]
    stepFunction(nextRoute, bestCost)


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
# routes = permuteRoutes(graph)
# runTSP_1(routes, graph)
runTSP_2(graph)