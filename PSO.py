import math

#  converted from AnntennaArray.java

MIN_FLOAT = 2.2250738585072014e-308
MAX_FLOAT = 1.7976931348623157e+308

def bounds(nAntennae) :
    bnds = []
    dimBnd = [0.0, (nAntennae /2)]
    for i in range(nAntennae) :
        bnds.append(dimBnd)
    return bnds


def isValid(design, nAntennae) :
    MIN_SPACING = 0.25
    if not len(design) == nAntennae:
        return False
    des = design[:]
    sorted(des)
    
    if abs(des[len(des) - 1] - nAntennae / 2.0) > 1e-10 :
        return False
    
    for i in range(len(des) - 1) :
        if des[i] < bounds(nAntennae)[i][0] or des[i] > bounds(nAntennae)[i][1] :
            return False
        if des[i+1] - des[i] < MIN_SPACING :
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

print(evaluate([0.5, 1.0, 1.5], 3, 90))