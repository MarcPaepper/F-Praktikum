import matplotlib.pyplot as plot
from InputOutput import readRawData

channelNumbers = range(1024)
channelsWasser = readRawData("Messdaten/TransmissionWasser.txt")
channelsLeer = readRawData("Messdaten/Transmission_leere_Küvette.txt")
channelsGlykol = readRawData("Messdaten/TransmissionGlykol.txt")
channelsEthanol = readRawData("Messdaten/Transmission_Ethanol.txt")

# convert channel number to wavelength [nm] for 1024 channels
channelNumbers = range(1024)
wavelengths1024 = []
for n in channelNumbers:
    wavelengths1024.append(316.049929 + 0.1500302240 * 2 * n)
#Tinenauswertung
# channelsSchwarz1Zu900 = readRawData("Messdaten/Transmission_schwarze_Tinten_1_zu_900.txt")
# channelsSchwarz2Zu900 = readRawData("Messdaten/Transmission_schwarze_Tinten_2_zu_900.txt")
# channelsSchwarzUnbekannt = readRawData("Messdaten/Transmission_schwarze_Tinten_unbekannt.txt")
# channelsBlau1Zu100 = readRawData("Messdaten/Transmission_blaue_Tinte_1_zu_100.txt")
# channelsBlau1Zu200 = readRawData("Messdaten/TransmissionBlaueTinte1zu200.txt")
# channelsBlau1Zu200 = readRawData("Messdaten/TransmissionBlaueTinte1zu200.txt")
# channelsSchwarz1Zu900Trans = []
# channelsSchwarz2Zu900Trans = []
# channelsSchwarzUnbekanntTrans = []
# channelsBlau1Zu100Trans = []
# channelsBlau1Zu200Trans = []
# for chWasser, chSchw1zu900 in zip(channelsWasser, channelsSchwarz1Zu900):
#     channelsSchwarz1Zu900Trans.append(chSchw1zu900 / chWasser)
# for chWasser, chSchw2zu900 in zip(channelsWasser, channelsSchwarz2Zu900):
#     channelsSchwarz2Zu900Trans.append(chSchw2zu900 / chWasser)
# for chWasser, chSchwUnbekannt in zip(channelsWasser, channelsSchwarzUnbekannt):
#     channelsSchwarzUnbekanntTrans.append(chSchwUnbekannt / chWasser)
#Pflanzenölauswertung
# channelsOlive = readRawData("Messdaten/TransmissionOlivenoelPur.txt")
# channelsSonne = readRawData("Messdaten/TransmissionSonnenblumenölPur.txt")
# channelsOlivenSonne = readRawData("Messdaten/TransmissionOliveSonne50zu50.txt")
# channelsEmpty = readRawData("Messdaten/Transmission_leere_Küvette.txt")
# channelsOliveTrans = []
# channelsSonneTrans = []
# channelsOlivenSonneTrans = []
# for chEmpty, chOlive in zip(channelsEmpty, channelsOlive):
#     channelsOliveTrans.append(chOlive / chEmpty)
# for chEmpty, chSonne in zip(channelsEmpty, channelsSonne):
#     channelsSonneTrans.append(chSonne / chEmpty)
# for chEmpty, chOlivenSonne in zip(channelsEmpty, channelsOlivenSonne):
#     channelsOlivenSonneTrans.append(chOlivenSonne / chEmpty)

