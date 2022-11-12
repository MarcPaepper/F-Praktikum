import InputOutput
import matplotlib.pyplot as plot
import math
from turtle import pos
from prakMath import linearRegression

channels = InputOutput.readRawData("Messdaten\kalibrierung.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe geringere Intensität')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.show()


channels = InputOutput.readRawData("Messdaten\kalibrierung_2.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe maximal')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.show()

channels = InputOutput.readRawData("Messdaten\kalibrierungmittel.txt")
channelNumber = range(1024)

plot.plot(channelNumber, channels, label='Hg-Lampe mittlgroßer Spalt')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()

channels = InputOutput.readRawData("Messdaten\kalibrierungLinks.txt")
channelNumber = range(2048)

plot.plot(channelNumber, channels, label='Hg-Lampe Links')
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Intensität")
plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()


[channels, wavelengths] = InputOutput.readRawKalData("Messdaten\kalibrierungsFunktion.txt")

linearRegression(channels,wavelengths)