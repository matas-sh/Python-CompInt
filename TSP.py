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

def probCityPicker(cityChoices, visited, graph, pheromoneTrails, alpha = 2, beta = 3) :

    # print('cityChoices: ', cityChoices)
    
    # print('visited: ', visited)
    
    # print('graph: ', graph)
    
    # print('pheromoneTrails: ', pheromoneTrails)


    valueArr = [0 for city in visited]
    currentCity = visited[len(visited) - 1]
    currentCityPos = graph[currentCity]

    # print('cityChoices: ', cityChoices)
    for city in cityChoices :
        nextCityPos = graph[city]
        key = str(currentCity) + str(city) if currentCity < city else str(city) + str(currentCity)
        pheromoneLevel = pheromoneTrails[key]
        valueArr.append(
            math.pow(pheromoneLevel, alpha) * math.pow(distanceToCost(currentCityPos, nextCityPos), beta)
        )
    cumArr = [valueArr[0]]
    # print('valueArr: ', valueArr)
    for i, val in enumerate(valueArr) :
        # print('val', val )
        if i > 0 :
            cumArr.append(val + cumArr[i - 1])
            # print('cumArr.append: ', cumArr)
    r = random.random() * cumArr[len(cumArr) - 1]

    # print('cumArr: ', cumArr)

    # print('r: ', r)
    chosenCity = False
    for i, val in enumerate(cumArr) :
        if val >= r :
            chosenIndex = i - (len(visited) )
            # print('chosenIndex: ', chosenIndex)
            # print('cityChoices len: ', len(cityChoices))
            chosenCity = cityChoices[chosenIndex]
            # print('chosenCit: ', chosenCity)
    return chosenCity

def runTSP_3Plus(graph, nStep, decayRate = 0.7, increaseRate = 1) :
    cityList = list(range(len(graph)))
    decayPheromones = lambda edgeList, decayX: {k: v * decayX for (k, v) in edgeList.items()}
    increasePheromones = lambda edge, edgeList, listLen, increaseX: { k: (v + increaseX/len(edgeList) if k == edge else v) for (k, v) in edgeList.items()}

    pheromoneKeys = []
    for cityA in cityList :
        for cityB in cityList :
            if cityA != cityB and [cityA, cityB] not in pheromoneKeys:
                pheromoneKeys.append([cityA, cityB])
    
    sortedPheromoneKeys = list(map(lambda key: str(key[0]) + str(key[1]) if key[0] < key[1] else str(key[1]) + str(key[0]), pheromoneKeys))
    # print('sortedPheromoneKeys: ', list(pheromoneKeys))
    pheromoneTrails = {key: 0.1 for key in sortedPheromoneKeys}
    # print('pheromoneTrails: ', pheromoneTrails)

    subRouteFreq = {}
    i = 0
    while nStep > i :
        currentPos = random.randint(0, len(cityList) - 1)
        cityChoices = [city for city in cityList if city != currentPos]
        # cityChoices = cityList[:]

        route = [currentPos]
        visited = [currentPos]
        # print('cityChoices: ', cityChoices)
        while len(list(cityChoices)) > 0 :
            # print('cityChoices length in loop: ', cityChoices)
            currentPos = probCityPicker(cityChoices, visited, graph, pheromoneTrails)
            route.append(currentPos)
            visited.append(currentPos)
            cityChoices = list(filter(lambda city : city not in visited, cityChoices))
        i += 1
        subRoutes = getSubRoutes(route)
        pheromoneTrails = decayPheromones(pheromoneTrails, decayRate)
        print('subRoutes: ', subRoutes)
        for edge in subRoutes :
            sorted(edge) 
            key = str(edge[0]) + str(edge[1]) if edge[0] < edge[1] else str(edge[1]) + str(edge[0])
            # print('key: ', key)
            if key in subRouteFreq :
                subRouteFreq[key] = (1 + subRouteFreq[key]) 
            else :
                subRouteFreq[key] = 0
            pheromoneTrails = increasePheromones(key, pheromoneTrails, len(route), increaseRate)
            
    print('pheromoneTrails: ', pheromoneTrails)
    print('subRouteFreq: ', subRouteFreq)
    topTenSubRoutes = [[k,v] for k,v in subRouteFreq.items()]
    topTenSubRoutes = sorted(topTenSubRoutes, key=lambda kToVList: kToVList[1], reverse=True)
    print('topTenSubRoutes: ',topTenSubRoutes[:10])
    # for k, v in subRouteFreq.items() :
    #     for i in list(range(10)) :
    #         # print('i', i)
    #         if len(topTenSubRoutes) > i :
    #             print( [k, v])
    #             if topTenSubRoutes[i][1] < v :
    #                 topTenSubRoutes[i] = [k, v]
    #                 break
    #         else :
    #             topTenSubRoutes.append([k, v])

    # print('top ten sub-routes: ', topTenSubRoutes)


graph = readCSV()
runTSP_3Plus(graph, 50)
# routes = permuteRoutes(graph)
# runTSP_1(routes, graph)
# runTSP_2(graph)
