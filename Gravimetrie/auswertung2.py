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

# --- Versuchsteil 2 ---

def auswertung(slopeDrift):
    # read in data
    datapoints = inputOutput.readRawData("Rohdaten_2.csv")

    # tidal correction
    gravBeforeTidalCorr = []
    for i in range(0, len(datapoints)):
        d = datapoints[i]
        t = d.time
        geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3])
        gravBeforeTidalCorr.append(datapoints[i].gravitation)
        datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)

    # drift correction
    for d in datapoints:
        timediff = (d.time - datapoints[0].time).total_seconds() / 60.0
        driftcorr = timediff * slopeDrift
        d.gravitation += driftcorr

    # height correction (Freiluftkorrektur)
    for d in datapoints:
        heightDiff = d.height - datapoints[0].height
        heightGradient = 0.308 # hardcoded in mGal / meter
        d.gravitation += heightGradient * heightDiff

    # populate two lists for x values (distance) and y values (gravitation)
    distances = []
    grav = []
    for d in datapoints:
        distances.append(d.distance)
        grav.append(d.gravitation)


    # calculate expected values

    # polygonal model of the railway embankment
    polygon = []
    polygon.append((12.05, 0.000))
    polygon.append((32.55, 0.000))
    polygon.append((24.98, 5.649))
    polygon.append((19.65, 5.649))


    # calculate gravitational defect due to the embankment attraction
    startValue = (datapoints[0].gravitation + datapoints[6].gravitation)/2
    xValuesEmbankment = np.arange(-5, 50, 0.05)
    yValuesEmbankment = []
    for x in xValuesEmbankment:
        yValuesEmbankment.append(startValue - gravitationAnomalyOfPolygon(polygon, (x, -0.1), 1680)) # the slight offset is needed because the math breaks down if the z values match exactly

    # move the model data vertically so that it matches with the start value at x=0
    diff = startValue - yValuesEmbankment[0]
    for i in range(0, len(yValuesEmbankment)):
        yValuesEmbankment[i] += diff

    # show plot
    fig = plot.figure(figsize=(8, 5), dpi=100)
    plot.errorbar(distances, grav, xerr=0.05, yerr=0.021, ls="none", label="Messpunkte")
    plot.plot(xValuesEmbankment, yValuesEmbankment, label="Modelldaten", color="green")
    plot.xlabel("Distanz in Messrichtung")
    plot.ylabel("$\delta g$ [mGal]")
    plot.legend(loc="upper center")
    plot.axis([-5, 50, 4926.25, 4926.6])
    plot.minorticks_on()
    plot.show()

    # print("Ablesefehler Gravimeter " + str(count2mgal_cologne.count2mgal(4814.92)[0] - count2mgal_cologne.count2mgal(4814.90)[0]))