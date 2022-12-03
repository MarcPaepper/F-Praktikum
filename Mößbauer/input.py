import os
import csv
import re


def readRawData(fileName) -> list[list]:
	directory = os.path.dirname(os.path.realpath('__file__'))
	absFileName = directory + "/" + fileName
	reader = csv.reader(open(absFileName, 'r'), delimiter='\t', skipinitialspace = True)
	channels = []
	counts = []
	wordReg = re.compile('[a-zA-Z]')
	for row in reader:
		if (row[0].startswith(("!","#")) or wordReg.match(row[0]) != None):
			continue
		else:
			# print(f"row ${row}")
			channel, countNumber, folded = row
			channels.append(int(channel))
			counts.append(int(countNumber))
	return (channels, counts)