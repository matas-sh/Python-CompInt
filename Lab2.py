import random
import time
from TravellingSalesmanProblem import getCostOfRoute, readCSV  

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674351-dt-content-rid-10882477_1/xid-10882477_1
'''

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
                clone[index1] = cityB
                clone[index2] = cityA
                if clone not in neighbourhood :
                    neighbourhood.append(clone)
    # print('neighbourhood : ', neighbourhood)
    return neighbourhood

def runTSP_2(graph) :
    cityList = list(range(len(graph)))
    route = intilializer(cityList)
    # print('route: ', route)
    startTime = time.time()
    currentTime = time.time()
    TERMINATION_TIME = 10
    bestCost = getCostOfRoute(route, graph)
    startRouteCost = bestCost
    startRoute = route
    bestRoute = None

    while (currentTime - startTime) < TERMINATION_TIME:
        neighbourhood = generateNeighbourhood(route)
        previousCost = bestCost
        for neighbour in neighbourhood : 
            neigbourCost = getCostOfRoute(neighbour, graph) 
            # print('neigbour: ', neighbour, ' cost', neigbourCost)
            if neigbourCost < bestCost :
                bestCost = neigbourCost
                bestRoute = neighbour
                route = neighbour
                # print('route: ', route , ' cost: ', bestCost )
        print('bestCost: ', bestCost , ' previousCost: ', previousCost )
        if bestCost == previousCost :
            route = intilializer(cityList)
        currentTime = time.time()
        print('time left', TERMINATION_TIME - (currentTime - startTime))
    print('bestRoute: ', bestRoute , ' bestCost: ', bestCost )
    print('startRoute: ', startRoute , ' bestCost: ', startRouteCost )

runTSP_2(readCSV())