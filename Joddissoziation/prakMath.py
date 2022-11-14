import math
import numpy

def linearRegression(xValues: list, yValues: list, descr: str = ""):
	"""Linear Regression for a list of x and value values

	Args:
		xValues (list<float>): the x values used for the regression
		yValues (list<float>): the y values used for the regression
		descr (str): a description of what is being fitting, if provided a message is printed with the description and the fit parameters

	Returns:
		(slope, intercept, slopeErr, interceptErr): the regression parameters with their standard deviation (list of floats)
	"""
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
	
	# optionally print values
	if (descr != ""):
		msg = "LinReg for %s: [" % descr
		
		slopePrecision = math.floor(math.log10(slopeErr))
		if (slopeErr * (10 ** (-slopePrecision)) < 2.5):
			slopePrecision -= 1
		
		slopeR = round(slope, -slopePrecision)
		slopeErrR = round(slopeErr, -slopePrecision)
		
		if (slopePrecision > -6 and slopePrecision < 7):
			msg += "slope = %s ± %s" % (floatString(slopeR, -slopePrecision), floatString(slopeErrR, -slopePrecision))
		# else:
			# msg += "slope = %s ± %s" % (floatString(slopeR, -slopePrecision), floatString(slopeErrR, -slopePrecision))
		
		interceptPrecision = math.floor(math.log10(interceptErr))
		if (interceptErr * (10 ** (-interceptPrecision)) < 2.5):
			interceptPrecision -= 1
		
		interceptR = round(intercept, -interceptPrecision)
		interceptErrR = round(interceptErr, -interceptPrecision)
		
		if (interceptPrecision > -6 and interceptPrecision < 7):
			msg += ", intercept = %s ± %s]" % (floatString(interceptR, -interceptPrecision), floatString(interceptErrR, -interceptPrecision))
		# else:
			# msg += ", intercept = %s ± %s]" % (floatString(interceptR, -interceptPrecision), floatString(interceptErrR, -interceptPrecision))
		
		print(msg)
	
	return (slope, intercept, slopeErr, interceptErr)

# calculate a list of x and y values for a linear function
def linearValues(start, stop, slope, intercept, many=True):
	diff = stop - start
	x = []
	if (many):
		x = numpy.linspace(start, stop, num=50)
	else:
		x = [start, start + 0.003*diff, stop - 0.003 * diff, stop]
	y = []
	for value in x:
		y.append(value * slope + intercept)
	
	return (x, y)

def floatString(FloatNumber, Precision):
    return "%0.*f" % (Precision, FloatNumber)