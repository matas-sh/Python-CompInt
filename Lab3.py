import math
from random import randint, uniform
from AntennaeArrayProblem import evaluate, bounds, isValid, MIN_SPACING              

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
    print('randDesign: ', anPos)

    return anPos

def getNewVelocity(particle, nAntennae, gBest, initialVelocity = False, inertiaCo = 1/(2 * math.log(2.0)), socCogCo = ((math.log(2)) + 0.5)) :

    pos = particle['position']
    vel = particle['velocity']
    pBest = particle['personalBestPos']

    if initialVelocity :
        randPos = randDesign(nAntennae) 
        iniVel = [velEl for velEl in [abs(pos[index] - randPos[index]) / 2 for index in list(range(nAntennae -1))]]
        # print('###############')
        # print('iniVel: ', iniVel)
        # print('###############')
        return iniVel

    r1Vec = [uniform(0,1) for el in vel]
    r2Vec = [uniform(0,1) for el in vel]
 
    inertia = [inertiaCo * velEl for velEl in vel]
    print('subList: ', [pBest[index] - pos[index] for index, el in enumerate(vel)])
    cognitiveAttraction = [socCogCo * postEs for postEs in [r1Vec[index] * (pBest[index] - pos[index]) for index, el in enumerate(vel)]]
    socialAttraction = [socCogCo * postEs for postEs in [r2Vec[index] * gBest[index] - pos[index] for index, el in enumerate(vel)]]

    print('prev vel: ', vel)
    print('###############')
    print('inertia: ', inertia)
    print('###############')
    print('cognitiveAttraction: ', cognitiveAttraction)
    print('###############')
    print('socialAttraction: ', socialAttraction)
    print('###############')
    newVel = [newVelEl for newVelEl in [inertia[index] + cognitiveAttraction[index] + socialAttraction[index] for index, el in enumerate(vel)]]
    print('newVelocity: ', newVel)  
    print('###############')
    return newVel

def getNewPosition(particlePos, newVelocity, nAntennae) :
    print('oldPos: ', particlePos) 
    newPos = [pos for pos in [particlePos[index] + el for index, el in enumerate(newVelocity)]]
    newPos.append(nAntennae / 2)
    print('newPos: ', newPos)
    print('###############')
    return newPos

def runPSO_1(numOfParticles, numOfIterations, nAntennae = 3, steeringAngle = 90) :

    positionList = [randDesign(nAntennae) for particle in list(range(numOfParticles))]
    globalBestValue = 100
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
        lowestInIterationValue = 100
        for particle in particleList :
            particle['velocity'] = getNewVelocity(particle, nAntennae, globalBest)
            particle['position'] = getNewPosition(particle['position'], particle['velocity'], nAntennae)
            position = particle['position']
            print('getting here! newPos: ', position, ' nAntennae: ', nAntennae, '  valid?', isValid(position, nAntennae))
            if isValid(position, nAntennae) :
                particlePosValue = evaluate(position, nAntennae, steeringAngle)
            
                print('getting here 2')
                if particlePosValue < globalBestValue :
                    globalBestValue = particlePosValue
                    globalBest = position

                print('getting here 3')
                if particlePosValue < particle['personalBest'] :
                    particle['personalBest'] = particlePosValue
                    particle['personalBestPos'] = position

                print('getting here 4')
                if particlePosValue < lowestInIterationValue :
                    lowestInIterationValue = particlePosValue
                    lowestInIteration = position
            print('lowest value in iteratiom iteration: ', lowestInIterationValue, ' design: ', lowestInIteration)
        i+=1
    print('global best value: ', globalBestValue, '  ', globalBest)

nAntennae = 3
runPSO_1(math.ceil(20 + math.sqrt(nAntennae)), 10, nAntennae)