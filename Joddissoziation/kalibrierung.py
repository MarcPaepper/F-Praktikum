import InputOutput
import matplotlib.pyplot as plot
import math
from turtle import pos
from prakMath import linearRegression

channels = InputOutput.readRawData("Messdaten/kalibrierung.txt")
channelNumber = range(1024)

# plot.plot(channelNumber, channels, label='Hg-Lampe geringere Intensität')
# plot.legend(loc="upper left")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# plot.show()


# channels = InputOutput.readRawData("Messdaten\kalibrierung_2.txt")
# channelNumber = range(1024)

# plot.plot(channelNumber, channels, label='Hg-Lampe maximal')
# plot.legend(loc="upper left")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# plot.show()

# channels = InputOutput.readRawData("Messdaten\kalibrierungmittel.txt")
# channelNumber = range(1024)

# plot.plot(channelNumber, channels, label='Hg-Lampe mittlgroßer Spalt')
# plot.legend(loc="upper left")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()

# channels = InputOutput.readRawData("Messdaten\kalibrierungLinks.txt")
# channelNumber = range(2048)

# plot.plot(channelNumber, channels, label='Hg-Lampe Links')
# plot.legend(loc="upper left")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()


[channels, wavelengths] = InputOutput.readRawKalData("Messdaten/kalibrierungsFunktion.txt")

(slope, intcp, slopeErr, intcpErr) = linearRegression(channels,wavelengths)

xValues = range(0, 2049)
yValues = [x * slope + intcp for x in xValues]
plot.plot(xValues, yValues, label='Kalibrierfunktion', color = "darkblue")
plot.scatter(channels, wavelengths, label = "Kalibrierpunkte", color = "blue")
plot.legend(loc="upper left")
plot.xlabel("Kanäle")
plot.ylabel("Wellenlänge")
plot.savefig("transparenteKalibrierungDiagramm", transparent = True)
plot.show()