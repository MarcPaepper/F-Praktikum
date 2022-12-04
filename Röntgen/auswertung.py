import matplotlib.pyplot as plot
from scipy.optimize import curve_fit
from scipy.stats.distributions import  t
import numpy as np
import math
from sklearn.metrics import r2_score

from InputOutput import readRawData


messreihen = []	#  file name                  	color	      	label											calcPeak
# messreihen.append(["221109_Sifein_Peak1.txt", 	"darkgreen",	"Silizium fein, Winkel 27-30 Grad",				True])
# messreihen.append(["221109_Sifein_Peak2.txt", 	"forestgreen",	"Silizium fein, Winkel 46-49 Grad",				True])
# messreihen.append(["221109_Sifein_Peak3.txt", 	"limegreen",	"Silizium fein, Winkel 55-58 Grad",				True])
# messreihen.append(["221109_Sigrob_Peak1.txt", 	"sienna",		"Silizium grob, Winkel xx-xx",					True])
# messreihen.append(["221109_Sigrob_Peak2.txt", 	"coral",	"Silizium grob, Winkel xx-xx",					True])
# messreihen.append(["221109_Sigrob_Peak3.txt", 	"orange",	"Silizium grob, Winkel xx-xx",					True])
# messreihen.append(["221109_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	False])
messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	False])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 26-29 Grad",	26, 29, "unbSalzPeak1"])
messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 26-29 Grad",	29, 34, "unbSalzPeak1,5"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 44-48 Grad",	44, 48, "unbSalzPeak2"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 52-56 Grad",	52, 56, "unbSalzPeak3"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 55-59 Grad",	55, 59, "unbSalzPeak4"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 65-68 Grad",	65, 68, "unbSalzPeak5"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 74-77 Grad",	74, 77, "unbSalzPeak6"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 83-86 Grad",	83, 86, "unbSalzPeak7"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 100-103 Grad",	100, 103, "unbSalzPeak8"])
# # messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	107, 110])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 109-112 Grad",	109, 112, "unbSalzPeak9"])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 117-120 Grad",	114, 120, True, "unbSalzPeak10", 119.5])
# messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	, ])

# Plot all data

drawPlots = False
savePlots = True
first = True

initGauss =		[0, 500, 1, 50, 0]
initLorentz =	[0, 500, 1, 50, 0]
initVoigt =		[0, 1000, 3, 3, 50, 20, -2]
param_bounds=([-np.inf,-np.inf,0,0,-30,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf,100,np.inf,np.inf]) # limit eta of voigt between 0 and 1

# fit curves

def gaussian(x, x_0, amplitude, fwhm, noiseOffset, noiseSlope):
	sigma = fwhm / (2 * math.sqrt(2 * math.log(2)))
	noise = noiseOffset + (x - x_0) * noiseSlope
	gauss = math.e ** (- 0.5 * ((x - x_0) ** 2)/(sigma ** 2))
	return amplitude * gauss + noise

def lorentzian(x, x_0, amplitude, fwhm, noiseOffset, noiseSlope):
	gamma = abs(fwhm) / 2
	noise = noiseOffset + (x - x_0) * noiseSlope
	lorentz = (gamma ** 2) / ((x - x_0) ** 2 + gamma ** 2)
	return amplitude * lorentz + noise

def pseudo_voigt(x, x_0, amplitude, fwhm_gauss, fwhm_lorentz, eta, noiseOffset, noiseSlope):
	eta = max(min(eta/100, 1), 0)
	noise = noiseOffset + (x - x_0) * noiseSlope
	gauss = gaussian(x, x_0, 1, fwhm_gauss, 0, 0)
	lorentz = lorentzian(x, x_0, 1, fwhm_lorentz, 0, 0)
	return amplitude * (eta * lorentz + (1 - eta) * gauss) + noise

