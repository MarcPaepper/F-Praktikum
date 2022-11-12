import matplotlib.pyplot as plot

from InputOutput import readRawData

channelNumbers = range(1024)
channelsWasser = readRawData("Messdaten\TransmissionWasser.txt")
channelsLeer = readRawData("Messdaten\Transmission_leere_Küvette.txt")

channelsSchwarz1Zu900 = readRawData("Messdaten\Transmission_schwarze_Tinten_1_zu_900.txt")
channelsSchwarz2Zu900 = readRawData("Messdaten\Transmission_schwarze_Tinten_2_zu_900.txt")
channelsSchwarz1Zu900Trans = []
for chWasser, chSchw1zu900 in zip(channelsWasser, channelsSchwarz1Zu900):
    channelsSchwarz1Zu900Trans.append(chSchw1zu900 / chWasser)
plot.plot(channelNumbers, channelsSchwarz1Zu900Trans, label='U = 0V')
plot.plot(channelNumbers, channels10V, label='U = 10V')
plot.plot(channelNumbers, channels22V, label='U = 22V')
plot.plot(channelNumbers, channels35V, label='U = 35V')
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge [nm]")
plot.ylabel("Intensität [a.u.]")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()