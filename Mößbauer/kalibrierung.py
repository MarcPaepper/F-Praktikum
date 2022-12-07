from matplotlib import pyplot as plot
from scipy.optimize import curve_fit
from scipy.stats.distributions import t
import numpy as np
import math
from sklearn.metrics import r2_score
from inputOutput import *
import math

def kalib():
    # read values
    (voltages, velocities, velErrs, voltErrs) = readRawKalib("Messwerte/kalib.txt")
    
    plot.errorbar(voltages, velocities, yerr=velErrs, fmt='s', capsize=3)
    plot.axis([0, 225, 0, 35])
    plot.show()

kalib()