import math
from random import randint

#  converted from AnntennaArray.java

MIN_FLOAT = 2.2250738585072014e-308
MAX_FLOAT = 1.7976931348623157e+308
MIN_SPACING = 0.25

def bounds(nAntennae) :
    bnds = []
    dimBnd = [0.0, (nAntennae /2)]
    for i in range(nAntennae) :
        bnds.append(dimBnd)

    print('bounds: ', bnds)
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
    
    return anPos

def PSO(numOfParticles, nAntennae) :
    randomDesign = randDesign(nAntennae)
    particles = [{personalBest: False, velocity: False, position: pos PBcost: evaluate(randomDesign)} for pos in randomDesign]
    initialiseParticles = lambda particleList, 

print(randDesign(3))