for messreihe in messreihen:
	# check which arguments were given
	if (len(messreihe) == 4):
		filename, color, label, calcPeak = messreihe
		saveName = filename
		useStartValue = False
		
		# read in data
		datapoints = readRawData(filename)
		[minX, minY] = [min(l) for l in zip(*datapoints)]
		[maxX, maxY] = [max(l) for l in zip(*datapoints)]
		
		# delete 0 values at beginning
		while 0 < len(datapoints):
			if (datapoints[0][1] == 0):
				datapoints.pop(0)
			else:
				break
		
		# draw all fits
		drawG = drawL = drawV = True
	elif (len(messreihe) == 6):
		filename, color, label, minX, maxX, saveName = messreihe
		calcPeak = True
		useStartValue = False
		
		# read in data
		datapoints = readRawData(filename)
		
		# delete 0 values and values outside the bounds
		while 0 < len(datapoints):
			if (datapoints[0][1] == 0 or datapoints[0][0] < minX):
				datapoints.pop(0)
			else:
				break
		
		while 0 < len(datapoints):
			dp = datapoints[len(datapoints)-1]
			if (dp[0] > maxX):
				datapoints.pop(len(datapoints)-1)
			else:
				break
		
		# only draw voigt because it has the best results
		drawG = drawL = False
		drawV = True
	else:
		filename, color, label, minX, maxX, drawAll, saveName, startValue = messreihe
		useStartValue = True
		calcPeak = True
		
		# read in data
		datapoints = readRawData(filename)
		
		# delete 0 values and values outside the bounds
		while 0 < len(datapoints):
			if (datapoints[0][1] == 0 or datapoints[0][0] < minX):
				datapoints.pop(0)
			else:
				break
		
		while 0 < len(datapoints):
			dp = datapoints[len(datapoints)-1]
			if (dp[0] > maxX):
				datapoints.pop(len(datapoints)-1)
			else:
				break
		print("hallo ballo")
		if (drawAll):
			drawG = drawL = drawV = True
		else:
			drawG = drawL = drawV = False
	# delete all outliers
	i = 1
	while i < len(datapoints) - 1:
		if (datapoints[i - 1][1] + 100 < datapoints[i][1] and datapoints[i + 1][1] + 100 < datapoints[i][1]):
			datapoints.pop(i)
		else:
			i += 1
	
	angles		= [row[0] for row in datapoints]
	intensities	= [row[1] for row in datapoints]
	fig = plot.figure(figsize=(8, 5.5), dpi=100)
	
	if (calcPeak):
		# fit peak curves
		angles = np.array(angles)
		intensities = np.array(intensities)
		initGauss[0] = initLorentz[0] = initVoigt[0] = startValue if useStartValue else (maxX + minX) / 2 # set x_0 at the middle
		
		parG, pcovG = curve_fit(gaussian,     angles, intensities, p0=initGauss)
		parL, pcovL = curve_fit(lorentzian,   angles, intensities, p0=initLorentz)
		parL[2] = abs(parL[2])
		parG[2] = abs(parG[2])
		
		initVoigt[0] = (parG[0] + parL[0])/2
		initVoigt[1] = (parG[1] + parL[1])/2
		initVoigt[2] = parG[2]
		initVoigt[3] = parL[2]
		initVoigt[5] = (parG[3] + parL[3])/2
		initVoigt[6] = (parG[4] + parL[4])/2
		
		i = 0
		vSuccess = False
		while not vSuccess and i < 2:
			try:
				if (i == 0):
					parV, pcovV = curve_fit(pseudo_voigt, angles, intensities, p0=initVoigt, bounds=param_bounds)
				if (i == 1):
					parV, pcovV = curve_fit(pseudo_voigt, angles, intensities, p0=initVoigt)
				vSuccess = True
			except Exception as inst:
				print(type(inst))    # the exception instance
				print(inst.args)     # arguments stored in .args
				print(inst)
				vSuccess = False
				parV = initVoigt
			i += 1
		parStDevG = np.sqrt(np.diag(pcovG))
		parStDevL = np.sqrt(np.diag(pcovL))
		parStDevV = np.sqrt(np.diag(pcovV))
		
		# calc R²
		calcIntG = [gaussian    (angle, parG[0], parG[1], parG[2], parG[3], parG[4]) for angle in angles]
		calcIntL = [lorentzian  (angle, parL[0], parL[1], parL[2], parL[3], parL[4]) for angle in angles]
		calcIntV = [pseudo_voigt(angle, parV[0], parV[1], parV[2], parV[3], parV[4], parV[5], parV[6]) for angle in angles]
		rSquaredG = r2_score(intensities, calcIntG)
		rSquaredL = r2_score(intensities, calcIntL)
		rSquaredV = r2_score(intensities, calcIntV)
		
		# print fit parameters
		# print(f" --- Gauss Fit for {label} ---")
		# print(f"x_0 		{round(parG[0], 3)}    +-    {round(parStDevG[0], 3)}")
		# print(f"amplitude	{round(parG[1], 3)}    +-    {round(parStDevG[1], 3)}")
		# print(f"fwhm 		{round(parG[2], 3)}    +-    {round(parStDevG[2], 3)}")
		# print(f"noise offset 	{round(parG[3], 3)}    +-    {round(parStDevG[3], 3)}")
		# print(f"noise slope 	{round(parG[4], 3)}    +-    {round(parStDevG[4], 3)}")
		# print(f"R² 		{round(rSquaredG, 4)}\r\n")
		
		# print(f" --- Lorentz Fit for {label} ---")
		# print(f"x_0 		{round(parL[0], 3)}    +-    {round(parStDevL[0], 3)}")
		# print(f"amplitude	{round(parL[1], 3)}    +-    {round(parStDevL[1], 3)}")
		# print(f"fwhm 		{round(parL[2], 3)}    +-    {round(parStDevL[2], 3)}")
		# print(f"noise offset 	{round(parL[3], 3)}    +-    {round(parStDevL[3], 3)}")
		# print(f"noise slope 	{round(parL[4], 3)}    +-    {round(parStDevL[4], 3)}")
		# print(f"R² 		{round(rSquaredL, 4)}\r\n")
		
		print(f" --- Voigt Fit for {label} ---")
		print(f"x_0 		{round(parV[0], 3)}    +-    {round(parStDevV[0], 3)}")
		print(f"amplitude	{round(parV[1], 3)}    +-    {round(parStDevV[1], 3)}")
		print(f"fwhm_gauss 	{round(parV[2], 3)}    +-    {round(parStDevV[2], 3)}")
		print(f"fwhm_lorentz 	{round(parV[3], 3)}    +-    {round(parStDevV[3], 3)}")
		eta_comb = 0.5 * (parV[4]*parV[3])/100 + ((1-parV[4]/100)*parV[2]) + 0.25 * parG[2] + 0.25 * parL[2]
		eta_comb_err = 0.5 * (parV[4]/100*parStDevV[3] + (1-parV[4]/100)*parStDevV[2]) + 0.25 * parStDevG[2] + 0.25 * parStDevL[2]
		print(f"fwhm_comb 	{round(eta_comb, 3)}    +-    {round(eta_comb_err, 3)}")
		print(f"eta 		{round((parV[4]/100), 3)}    +-    {round((parStDevV[4]/100), 3)}")
		# print(f"noise offset 	{round(parV[5], 3)}    +-    {round(parStDevV[5], 3)}")
		# print(f"noise slope 	{round(parV[6], 3)}    +-    {round(parStDevV[6], 3)}")
		print(f"R² 		{round(rSquaredV, 4)}\r\n\r\n\r\n")
		
		
		# simulate fit values for the plot
		calcAngles = np.linspace(minX, maxX, 500)
		calcIntG = [gaussian(angle, parG[0], parG[1], parG[2], parG[3], parG[4]) for angle in calcAngles]
		calcIntL = [lorentzian(angle, parL[0], parL[1], parL[2], parL[3], parL[4]) for angle in calcAngles]
		calcIntV = [pseudo_voigt(angle, parV[0], parV[1], parV[2], parV[3], parV[4], parV[5], parV[6]) for angle in calcAngles]
		
		if (drawG and not vSuccess):
			plot.plot(calcAngles, calcIntG, zorder=.3, color="blue",       	label=f"Fit (Gauß)") #  - $   R^2={round(rSquaredG, 4)}$
		if (drawL and not vSuccess):
			plot.plot(calcAngles, calcIntV, zorder=.7, color="blueviolet", 	label=f"Fit (Voigt)")
		if (drawV and vSuccess):
			plot.plot(calcAngles, calcIntL, zorder=.5, color="mediumvioletred",label=f"Fit (Lorentz)")
	
	# plot data
	plot.plot(angles, intensities, label = "Messwerte", color = color)
	minX = minX - (+minX % 0.5)
	maxX = maxX + (-maxX % 0.5)
	maxY = max(intensities)
	maxY = (1.2 * maxY) + (-maxY * 1.2) % (10 ** math.floor(math.log10(maxY * 0.4)))
	plot.axis([minX, maxX, 0, maxY])
	plot.legend(loc="upper left")
	plot.xlabel("Winkel ($2\\theta$) in °")
	plot.ylabel(f"Intensität")
	if (savePlots):
		plot.savefig("Abbildungen/" + saveName.replace(".txt", "") + ".png", dpi=300, transparent = True)
	if(first or drawPlots):
		plot.show()
		first = False
	# if (not (savePlots or drawPlots)):
	# 	break