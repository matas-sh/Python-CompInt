import math
from random import randint
import random

#  converted from AnntennaArray.java

MIN_FLOAT = 2.2250738585072014e-308
MAX_FLOAT = 1.7976931348623157e+308
MIN_SPACING = 0.25

def bounds(nAntennae) :
    bnds = []
    dimBnd = [0.0, (nAntennae /2)]
    for i in range(nAntennae) :
        bnds.append(dimBnd)

    # print('bounds: ', bnds)
    return bnds


def isValid(design, nAntennae) :

    if not len(design) == nAntennae:
        return False
    des = design[:]
    des = sorted(des)
    print('des: ', des)
    if abs(des[len(des) - 1] - nAntennae / 2.0) > 1e-10 :
        return False
    
    for i in range(len(des) - 1) :
        if des[i] < bounds(nAntennae)[i][0] or des[i] > bounds(nAntennae)[i][1] :
            print('invalid: ', des, ' out of bounds')
            return False
        if des[i+1] - des[i] < MIN_SPACING :
            print('invalid: ', des, ' apeture spacing too small')
            return False
 
    return True

def arrayFactor(design, elevation, steeringAngle) :
    summ = 0.0
    steering = 2.0 * math.pi * steeringAngle/360.0
    elevation = 2.0 * math.pi * elevation/360.0

    for x in design :
        summ += math.cos(2 * math.pi * x * (math.cos(elevation) - math.cos(steering)))
    
    return 20.0 * math.log(abs(summ))

def powerPeakGen(e, p) :
     return {
        'elevation' : e,
        'power' : p
    } 

def evaluate(design, nAntennae, steeringAngle) :

    if not len(design) == nAntennae :
        raise RuntimeError(
            'AntennaArray::evaluate called on design of the wrong size. Expected: ',
            nAntennae, '. Actual: ', len(design)) from error
    if isValid(design, nAntennae) == False :
        return MAX_FLOAT
    peaks = []
    prev = powerPeakGen(0.0, MIN_FLOAT)
    current = powerPeakGen(0.0, arrayFactor(design, 0.0, steeringAngle))

    elevation = 0.01
    while elevation <= 180.0 :
        nextOne = powerPeakGen(elevation, arrayFactor(design, elevation, steeringAngle))
        if current["power"] >= prev["power"] and current["power"] >= nextOne["power"] :
            peaks.append(current)
        prev = current
        current = nextOne
        elevation += 0.01
    peaks.append(powerPeakGen(180.0, arrayFactor(design, 180.0, steeringAngle)))
    peaks = sorted(peaks, key = lambda peak: peak["power"])

    if len(peaks) < 2 :
        return MIN_FLOAT

    distanceFromSteering = abs(peaks[0]["elevation"] - steeringAngle)

    for peak in peaks :
        if abs(peak["elevation"] - steeringAngle) < distanceFromSteering :
            return peak["power"]
    return peak[1]["power"]

# print(evaluate([0.5, 1.0, 1.5], 3, 90))

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
    

print(PSO(3, 1))