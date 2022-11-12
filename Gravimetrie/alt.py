import ephem
import pytz
import csv
from datetime import datetime

from GitHubFiles.geo2utm import geo2utm

gps_e = "13.100"
gps_n = "52.000"
hours = range(0, 24)
y1 = []
y2 = []
for h in hours:
	date = datetime(2022, 10, 10, h, 0)
	dp = datapoint(0, date, 0, gps_n, gps_e)
	correctTidalAttraction(dp)
	y1.append(dp.gravitation)
	y2.append(dp.gps_e)

plot.plot(hours, y1, label="Lunar")
plot.plot(hours, y2, label="Solar")
plot.legend(loc="upper left")
plot.axis([0, 24, 0, 180])
plot.show()

# read in datapoints from csv file

def readDataVersuchsteil1(date):
	reader = csv.reader(open('Rohdaten_1.csv', 'r'))
	datapoints = []
	# the gps coordinates are the same for every datapoint and are hardcoded here
	utm = geo2utm(52.28014, 10.5478)
	for row in reader:
		floor, timestamp, counts = row
		datapoints.append(datapoint())
		
	return 

# correct the deviations due to the tidal attraction of sun and moon based on position and time
def getSolarZenith(dp):
	d = dp.time.timetuple().tm_yday # days since start of year beginning with 1 at Jan 1st
	
	#calculate hour angle
	
	# local standard time meridian in ° for Germany (Sommerzeit)
	lstm = 15 * 2
	
	B = 2 * pi / 365 * (d - 81) # just a shortcut to reduce space in the following line
	EoT = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B) # correction for earth path eccentricity
	TC = 4 * (dp.gps_e - lstm) + EoT # time correction in minutes
	LT = dp.time.hour + dp.time.minute / 60 + dp.time.second / 3600 # local time in decimal hours
	LST = LT + TC / 60 # local solar time in decimal hours
	HRA = 15 * (LST - 12) # hour angle
	HRA_r = 15 * (LST - 12) # hour angle in radians
	
	# calculate 
	declination = - 23.45 * cos(2 * pi * (d+10)) # declination in °
	dcl = - 23.45 * cos(2 * pi * (d+10)) # declination in radians
	
	lat = dp.gps_n * 2 * pi / 360
	
	elevation = arcsin(sin(dcl) * sin(lat) + cos(dcl) * cos(lat) * cos(HRA_r)) # elevation angle in radians
	
	zenith = pi / 2 - elevation # zenith angle in radians
	return zenith

#def getLunarZenith(dp):
	

# correct the deviations due to the tidal attraction of sun and moon based on position and time   
def correctTidalAttraction(dp):
	# create observer on the datapoint position
	
	obs = ephem.Observer()
	obs.lat = dp.gps_n
	obs.lon = dp.gps_e
	obs.pressure = 0
	# convert local time to utc time (required for pyephem)
	tz_germany = pytz.timezone('Europe/Berlin')
	germany_time = dp.time
	utc_time = germany_time.astimezone(pytz.utc)
	obs.date = utc_time
	
	# calc solar zenith angle
	sun = ephem.Sun(obs)
	alt = sun.alt # altitude in °
	solarZenith = 90 - 360 / (2 * pi) * (alt) # zenith in degrees
	
	# calc lunar zenith angle
	moon = ephem.Moon(obs)
	alt = moon.alt # altitude in °
	lunarZenith = 90 - 360 / (2 * pi) * (alt) # zenith in degrees
	#lunarZenith = (90 - alt) # zenith in radians
	
	dp.gravitation = lunarZenith
	dp.gps_e = solarZenith