# plot.plot(wavelengths1024, channelsOliveTrans, label='Olivenöl', color = "olive")
# plot.plot(wavelengths1024, channelsSonneTrans, label='Sonnenblumenöl', color = "gold")
# plot.plot(wavelengths1024, channelsOlivenSonneTrans, label='Mischung aus Oliven- und Sonnenblumenöl', color = "goldenrod")
# plot.legend(loc="upper right")
# plot.xlabel("Wellenlänge in nm")
# plot.ylabel("Transmission T")
# # plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()
# plot.plot(channelNumbers, channelsOliveTrans, label='Olivenöl', color = "olive")
# plot.plot(channelNumbers, channelsSonneTrans, label='Sonnenblumenöl', color = "gold")
# plot.plot(channelNumbers, channelsOlivenSonneTrans, label='Mischung aus Oliven- und Sonnenblumenöl', color = "goldenrod")
# plot.legend(loc="upper right")
# plot.xlabel("Kanäle")
# plot.ylabel("Transmission T")
# # plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()
# print("Olive = %s, Sonne = %s Mischung = %s" % (channelsOliveTrans[359], channelsSonneTrans[359], channelsOlivenSonneTrans[359]))
# print("Olivef = %s, Sonnef = %s Mischungf = %s" % (channelsOliveTrans[357], channelsSonneTrans[357], channelsOlivenSonneTrans[357]))
# print("Oliveg = %s, Sonneg = %s Mischungg = %s" % (channelsOliveTrans[361], channelsSonneTrans[361], channelsOlivenSonneTrans[361]))

# #Berechne Mittel Sonnenöl
# channelsSonneTransMittel = 0
# for n in channelsSonneTrans:
#     channelsSonneTransMittel += n
# print("Mitte Sonnenblumenöl = " + str(channelsSonneTransMittel/1024))
#Transmission Weißwein
# channelsWeiss1 = readRawData("Messdaten/Transmission_Weißwein_1.txt")
# channelsWeiss2 = readRawData("Messdaten/Transmission_Weißwein_2.txt")
# channelsRot2 = readRawData("Messdaten/Transmission_Rotwein_2.txt")
# channelsRot1 = readRawData("Messdaten/TransmissionRotwein1.txt")

# plot.plot(channelNumbers, channelsWeiss1, label='Weißwein 1', color = "goldenrod")
# plot.plot(channelNumbers, channelsWeiss2, label='Weißwein 2', color = "gold")
# plot.legend(loc="upper right")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# # # plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()
# plot.plot(channelNumbers, channelsRot1, label='Rotwein 1', color = "red")
# plot.plot(channelNumbers, channelsRot2, label='Rotwein 2', color = "darkred")

# plot.legend(loc="upper right")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# # # plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()
# plot.plot(channelNumbers, channelsWasser, label='Wasser', color = "aqua")
# plot.plot(channelNumbers, channelsGlykol, label='Glykol', color = "darkturquoise")
# plot.legend(loc="upper right")
# plot.xlabel("Kanäle")
# plot.ylabel("Intensität")
# # # plot.savefig("transparenteKalibrierung", transparent = True)
# plot.show()

channelsKleinUndGrün = readRawData("Messdaten/TransmissionKleineGrüneBlätter.txt")
channelsGrossUndGelb = readRawData("Messdaten/TransmissionGrossesGelbesBlatt.txt")
channelsGrossUndGrün = readRawData("Messdaten/TransmissionGrossesGrünesBlatt.txt")

channelsKleinUndGrünTrans = []
channelsGrossUndGelbTrans = []
channelsGrossUndGrünTrans = []

for chEthan, chSchmün in zip(channelsEthanol, channelsKleinUndGrün):
    channelsKleinUndGrünTrans.append(chSchmün / chEthan)
for chEthan, chGress in zip(channelsEthanol, channelsGrossUndGelb):
    channelsGrossUndGelbTrans.append(chGress / chEthan)
for chEthan, chGrüss in zip(channelsEthanol, channelsGrossUndGrün):
    channelsGrossUndGrünTrans.append(chGrüss / chEthan)

plot.plot(wavelengths1024, channelsKleinUndGrünTrans, label='Kleines grünes Blatt', color = "darkgreen")
plot.plot(wavelengths1024, channelsGrossUndGelbTrans, label='Großes gelbes Blatt', color = "goldenrod")
plot.plot(wavelengths1024, channelsGrossUndGrünTrans, label='Großes grünes Blatt', color = "forestgreen")
plot.legend(loc="upper left")
plot.xlabel("Wellenlänge in nm")
plot.ylabel("Transmission T")
# plot.savefig("transparenteKalibrierung", transparent = True)
plot.show()