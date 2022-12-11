from matplotlib import pyplot as plot
from scipy.optimize import curve_fit
from scipy.stats.distributions import t
import numpy as np
import math
from sklearn.metrics import r2_score
from inputOutput import *
from prakMath import linearRegression
import math

def kalib():
    # read values
    (voltages, velocities, velErrs, voltErrs) = readRawKalib("Messwerte/kalib.txt")
    
    # plot before adding
    plot.errorbar(voltages, velocities, yerr=velErrs, fmt='s', color="blue", capsize=5, markersize=3, label="Messdaten (vorige Gruppen)")
    
    # add own value
    voltages.append(63)
    velocities.append(10.232)
    
    # plot own value
    plot.errorbar([63], [10.232], yerr=[.044], fmt="s", color="red", capsize=5, markersize=3, label="Messdaten (neuer Wert)")
        
    # lin reg
    (slope, intcp, slopeErr, intcpErr) = linearRegression(voltages, velocities, descr="Kalibrierung")
    
    # interp values
    xVal = [0, 255]
    yVal = [x * slope + intcp for x in xVal]
    
    # plot
    plot.plot(xVal, yVal, color="violet", label="Lineare Regression")
    plot.axis([0, 225, 0, 35])
    plot.legend(loc="upper left")
    plot.savefig("Abbildungen/Kalibrierung.png", dpi=300)
    plot.show()

kalib()