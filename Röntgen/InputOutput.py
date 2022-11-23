import os
import csv


def readRawData(fileName) -> list:
	directory = os.path.dirname(os.path.realpath('__file__'))
	absFileName = directory + "/" + fileName
	reader = csv.reader(open(absFileName, 'r'), delimiter=' ', skipinitialspace = True)
	datapoints = []
	for row in reader:
		if (row[0].startswith(("!","#"))):
			continue
		else:
			winkel, intensität = row
			datapoints.append([float(winkel), int(intensität)])
	return datapoints