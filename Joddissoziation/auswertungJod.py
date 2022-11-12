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

# plot.figure(figsize=(8, 5.5), dpi=100)
# plot.plot(wavelengths1024, channels0V, label='U = 0V', color="blue")
# plot.plot(wavelengths1024, channels10V, label='U = 10V', color="violet")
# plot.plot(wavelengths1024, channels22V, label='U = 22V', color="orangered")
# plot.plot(wavelengths1024, channels35V, label='U = 35V', color="gold")
# plot.legend(loc="upper right")
# plot.xlabel("Wellenlänge [nm]")
# plot.ylabel("Intensität [a.u.]")
# plot.axis([320, 620, 0, 260])
# plot.minorticks_on()
# plot.savefig("Abbildungen\Jod_Übersicht", transparent = True)
# plot.show()


plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(wavelengths1024, channels0V, label='U = 0V', color="blue")
plot.plot(wavelengths1024, channels10V, label='U = 10V', color="violet")
plot.plot(wavelengths1024, channels22V, label='U = 22V', color="orangered")
plot.plot(wavelengths1024, channels35V, label='U = 35V', color="gold")
plot.legend(loc="upper right")
plot.xlabel("Wellenlänge [nm]")
plot.ylabel("Intensität [a.u.]")
plot.axis([430, 530, 0, 170])
plot.minorticks_on()
plot.savefig("Abbildungen\Jod_Übersicht_CloseUp", transparent = True)
plot.show()