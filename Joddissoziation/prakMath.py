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
	
	slopeErr = math.sqrt((1/(count-2)) * numerator / denominator)
	
	# calculate standard error for intercept (under normality assumption)
	# m = intercept error * sqrt(Σ x_i^2 / n)
	radicand = 0
	for x in xValues:
		radicand += x * x
	radicand /= count
	
	interceptErr = slopeErr * math.sqrt(radicand)
	return (slope, intercept, slopeErr, interceptErr)