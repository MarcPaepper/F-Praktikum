from gravMath import linearRegression

def übergabe(x, y):
    (slope, intercept, slopeErr, interceptErr) = linearRegression(x, y)
    return (slope, intercept)