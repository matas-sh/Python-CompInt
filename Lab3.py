import math
from random import randint, uniform
from pprint import pprint
from AntennaeArrayProblem import evaluate, bounds, isValid, MIN_SPACING              

'''
    Lab instructions:
        https://vle.aston.ac.uk/bbcswebdav/pid-1674352-dt-content-rid-10821785_1/xid-10821785_1
'''

def randDesign(nAntennae) :
    bnds = bounds(nAntennae)
    anPos = [bnds[0][1]]

    for antennae in list(range(nAntennae - 1)) :
        antennaePlaced = False
        while antennaePlaced != True :
            possiblePos = uniform(bnds[0][0], bnds[0][1])
            valid = len([antennae for antennae in anPos if abs(antennae - possiblePos) < MIN_SPACING]) == 0
            if valid :
                antennaePlaced = True
        anPos.append(possiblePos)

    if not isValid(anPos, nAntennae) :
       anPos = randDesign(nAntennae)
    
    anPos = sorted(anPos)

    return anPos

def getInitialVelocity(pos, nAntennae) :
    randPos = randDesign(nAntennae) 
    iniVel = [velEl for velEl in [abs(randPos[index] - pos[index]) / 2 for index in list(range(nAntennae -1))]]
    return iniVel

def getNewVelocity(particle, nAntennae, gBest, inertiaCo, socCogCo) :

    pos = particle['position']
    vel = particle['velocity']
    pBest = particle['personalBestPos']

    r1Vec = [uniform(0,1) for el in vel]
    r2Vec = [uniform(0,1) for el in vel]
    newVel = []

    for index, velElem in enumerate(vel) :
        inertia = inertiaCo * velElem
        cognitiveAttraction = socCogCo * r1Vec[index] * (pBest[index] - pos[index])
        socialAttraction = socCogCo * r2Vec[index] * (gBest[index] - pos[index])
        newVel.append(inertia + cognitiveAttraction + socialAttraction)

    return newVel

def getNewPosition(particlePos, newVelocity, nAntennae) :
    newPos = [pos for pos in [particlePos[index] + el for index, el in enumerate(newVelocity)]]
    newPos.append(nAntennae / 2)
    return newPos

def generateParticleList(positionList, nAntennae, steeringAngle) :
    print('generating particles...')
    particleList = [
        { 
         'personalBest': evaluate(pos, nAntennae, steeringAngle),
         'personalBestPos': pos,
         'velocity': getInitialVelocity(pos, nAntennae),
         'position': pos,
        } for pos in positionList
    ]
    pprint(particleList)
    return particleList

def runPSO_1(numOfParticles, numOfIterations, nAntennae = 3, steeringAngle = 90) :

    inertiaCo = 1/(2 * math.log(2.0))
    socCogCo = math.log(2) + 0.5

    positionList = [randDesign(nAntennae) for particle in list(range(numOfParticles))]
    particleList = generateParticleList(positionList,  nAntennae, steeringAngle)

    globalBestValue = math.inf
    globalBest = False

    #  set initial global best
    for pos in positionList :
        posValue = evaluate(pos, nAntennae, steeringAngle)
        if posValue < globalBestValue : 
            globalBestValue = posValue
            globalBest = pos

    # main loop
    i = 0
    while i < numOfIterations :
        for particle in particleList :
            particle['velocity'] = getNewVelocity(particle, nAntennae, globalBest, inertiaCo, socCogCo)
            particle['position'] = getNewPosition(particle['position'], particle['velocity'], nAntennae)
            position = particle['position']
            if isValid(position, nAntennae) :
                particlePosValue = evaluate(position, nAntennae, steeringAngle)
            
                if particlePosValue < globalBestValue :
                    globalBestValue = particlePosValue
                    globalBest = position

                if particlePosValue < particle['personalBest'] :
                    particle['personalBest'] = particlePosValue
                    particle['personalBestPos'] = position

        print('global best value: ', globalBestValue, '  design: ', globalBest)
        i+=1
    pprint(particleList)

nAntennae = 3
runPSO_1(math.ceil(20 + math.sqrt(nAntennae)), 100, nAntennae)