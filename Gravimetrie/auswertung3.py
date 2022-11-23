import math
import seaborn as sns
import inputOutput
from GitHubFiles import count2mgal_cologne, geo2utm, utm2geo, gezeiten
import matplotlib.pyplot as plot
import matplotlib
import driftkorrektur
import numpy as np
import statsmodels.api as sm
from gravMath import linearRegression, gravitationAnomalyOfPolygon

# --- Versuchsteil 3 ---

def auswertung(slopeDrift, slopeIntercept):
	# color map for heat map
	# norm = matplotlib.colors.Normalize(0,20)
	# colors = [[0.0, (255/255, 252/255, 205/255)],
	# 		[0.0015683, (255/255, 237/255, 165/255)],
	# 		[0.00583, (255/255, 180/255, 119/255)],
	# 		[0.0174, (255/255, 56/255, 92/255)],
	# 		[0.0489, (182/255, 54/255, 121/255)],
	# 		[0.135, (127/255, 36/255, 129/255)],
	# 		[0.367, (42/255, 17/255, 92/255)],
	# 		[1.0, (0, 0, 0)]]
	# colors = [[0.0, (255/255, 252/255, 205/255)],
	# 		[0.048, (255/255, 180/255, 119/255)],
	# 		[0.12, (255/255, 56/255, 92/255)],
	# 		[0.23, (182/255, 54/255, 121/255)],
	# 		[0.63, (127/255, 36/255, 129/255)],
	# 		[0.8, (42/255, 17/255, 92/255)],
	# 		[1.0, (0, 0, 0)]]

	# cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)
	cmap = sns.color_palette("rocket_r", as_cmap=True)
	
	# read in data
	datapoints = inputOutput.readRawData("Rohdaten_3.csv")
	modelDist = range(-100, 1201, 5)
	# tidal correction
	distances = []
	gravBeforeAnyCorr = []
	gravAfterTidalCorr = []
	gravAfterDriftCorr = []
	gravAfterHeightCorr = []

	# tidal correction
	for i in range(0, len(datapoints)):
		d = datapoints[i]
		distances.append(d.distance)
		gravBeforeAnyCorr.append(d.gravitation)
		t = d.time
		geo = utm2geo.utm2geo(d.utm[0], d.utm[1], d.utm[2], d.utm[3])
		datapoints[i].gravitation += gezeiten.gezeiten(t.year, t.month, t.day, t.hour, t.minute, 2, geo[0], geo[1], d.height)
		gravAfterTidalCorr.append(d.gravitation)

	# drift correction
	for d in datapoints:
		timediff = (d.time - datapoints[0].time).total_seconds() / 60.0
		driftcorr = slopeIntercept + timediff * slopeDrift
		d.gravitation -= driftcorr
		gravAfterDriftCorr.append(d.gravitation)

	# height correction (Freiluftkorrektur)
	for d in datapoints:
		heightDiff = d.height - datapoints[0].height
		heightGradient = 0.308 # hardcoded in mGal / meter
		d.gravitation += heightGradient * heightDiff
		gravAfterHeightCorr.append(d.gravitation)

	# # display all corrections

	# fig = plot.figure(figsize=(8, 5), dpi=100)
	# print("dist %s gravBefore %s" % (gravBeforeAnyCorr, gravAfterTidalCorr))
	# plot.errorbar(distances, gravBeforeAnyCorr, xerr=0.05, yerr=0.021, ls="none", label="Vor Korrekturen")
	# plot.errorbar(distances, gravAfterTidalCorr, xerr=0.05, yerr=0.021, ls="none", label="Nach Gezeitenkorrektur")
	# plot.errorbar(distances, gravAfterDriftCorr, xerr=0.05, yerr=0.021, ls="none", label="Nach Gezeiten- & Driftkorrektur")
	# plot.errorbar(distances, gravAfterHeightCorr, xerr=0.05, yerr=0.021, ls="none", label="Nach Gezeiten-, Drift- & Höhenkorrektur")
	# plot.axis([-100, 1200, 4923, 4927])
	# plot.xlabel("Akkumulierte Distanz zwischen Messpunkten [m]")
	# plot.ylabel("$\delta g$ [mGal]")
	# plot.minorticks_on()
	# plot.legend(loc="upper center")
	# plot.show()

	# inversion

	# find measurment value with lowest gravitation to determine the middle of the salt stock
	distances = []
	measuredGrav = []
	middle = 0 # the distance at which half of the salt stock lies
	lowestGrav = 10E9
	for d in datapoints:
		dist = d.distance
		distances.append(dist)
		measuredGrav.append(d.gravitation)
		if (d.gravitation < lowestGrav):
			lowestGrav = d.gravitation
			middle = dist
	avgMeasuredGrav = np.mean(measuredGrav)
	
	
	
	# # --- fit depth T (100:10:300) and salt density rho (2000:50:3000) with fixed salt stock width ---
	
	
	# width = 963 # fixed width of the salt stock in m (measured in the Versuchsaufgaben.pdf figure 1)

	# # startDepth = 100 # 
	# # stepSizeDepth = 5 # divisible 50
	# # maxDepth = 300 # 
	# startDepth = 0 # 
	# stepSizeDepth = 25 # divisible 50
	# maxDepth = 1000 # 

	# startDensity = 2000 # 
	# stepSizeDensity = 20 # divisible 200
	# maxDensity = 3000 # 

	# rows = math.floor((maxDepth - startDepth)/stepSizeDepth)+1
	# cols = math.floor((maxDensity - startDensity)/stepSizeDensity)+1
	# fitnesses = np.zeros((rows, cols)) # the fitness of each combination (Chi²)

	# k = -1
	# j = -1
	# lowest_chi_squared = [1000000, 0, 0]
	# for depth in range(startDepth, maxDepth+1, stepSizeDepth):
	# 	k += 1
	# 	# row = []
	# 	j = -1
		
	# 	polygon = []
	# 	polygon.append([middle + width/2, 2000])
	# 	polygon.append([middle + width/2, depth])
	# 	polygon.append([middle - width/2, depth])
	# 	polygon.append([middle - width/2, 2000])
		
	# 	# calculate delta g once for the density 1 kg / m^3 and multiply that value for the different densities
		
	# 	gravBefore = []
		
	# 	for d in distances:
	# 		gravBefore.append(gravitationAnomalyOfPolygon(polygon, (d, 0), 1) * 2) # *2 because the stock stretches to infinity in both y-directions
		
	# 	for density in range(startDensity, maxDensity+1, stepSizeDensity):
	# 		j += 1
	# 		# multiply all gravitation values by density
	# 		grav = []
	# 		for g in gravBefore:
	# 			grav.append(g * (2670 - density))
			
	# 		# match the average value
	# 		diff = avgMeasuredGrav - np.mean(grav)
	# 		for l in range(len(datapoints)):
	# 			grav[l] += diff
			
	# 		differences = []
	# 		for n in range(len(grav)):
	# 			differences.append((measuredGrav[n] - grav[n]))
	# 		# print("measured " + str(measuredGrav))
	# 		# print("model " + str(grav))
	# 		# print("differences " + str(differences))
	# 		# calculate fitness values
			
	# 		chi_squared = 0
	# 		for di in differences:
	# 			chi_squared += di ** 2
			
	# 		if (chi_squared < lowest_chi_squared[0]):
	# 			lowest_chi_squared = [chi_squared, depth, density, diff, chi_squared]
			
	# 		# if (k==0):
	# 			# chi_squared-= 1E8
			
	# 		fitnesses[k, j] = math.log10(chi_squared)

	# # display fitness as heat map

	# # cmap = sns.cm.mako_r

	# xlabels =[]
	# for i in range(round((maxDensity-startDensity)/200)):
	# 	xlabels.append((startDensity + 200*i)/1000)
	# 	for j in range(round(200/stepSizeDensity)-1):
	# 		xlabels.append("")
	# xlabels.append(maxDensity/1000)

	# ylabels = []
	# for i in range(round((maxDepth-startDepth)/50)):
	# 	ylabels.append(startDepth + 50*i)
	# 	for j in range(round(50/stepSizeDepth)-1):
	# 		ylabels.append("")
	# ylabels.append(maxDepth)

	# plot.figure(figsize=(7.5, 6), dpi=100)
	# heatmap = sns.heatmap(fitnesses, xticklabels=xlabels, yticklabels=ylabels, cmap=cmap, cbar_kws={"label":"$\log_{10}(\chi^2)$"}) #, norm=matplotlib.colors.LogNorm()
	# heatmap.set(xlabel="Dichte [t/m³]", ylabel="Tiefe [m]")
	# plot.savefig("Abbildungen\\3_Tiefe_Dichte_unrealistisch_Grenzen.png", transparent = True, dpi=300)
	# plot.show()

	# # store predicted data to plot it later
	
	# print("best fit: %s (depth %s, density %s, diff %s, chi %s)" % tuple(lowest_chi_squared))

	# polygon = []
	# polygon.append([middle + width/2, 2000])
	# polygon.append([middle + width/2, lowest_chi_squared[1]])
	# polygon.append([middle - width/2, lowest_chi_squared[1]])
	# polygon.append([middle - width/2, 2000])

	# modelDensityDepth = []
	# for dist in modelDist:
	# 	modelDensityDepth.append(gravitationAnomalyOfPolygon(polygon, (dist, 0), (2670 - lowest_chi_squared[2])) * 2 + lowest_chi_squared[3]) # *2 because the stock stretches to infinity in both y-directions
	
	
	# --- fit width (200:50:1000) and salt density rho (2000:50:3000) with fixed depth (200m) ---
	
	
	depth = 200

	startWidth = 0
	stepSizeWidth = 10 # divisible 200
	maxWidth = 600

	startDensity = 0 # 
	stepSizeDensity = 50 # divisible 200
	maxDensity = 3000 # 

	rows = math.floor((maxWidth - startWidth)/stepSizeWidth)+1
	cols = math.floor((maxDensity - startDensity)/stepSizeDensity)+1
	fitnesses = np.zeros((rows, cols)) # the fitness of each combination (Chi²)

	k = -1
	j = -1
	lowest_chi_squared = [1000000, 0, 0]
	for width in range(startWidth, maxWidth+1, stepSizeWidth):
		k += 1
		j = -1
		polygon = []
		polygon.append([middle + width/2+1, 2000 ])
		polygon.append([middle + width/2+1, depth+1])
		polygon.append([middle - width/2-1, depth+1])
		polygon.append([middle - width/2-1, 2000 ])
		
		# calculate delta g once for the density 1 kg / m^3 and multiply that value for the different densities
		
		gravBefore = []
		
		for d in distances:
			gravBefore.append(gravitationAnomalyOfPolygon(polygon, (d, 0), 1) * 2) # *2 because the stock stretches to infinity in both y-directions
		
		for density in range(startDensity, maxDensity+1, stepSizeDensity):
			j += 1
			# multiply alll gravitation values by density
			grav = []
			for g in gravBefore:
				grav.append(g * (2670 - density))
			
			# match the average value
			diff = avgMeasuredGrav - np.mean(grav)
			for l in range(len(datapoints)):
				grav[l] += diff
			
			differences = []
			for n in range(len(grav)):
				differences.append((measuredGrav[n] - grav[n]))
			
			# calculate fitness values
			
			chi_squared = 0
			for di in differences:
				chi_squared += di ** 2
			
			if (chi_squared < lowest_chi_squared[0]):
				lowest_chi_squared = [chi_squared, width, density, diff, chi_squared]
			
			# if (k==0):
				# chi_squared-= 1E8
			
			fitnesses[k, j] = math.log10(chi_squared)

	# # display fitness as heat map
	
	print("best fit: %s (width %s, density %s, diff %s, chi %s)" % tuple(lowest_chi_squared))

	# cmap = sns.cm.rocket_r

	xlabels =[]
	for i in range(round((maxDensity-startDensity)/200)):
		xlabels.append((startDensity + 200*i)/1000)
		for j in range(round(200/stepSizeDensity)-1):
			xlabels.append("")
	xlabels.append(maxDensity/1000)

	ylabels = []
	for i in range(round((maxWidth-startWidth)/100)):
		ylabels.append(startWidth + 100*i)
		for j in range(round(100/stepSizeWidth)-1):
			ylabels.append("")
	ylabels.append(maxWidth)

	plot.figure(figsize=(7.5, 6), dpi=100)
	heatmap = sns.heatmap(fitnesses, xticklabels=xlabels, yticklabels=ylabels, cmap=cmap, cbar_kws={"label":"$\log_{10}(\chi^2)$"})
	heatmap.set(xlabel="Dichte [t/m³]", ylabel="Breite [m]")
	plot.savefig("Abbildungen\\3_Breite_Dichte_unrealistisch_Grenzen.png", transparent = True, dpi=300)
	plot.show()
	# store predicted data to plot it later

	polygon = []
	polygon.append([middle + lowest_chi_squared[1]/2, 2000])
	polygon.append([middle + lowest_chi_squared[1]/2, depth])
	polygon.append([middle - lowest_chi_squared[1]/2, depth])
	polygon.append([middle - lowest_chi_squared[1]/2, 2000])
	
	modelDensityWidth = []
	for dist in modelDist:
		modelDensityWidth.append(gravitationAnomalyOfPolygon(polygon, (dist, 0), (2670 - lowest_chi_squared[2])) * 2 + lowest_chi_squared[3]) # *2 because the stock stretches to infinity in both y-directions
	
	
	
	# # --- fit width (200:50:1000) and depth T (100:10:300) with fixed density (2350kg/m³) ---
	
	
	# density = 2350

	# startWidth = 200
	# stepSizeWidth = 20 # divisible 200
	# maxWidth = 1000

	# startDepth = 00 # 
	# stepSizeDepth = 5 # divisible 50
	# maxDepth = 300 # 

	# rows = math.floor((maxWidth - startWidth)/stepSizeWidth)+1
	# cols = math.floor((maxDepth - startDepth)/stepSizeDepth)+1
	# fitnesses = np.zeros((rows, cols)) # the fitness of each combination (Chi²)

	# k = -1
	# j = -1
	# lowest_chi_squared = [1000000, 0, 0]
	# for width in range(startWidth, maxWidth+1, stepSizeWidth):
	# 	k += 1
	# 	j = -1
		
	# 	for depth in range(startDepth, maxDepth+1, stepSizeDepth):
	# 		j += 1
	# 		# calculate gravitational defect
			
	# 		polygon = []
	# 		polygon.append([middle + width/2, 2000 ])
	# 		polygon.append([middle + width/2, depth])
	# 		polygon.append([middle - width/2, depth])
	# 		polygon.append([middle - width/2, 2000 ])
			
	# 		grav = []
	# 		for d in distances:
	# 			grav.append(gravitationAnomalyOfPolygon(polygon, (d, 0), (2670 - density)) * 2) # *2 because the stock stretches to infinity in both y-directions
			
	# 		# match the average value
	# 		diff = avgMeasuredGrav - np.mean(grav)
	# 		for l in range(len(datapoints)):
	# 			grav[l] += diff
			
	# 		differences = []
	# 		for n in range(len(grav)):
	# 			differences.append((measuredGrav[n] - grav[n]))
			
	# 		# calculate fitness values
			
	# 		chi_squared = 0
	# 		for di in differences:
	# 			chi_squared += di ** 2
			
	# 		if (chi_squared < lowest_chi_squared[0]):
	# 			lowest_chi_squared = [chi_squared, width, depth, diff, chi_squared]
			
	# 		# if (k==0):
	# 			# chi_squared-= 1E8
			
	# 		fitnesses[k, j] = math.log10(chi_squared)

	# # display fitness as heat map
	
	# print("best fit: %s (width %s, depth %s, diff %s, chi %s)" % tuple(lowest_chi_squared))

	# # cmap = sns.cm.rocket_r
	
	# xlabels = []
	# for i in range(round((maxDepth-startDepth)/50)):
	# 	xlabels.append((startDepth + 50*i))
	# 	for j in range(round(50/stepSizeDepth)-1):
	# 		xlabels.append("")
	# xlabels.append(maxDepth)

	# ylabels = []
	# for i in range(round((maxWidth-startWidth)/200)):
	# 	ylabels.append(startWidth + 200*i)
	# 	for j in range(round(200/stepSizeWidth)-1):
	# 		ylabels.append("")
	# ylabels.append(maxWidth)


	# plot.figure(figsize=(7.5, 6), dpi=100)
	# heatmap = sns.heatmap(fitnesses, xticklabels=xlabels, yticklabels=ylabels, cmap=cmap, cbar_kws={"label":"$\log_{10}(\chi^2)$"})
	# heatmap.set(ylabel="Breite [m]", xlabel="Tiefe [m]")
	# # plot.savefig("""Abbildungen\\3_Tiefe_Breite_Neu.png""", transparent = True, dpi=300)
	# # plot.show()
	# # store predicted data to plot it laterf

	# polygon = []
	# polygon.append([middle + lowest_chi_squared[1]/2, 2000])
	# polygon.append([middle + lowest_chi_squared[1]/2, lowest_chi_squared[2]])
	# polygon.append([middle - lowest_chi_squared[1]/2, lowest_chi_squared[2]])
	# polygon.append([middle - lowest_chi_squared[1]/2, 2000])
	
	# modelWidthDepth = []
	# for dist in modelDist:
	# 	modelWidthDepth.append(gravitationAnomalyOfPolygon(polygon, (dist, 0), (2670 - 2350)) * 2 + lowest_chi_squared[3]) # *2 because the stock stretches to infinity in both y-directions
	
	
	
	# # --- display measurement values and the different fits ---
	
	
	# fig = plot.figure(figsize=(8, 5), dpi=100)
	# plot.scatter(distances, measuredGrav, label="Messpunkte", color="limegreen", zorder=5)
	# plot.plot(modelDist, modelDensityDepth, label="Bester Fit für Dichte (=2290kg/m^3) & Tiefe (=294m) ", color="darkorchid")
	# plot.plot(modelDist, modelDensityWidth, label="Bester Fit für Dichte (=2000kg/m^3) & Breite (=295m) ", color="cornflowerblue")
	# plot.plot(modelDist, modelWidthDepth, label="Bester Fit für Tiefe (=90) & Breite (=460m)", color="red")
	# plot.xlabel("Distanz in Messrichtung")
	# plot.ylabel("$\delta g$ [mGal]")
	# legend = plot.legend(loc="upper right", edgecolor="black", facecolor="green")
	# legend.get_frame().set_alpha(None)
	# legend.get_frame().set_facecolor("blue")
	# plot.axis([-100, 1200, 4923, 4927])
	# plot.minorticks_on()
	# # plot.savefig("Abbildungen\\3_Fits_neu.png", transparent = True, dpi=300)
	# # plot.show()