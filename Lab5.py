from TravellingSalesmanProblem import getCostOfRoute, readCSV
from Lab2  import intilializer, generateNeighbourhood
from functools import reduce
from random import randint 

'''
    Lab instructions:
        https://vle.aston.ac.uk/webapps/blackboard/execute/content/file?cmd=view&content_id=_1674355_1&course_id=_25312_1&launch_in_new=true
'''


def parentSelection(graph, population, numOfparents = 20, k = 20) :
    parents = []
    counterA = 0

    while counterA < numOfparents : 
        tournamentSample = []
        counterB = 0
        nextParentIndex = 0

        while counterB < k :
            candidate  = population[randint(0, len(population) - 1)]

            if candidate not in tournamentSample :
                tournamentSample.append(candidate)
            counterB += 1
        possibleParents = sorted(tournamentSample, key=lambda candidateA: getCostOfRoute(candidateA, graph))
  
        for parent in possibleParents :
            if parent not in parents :
                parents.append(parent)
                counterA += 1 
                break
        
    # print('parents: ', parents)
    return parents

def survivorSelection(population, graph, genSizeLimit) : 
    populationSize = len(population)

    if populationSize >= genSizeLimit :
        sortedPopulation = sorted(population, key = lambda candidate: getCostOfRoute(candidate, graph))
        newPopulation = sortedPopulation[0 : genSizeLimit -1]
    # print('newPopulation: ', newPopulation)
    return newPopulation

def mutation(offspring, prob = 70) :
    mutatedOffspring = offspring

    if randint(0, 100) <= prob :
        mutationOptions = generateNeighbourhood(offspring)
        mutatedOffspring = mutationOptions[randint(0, len(mutationOptions) - 1)]

    return mutatedOffspring


def getRandParents(parentsArr) :
    firstRandParentPos = randint(0, len(parentsArr) - 1)
    secondRandParentPos = randint(0, len(parentsArr) - 1)

    while firstRandParentPos == secondRandParentPos:
        firstRandParentPos = randint(0, len(parentsArr) - 1)
        secondRandParentPos = randint(0, len(parentsArr) - 1)

    return [parentsArr[firstRandParentPos], parentsArr[secondRandParentPos]] 


def getRandParentArraySlice(parent, minimumSliceLength = 2, maximumSliceLength = 10 ) :
    parentLength = len(parent)
    firstSlice = randint(0, parentLength - 1)
    secondSlice = randint(0, parentLength - 1)
    sliceStartPos = False
    sliceEndPos = False

    while abs(firstSlice - secondSlice) < minimumSliceLength or abs(firstSlice - secondSlice) > maximumSliceLength :
        firstSlice = randint(0, parentLength - 1)
        secondSlice = randint(0, parentLength - 1)

    if firstSlice < secondSlice :
        sliceStartPos = firstSlice
        sliceEndPos =  secondSlice
    else :
        sliceStartPos = secondSlice
        sliceEndPos =  firstSlice
    

    arrSlice = parent[sliceStartPos : sliceEndPos]
    return arrSlice, sliceStartPos, sliceEndPos 

def recombineParents(primaryParent, secondaryParent) :
    arrSlice, sliceStartPos, sliceEndPos = getRandParentArraySlice(primaryParent)
    parentLength = len(primaryParent)
    recombinationArr = [None for x in list(range(parentLength))]
    recombinationArr = [arrSlice[i - sliceStartPos] if sliceStartPos <= i and i < sliceEndPos else el for i, el in enumerate(recombinationArr)]
    offsetIndex  = lambda index: (index + sliceEndPos) % (parentLength)
    counterA = 0
    counterB = 0
    printFlag = False

    while counterA <= parentLength :
        secondaryParentIndex = offsetIndex(counterA)
        recombinationArrIndex = offsetIndex(counterB)
        
        transferElement = secondaryParent[secondaryParentIndex]

        if transferElement not in recombinationArr :
            recombinationArr[recombinationArrIndex] = transferElement
            counterB += 1
        counterA+=1
    return recombinationArr
    # print(f'    recombined array: {recombinationArr} \n     primary parent: {primaryParent} \n     secondaryParent: {secondaryParent} \n     slice started: {sliceStartPos}, slice ended: {sliceEndPos}')


def recombination(parents, numOfOffspring, prob = 100) :
    offsprings = []
    
    if randint(0, 100) <= prob :
        counter = 0

        while counter < numOfOffspring :
            chosenParents = getRandParents(parents)
            for i, primaryParent in enumerate(chosenParents):
                # print('parents: ', primaryParent, chosenParents[abs(i - 1)])
                offspring = recombineParents(primaryParent, chosenParents[abs(i - 1)])
                offsprings.append(offspring)
                counter += 1
    else :
        offsprings = parents

    # print(f'parents: {parents}, offsprings: {offsprings}')
    return offsprings

def runTSP_5(graph, popSize = 100, gens = 100) :
    print('initialise population...')
    population = [intilializer(list(range(len(graph)))) for each in list(range(popSize))]
    firstGenPopulation = population
    print('firstGenPopulation: ', firstGenPopulation)

    counter = 0

    while counter < gens :
        print('evolution start...')
        parents = parentSelection(graph, population)
        # print('parents: ', parents)
        offsprings = recombination(parents, len(parents) * 3)
        # print('offsprings: ', offsprings)

        for offspring in offsprings :
            mutatedOffspring = mutation(offspring)
            # print('mutatedOffspring: ', mutatedOffspring)
            population.append(mutatedOffspring)
        population = survivorSelection(population, graph, popSize)
        populationBestRoute = reduce(lambda candidateA, candidateB: candidateB if getCostOfRoute(candidateA, graph) > getCostOfRoute(candidateB, graph) else candidateA, population)
        print(f'population {counter} best cost route: {populationBestRoute}', getCostOfRoute(populationBestRoute, graph))
        counter += 1

    # firstGenPopulationCostAverage = reduce(lambda accum, current: accum + current, firstGenPopulation) / popSize
    # LastGenPopulationCostAverage = reduce(lambda accum, current: accum + current, population) / popSize

    # print(f'gen num {gens}: {population}')
    # print(f'first generation average cost: {firstGenPopulationCostAverage}')
    # print(f'last generation average cost: {LastGenPopulationCostAverage}')

print('start TSP5...')
runTSP_5(readCSV())
    