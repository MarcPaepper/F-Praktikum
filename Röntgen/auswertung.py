import matplotlib.pyplot as plot
from scipy.optimize import curve_fit
from scipy.stats.distributions import  t
import numpy as np
import math

from InputOutput import readRawData


messreihen = []	#  file name                  	color	      	label											calcPeak
messreihen.append(["221109_Sifein_Peak1.txt", 	"darkgreen",	"Silizium fein, Winkel 27-30 Grad",				True])
messreihen.append(["221109_Sifein_Peak2.txt", 	"forestgreen",	"Silizium fein, Winkel 46-49 Grad",				True])
messreihen.append(["221109_Sifein_Peak3.txt", 	"limegreen",	"Silizium fein, Winkel 55-58 Grad",				True])
messreihen.append(["221109_Sigrob_Peak1.txt", 	"darkred",		"Silizium grob, Winkel xx-xx",					True])
messreihen.append(["221109_Sigrob_Peak2.txt", 	"firebrick",	"Silizium grob, Winkel xx-xx",					True])
messreihen.append(["221109_Sigrob_Peak3.txt", 	"indianred",	"Silizium grob, Winkel xx-xx",					True])
messreihen.append(["221109_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	False])
messreihen.append(["221110_unbekanntesSalz.txt","goldenrod", 	"unbekanntes erstes Salz, Winkel 10-120 Grad",	False])

# Plot all data

drawPlots = True
savePlots = True
first = True

initialGuessGauss = [0, 100, 0.7, 50]
alpha = 0.10 # 90%-confidence intervals for fit parameters

# fit curves

def gaussian(x, x_0, stretch, a, offset):
    'nonlinear function in a and b to fit to data'
    return (offset + stretch * math.e ** (- a * (x - x_0) ** 2))

for filename, color, label, calcPeak in messreihen:
	# read in data
	datapoints = readRawData(filename)
	[minX, minY] = [min(l) for l in zip(*datapoints)]
	[maxX, maxY] = [max(l) for l in zip(*datapoints)]
	
	if (calcPeak):
		# fit peak curves
		initialGuessGauss[0] = (maxX + minX) / 2
		angles 		= [row[0] for row in datapoints]
		intensities = [row[1] for row in datapoints]
		par, pcov = curve_fit(gaussian, np.array(angles), np.array(intensities), p0=initialGuessGauss)
		parStDev = np.sqrt(np.diag(pcov))
		print(f" --- Fit for {label} ---")
		print(f"x_0 	{par[0]} +- {parStDev[0]}")
		print(f"stretch {par[1]} +- {parStDev[1]}")
		print(f"a 		{par[2]} +- {parStDev[2]}")
		print(f"offset 	{par[3]} +- {parStDev[3]}")
		
		calcInt = [gaussian(angle, par[0], par[1], par[2], par[3]) for angle in angles]
		plot.plot(angles, calcInt, color="black")
	
	# plot data
	plot.plot(angles, intensities, label = label, color = color)
	maxY = (1.1 * maxY) + (-maxY * 1.1) % (10 ** math.floor(math.log10(maxY * 0.5)))
	plot.axis([minX, maxX+0.02, 0, maxY])
	plot.legend(loc="upper left")
	plot.xlabel("Winkel")
	plot.ylabel(f"Intensität, {maxX}")
	if (savePlots):
		plot.savefig("Abbildungen/" + filename.replace(".txt", ".png"), dpi=300, transparent = True)
	if(first or drawPlots):
		plot.show()
		first = False
		


# datapointsSifein1	 = readRawData("221109_Sifein_Peak1.txt")
# datapointsSifein2	 = readRawData("221109_Sifein_Peak2.txt")
# datapointsSifein3	 = readRawData("221109_Sifein_Peak3.txt")
# datapointsSigrob1	 = readRawData("221109_Sigrob_Peak1.txt")
# datapointsSigrob2	 = readRawData("221109_Sigrob_Peak2.txt")
# datapointsSigrob3	 = readRawData("221109_Sigrob_Peak3.txt")
# datapointsUnbekannt1 = readRawData("221109_unbekanntesSalz.txt")
# datapointsUnbekannt2 = readRawData("221110_unbekanntesSalz.txt")
# messreihen = [datapointsSifein1, datapointsSifein2, datapointsSifein3, datapointsSigrob1, datapointsSigrob2, datapointsSigrob3, datapointsUnbekannt1, datpointsUnbekannt2]
# colors = ["darkgreen", "forestgreen", "limegreen", "darkred", "firebrick", "indianred", "goldenrod", "darkgoldenrod"]
# labels = ["Silizium fein, Winkel 27-30 Grad", "Silizium fein, Winkel 46-49 Grad", "Silizium fein, Winkel 55-58", "Silizium grob, Winkel xx-xx", "Silizium grob, Winkel xx-xx", "Silizium grob, Winkel xx-xx", 'unbekanntes erstes Salz, Winkel 10-120 Grad', 'unbekanntes erstes Salz, Winkel 10-120 Grad']

# dp = datapointsSifein1
# plot.plot(*zip(*dp), label='Silizium fein, Winkel 27-30 Grad', color = "darkgreen")
# [minX, minY] = [min(l) for l in zip(*dp)]
# [maxX, maxY] = [max(l) for l in zip(*dp)]
# maxY = maxY + (-maxY) % 100 if maxY < 100 else maxY + (-maxY) % 100
# plot.axis([minX, maxX, 0, maxY])
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(True):
	# plot.show()

# dp = datapointsSifein2
# plot.plot(*zip(*datapointsSifein2), label='Silizium fein, Winkel 46-49 Grad', color = "forestgreen")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# dp = datapointsSifein3
# plot.plot(*zip(*datapointsSifein3), label='Silizium fein, Winkel 55-58 Grad', color = "limegreen")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# plot.plot(*zip(*datapointsSigrob1), label='Silizium grob, Winkel 55-58 Grad', color = "darkred")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# plot.plot(*zip(*datapointsSigrob2), label='Silizium grob, Winkel 55-58 Grad', color = "firebrick")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# dp = datapointsSigrob3
# plot.plot(*zip(*datapointsSigrob3), label='Silizium grob, Winkel 55-58 Grad', color = "indianred")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# dp = datapointsUnbekannt1
# plot.plot(*zip(*datapointsUnbekannt1), label='unbekanntes erstes Salz, Winkel 10-120 Grad', color = "goldenrod")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()

# dp = datapointsUnbekannt2
# plot.plot(*zip(*datapointsUnbekannt2), label='unbekanntes zweites Salz, Winkel 10-120 Grad', color = "darkgoldenrod")
# plot.legend(loc="upper left")
# plot.xlabel("Winkel")
# plot.ylabel("Intensität")
# if (savePlots):
	# plot.savefig("transparenteKalibrierung", transparent = True)
# if(drawPlots):
	# plot.show()
