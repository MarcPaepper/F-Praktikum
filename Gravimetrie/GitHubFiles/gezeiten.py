import numpy as np
import math

def gezeiten(year,month,day,hour,minute,utc_offset,lat,long,H_m):
    
    """
    
    Dieses Skript berechnet die Gezeitenbeschleunigung von Sonne und Mond zu
    einer vorgegebenen Uhrzeit an einem vorgegebenen Messpunkt.
    
    I. M . Longman (1959)
    Formulas for Computing the Tidal Accelerations Due to the Moon and the Sun
    Journal of Geophysical Research 64: 2351-2355
    
    Parameters
    ----------
    year, month, day : Datum der Messung
    
    hour, minute : Uhrzeit der Messung
    
    utc_offset : Offset der Zeitzone gegenüber UTC-Zeit in Stunden
    
    lat, long : Längen- und Breitengrad des Messpunktes in Dezimalgrad
    
    H_m : Höhe des Messpunktes über dem Meeresspiegel in Meter

    Returns
    -------
    gt : Gezeitenbeschleunigung in mGal

    """
    
    # Konstanten
    
    a = 6.37827e8 # Erdradius in cm
    c = 3.84402e10 # Abstand Erdmittelpunkt zu Mondmittelpunkt in cm
    c1 = 1.495e13 # Abstand Erdmittelpunkt zu Sonnenmittelpunkt in cm
    e = 0.05489972 # Exzentrizität des Mondorbits
    i = np.deg2rad(5.145) # Inklination des Mondorbits gegen die Ekliptik
    m = 0.074804 # Verhältnis der mittleren Sonnenbewegung zu der des Mondes
    omega = np.deg2rad(23.452) # Neigung des Äquators gegen die Ekliptik
    mu = 6.67e-8 # Gravitationskonstante in cgs-Einheiten
    M = 7.7537e25 # Masse des Mondes in g
    S = 1.993e33 # Masse der Sonne in g
    
    second = 0 # Betrachte nur ganze Minuten
    
    # Umrechnung der Koordinaten
    
    lt = np.deg2rad(lat) # Breitengrad in rad
    H = H_m*1e2 # Höhe über dem Meeresspiegel in cm
    
    # Berechnung Julianisches Datum
    jd = ( juliandate(year,month,day,hour,minute,second)
          - juliandate(1899,12,31,12,0,0) ) # Tage seit Mittag des 31.12.1899
    T = jd/36525 # Julianische Epochen seit Mittag des 31.12.1899
    utc_hour = hour-utc_offset
    t0 = utc_hour+minute/60+second/3600 # Dezimalstunde in UTC
    
    # Überprüfung desr Bedingung 0 <= t0 < 24, ggf. Korrektur
    if (t0 < 0):
        t0 = t0+24
    elif (t0 >= 24):
        t0 = t0-24
    
    # Berechnung Zenitdistanzen
    # Mittlere Länge des Mondes vom Äquinoktium (Gl. 10)
    s = ( dms2rad(270,26,14.72) + revsec2rad(1336,1108411.2)*T
         + revsec2rad(0,9.09)*T**2 + revsec2rad(0,0.0068)*T**3 )
    # Mittlere Länge des Mondperigäums (Gl. 11)
    p = ( dms2rad(334,19,40.87) + revsec2rad(11,392515.94)*T
         - revsec2rad(0,37.24)*T**2 )
    # Mittlere Länge der Sonne (Gl. 12)
    h = ( dms2rad(279,41,48.04) + revsec2rad(0,129602768.13)*T
         + revsec2rad(0,1.089)*T**2 )
    # Länge des aufsteigen Knoten des Mondorbits (Gl. 19)
    N = ( dms2rad(259,10,57.12) - revsec2rad(5,482912.63)*T
         + revsec2rad(0,7.58)*T**2+revsec2rad(0,0.008)*T**3 )
    # Inklination des Mondorbits gegen den Äquator (Gl. 30)
    I = np.arccos(np.cos(omega)*np.cos(i)-np.sin(omega)*np.sin(i)*np.cos(N))
    # Länge des Schnittpunkts mit dem Himmelsäquator auf dem Mondorbit (Gl. 14)
    xi = N-np.arcsin(np.sin(omega)*np.sin(N)/np.sin(I))
    # Mittlere Länge des Mondes vom Schnittpunkt Ekliptik und Äquator (Gl. 13)
    sigma = s-xi
    # Länge des Schnittpunkts mit dem Mondorbit auf dem Himmelsäquator (Gl. 21)
    nu = np.arcsin(np.sin(i)*np.sin(N)/np.sin(I))
    
    # Stundenwinkel der Sonne, westlich vom Beobachtungspunkt (Gl. 24)
    t = np.deg2rad(15*(t0-12)+long)
    
    # Rektaszension des Meridians des Beobachtungspunktes vom Schnittpunkt
    # Ekliptik und Äquator (Gl. 23)
    chi = t+h-nu
    # Länge des Mondes auf dem Mondorbit vom Schnittpunkt Ekliptik und Äquator
    # (Gl. 9)
    l = ( sigma + 2*e*np.sin(s-p)+5*e**2*np.sin(2*(s-p))/4
         + 15*m*e*np.sin(s-2*h+p)/4
         + 11*m**2*np.sin(2*(s-h))/8 )
    # Zenitdistanz des Mondes (Gl. 7)
    theta = ( np.arccos(np.sin(lt)*np.sin(I)*np.sin(l)
                        + np.cos(lt)*((np.cos(I/2))**2*np.cos(l-chi)
                                      + (np.sin(I/2))**2*np.cos(l+chi))) )
    
    # Mittlere Länge des Sonnenperigäums (Gl. 26)
    p1 = ( dms2rad(281,13,15) + revsec2rad(0,6189.03)*T
          + revsec2rad(0,1.63)*T**2 + revsec2rad(0,0.012)*T**3 )
    # Exzentrizität des Erdorbits (Gl. 27)
    e1 = 0.01675104-0.0000418*T-0.00000126*T**2
    # Rektaszension des Meridians des Beobachtungspunktes vom Frühlingspunkt
    # (Gl. 25)
    chi1 = t+h
    # Länge der Sonne in der Ekliptik vom Frühlingspunkt (Gl. 25)
    l1 = h+2*e1*np.sin(h-p1)
    # Zenitdistanz der Sonne (Gl. 8)
    phi = ( np.arccos(np.sin(lt)*np.sin(omega)*np.sin(l1)
                      + np.cos(lt)*((np.cos(omega/2))**2*np.cos(l1-chi1)
                                    + (np.sin(omega/2))**2*np.cos(l1+chi1))) )
    
    # Berechnung der Abstände von Sonne und Mond zum Messpunkt
    # (Gl. 31)
    a_s = 1/(c*(1-e**2))
    # (Gl. 32)
    a1s = 1/(c1*(1-e1**2))
    # Inverser Abstand der Mittelpunkte von Erde und Mond (Gl. 29)
    d_inv = ( 1/c + a_s*e*np.cos(s-p)
             + a_s*e**2*np.cos(2*(s-p))
             + 15*a_s*m*e*np.cos(s-2*h+p)/8
             + a_s*m**2*np.cos(2*(s-h)) )
    # Inverser Abstand der Mittelpunkte von Erde und Sonne (Gl. 30)
    D_inv = 1/c1+a1s*e1*np.cos(h-p1)
    
    # (Gl. 34)
    C = np.sqrt(1/(1+0.006738*(np.sin(lt))**2))
    # Abstand des Beobachtungspunktes vom Erdmittelpunkt
    r = C*a+H
    
    # Berechnung der vertikalen Gezeitenbeschleunigung
    # Love-Zahlen (aus Orsulic et al., 2019)
    h2 = 0.6135
    k2 = 0.305
    # Geometriefaktor (aus Orsulic et al., 2019)
    beta = 1+h2-3*k2/2
    
    # Vertikalkomponente der Gezeitenbeschleunigung des Mondes (Gl. 1)
    gm = ( mu*M*r*d_inv**3*(3*(np.cos(theta))**2-1)
          + 3*mu*M*r**2*d_inv**4*(5*(np.cos(theta))**3-3*np.cos(theta))/2 )
    # Vertikalkomponente der Gezeitenbeschleunigung der Sonne (Gl. 3)
    gs = mu*S*r*D_inv**3*(3*(np.cos(phi))**2-1)
    # Addition und Umrechnung in Beschleunigung in mGal
    gt = 1e3*beta*(gm+gs)
    
    # Ausgabe der Gezeitenbeschleunigung
    return gt
    
    
