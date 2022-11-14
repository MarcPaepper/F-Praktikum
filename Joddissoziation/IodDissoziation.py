from matplotlib import pyplot as plot
from prakMath import *

# calculated energies of each excited state E(n), see Google Sheet

energies = [0.016, 0.016, 0.018, 0.012, 0.017, 0.015, 0.018, 0.015, 0.017, 0.016, 0.016, 0.016, 0.016, 0.015, 0.015, 0.018, 0.014, 0.016, 0.015, 0.015, 0.016, 0.014, 0.016, 0.014, 0.016, 0.013, 0.015, 0.013, 0.014, 0.012, 0.013, 0.011, 0.012]
energyErrors = [0.006, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.004]
numbers = range(1, len(energies) + 1) # the number of each excited state

# lin reg

(slope, intercept, slopeErr, interceptErr) = linearRegression(numbers, energies, descr="energies")
(regX, regY) = linearValues(0, 150, slope, intercept)

# plot values and regression (close up)

plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(regX, regY, color="green", label="Linearer Fit")
plot.errorbar(numbers, energies, yerr=energyErrors, fmt='o', label="Messdaten")
plot.axis([0, 40, 0.0, 0.025])

plot.legend(loc="upper right")
plot.xlabel("Zahl des Anregungsniveaus (n)")
plot.ylabel("Energie E(n) / eV")
# plot.savefig("Abbildungen\Jod_Energie_CloseUp")
plot.minorticks_on()
# plot.grid()

plot.show()

# plot values and regression

plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(regX, regY, color="green", label="Linearer Fit")
plot.scatter(numbers, energies, label="Messdaten")
plot.axis([0, 160, 0.0, 0.02])

plot.legend(loc="upper right")
plot.xlabel("Zahl des Anregungsniveaus (n)")
plot.ylabel("Energie ΔE(n) / eV")
plot.savefig("Abbildungen\Jod_Energie")
plot.minorticks_on()
plot.grid()

plot.show()