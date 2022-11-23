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




from GitHubFiles import utm2geo, gezeiten
import inputOutput, driftkorrektur
import os
import matplotlib.pyplot as plt
import numpy
from scipy.interpolate import griddata
import scipy.interpolate as interp



# calculate slope for first and second day of measurement
def calculateSlope(fileName) -> float:
    # read in data
    datapoints = inputOutput.readRawData(fileName)

    # tidal correction
    for i in range(0, len(datapoints)):
        d = datapoints[i]
        t = d.time
        geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3]) # utm to gps
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
    
    return slopeDrift

def auswertung():
    # get slope drifts for first and second measurement day
    
    slopeDrift1 = calculateSlope("referenz.csv")
    slopeDrift2 = calculateSlope("referenz2.csv")
    
    # read in our data

    datapoints1 = inputOutput.readRawData("Rohdaten_3.csv")
    datapoints2  = inputOutput.readRawData("Rohdaten_4.csv")
    datapoints2 += inputOutput.readRawData("Rohdaten_5.csv")

    # tidal correction
    distances = []
    gravBeforeAnyCorr = []
    gravAfterTidalCorr = []
    gravAfterDriftCorr = []
    gravAfterHeightCorr = []
    
    # drift correction (day 1)
    for d in datapoints1:
        timediff = (d.time - datapoints1[0].time).total_seconds() / 60.0
        driftcorr = timediff * slopeDrift1
        d.gravitation += driftcorr
        gravAfterDriftCorr.append(d.gravitation)
    
    # drift correction (day 2)
    for d in datapoints2:
        timediff = (d.time - datapoints2[0].time).total_seconds() / 60.0
        driftcorr = timediff * slopeDrift2
        d.gravitation += driftcorr
        gravAfterDriftCorr.append(d.gravitation)
    
    # join both lists
    datapoints = datapoints1 + datapoints2

    # tidal correction
    for i in range(0, len(datapoints)):
        d = datapoints[i]
        distances.append(d.distance)
        gravBeforeAnyCorr.append(d.gravitation)
        t = d.time
        geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3])
        datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)
        gravAfterTidalCorr.append(d.gravitation)

    # height correction (Freiluftkorrektur)
    for d in datapoints:
        heightDiff = d.height - datapoints[0].height
        heightGradient = 0.308 # hardcoded in mGal / meter
        d.gravitation += heightGradient * heightDiff
        gravAfterHeightCorr.append(d.gravitation)


    # # read in external data
    # datapoints = []
    # path = "./ExterneProfile"
    # files = (file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)))
    # for file in files:
    #     datapoints += inputOutput.readCSV(os.path.join(path, file))
    # print(datapoints)
    
    utmE = utmN = grav = []
    
    # convert to arrays
    for d in datapoints:
        utmE.append(d.utm[0])
        utmN.append(d.utm[1])
        grav.append(d.gravitation)
    
    utmE = numpy.array(utmE)
    utmN = numpy.array(utmN)
    grav = numpy.array(grav)
    
    # target grid to interpolate to
    xi = numpy.arange(0, 4.05, 0.05)
    yi = numpy.arange(0, 4.05, 0.05)
    xi, yi = numpy.meshgrid(xi, yi)

    # interpolate
    zi = griddata((x, y), z, (xi, yi), method='linear')

    yy, xx = numpy.meshgrid(y,x)
    sparse_points = numpy.stack([x.ravel(), y.ravel()], -1)
    zz = interp.RBFInterpolator(sparse_points, z.ravel(), smoothing=0, kernel='cubic')  # explicit default smoothing=0 for interpolation

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.contourf(xi,yi,zi)
    plt.plot(x, y, 'k.')
    plt.xlabel('xi', fontsize=16)
    plt.ylabel('yi', fontsize=16)
    # plt.savefig('interpolated.png',dpi=100)
    plt.show()
    plt.close(fig)

    # scattered_points = numpy.stack([utmE.ravel(), utmN.ravel()],-1)
    # x_dense, y_dense = numpy.meshgrid(numpy.linspace(min(utmE), max(utmE), 20),numpy.linspace(min(utmN), max(utmN), 21))
    # dense_points = numpy.stack([x_dense.ravel(), y_dense.ravel()], -1)
    # interpolation = interp.RBFInterpolator(scattered_points, grav.ravel(), smoothing = 0, kernel='linear',epsilon=1, degree=0)
    # z_dense = interpolation(dense_points).reshape(x_dense.shape)
    # fig = plt.figure(figsize=(8,6),dpi=100)
    # ax = plt.axes()

    # ax.contourf(x_dense, y_dense, z_dense)
    # ax.set_title('Surface plot')
    # plt.show()

auswertung()