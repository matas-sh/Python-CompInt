
import getCostOfRoute, readCSV from TravellingSalesmanProblem
import intilializer, generateNeighbourhood from Lab2 
import reduce from functools 
import randint from random

'''
    Lab instructions:
        Whttps://vle.aston.ac.uk/webapps/blackboard/execute/content/file?cmd=view&content_id=_1674355_1&course_id=_25312_1&launch_in_new=true
'''


def parentSelection(population, numOfParentPairs = 1, k = 20) :
    parentPairs = []
    counterA, counterB, counterC = 0

    while counterA < numOfParentPairs
        parents = []
        while counterB < 2 : 
            tournamentSample = []
            while counterC < k :
                candidate  = population[randint(len(population) - 1)]
                if candidate not in tournamentSample :
                    tournamentSample.append(candidate)
                counterC += 1
            parent = reduce(lambda candidateA, candidateB: candidateA = candidateB if getCostOfRoute(candidateA) > getCostOfRoute(candidateB) else candidateA = candidateA)
            parents.append(parent)
            counterB += 1
        parentPairs.append(parents)
        counterA += 1

    return parentPairs

def survivorSelection() : 
    return False

def mutation(offsprings, prob = 70) :
    mutatedOffsprings = []

    if randint(100) <= prob :
        for offspring in offsprings :
            mutationOptions = generateNeighbourhood(offspring)
            mutatedOffsprings.append(mutationOptions[randint(len(mutationOptions) - 1)])
    else :
        mutatedOffsprings = offsprings

    return mutatedOffsprings

def recombination(parentPairs, prob = 100, numOffspring = 2) :
    recombinedOffsprings = []

    if randint(100) <= prob :
        

    return False

def runTSP_5(graph, popSize=100, gens = 100) :
    population = [intilializer(list(range(len(graph)) for each in list(range(popSize))]
    firstGenPopulation = population
    populationFitness = {k: getCostOfRoute(k) for k in population}
    counter = 0

    while counter < gens :
        parents = parentSelection(population)
        offsprings = recombination(parents)
        offsprings = mutation(offsprings)
        population += offsprings
        for offspring in offsprings :
            populationFitness[offspring] = getCostOfRoute(offspring)
        population = nextGenSelection(population, populationFitness)
        counter += 1

    firstGenPopulationCostAverage = reduce(lambda accum, current: accum + current, firstGenPopulation)
    LastGenPopulationCostAverage = reduce(lambda accum, current: accum + current, population)

    print(f'gen num {gens}: {population}')
    print(f'first generation average cost: {firstGenPopulationCostAverage}')
    print(f'last generation average cost: {LastGenPopulationCostAverage}')

    