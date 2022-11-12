import matplotlib.pyplot as plot

from InputOutput import readRawData
from prakMath import linearRegression

# convert channel number to wavelength [nm] for 1024 channels
channelNumbers = range(1024)
wavelengths1024 = []
for n in channelNumbers:
    wavelengths1024.append(316.049929 + 0.1500302240 * 2 * n)
    
# convert channel number to wavelength [nm] for 2048 channels
channelNumbers = range(2048)
wavelengths2048 = []
for n in channelNumbers:
    wavelengths2048.append(316.049929 + 0.1500302240 * n)


channels0V = readRawData("Messdaten\Iod_0V.txt")
channels0V = channels0V[1024:]
channels10V = readRawData("Messdaten\Iod_10V.txt")
channels22V = readRawData("Messdaten\Iod_22V.txt")
channels35V = readRawData("Messdaten\Iod_35V.txt")

plot.plot(wavelengths1024, channels0V, label='U = 0V')
plot.plot(wavelengths1024, channels10V, label='U = 10V')
plot.plot(wavelengths1024, channels22V, label='U = 22V')
plot.plot(wavelengths1024, channels35V, label='U = 35V')
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge [nm]")
plot.ylabel("Intensität [a.u.]")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()