import numpy as np

def geo2utm(lat,long):

    """
    
    Mithilfe dieser Funktion können Koordinaten aus dem geographischen 
    Koordinatensytem in das UTM-Koordinatensystem umgerechnet werden.
    
    C. F. F. Karney (2011)
    Transverse Mercator with an accuracy of a few nanometers
    Journal of Geodesy 85: 475-485
    
    Parameters
    ----------
    lat : Breitengrad der geographischen Koordinaten in Dezimalgrad
    
    long : Längengrad der geopgraphischen Koordinaten in Dezimalgrad

    Returns
    -------
    E : Easting-Koordinate im UTM-System in Meter
    
    N : Northing-Koordinate im UTM-System in Meter
    
    zone : Nummer der UTM-Zone
    
    hem : Angabe der Hemisphäre (N oder S) als String

    """
    
    # Bestimme Hemisphäre
    
    if lat < 0:
        hemisphere = 1
        hem = 'S'
    else:
        hemisphere = 0
        hem = 'N'
        
    # Konstanten
    
    a = 6378.137 # Erdradius
    f = 1/298.257223563 # Abplattung
    e = np.sqrt(f*(2-f)) # Exzentrizität
    n = f/(2-f) # Dritte Abplattung
    
    N0 = hemisphere*10000000 # Offset Northing
    E0 = 500000 # Offset Easting
    k0 = 0.9996 # Skalierungsfaktor
    
    # Berechnung UTM-Zone
    
    zone = (long-(long%6))/6+31
    
    # Berechnung Mittlerer Längengrad
    
    long0 = zone*6-183
    
    # Umrechnung in Radiant
    
    lng = np.deg2rad(long-long0)
    lt = np.deg2rad(lat)
    
    # Berechnung der Zwischenschritte (siehe Karney, 2011)
    
    A = a/(1+n)*(1+ns(n,1,4,2)+ns(n,1,64,4)+ns(n,1,256,6)+ns(n,25,16384,8))
    
    alpha = [( ns(n,1,2,1)-ns(n,2,3,2)+ns(n,5,16,3)+ns(n,41,180,4)-
             ns(n,127,288,5)+ns(n,7891,37800,6)+ns(n,72161,387072,7)-
             ns(n,18975107,50803200,8) ),
             ( ns(n,13,48,2)-ns(n,3,5,3)+ns(n,557,1440,4)+ns(n,281,630,5)-
             ns(n,1983433,1935360,6)+ns(n,13769,28800,7)+
             ns(n,148003883,174182400,8) ),
             ( ns(n,61,240,3)-ns(n,103,140,4)+ns(n,15061,26880,5)+
             ns(n,167603,181440,6)-ns(n,67102379,29030400,7)+
             ns(n,79682431,79833600,8) ),
             ( ns(n,49561,161280,4)-ns(n,179,168,5)+ns(n,6601661,7257600,6)+
             ns(n,97445,49896,7)-ns(n,40176129013,7664025600,8) ),
             ( ns(n,34729,80640,5)-ns(n,3418889,1995840,6)+
             ns(n,14644087,9123840,7)+ns(n,2605413599,622702080,8) ),
             ( ns(n,212378941,319334400,6)-ns(n,30705481,10378368,7)+
             ns(n,175214326799,58118860800,8) ),
             ( ns(n,1522256789,1383782400,7)-ns(n,16759934899,3113510400,8) ),
             ( ns(n,1424729850961,743921418240,8) )]

    tau = np.tan(lt)
    sigma = np.sinh(e*np.arctanh((e*tau)/(np.sqrt(1+tau**2))))
    
    taus = tau*np.sqrt(1+sigma**2)-sigma*np.sqrt(1+tau**2)
    
    xis = np.arctan2(taus,np.cos(lng))
    etas = np.arcsinh(np.sin(lng)/(np.sqrt(taus**2+(np.cos(lng))**2)))
    
    xi_sum = 0
    for j in range(1,9):
        xi_sum = xi_sum + alpha[j-1]*np.sin(2*j*xis)*np.cosh(2*j*etas)
    xi = xis + xi_sum
    
    eta_sum = 0
    for j in range(1,9):
        eta_sum = eta_sum + alpha[j-1]*np.cos(2*j*xis)*np.sinh(2*j*etas)
    eta = etas + eta_sum
    
    # Berechnung und Ausgabe der UTM-Koordinaten
    
    E = E0 + 1e3*k0*A*eta # Easting
    N = N0 + 1e3*k0*A*xi # Northing
    
    return [E,N,zone,hem]

def ns(n,a,b,p):

    """
    
    Berechnung der Summanden für die Reihenentwicklung nach der Dritten 
    Abplattung
    
    Parameters
    ----------
    n : Dritte Abplattung
    
    a : Zähler des Vorfaktors
    
    b : Nenner des Vorfaktors
    
    p : Exponent

    Returns
    -------
    summ: Summanden der Form (a/b)*n^p für die Reihenentwicklungen

    """
    
    summ = (a/b)*(n**p)
    
    return summ