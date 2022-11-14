import os
import csv


def readRawData(fileName) -> list:
	directory = os.path.dirname(os.path.realpath('__file__'))
	absFileName = directory + "/" + fileName
	reader = csv.reader(open(absFileName, 'r'), delimiter='\t')
	channels = []
	for s in reader:
		row = s[0]
		if (row == "I [a.u.]"):
			continue
		else:
			channels.append(float(row))
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