import math
import itertools
import random
import time
from random import randint


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

def probCityPicker(cityChoices, visited, graph, pheromoneTrails, alpha = 2, beta = 3) :

    valueArr = [0 for city in visited]
    currentCity = visited[len(visited) - 1]
    currentCityPos = graph[currentCity]

    for city in cityChoices :
        nextCityPos = graph[city]
        key = str(currentCity) + str(city) if currentCity > city else str(city) + str(currentCity)
        pheromoneLevel = pheromoneTrails[key] if key in pheromoneTrails else 0.1
        valueArr.append(
            math.pow(pheromoneLevel, alpha) * math.pow(distanceToCost(currentCityPos, nextCityPos), beta)
        )
        cumArr = [valueArr[0]]
        for i, val in enumerate(valueArr) :
            if i > 0 :
                cumArr.append(val + cumArr[i - 1])
        r = random.random() + cumArr[len(cumArr) - 1]

        chosenCity = False
        for i, val in enumerate(cumArr) :
            if val >= r :
                chosenIndex = i - (len(visited) - 1)
                chosenCity = cityChoices[chosenIndex]
                breakpoint
        
        return chosenCity




def runTSP_3Plus(graph, nStep, decayRate = 0.5, increaseRate = 1) :
    cityList = list(range(len(graph)))
    decayPheromones = lambda edgeList, decayX: {k: v * decayX for (k, v) in edgeList.items()}
    increasePheromones = lambda edge, edgeList, listLen, increaseX: { k: (v + increaseX/len(edgeList) if k == edge else v) for (k, v) in edgeList.items()}

    print('cityList: ', cityList)
    pheromoneKeys = list(itertools.permutations(cityList, 2))
    filter
    for
    # pheromoneTrails = {key[0]+ key[1]: 0.1 for key in pheromoneKeys}
    print('pheromoneKeys: ', list(pheromoneKeys))

    pheromoneTrails = {str(key[0])+ str(key[1]) if key[0] > key[1] else str(key[1]) + str(key[0]): 0.1 for key in pheromoneKeys}
    print('pheromoneTrails: ', pheromoneTrails)

    i = 0
    while nStep > i :
        currentPos = randint(0, len(cityList) - 1)
        cityChoices = cityList[:]
        route = [currentPos]
        visited = [currentPos]
        while len(cityChoices) > 0 :
            cityChoices = filter(lambda city : city not in visited, cityChoices)
            currentPos = probCityPicker(cityChoices, visited, graph, pheromoneTrails)
            route.append(currentPos)
            visited.append(currentPos)
        i += 1
        subRoutes = getSubRoutes(route)
        print('subRoutes: ', subRoutes)
        for edge in subRoutes :
            sorted(edge) 
            key = str(edge[0]) + str(edge[1])
            if key not in pheromoneTrails :
               pheromoneTrails[key] = 0.1
            pheromoneTrails = decayPheromones(pheromoneTrails, decayRate)
            pheromoneTrails[key] = increasePheromones(edge, pheromoneTrails, len(route), increaseRate)
            
        print('pheromoneTrails: ', pheromoneTrails)


graph = readCSV()
runTSP_3Plus(graph, 10)
# routes = permuteRoutes(graph)
# runTSP_1(routes, graph)
# runTSP_2(graph)
