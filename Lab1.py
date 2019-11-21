from TravellingSalesmanProblem import getCostOfRoute, readCSV
from itertools import permutations

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674349-dt-content-rid-10821790_1/xid-10821790_1
'''

def runTSP_1(graph) : 
    bestRoute = []
    bestCost = 100
    routes = permuteRoutes(graph)

    for route in routes :
        routeCost = getCostOfRoute(route, graph)
        if (routeCost < bestCost) :
            bestCost = routeCost
            bestRoute = route
    print('best route - ', bestRoute, ' cost: ', bestCost)


def permuteRoutes(cityList) :
    print(list(permutations(range(len(cityList)))))
    return permutations(range(len(cityList)))

runTSP_1(readCSV())