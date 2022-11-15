from matplotlib import pyplot as plot
from prakMath import *

# calculated energy slopes dE/dN for h = 1 and h = 4, see Google Sheet

energiesH1 = [0.016, 0.016, 0.018, 0.012, 0.017, 0.015, 0.018, 0.015, 0.017, 0.016, 0.016, 0.016, 0.016, 0.015, 0.015, 0.018, 0.014, 0.016, 0.015, 0.015, 0.016, 0.014, 0.016, 0.014, 0.016, 0.013, 0.015, 0.013, 0.014, 0.012, 0.013, 0.011, 0.012]
energiesH4 = [0.0165, 0.0152, 0.0155, 0.0145, 0.0168, 0.0160, 0.0168, 0.0161, 0.0164, 0.0160, 0.0159, 0.0156, 0.0155, 0.0160, 0.0157, 0.0159, 0.0152, 0.0155, 0.0155, 0.0152, 0.0154, 0.0148, 0.0152, 0.0143, 0.0147, 0.0137, 0.0142, 0.0129, 0.0128, 0.0118, 0.0121]
energyErrH1 = [0.006, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.005, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.004, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.003, 0.004]
energyErrH4 = [0.0021, 0.0017, 0.0017, 0.0016, 0.0016, 0.0016, 0.0014, 0.0014, 0.0014, 0.0012, 0.0012, 0.0012, 0.0012, 0.0012, 0.0012, 0.0011, 0.0011, 0.0011, 0.0011, 0.0011, 0.0011, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0010, 0.0009, 0.0010, 0.0013]
numbersH1 = range(1, len(energiesH1) + 1) # the number of each excited state
numbersH4 = range(1, len(energiesH4) + 1)

# lin reg

(slopeH1, interceptH1, slopeErrH1, interceptErrH1) = linearRegression(numbersH1, energiesH1, descr="energies (h = 1)")
(slopeH4, interceptH4, slopeErrH4, interceptErrH4) = linearRegression(numbersH4, energiesH4, descr="energies (h = 3)")
(regXH1, regYH1) = linearValues(0, 150, slopeH1, interceptH1)
(regXH4, regYH4) = linearValues(0, 150, slopeH4, interceptH4)

# plot values and regression (close up) h1

plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(regXH1, regYH1, color="green", label="Linearer Fit")
plot.errorbar(numbersH1, energiesH1, yerr=energyErrH1, fmt='o', label="Messdaten")
plot.axis([0, 40, 0.0, 0.025])

plot.legend(loc="upper right")
plot.xlabel("Zahl des Anregungsniveaus (n)")
plot.ylabel(r"Energieniveaudifferenzen $\frac{E(n + 1) - E(n)} {1}$ in eV")
plot.savefig("Abbildungen\Jod_Energie_CloseUp")
plot.minorticks_on()
# plot.grid()

plot.show()

# plot values and regression (close up) h4

plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(regXH4, regYH4, color="green", label="Linearer Fit")
plot.errorbar(numbersH4, energiesH4, yerr=energyErrH4, fmt='o', label="Messdaten")
plot.axis([0, 40, 0.0, 0.025])

plot.legend(loc="upper right")
plot.xlabel("Zahl des Anregungsniveaus (n)")
plot.ylabel(r'Energieniveaudifferenzen $\frac{E(n + 3) - E(n)} {3}$ in eV')
plot.savefig("Abbildungen\Jod_Energie_CloseUp_h3")  
plot.minorticks_on()
# plot.grid()

plot.show()

# # plot values and regression

# plot.figure(figsize=(8, 5.5), dpi=100)
# plot.plot(regXH1, regYH1, color="green", label="Linearer Fit")
# plot.scatter(numbersH1, energiesH1, label="Messdaten")
# plot.axis([0, 160, 0.0, 0.02])

# plot.legend(loc="upper right")
# plot.xlabel("Zahl des Anregungsniveaus (n)")
# plot.ylabel("Energie ΔE(n) / eV")
# plot.savefig("Abbildungen\Jod_Energie")
# plot.minorticks_on()
# plot.grid()

plot.show()