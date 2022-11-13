import matplotlib.pyplot as plot

from InputOutput import readRawData
import math
from prakMath import linearRegression

# convert channel number to wavelength [nm] for 1024 channels
channels = range(1024)
wavelengths1024 = []
for n in channels:
    wavelengths1024.append(316.049929 + 0.1500302240 * 2 * n)

intensity0V = readRawData("Messdaten\Iod_0V.txt")
intensity0V = intensity0V[1024:]
intensity10V = readRawData("Messdaten\Iod_10V.txt")
intensity22V = readRawData("Messdaten\Iod_22V.txt")
intensity35V = readRawData("Messdaten\Iod_35V.txt")
intensity10VN = []
intensity22VN = []
intensity35VN = []
intensityAvgN = []

for i35, i22, i10, i0 in zip(intensity35V, intensity22V, intensity10V, intensity0V):
    intensity35VN.append(i35 / i0)
    intensity22VN.append(i22 / i0)
    intensity10VN.append(i10 / i0)
    print(str(i35 / i0))

for i in range(0, 1024):
    avg = 0
    n = 0
    for j in range(max(i-8, 0), min(1023, i+9)):
        m = math.e**(-((i-j)*0.3)**2)
        avg += intensity0V[j] * m
        n += m
    avg /= n
    
    v = (intensity10V[i] + intensity22V[i] + intensity35V[i]) / 3
    intensityAvgN.append(v / (0.1 * intensity0V[i] + 0.9 * avg))
    # intensityAvgN.append(avg)

# plot.figure(figsize=(8, 5.5), dpi=100)
# plot.plot(wavelengths1024, intensity0V, label='U = 0V', color="blue")
# plot.plot(wavelengths1024, intensity10V, label='U = 10V', color="violet")
# plot.plot(wavelengths1024, intensity22V, label='U = 22V', color="orangered")
# plot.plot(wavelengths1024, intensity35V, label='U = 35V', color="gold")
# plot.legend(loc="upper right")
# plot.xlabel("Wellenlänge [nm]")
# plot.ylabel("Intensität [a.u.]")
# plot.axis([320, 620, 0, 260])
# plot.minorticks_on()
# plot.savefig("Abbildungen\Jod_Übersicht", transparent = True)
# plot.show()

for i in range (360, 700) :
    if (intensity35VN[i-1] <= intensity35VN[i] and intensity35VN[i] >= intensity35VN[i+1]):
        print("35V:   %s   [%s  %s  %s]" % (i, intensity35VN[i-1], intensity35VN[i], intensity35VN[i+1]))
for i in range (400, 700) :
    if (intensity22VN[i-1] <= intensity22VN[i] and intensity22VN[i] >= intensity22VN[i+1]):
        print("22V:   %s   [%s  %s  %s]" % (i, intensity22VN[i-1], intensity22VN[i], intensity22VN[i+1]))
for i in range (400, 700) :
    if (intensity10VN[i-1] <= intensity10VN[i] and intensity10VN[i] >= intensity10VN[i+1]):
        print("10V:   %s   [%s  %s  %s]" % (i, intensity10VN[i-1], intensity10VN[i], intensity10VN[i+1]))

# plot.figure(figsize=(8, 5.5), dpi=100)
# plot.plot(channelNumbers, channels0V, label='U = 0V', color="blue")
# plot.plot(channelNumbers, channels10V, label='U = 10V', color="violet")
# plot.plot(channelNumbers, channels22V, label='U = 22V', color="orangered")
# plot.plot(channelNumbers, channels35V, label='U = 35V', color="gold")
# plot.legend(loc="upper right")
# plot.xlabel("Wellenlänge [nm]")
# plot.ylabel("Intensität [a.u.]")
# plot.axis([(430 - 316.049929)/(0.1500302240 * 2), (530 - 316.049929)/(0.1500302240 * 2), 0, 170])
# plot.minorticks_on()
# # plot.grid()
# plot.grid(b=True, which='major', color='r')
# plot.grid(b=True, which='minor', color='b')
# # plot.savefig("Abbildungen\Jod_Übersicht_CloseUp", transparent = True)
# plot.show()

for i in range(1024):
    intensity10V[i] *= 0.00 + 0.034 * (i/ 1024)
    # intensityAvgN[i] *= -0.07 + 0.17 * i/ 1024

plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(channels, intensity10VN, label='U = 10V', color="violet")
plot.plot(channels, intensity22VN, label='U = 22V', color="orangered")
plot.plot(channels, intensity35VN, label='U = 35V', color="gold")
plot.plot(channels, intensity10V, label='U = 35V', color="black")
plot.plot(channels, intensityAvgN, label='Avg', color="green")
plot.legend(loc="upper right")
plot.xlabel("Wellenlänge [nm]")
plot.ylabel("Intensität [a.u.]")
plot.axis([320, 730, 0.2, 2])
plot.minorticks_on()
# plot.grid()
plot.grid(visible=True, which='major', color='r')
plot.grid(visible=True, which='minor', color='b')
# plot.savefig("Abbildungen\Jod_Übersicht_Norm", transparent = True)
plot.show()