import math

def linearRegression(xValues: list, yValues: list):
	count = len(xValues)
	
	# calculate x̄
	xAvg = 0.0
	for value in xValues:
		xAvg += value * 1.0
	xAvg /= count
	
	# calculate ȳ
	yAvg = 0.0
	for value in yValues:
		yAvg += value * 1.0
	yAvg /= count
	
	# calculate the best fit slope with ordinary least squares
	# slope = Σ(x_i - x̄)(y_i - ȳ) / Σ(x_i - x̄)²
	
	# calculate numerator
	numerator = 0
	for i in range(count):
		numerator += (xValues[i] * 1.0 - xAvg) * (yValues[i] * 1.0 - yAvg)
	
	# calculate denominator
	denominator = 0
	for i in range(count):
		base = (xValues[i] * 1.0 - xAvg)
		denominator += base * base
	
	slope = numerator / denominator
	
	# calculate best fit intercept
	intercept = yAvg - xAvg * slope
	
	# calculate standard error for slope (under normality assumption)
	# m = sqrt((1/(n-2)) * Σ(y_i - x_i * slope - intercept)² / Σ(x_i - x̄)²)
	
	# calculate numerator
	
	numerator = 0
	for i in range(count):
		base = yValues[i] - (xValues[i] * slope + intercept)
		numerator += base * base
	
	# denominator stays the same
	
	slopeErr = math.sqrt((1/(count-2)) * numerator / denominator) if count > 2 else 0
	
	# calculate standard error for intercept (under normality assumption)
	# m = intercept error * sqrt(Σ x_i^2 / n)
	radicand = 0
	for x in xValues:
		radicand += x * x
	radicand /= count
	
	interceptErr = slopeErr * math.sqrt(radicand)
	
	return (slope, intercept, slopeErr, interceptErr)

"""
calculate the expected gravitational anomaly of a polygon prism
which has its base in the xz-plane (where x is the direction of
measurement and z is height) and stretches to infinty in the y-
direction with a homogenous density. The formula is taken from
equation 14 of the "Versuchsskript Gravimetrie"

Parameters
----------
vertices: a list of all 2D coordinates of every corner of the
          polygon as tuples (xValue, zValue) in m. The last
		  coordinate must not equal the first one, as an edge
		  is automatically drawn between the two.
position: a 2D tuple (xValue, zValue) of the observer in meters
density: the homogenous density in kg/m^3


Returns
-------
the additional or missing gravitational acceleration in
the z-direction (in mGal) due to the prism an observer
experiences at the specified position
"""
def gravitationAnomalyOfPolygon(vertices: list[tuple[float, float]],
                                position: tuple[float, float],
								density: float) -> float:
	vertices = vertices.copy()
	position = (float(position[0]), float(position[1]))
	N = len(vertices)
	
	# convert absolut polygon coordinates to relative ones
	# i.e. move the coordinate system such that the observer is in the origin
	
	for i in range(0, N):
		x = vertices[i][0]
		z = vertices[i][1]
		vertices[i] = (x - position[0], z - position[1])
	
	dg = 0 # the expected gravitational acceleration in mGal
	for i in range(0, N):
		x_i = vertices[i][0]
		z_i = vertices[i][1]
		x_ipo = vertices[(i+1) % N][0] # po meaning 'plus one'
		z_ipo = vertices[(i+1) % N][1] # po meaning 'plus one'
		x_delta = x_ipo - x_i
		z_delta = z_ipo - z_i
		r_i   = sqrt(x_i   ** 2 + z_i   ** 2)
		r_ipo = sqrt(x_ipo ** 2 + z_ipo ** 2)
		theta_i   = arctan(z_i, x_i)
		theta_ipo = arctan(z_ipo, x_ipo)
		
		numerator = (x_i * z_ipo - z_i * x_ipo) * (x_delta * (theta_i - theta_ipo) + z_delta * math.log(r_ipo / r_i))
		denominator = x_delta**2 + z_delta**2
		
		dg += numerator / denominator
	
	return dg * 6.6743e-6 * density
	# 6.6743e-6 is the gravitational constant in mGal * kg / m^2
	# the formula lacks the *2 factor, because the function only deals with a half-infinite prism whereas the source deals with an infinite prism

# test case to test whether gravitationAnomalyOfPolygon works as expected
def testPolygon():
	polygon = []
	polygon.append([350, 100])
	polygon.append([650, 100])
	polygon.append([650, 500])
	polygon.append([350, 500])
	grav=[]
	x = range(0, 1000, 20)
	for i in x:
		grav.append(gravitationAnomalyOfPolygon(polygon, (i, 0), -100)*2)

def sqrt(radicand):
	return math.sqrt(radicand)

def arctan(numerator, denominator):
	return math.atan2(numerator, denominator)