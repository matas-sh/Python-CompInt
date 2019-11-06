import math
import itertools
import random
import time

def getSubRoutes(route) :
    subRoutes = []
    for index in range(len(route)) :
            if index > 0 : 
                subRoutes.append([route[index - 1], route[index]])
    
    subRoutes.append([route[len(route) - 1], route[0]])
    return subRoutes

def getCostOfRoute(route, cityList) :
        cost=0
        subRoutes = getSubRoutes(route)

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


def probCityPicker(cityChoices, visitedCities, pheromoneTrails, graph, apha, beta) :
    valueArr = [ i * 0 for i in range(len(visitedCities))]
    aPos = visitedCities[len(visitedCities) - 1]
    # print('cityChoices: ', list(cityChoices))
    print('valueArr1', valueArr) 
    for city in cityChoices :
        key = str(aPos) + str(city) if aPos > city else str(city) + str(aPos)
        print('aPos - city: ', aPos, ' - ', city)
        print('key: ', key)
        if key not in pheromoneTrails :
            pheromoneTrails[key] = 1
        print(pheromoneTrails[key])
        valueArr.append(
            math.pow(pheromoneTrails[key], apha) * math.pow(1 / distanceToCost(graph[aPos], graph[city]), beta)
        )
    print('valueArr2', valueArr)
    cumArr = []
    for i, val in enumerate(valueArr, 0) :
        if i > 0 :
            print('index: ', i, valueArr[i - 1])
            cumArr.append(val + cumArr[i - 1])
        else :
            cumArr.append(val)

    print('cumArr: ', cumArr)
    randI = random.random()
    print('randI1: ', randI)
    randI = randI * cumArr[len(cumArr) - 1]
    print('randI2: ', randI)
    probIndex = 0
    for i, value in enumerate(cumArr, 0) :
        print('probIndex = i: ', probIndex, value, i )
        if value >= randI :
            probIndex = i
            print('shouldBreak')
            break
    print('probIndex: ', probIndex)
    probIndex -= (len(visitedCities) - 1)
    print('probIndex2: ', probIndex)
    print('len(visitedCities): ', len(visitedCities))
    print('cityChoices: ', len(cityChoices))
    print('cityChoices: ', list(cityChoices))
    return cityChoices[probIndex - 1]

def runTSP_3Plus(graph, nStep, nAnts, decayRate = 0.5, increaseRate = 1, alpha = 2, beta = 2) :

    cityList = list(range(len(graph)))
    decayPheromones = lambda edgeList, decayX: {k: v * decayX for (k, v) in edgeList.items()}
    increasePheromones = lambda edge, edgeList, increaseX: { k: (v + increaseX if k == edge else v) for (k, v) in edgeList.items()}
    pheromoneTrails = {}

    i = 0
    a = 0
    while i < nStep :
        while a < nAnts :
            currentPos = random.randint(0, len(cityList) - 1)
            cityChoices = cityList[:]
            route = []
            visited = []
            route.append(currentPos)
            visited.append(currentPos)
            while len(cityChoices) > 0 :
                cityChoices = list(filter(lambda city : city not in visited, cityChoices))
                print('visited: ', visited)
                print('cityChoices: ', list(cityChoices))
                currentPos = probCityPicker(cityChoices, visited, pheromoneTrails, graph, alpha, beta)
                print('currentPos: ', currentPos)
                route.append(currentPos)
                visited.append(currentPos)
            i += 1
            subRoutes = getSubRoutes(route)
            print('subRoutes: ', subRoutes)
            for edge in subRoutes :
                sorted(edge) 
                key = str(edge[0]) + str(edge[1])
                decayPheromones(pheromoneTrails, decayRate)
                if key not in pheromoneTrails :
                    pheromoneTrails[key] = 0
                pheromoneTrails = increasePheromones(key, pheromoneTrails, increaseRate)
                
            print('pheromoneTrails: ', pheromoneTrails)


graph = readCSV()
runTSP_3Plus(graph, 10, 10)
# routes = permuteRoutes(graph)
# runTSP_1(routes, graph)
# runTSP_2(graph)
