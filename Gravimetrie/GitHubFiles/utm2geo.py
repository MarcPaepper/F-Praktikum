import numpy as np

def utm2geo(E,N,zone,hem):

    """
    
    Mithilfe dieser Funktion können Koordinaten aus dem UTM-Koordinatensystem 
    in das geographische Koordinatensystem umgerechnet werden.
    
    C. F. F. Karney (2011)
    Transverse Mercator with an accuracy of a few nanometers
    Journal of Geodesy 85: 475-485
    
    Parameters
    ----------
    E : Easting-Koordinate im UTM-System in Meter
    
    N : Northing-Koordinate im UTM-System in Meter
    
    zone : Nummer der UTM-Zone
    
    hem : Angabe der Hemisphäre (N oder S) als String

    Returns
    -------
    lat : Breitengrad der geographischen Koordinaten in Dezimalgrad
    
    long : Längengrad der geopgraphischen Koordinaten in Dezimalgrad

    """
    
    # Konstanten
    
    a = 6378.137 # Erdradius
    f = 1/298.257223563 # Abplattung
    e = np.sqrt(f*(2-f)) # Exzentrizität
    n = f/(2-f) # Dritte Abplattung
    k0 = 0.9996 # Skalierungsfaktor
    
    # Subtraktion des Offsets
    
    if hem == 'N':
        N = N*1e-3 # Northing für die nördliche Hemisphäre
    elif hem == 'S':
        N = (N-10000000)*1e-3 # Northing für die südliche Hemisphäre
    else:
        raise ValueError("Die Hemisphäre muss mit N oder S angegeben werden.")
    E = (E-500000)*1e-3 # Easting
    
    # Berechnung der Zwischenschritte (siehe Karney, 2011)
    
    A = a/(1+n)*(1+ns(n,1,4,2)+ns(n,1,64,4)+ns(n,1,256,6)+ns(n,25,16384,8))
    
    eta = E/(k0*A)
    xi = N/(k0*A)
    
    beta = [( ns(n,1,2,1)-ns(n,2,3,2)+ns(n,37,96,3)-ns(n,1,360,4)-
            ns(n,81,512,5)+ns(n,96199,604800,6)-ns(n,5406467,38707200,7)+
            ns(n,7944359,67737600,8) ),
            ( ns(n,1,48,2)+ns(n,1,15,3)-ns(n,437,1440,4)+ns(n,46,105,5)-
            ns(n,1118711,3870720,6)+ns(n,51841,1209600,7)+
            ns(n,24749483,348364800,8) ),
            ( ns(n,17,480,3)-ns(n,37,840,4)-ns(n,209,4480,5)+ns(n,5569,90720,6)+
            ns(n,9261899,58060800,7)-ns(n,6457463,17740800,8) ),
            ( ns(n,4397,161280,4)-ns(n,11,504,5)-ns(n,830251,7257600,6)+
            ns(n,466511,2494800,7)+ns(n,324154477,7664025600,8) ),
            ( ns(n,4583,161280,5)-ns(n,108847,3991680,6)-
            ns(n,8005831,63866880,7)+ns(n,22894433,124540416,8) ),
            ( ns(n,20648693,638668800,6)-ns(n,16363163,518918400,7)-
            ns(n,2204645983,12915302400,8) ),
            ( ns(n,219941297,5535129600,7)-ns(n,497323811,12454041600,8) ),
            ( ns(n,191773887257,3719607091200,8) )]
    
    xis_sum = 0
    for j in range(1,9):
        xis_sum = xis_sum + beta[j-1]*np.sin(2*j*xi)*np.cosh(2*j*eta)
    xis = xi - xis_sum
    
    etas_sum = 0
    for j in range(1,9):
        etas_sum = etas_sum + beta[j-1]*np.cos(2*j*xi)*np.sinh(2*j*eta)
    etas = eta - etas_sum
    
    taus = np.sin(xis)/(np.sqrt((np.sinh(etas))**2+(np.cos(xis))**2))
    
    # Iterative Lösung für tau
    
    tau_im1 = taus
    sigmai0 = np.sinh(e*np.arctanh((e*tau_im1)/(np.sqrt(1+tau_im1**2))))
    tausi0 = tau_im1*np.sqrt(1+sigmai0**2)-sigmai0*np.sqrt(1+tau_im1**2)
    dtau_im1 = ( ((taus-tausi0)/(np.sqrt(1+tausi0**2)))*
                (1+(1-e**2)*tau_im1**2)/((1-e**2)*np.sqrt(1+tau_im1**2)) )
    for ii in range(1,9):
        taui = tau_im1+dtau_im1
        sigmai = np.sinh(e*np.arctanh((e*taui)/(np.sqrt(1+taui**2))))
        tausi = taui*np.sqrt(1+sigmai**2)-sigmai*np.sqrt(1+taui**2)
        tau_im1 = taui
        dtau_im1 = ( ((taus-tausi)/(np.sqrt(1+tausi**2)))*
                    (1+(1-e**2)*taui**2)/((1-e**2)*np.sqrt(1+taui**2)) )
    tau = taui
    
    # Berechnung der geographischen Koordinaten
    
    lng = np.arctan2(np.sinh(etas),np.cos(xis))
    lt = np.arctan2(tau,1)
    
    lat = np.rad2deg(lt) # Breitengrad
    long0 = zone*6-183 # Mittlerer Längengrad
    long = np.rad2deg(lng)+long0 # Längengrad
    
    return [lat,long]
    
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
