import matplotlib.pyplot as plot
from datetime import datetime
import math
import csv

from GitHubFiles import count2mgal_cologne, geo2utm, gezeiten

class datapoint:
	def __init__(self, gravitation, time, height, utm=None, distance=0):
		self.time = time
		self.utm = utm # the position in utm coordinates
		self.height = float(height) # height difference in m to the reference point in m relative to Normal Null
		self.gravitation = float(gravitation) # gravitational acceleration in mGal (or counts at first for raw data)
		self.distance = float(distance) # the distance in m for measuring only in one direction
	
	def __repr__(self):
		return("Datapoint: [gravitation: %s, time: %s, coordinates: %s, height: %s, distance: %s]"
			% (self.gravitation, self.time, self.utm, self.height, self.distance))

def readRawData(fileName) -> list[datapoint]:
	reader = csv.reader(open(fileName, 'r'), delimiter='\t')
	datapoints = []
	# the gps coordinates for the Physikzentrum (used for the drift reference measurements where no gps coordinates were measured)
	utm = geo2utm.geo2utm(52.28014, 10.5478)
	counter = 0
	totalDist = 0
	for row in reader:
		counter += 1
		if (len(row) == 3):
			timestring, counts, height = row
			# convert time string to datetime object
			timestamp = datetime.strptime(timestring.replace('\'', ''), '%Y-%m-%d %H:%M:%S')
			# convert counts to mGal
			gravitation_uncorrected = count2mgal_cologne.count2mgal([float(counts)])[0]
			# add new datapoint to list
			datapoints.append(datapoint(gravitation_uncorrected, timestamp, height, utm=utm))
		
		if (len(row) == 4):
			timestring, counts, height, dist = row
			# convert time string to datetime object
			timestamp = datetime.strptime(timestring.replace('\'', ''), '%Y-%m-%d %H:%M:%S')
			# convert counts to mGal
			gravitation_uncorrected = count2mgal_cologne.count2mgal([float(counts)])[0]
			# sum up distances
			totalDist += float(dist)
			# add new datapoint to list
			datapoints.append(datapoint(gravitation_uncorrected, timestamp, height, utm=utm, distance=totalDist))
		
		if (len(row) == 5):
			timestring, counts, height, gpsN, gpsE = row
			# convert time string to datetime object
			timestamp = datetime.strptime(timestring.replace('\'', ''), '%Y-%m-%d %H:%M:%S')
			# convert counts to mGal
			gravitation_uncorrected = count2mgal_cologne.count2mgal([float(counts)])[0]
			# convert to utm object
			utm = geo2utm.geo2utm(float(gpsN), float(gpsE))
			# add new datapoint to list
			datapoints.append(datapoint(gravitation_uncorrected, timestamp, height, utm=utm))
		
		if (len(row) == 6):
			timestring, counts, height, dist, gpsN, gpsE = row
			# convert time string to datetime object
			timestamp = datetime.strptime(timestring.replace('\'', ''), '%Y-%m-%d %H:%M:%S')
			# convert counts to mGal
			gravitation_uncorrected = count2mgal_cologne.count2mgal([float(counts)])[0]
			# convert to utm object
			utm = geo2utm.geo2utm(float(gpsN), float(gpsE))
			# sum up distances
			totalDist += float(dist)
			# add new datapoint to list
			datapoints.append(datapoint(gravitation_uncorrected, timestamp, height, distance=totalDist, utm=utm))
	return datapoints

#def readGitLabData()