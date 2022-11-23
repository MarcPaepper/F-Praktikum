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

# --- Versuchsteil 1 ---

def auswertung(slopeDrift, slopeIntercept):
    # read in data
    datapoints = inputOutput.readRawData("Rohdaten_1.csv")

    # tidal correction
    gravBeforeTidalCorr = []
    for i in range(0, len(datapoints)):
        d = datapoints[i]
        t = d.time
        geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3])
        gravBeforeTidalCorr.append(datapoints[i].gravitation)
        datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)

    # store data to plot it later
    gravBeforeDriftCorr = []
    for d in datapoints:
        gravBeforeDriftCorr.append(d.gravitation)

    # drift correction
    for d in datapoints:
        timediff = (d.time - datapoints[0].time).total_seconds() / 60.0
        driftcorr = slopeIntercept + timediff * slopeDrift
        d.gravitation -= driftcorr

    # make two lists for the heights (x values) and gravitational acceleration (y values)
    heights = []
    grav = []
    for d in datapoints:
        heights.append(d.height)
        grav.append(d.gravitation)

    # linear regression to find vertical gradient (acceleration per height)
    heightGradient = linearRegression(heights, grav)
    slopeHeightGradient = heightGradient[0]
    interceptHeightGradient = heightGradient[1]
    print("höhengradient " + str(heightGradient))

    # calculate values to display linear regression line
    xValuesGradient = [0, 30]
    yValuesGradient = []
    for xValue in xValuesGradient:
        yValuesGradient.append(slopeHeightGradient * xValue + interceptHeightGradient)

    # show plot for values before and after tidal / drift correction and the linear fit
    plot.figure(figsize=(8, 6), dpi=100)
    plot.scatter(heights, gravBeforeTidalCorr, label="unkorrigierte Daten")
    plot.scatter(heights, gravBeforeDriftCorr, label="nach Gezeitenkorr.")
    plot.scatter(heights, grav, label="nach Driftkorr.")
    plot.plot(xValuesGradient, yValuesGradient, label="Linearer Fit der korrigierten Daten", color="green")
    plot.xlabel("Höhendifferenz zum 2. Untergeschoss [m]")
    plot.ylabel("$\delta g$ [mGal]")
    plot.legend(loc="upper center")
    plot.axis([0, 30, 4915, 4930])
    plot.yticks(range(4915, 4935, 5))
    plot.minorticks_on()
    #plot.show()

    # Calculate heights from our measured vertical gradient
    errechneteHoehen = []
    for h in datapoints:
        eH = (datapoints[0].gravitation - h.gravitation) / 0.308
        errechneteHoehen.append(eH)