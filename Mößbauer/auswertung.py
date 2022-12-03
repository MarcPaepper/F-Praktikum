from matplotlib import pyplot as plot
from input import readRawData
import math

savePlots = False
showPlots = True

def auswertung(fileName, shift, saveName):
	# read data
	
	channels, counts = readRawData("Messwerte/" + fileName)
	lineCount = len(channels)
	middle = math.ceil(lineCount / 2)
	
	# fold half of the channels over
	
	channelsRev = channels.copy()
	countsRev = counts.copy()
	channelsRev.reverse()
	countsRev.reverse()
	
	# cut out second half of values and those at the beginning / end which have no folded counterpart
	
	channels = channels[max(0, shift) : middle - max(0, -shift)]
	counts   = counts  [max(0, shift) : middle - max(0, -shift)]
	
	channelsRev = channelsRev[max(0, -shift) : middle - max(0, shift)]
	countsRev   = countsRev  [max(0, -shift) : middle - max(0, shift)]
	
	for i in range(0, len(channelsRev)):
		channelsRev[i] = i + max(0, shift)
	
	# add counts and folded counts together
	
	for i in range(0, len(channels)):
		counts[i] += countsRev[i]
	
	# calculate velocity
	
	velocities = []
	
	minCh = min(channels)
	maxCh = max(channels)
	for i in range(minCh, maxCh+1):
		velocities.append(math.cos((i / maxCh) * math.pi))
	
	# plotting
	
	# reasonable boundaries
	minX = 0
	maxX = max(channels)
	minY = 0
	maxY = max(counts)
	maxY = (1.2 * maxY) + (-maxY * 1.2) % (10 ** math.floor(math.log10(maxY * 0.4)))
	
	for i in range(len(velocities)):
		velocities[i] *= maxY / 2
		velocities[i] += maxY / 2
	
	plot.plot(channels, counts, label="Messwerte", color="violet")
	plot.plot(channels, velocities, label="vel", color="red")
	plot.axis([minX, maxX, minY, maxY])
	
	plot.legend(loc="upper left")
	plot.xlabel("Geschwindigkeit [mm/s]")
	plot.ylabel(f"Anzahl Ereignisse")
	if (savePlots):
		plot.savefig("Abbildungen/" + saveName + ".png", dpi=300, transparent = True)
	if(showPlots):
		plot.show()

auswertung("Eisen_folie_NEU.txt", 4, "Eisen")
auswertung("Stahl_folie.txt", 5, "Stahl")