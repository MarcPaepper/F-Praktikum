import matplotlib.pyplot as plot
import math
from InputOutput import readRawData

channelsReffel = readRawData("Messdaten/6_Referenzspiegel_neu.txt")
channelSpieZwei = readRawData("Messdaten/6_Spiegel2.txt")
channelSpieDrei = readRawData("Messdaten/6_Spiegel3.txt")
channelSpieVier = readRawData("Messdaten/6_Spiegel4.txt")
channelSpieFünf = readRawData("Messdaten/6_Spiegel5.txt")
channelSpieSieben = readRawData("Messdaten/6_Spiegel7.txt")
channelNumbers = range(1024)
wavelengths1024 = []
for n in channelNumbers:
    wavelengths1024.append(316.049929 + 0.1500302240 * 2 * n)
ReflektivitätRef = []
for n in wavelengths1024:
    if(200 < n < 400): 
       ReflektivitätRef.append(7.7+0.368 * n - 3.77 * n**2 * 10**(-4))
    if(400 <= n <= 2000):
        ReflektivitätRef.append(96 + 2.19 * 10**(-3) * n - 3.75 * 10**(-7) * n**2 - 93.8/(n-367) * math.cos(((n-367)* math.pi/180)/60.5))
LampenIntensität = []
for chaReffel, chReflek in zip(channelsReffel, ReflektivitätRef):
    LampenIntensität.append(chaReffel / chReflek)
ReflexionZwei = []
for chaLaI, chZwei in zip(LampenIntensität, channelSpieZwei):
    ReflexionZwei.append(chZwei / chaLaI)
ReflexionDrei = []
for chaLaI, chDrei in zip(LampenIntensität, channelSpieDrei):
    ReflexionDrei.append(chDrei / chaLaI)
ReflexionVier = []
for chaLaI, chZwei in zip(LampenIntensität, channelSpieVier):
    ReflexionVier.append(chZwei / chaLaI)
ReflexionFünf = []
for chaLaI, chZwei in zip(LampenIntensität, channelSpieFünf):
    ReflexionFünf.append(chZwei / chaLaI)
ReflexionSieben = []
for chaLaI, chZwei in zip(LampenIntensität, channelSpieSieben):
    ReflexionSieben.append(chZwei / chaLaI)
plot.plot(wavelengths1024, ReflektivitätRef, label='Reflektivität Referenzspigel', color = "darkgreen")
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge in nm")
plot.ylabel("Reflektivität R")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()
plot.figure(figsize=(8, 5.5), dpi=100)
plot.plot(wavelengths1024, ReflexionZwei, label='Reflexion des zweiten Spiegels', color = "wheat")
plot.plot(wavelengths1024, ReflexionDrei, label='Reflexion des dritten Spiegels', color = "chocolate")
plot.plot(wavelengths1024, ReflexionVier, label='Reflexion des vierten Spiegels', color = "silver")
plot.plot(wavelengths1024, ReflexionFünf, label='Reflexion des fünften Spiegels', color = "black")
plot.plot(wavelengths1024, ReflexionSieben, label='Reflexion des siebten Spiegels', color = "grey")
plot.axis([315, 624, 0.0, 140])
plot.axhline(100, color = "red")
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge in nm")
plot.ylabel("Reflektivität R")
plot.legend(fontsize="small")
plot.tight_layout()
#plot.legend(bbox_to_anchor=(0.65,1), loc="upper left")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()