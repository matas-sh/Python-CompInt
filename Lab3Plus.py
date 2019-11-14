import random
import time
import getCostOfRoute, readCSV from TravellingSalesmanProblem

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674353-dt-content-rid-10821784_1/xid-10821784_1
'''

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

def runTSP_3Plus(graph, nStep = 50, decayRate = 0.7, increaseRate = 1) :
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
    print('final route: ', route, ' cost: ', getCostOfRoute(route))

runTSP_3Plus(readCSV())