def juliandate(year,month,day,hour,minute,second):
    
    """
    
    Berechnung des Julianischen Datums.
    
    Parameters
    ----------
    year, month, day : Datum im Gregorianischen Kalender
    
    hour, minute, second : Uhrzeit

    Returns
    -------
    jd : Julianisches Datum
    
    """    
        
    if (month < 2) :
        year = year-1
        month = month+12
      
    day = day+hour/24+minute/1440+second/86400
    B = 2 - math.floor(year/100) + math.floor(year/400)
      
    jd = ( math.floor(365.25*(year+4716))+math.floor(30.6001*(month+1))
          + day + B - 1524.5 )
    return jd
    
def dms2rad(d,m,s):
    
    """
    
    Umrechnung von Grad, Bogenminuten und Bogensekunden in Radiant
    
    Parameters
    ----------
    d : Grad
    
    m : Bogenminuten
    
    s : Bogensekunden

    Returns
    -------
    rad : Wert in Radiant
    
    """    
    
    rad = np.deg2rad(d+m/60+s/3600)
    
    return rad

def revsec2rad(rev,sec):
    
    """
    
    Umrechnung von Revolutionen und Bogensekunden in Radiant
    
    Parameters
    ----------
    rev : Anzahl der Revolutionen
    
    s : Bogensekunden

    Returns
    -------
    rad : Wert in Radiant
    
    """    
    
    rad = np.deg2rad(rev*360+sec/3600)
    
    return rad
