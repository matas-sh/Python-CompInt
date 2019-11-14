import math
from random import randint, random
from AntennaeArrayProblem import evaluate, bounds, isValid

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674352-dt-content-rid-10821785_1/xid-10821785_1
'''

def randDesign(nAntennae) :
    bnds = bounds(nAntennae)
    anPos = [bnds[0][1]]

    # for antennae in list(range(nAntennae - 1)) :
    #     anPos.append(randint(bnds[0][0] * 10, bnds[0][1] * 10) / 10)

    for antennae in list(range(nAntennae - 1)) :
        antennaePlaced = False
        while antennaePlaced != True :
            possiblePos = randint(bnds[0][0] * 10, bnds[0][1] * 10) / 10
            valid = len([antennae for antennae in anPos if abs(antennae - possiblePos) < MIN_SPACING]) == 0
            if valid :
                antennaePlaced = True
        anPos.append(possiblePos)

    if not isValid(anPos, nAntennae) :
       anPos = randDesign(nAntennae)
    
    anPos = sorted(anPos)

    return anPos

def getNewVelocity(particle, nAntennae, gBest, initialVelocity = False, inertiaCo = 0.721, socCogCo = 1.1193) :
    r1Vec = [random.random(), random.random()]
    r2Vec = [random.random(), random.random()]

    pos = particle['position']
    vel = particle['velocity']
    pBest = particle['personalBestPos']

    if initialVelocity :
        randPos = randDesign(nAntennae) 
        iniVel = [velEl for velEl in [abs(pos[index] - randPos[index]) / 2 for index in list(range(nAntennae -1))]]
        print('###############')
        print('iniVel: ', iniVel)
        print('###############')
        return iniVel
 
    inertia = [inertiaCo * velEl for velEl in vel]
    print('subList: ', [pBest[index] - pos[index] for index, el in enumerate(vel)])
    cognitiveAttractionPt1 = [socCogCo * r1Vec * postEs for postEs in [pBest[index] - pos[index] for index, el in enumerate(vel)]]
    socialAttraction = [socCogCo * float(r2Vec) * postEs for postEs in [gBest[index] - pos[index] for index, el in enumerate(vel)]]


    print('###############')
    print('inertia: ', inertia)
    print('###############')
    print('cognitiveAttraction: ', cognitiveAttraction)
    print('###############')
    print('socialAttraction: ', socialAttraction)
    print('###############')
    newVel = [newVelEl for newVelEl in [inertia[index] + cognitiveAttraction[index] + socialAttraction[index] for index in enumerate(vel)]]
    print('newVelocity: ', newVel)  
    print('###############')
    return newVel

def getNewPosition(particlePos, newVelocity) :
    newPos = [newPos for newPos in [particlePos[index] + newVelocity[index] for index in enumerate(newVelocity)]]
    print('newPos: ', newPos)
    print('###############')
    return newPos

def PSO(numOfParticles, numOfIterations, nAntennae = 3, steeringAngle = 90) :

    positionList = [randDesign(nAntennae) for particle in list(range(numOfParticles))]
    globalBestValue = math.inf
    globalBest = False

    for pos in positionList :
        posValue = evaluate(pos, nAntennae, steeringAngle)
        if posValue < globalBestValue : 
            globalBestValue = posValue
            globalBest = pos
    #  initialise particles
    particleList = [
        { 
         'personalBest': evaluate(pos, nAntennae, steeringAngle),
         'personalBestPos': pos,
         'velocity': False,
         'position': pos,
        } for pos in positionList
    ]

    print('particleList v1: ', particleList)

    for particle in particleList :
        particle['velocity'] = getNewVelocity(particle, nAntennae, globalBest, True)

    print('particleList v2: ', particleList)

    # main loop
    i = 0
    while i < numOfIterations :
        lowestInIteration = False
        lowestInIterationValue = math.inf
        for particle in particleList :
            particle['velocity'] = getNewVelocity(particle, nAntennae, globalBest)
            particle['position'] = getNewPosition(particle.position, particle.velocity)
            
            if isValid(particle.position, nAntennae) :
                particlePosValue = evaluate(particle.position, nAntennae, steeringAngle)
            
                if particlePosValue < globalBestValue :
                    globalBestValue = particlePosValue
                    globalBest = particle.position

                if particlePosValue < particle.personalBest :
                    particle['personalBest'] = particlePosValue
                    particle['personalBestPos'] = particle.position

                if particlePosValue < lowestInIterationValue :
                    lowestInIterationValue = math.inf
                    lowestInIteration = particle.position
        print('lowest value in iteratiom iteration: ', lowestInIterationValue, '  ', lowestInIteration)
        i+=1
    print('global best value: ', globalBestValue, '  ', globalBest)

PSO(3, 1)