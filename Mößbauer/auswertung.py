from matplotlib import pyplot as plot
from scipy.optimize import curve_fit
from scipy.stats.distributions import t
import numpy as np
import math
from sklearn.metrics import r2_score
from inputOutput import *

savePlots = True
showPlots = True

def lorentzian(x, x_0, amplitude, fwhm):
	gamma = abs(fwhm) / 2
	lorentz = (gamma ** 2) / ((x - x_0) ** 2 + gamma ** 2)
	return amplitude * lorentz

def lorentzianX6(x, offset,
					x_1, x_2, x_3, x_4, x_5, x_6,
					amp_1, amp_2, amp_3, amp_4, amp_5, amp_6,
					fwhm_1, fwhm_2, fwhm_3, fwhm_4, fwhm_5, fwhm_6):
	value = offset
	value -= lorentzian(x, x_1, amp_1, fwhm_1)
	value -= lorentzian(x, x_2, amp_2, fwhm_2)
	value -= lorentzian(x, x_3, amp_3, fwhm_3)
	value -= lorentzian(x, x_4, amp_4, fwhm_4)
	value -= lorentzian(x, x_5, amp_5, fwhm_5)
	value -= lorentzian(x, x_6, amp_6, fwhm_6)
	
	return value
	

def peakFit(caption, fileName, shift, saveName, numberPeaks, startDiff, ymin, ymax):
	# read data
	
	channels, counts = readRawData("Messwerte/" + fileName)
	lineCount = len(channels)
	middle = math.ceil(lineCount / 2)
	
	# fold half of the channels over
	
	channelsRev = channels.copy()
	countsRev = counts.copy()
	channelsRev.reverse()
	countsRev.reverse()
	
	# cut out second half of values and those at the beginning / end which have no folded counterpart
	
	channels = channels[max(0, shift) : middle - max(0, -shift)]
	counts   = counts  [max(0, shift) : middle - max(0, -shift)]
	
	channelsRev = channelsRev[max(0, -shift) : middle - max(0, shift)]
	countsRev   = countsRev  [max(0, -shift) : middle - max(0, shift)]
	
	for i in range(0, len(channelsRev)):
		channelsRev[i] = i + max(0, shift)
	
	# add counts and folded counts together
	
	for i in range(0, len(channels)):
		counts[i] += countsRev[i]
	
	# boundaries
	
	minX = 0
	maxX = max(channels)
	minY = 0
	maxY = max(counts)
	
	# calculate velocity
	
	velocities = []
	
	minCh = min(channels)
	maxCh = max(channels)
	for i in range(minCh, maxCh+1):
		velocities.append(math.cos((i / maxCh) * math.pi))
	
	# start params
	offset = maxY
	fwhm = startDiff / 5
	amp = maxY / 5
	x_0s = []
	for i in range(numberPeaks):
		x_0s.append((i - (numberPeaks - 1) / 2) * startDiff)
	
	if (numberPeaks == 6):
		initParams = [(offset,
						x_0s[0], x_0s[1], x_0s[2], x_0s[3], x_0s[4], x_0s[5],
						amp, amp, amp, amp, amp, amp,
						fwhm, fwhm, fwhm, fwhm, fwhm, fwhm)]
	fitCounts = []
	# for v in velocities:
	# 	fitCounts.append(lorentzianMulti(v, offset,
	# 									x_0s[0], x_0s[1], x_0s[2], x_0s[3], x_0s[4], x_0s[5],
	# 									amp, amp, amp, amp, amp, amp,
	# 									fwhm, fwhm, fwhm, fwhm, fwhm, fwhm))
	
	par, pcov = curve_fit(lorentzianX6, velocities, counts, p0=initParams)
	parStDev = np.sqrt(np.diag(pcov))
	
	print(f"offset:\t{round(par[0], 2)}\t±\t{round(parStDev[0], 2)}")
	for i in range(numberPeaks):
		print(f"i={i+1}")
		print(f"x_0={round(par[i+1], 5)}\t±\t{round(parStDev[i+1], 5)}")
		print(f"amp={round(par[i+1+numberPeaks])}\t±\t{round(parStDev[i+1+numberPeaks])}")
		print(f"fwhm={round(par[i+1+2*numberPeaks], 5)}\t±\t{round(parStDev[i+1+2*numberPeaks], 5)}\n\n")
	
	# print out latex list
	
	captionL = "Fitparameter der Peaks für %s" % caption
	headers = ["$\\#$ des Peaks", "$x_0$", "amp", "fwhm"]
	
	ii = list(range(1, numberPeaks + 1))
		
	x_0s = zipValuesErrors(par[1:numberPeaks+1], parStDev[1:numberPeaks+1], True)
	amps = zipValuesErrors(par[numberPeaks + 1 : 2 * numberPeaks + 1], parStDev[numberPeaks + 1 : 2 * numberPeaks + 1], True)
	fwhms = zipValuesErrors(par[2 * numberPeaks + 1 : ], parStDev[2 * numberPeaks + 1 : ], True)
	
	showListAsLatexTable(captionL, caption, headers, [ii, x_0s, amps, fwhms])
	
	velocitiesFit = np.linspace(-1, 1.01, 1500)
	for v in velocitiesFit:
		fitCounts.append(lorentzianX6(v, *par))
	
	# plotting
	
	# reasonable boundary
	minX = -1
	maxX = 1
	# maxY = (1.2 * maxY) + (-maxY * 1.2) % (10 ** math.floor(math.log10(maxY * 0.4)))
	minY, maxY = (ymin, ymax)
	
	plot.plot(velocities, counts, label="Messwerte", color="violet")
	plot.plot(velocitiesFit, fitCounts, label="Fit", color="red")
	plot.axis([minX, maxX, minY, maxY])
	
	plot.legend(loc="lower left")
	plot.xlabel("Geschwindigkeit (unbekannter Faktor)")
	plot.ylabel(f"Anzahl Ereignisse")
	if (savePlots):
		plot.savefig("Abbildungen/" + saveName + ".png", dpi=300, transparent = True)
	if(showPlots):
		plot.show()

# peakFit("Eisenfolie", "Eisen_folie_NEU.txt", 4, "Eisen", 6, 0.21, 22000, 32000)
# auswertung("Stahlfolie", "Stahl_folie.txt", 5, "Stahl", 1)