from TravellingSalesmanProblem import getCostOfRoute, readCSV, randomRouteGenerator
from itertools import permutations
import time
import math

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674349-dt-content-rid-10821790_1/xid-10821790_1
'''

def randomSearch(graph, terminationTime) :
    bestRoute = []
    bestCost = math.inf
    cityList = list(range(len(graph)))
    i = 0
    print('begin random search...')
    startTime = time.time()
    while time.time() - startTime < terminationTime :
        route = randomRouteGenerator(cityList)
        routeCost = getCostOfRoute(route, graph)

        if routeCost < bestCost :
            bestCost = routeCost
            bestRoute = route
        i+=1

    print('Number of routes checked - ', i, ' in approx.', terminationTime, ' seconds')   
    print('best route - ', bestRoute, ' cost: ', bestCost)

def naiveSearch(graph, terminationTime) :
    bestRoute = []
    bestCost = math.inf
    routes = permuteRoutes(graph)
    print('begin naive search...')
    startTime = time.time()
    for index, route in enumerate(routes) :
        if  time.time() - startTime > terminationTime :
            numOfRoutesChecked = index
            break

        routeCost = getCostOfRoute(route, graph)

        if routeCost < bestCost :
            bestCost = routeCost
            bestRoute = route

    print('Number of routes checked - ', numOfRoutesChecked, ' in approx.', terminationTime, ' seconds')   
    print('best route - ', bestRoute, ' cost: ', bestCost)
 
def runTSP_1(graph, terminationTime) :
    randomSearch(graph, terminationTime)
    # naiveSearch(graph, terminationTime)
  
def permuteRoutes(cityList) :
    print('cityList length: ', len(cityList))
    return permutations(range(len(cityList)))

runTSP_1(readCSV(), 3)