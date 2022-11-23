# import numpy as numpy
# import scipy.interpolate as interp
# import matplotlib.pyplot as plot

# x = numpy.array([0, 4, 3, 0])
# y = numpy.array([0, 0, 3, 4])
# z = numpy.array([1, 2, 3, 4])

# yy, xx = numpy.meshgrid(y,x)
# sparse_points = numpy.stack([x.ravel(), y.ravel()], -1)
# zz = interp.RBFInterpolator(sparse_points, z.ravel(), smoothing=0, kernel='cubic')  # explicit default smoothing=0 for interpolation
# plot.pcolormesh(x, y, z)
# plot.show()

# sparse = np.stack([x.ravel(), y.ravel()], -1)  # shape (N, 2) in 2d

# zfun_smooth_rbf = interp.RBFInterpolator(sparse, z.ravel(),
#                                          smoothing=0, kernel='cubic')  # explicit default smoothing=0 for interpolation

# plot.pcolormesh(x, y, z)




# import matplotlib.pyplot as plt
# import numpy
# from scipy.interpolate import griddata
# import scipy.interpolate as interp

# x = numpy.array([0, 4, 3, 0])
# y = numpy.array([0, 0, 3, 4])
# z = numpy.array([1, 2, 3, 4])

# # target grid to interpolate to
# xi = numpy.arange(0, 4.05, 0.05)
# yi = numpy.arange(0, 4.05, 0.05)
# xi, yi = numpy.meshgrid(xi, yi)

# # interpolate
# zi = griddata((x, y), z, (xi, yi), method='linear')

# yy, xx = numpy.meshgrid(y,x)
# sparse_points = numpy.stack([x.ravel(), y.ravel()], -1)
# zz = interp.RBFInterpolator(sparse_points, z.ravel(), smoothing=0, kernel='cubic')  # explicit default smoothing=0 for interpolation

# # plot
# fig = plt.figure()
# ax = fig.add_subplot(111)
# plt.contourf(xi,yi,zi)
# plt.plot(x, y, 'k.')
# plt.xlabel('xi', fontsize=16)
# plt.ylabel('yi', fontsize=16)
# # plt.savefig('interpolated.png',dpi=100)
# plt.show()
# plt.close(fig)




from GitHubFiles import gezeiten
import inputOutput, driftkorrektur
import os
import math
import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import griddata
import scipy.interpolate as interp
from GitHubFiles.utm2geo import utm2geo



# calculate slope and intercept (drift) for first and second day of measurement
def calculateDrift(fileName):
	# read in data
	datapoints = inputOutput.readRawData(fileName)

	# tidal correction
	for i in range(0, len(datapoints)):
		d = datapoints[i]
		t = d.time
		geo = utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3]) # utm to gps
		datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)

	timediff = []
	gravBefore = []
	for d in datapoints:
		timediff.append((d.time - datapoints[0].time).total_seconds() / 60.0)
		gravBefore.append(d.gravitation)

	# # display reference data as scatter plot
	# plot.scatter(timediff, grav, label="nachher")
	# plot.show()

	# calculate slope of the drift
	(slopeDrift, interceptDrift) = driftkorrektur.übergabe(x=timediff, y=gravBefore)

	# calculate values to display linear regression line
	xValuesDriftReg = range(0, 500)
	yValuesDriftReg = []
	for xValue in xValuesDriftReg:
		yValuesDriftReg.append(slopeDrift * xValue + interceptDrift)
	
	utm = datapoints[0].utm
	
	return (datapoints[0].time, slopeDrift, interceptDrift)

