import matplotlib.pyplot as plot
from datetime import datetime
import math
import csv


def readRawData(fileName) -> list:
	reader = csv.reader(open(fileName, 'r'), delimiter='\t')
	channels = []
	for s in reader:
		channels.append(float(s[0]))
	return channels

def readRawKalData(fileName) -> list:
	reader = csv.reader(open(fileName, 'r'), delimiter='\t')
	channels = []
	wavelengths = []
	for s in reader:
		channel = s[0]
		wavelength = s[1]
		channels.append(float(s[0]))
		wavelengths.append(float(s[1]))
	return [channels, wavelengths]