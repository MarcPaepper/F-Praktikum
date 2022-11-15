import matplotlib.pyplot as plot
import math
from InputOutput import readRawData

channelNumbers = range(1024)
wavelengths1024 = []
for n in channelNumbers:
    wavelengths1024.append(316.049929 + 0.1500302240 * 2 * n)
ReflektivitätRef = []
for n in wavelengths1024:
    if(200 < n < 400): 
       ReflektivitätRef.append(7.7+0.368 * n - 3.77 * n**2 * 10**(-4))
    if(400 <= n <= 2000):
        ReflektivitätRef.append(96 + 2.19 * 10**(-3) * n - 3.75 * 10**(-7) * n**2 - 938/(n-367) * math.cos((n-367)/60.5))

plot.plot(wavelengths1024, ReflektivitätRef, label='Reflektivität Referenzspigel', color = "darkgreen")
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge in nm")
plot.ylabel("Reflektivität R")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()