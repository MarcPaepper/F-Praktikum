import InputOutput
import matplotlib.pyplot as plot
import math
from turtle import pos

channels = InputOutput.readRawData("kalibrierung.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe geringere Intensität')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.show()


channels = InputOutput.readRawData("kalibrierung_2.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe maximal')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.show()

channels = InputOutput.readRawData("kalibrierungmittel.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe mittlgroßer Spalt')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()

channels = InputOutput.readRawData("kalibrierungLinks.txt")
channelNumber = range(2048)

plot.plot(channelNumber, channels, label='Hg-Lampe Links')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()


[channels, wavelengths] = InputOutput.readRawKalData("kalibrierungsFunktion.txt")

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
	print(slope, intercept, slopeErr, interceptErr)
	return (slope, intercept, slopeErr, interceptErr)
   
linearRegression(channels,wavelengths)