def auswertung():
	# get slope drifts for first and second measurement day
	
	(startTime1, slopeDrift1, incpDrift1) = calculateDrift("referenz.csv")
	(startTime2, slopeDrift2, incpDrift2) = calculateDrift("referenz2.csv")
	
	# read in our data

	datapoints1  = inputOutput.readRawData("Rohdaten_3.csv")
	datapoints2  = inputOutput.readRawData("Rohdaten_4.csv")

	# tidal correction
	distances = []
	gravBeforeAnyCorr = []
	gravAfterTidalCorr = []
	gravAfterDriftCorr = []
	gravAfterHeightCorr = []
	
	# drift correction (day 1)
	for d in datapoints1:
		timediff = (d.time - startTime1).total_seconds() / 60.0
		driftcorr = incpDrift1 + timediff * slopeDrift1
		d.gravitation -= driftcorr
		gravAfterDriftCorr.append(d.gravitation)
	
	# drift correction (day 2)
	for d in datapoints2:
		timediff = (d.time - startTime2).total_seconds() / 60.0
		driftcorr = incpDrift2 + timediff * slopeDrift2
		d.gravitation -= driftcorr
		gravAfterDriftCorr.append(d.gravitation)
	
	# join both lists
	datapoints = datapoints1 + datapoints2

	# tidal correction
	for i in range(0, len(datapoints)):
		d = datapoints[i]
		distances.append(d.distance)
		gravBeforeAnyCorr.append(d.gravitation)
		t = d.time
		geo = utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3])
		datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)
		gravAfterTidalCorr.append(d.gravitation)

	# height correction (Freiluftkorrektur)
	for d in datapoints:
		heightDiff = d.height - datapoints[0].height
		heightGradient = 0.308 # hardcoded in mGal / meter
		d.gravitation += heightGradient * heightDiff
		gravAfterHeightCorr.append(d.gravitation)
	
	# Latitude correction (Breitenkorrektur)
	utm = datapoints[0].utm
	(startLat, startLong) = utm2geo(utm[0], utm[1], utm[2], utm[3])
	for d in datapoints:
		(lat, long) = utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3]) # utm to gps
		latDiffRad = (lat - startLat) * 2 * math.pi / 360
		radiusEarth = 6371000
		southNorthDistance = latDiffRad * radiusEarth
		d.gravitation += -0.00081 * math.sin(2 * startLat * 2 * math.pi / 360) * southNorthDistance
	
	# read in external data
	path = "./ExterneProfile"
	files = (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
	for file in files:
		d = inputOutput.readCSV(os.path.join(path, file))
		datapoints += d
	for d in datapoints:
		print(d)
	
	utmE = []
	utmN = []
	grav = []
	
	# convert to arrays
	for d in datapoints:
		utmE.append(d.utm[0])
		utmN.append(d.utm[1])
		grav.append(d.gravitation)
	
	utmE = numpy.array(utmE)
	utmN = numpy.array(utmN)
	grav = numpy.array(grav)
	
	lowestE = lowestN = 1000000000
	highestE = highestN = -1000000000
	for (e, n) in zip(utmE, utmN):
		if (e < lowestE):
			lowestE = e
		if (n < lowestN):
			lowestN = n
		if (e > highestE):
			highestE = e
		if (n > highestN):
			highestN = n
	diffE = (highestE - lowestE) * 1
	diffN = (highestN - lowestN)

	# target grid to interpolate to
	xi = numpy.arange(lowestE - diffE * 0.1, highestE + diffE * 0.1, diffE / 200)
	yi = numpy.arange(lowestN - diffN * 0.1, highestN + diffN * 0.1, diffN / 200)
	xi, yi = numpy.meshgrid(xi, yi)
	
	# interpolate
	zi = griddata((utmE, utmN), grav, (xi, yi), method='linear')

	# plot
	fig = plt.figure()
	# ax = fig.add_subplot(111)
	plt.contourf(xi,yi,zi)
	plt.axis("equal")
	plt.colorbar(label="$\delta g$ [mGal]")
	plt.plot(utmE, utmN, 'k.')
	plt.xlabel('UTM-E', fontsize=16)
	plt.locator_params(nbins=6)
	plt.ylabel('UTM-N', fontsize=16)
	plt.savefig('Abbildungen/Schwere_karte.png',dpi=600)
	plt.show()
	plt.close(fig)

auswertung()