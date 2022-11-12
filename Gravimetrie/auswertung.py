import math
import seaborn as sns
import inputOutput
from GitHubFiles import count2mgal_cologne, geo2utm, utm2geo, gezeiten
import matplotlib.pyplot as plot
import matplotlib
import driftkorrektur
import numpy as np
import statsmodels.api as sm
from gravMath import linearRegression, gravitationAnomalyOfPolygon
import auswertung1, auswertung2, auswertung3, auswertung4


# --- Einstellungen ---

plot.style.use('seaborn-whitegrid')


# --- Auswertung der Referenzdaten für Driftkorrektur ---



# read in data
datapoints = inputOutput.readRawData("referenz.csv")

# tidal correction
for i in range(0, len(datapoints)):
	d = datapoints[i]
	t = d.time
	geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3]) # utm to gps
	datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)

timediff = []
gravBefore = []
for d in datapoints:
	timediff.append((d.time - datapoints[0].time).total_seconds() / 60.0)
	gravBefore.append(d.gravitation)

# # display reference data as scatter plot
# plot.scatter(timediff, grav, label="nachher")
# plot.show()

# calculate slope of the drift
(slopeDrift, interceptDrift) = driftkorrektur.übergabe(x=timediff, y=gravBefore)

# calculate values to display linear regression line
xValuesDriftReg = range(0, 500)
yValuesDriftReg = []
for xValue in xValuesDriftReg:
	yValuesDriftReg.append(slopeDrift * xValue + interceptDrift)

# # show plot for values and regression
# plot.scatter(timediff, grav, label="Daten inklusive Gezeitenkorrektur")
# plot.plot(xValuesDriftReg, yValuesDriftReg, label = "Lineare Regression für Driftkorrektur", color = "green")
# plot.xlabel("Zeitdifferenz zur ersten Referenzmessung [min]")
# plot.ylabel("$\delta g$ [mGal]")
# plot.legend(loc="upper center")
# plot.axis([0, 500, 4926, 4927])
# plot.minorticks_on()
# plot.show()

auswertung3.auswertung(slopeDrift)