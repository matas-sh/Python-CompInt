import random
import time
import math
from TravellingSalesmanProblem import getCostOfRoute, readCSV, randomRouteGenerator  

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674351-dt-content-rid-10882477_1/xid-10882477_1
'''

def generateNeighbourhood(route) :
    neighbourhood = []

    for index1, cityA in enumerate(route) :
        for index2, cityB in enumerate(route) :
            # if (index1 != index2) :   
                clone = route[:]
                clone[index1] = cityB
                clone[index2] = cityA
                if clone not in neighbourhood:
                    neighbourhood.append(clone)
    return neighbourhood

def bestNeigbourhoodMember(neighbourhood, graph) :
    bestRoute = neighbourhood[0]
    bestCost = getCostOfRoute(bestRoute, graph)
    for i, neighbour in enumerate(neighbourhood) : 
        neigbourCost = getCostOfRoute(neighbour, graph)
        if neigbourCost < bestCost :
            bestRoute = neighbour
            bestCost = neigbourCost
    return bestRoute, bestCost

def runTSP_2(graph, terminationTime) :
    cityList = list(range(len(graph)))
    route = randomRouteGenerator(cityList)
    startTime = time.time()
    currentTime = time.time()
    bestCost = getCostOfRoute(route, graph)
    bestRoute = route
    print('start cost: ', bestCost)

    while (currentTime - startTime) < terminationTime:
        neighbourhood = generateNeighbourhood(route)

        bestNeighbour, bestNeighbourCost = bestNeigbourhoodMember(neighbourhood, graph)
            
        if bestNeighbour == route :
            if bestNeighbourCost < bestCost :
                print('new best cost: ', bestCost)
                bestCost = bestNeighbourCost
                bestRoute = bestNeighbour
            route = randomRouteGenerator(cityList)
        else  :
            route = bestNeighbour

        currentTime = time.time()
    print('bestRoute: ', bestRoute , ' bestCost: ', bestCost)

runTSP_2(readCSV(), 5)