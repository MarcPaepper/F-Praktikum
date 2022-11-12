# Beschreibung der Skripte (Python)

Dieser Unterordner enthält alle zur Verfügung gestellten Python-Skripte. Im folgenden werden die Einzelnen Skripte kurz beschrieben und angegeben, wie die Funktion aufgerufen werden kann.

## count2mgal

Umrechnung der am Gravimeter abgelesenen Counter-Werte in eine Schwerebeschleungigung. Grundlage ist die Kalibrierung vom 14.12.1993.

Aufruf: `count2mgal(ct)`

Parameter: 
- `ct` - Array mit den am Gravimeter abgelesenen Werten in Counts

Ausgabe: 
- `mgal` - Schwerebeschleungigung in mGal

## geo2utm

Umrechnung von geographischen Koordinaten in UTM-Koordinaten (WGS84).

Aufruf: `geo2utm(lat,long)`

Parameter: 
- `lat` - Breitengrad im geographischen Koordinatensystem, angegeben in Dezimalgrad
- `long` - Längengrad im geographischen Koordinatensystem, angegeben in Dezimalgrad

Ausgabe: 
- `E` - Easting-Koordinate im UTM-Koordinatensystem, angegeben in Meter
- `N` - Northing-Koordinate im UTM-Koordinatensystem, angegeben in Meter
- `zone` - Nummer der UTM-zone
- `hem` - Angabe der Hemisphäre als String ('N' für nördliche, 'S' für südliche Hemisphäre)

## gezeiten

Berechnung der Gezeitenbeschleunigung von Sonne und Mond an einer vorgegebenen Position zu einem vorgegebenen Zeitpunkt.

Aufruf: `gezeiten(year,month,day,hour,minute,utc_offset,lat,long,H_m)`

Parameter:
- `year, month day` - Datum der Messung
- `hour, minute` - Uhrzeit der Messung
- `utc_offset` - Verschiebung der Zeitzone zur UTC-Zeit, angegeben in Stunden
- `lat, long` - geographische Koordinaten der Messung, angegeben in Dezimalgrad
- `H_m` - Höhe über NN, angegeben in Meter

Ausgabe:
- `gt` - Gezeitenbeschleunigung von Sonne und Mond

## topographie_quader

Berechnung der Schwerestörung eines Quaders mit homogener Dichte zur Abschätzung der Topographiekorrektur. Für Fälle, in denen Lösung nicht existiert, wird eine Näherungslösung berechnet.

Aufruf: `topographie_quader(x,y,z,rho)`

Parameter:
- `x, y, z` - Array mit den Integrationsgrenzen in x-, y- und z-Richtung, angegeben in Meter
- `rho` - Dichte des Quaders, angegeben in kg/m³

Ausgabe:
- `dg` - Schwerestörung des Quaders, angegeben in mGal

## utm2geo

Umrechnung von Koordinaten im UTM-Koordinatensystem in geographische Koordinaten.

Aufruf: `utm2geo(E,N,zone,hem)`

Parameter: 
- `E` - Easting-Koordinate im UTM-Koordinatensystem, angegeben in Meter
- `N` - Northing-Koordinate im UTM-Koordinatensystem, angegeben in Meter
- `zone` - Nummer der UTM-zone
- `hem` - Angabe der Hemisphäre als String ('N' für nördliche, 'S' für südliche Hemisphäre)

Ausgabe: 
- `lat` - Breitengrad im geographischen Koordinatensystem, angegeben in Dezimalgrad
- `long` - Längengrad im geographischen Koordinatensystem, angegeben in Dezimalgrad
