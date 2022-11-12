import numpy as np

def topographie_quader(x,y,z,rho):
    
    """
    
    Mithilfe dieser Funktion kann eine analytische Lösung zur Berechnung der
    Schwerestörung eines Quaders mit konstanter Dichte zur Abschätzung des 
    gravimetrischen Einflusses der Topographie ausgewertet werden.
    
    D. Nagy, G. Papp, J. Benedek (2000)
    The gravitational potential and its derivatives for the prism
    Journal of Geodesy 74: 552-560
    
    Parameters
    ----------
    x, y, z : Tuple mit den Grenzen des Quaders in x-, y- und z-Richtung in
              Meter
    
    rho : Dichte des Quaders in kg/m^3

    Returns
    -------
    dg : Schwerestörung des Quaders im Ursprung in mGal

    """
    
    # Umwandlung der Tuple in Arrays
    
    x = np.array(x); y = np.array(y); z = np.array(z);
    
    if (x[0]==x[1]) or (y[0]==y[1]) or (z[0]==z[1]):
        
        # obere = untere Grenze -> kein Volumen -> keine Störmasse
        
        dg = 0
        
    else:
    
    
        def T_eval(x,y,z):
            
            """
    
            Analytische Lösung für die Integration (Stammfunktion)
    
    
            Parameters
            ----------
            x, y, z : Koordinaten, an denen die Stammfunktion ausgewertet wird

            Returns
            -------
            Ti : Wert der Stammfunktion am angegebenen Punkt

            """
            
            Ti = ( x*np.log(y+np.sqrt(x**2+y**2+z**2)) +
                  y*np.log(x+np.sqrt(x**2+y**2+z**2)) -
                  z*np.arctan2(x*y,z*np.sqrt(x**2+y**2+z**2)) )
            
            return Ti
        
        # Auswertung des Integrals an den Integrationsgrenzen
        
        T = ( T_eval(x[1],y[1],z[1]) - T_eval(x[0],y[1],z[1]) - 
             T_eval(x[1],y[0],z[1]) + T_eval(x[0],y[0],z[1]) -
             T_eval(x[1],y[1],z[0]) + T_eval(x[0],y[1],z[0]) +
             T_eval(x[1],y[0],z[0]) - T_eval(x[0],y[0],z[0]))

        gamma = 6.6743e-6 # Gravitationskonstante in (mGal*m^2)/kg
        
        # Berechnung der postitiven Schwerestörung
        
        dg = np.abs(gamma*rho*T)
        
    if np.isnan(dg):
        
        # Abfangen der Fälle, in denen T keine analytische Lösung liefert
        # Berechnung über Zerlegung und anschließende Grenzwertbetrachtung
        # Überschreibe dg mit neuem Wert
        
        dg = np.abs(topographie_zerlegung(x,y,z,rho))
        
    return dg

def topographie_zerlegung(xb,yb,zb,rho):
    
    """
    
    Diese Funktion zerlegt einen Quader, für den die analytische Lösung des
    Integrals nicht existiert, in Teilquader, deren untere Grenze 0 und deren
    obere Grenze der eigentlichen Grenze entspricht. Anschließend ruft die
    Funktion eine weitere Funktion auf, die eine Grenzwertlösung für das 
    Integral berechnet.
    
    Parameters
    ----------
    xb, yb, zb : Tuple mit den Grenzen des Quaders in x-, y- und z-Richtung in
              Meter
    
    rho : Dichte des Quaders in kg/m^3

    Returns
    -------
    dg : Schwerestörung des Quaders im Ursprung in mGal

    """
    
    # Bestimme, ob obere oder untere Integrationsgrenze von zb ungleich null
    # ist (die analytische Lösung existiert nicht, wenn eine der beiden Grenzen
    # von zb und (mindestens) eine Integrationsgrenze von xb oder yb null ist)
    zind = np.flatnonzero(zb)
    
    # Überprüfe, ob eine der beiden Integrationsgranzen von xb null ist
    if 0 in xb:
        
        # Obere oder untere Grenze von xb ungleich null?
        xind = np.flatnonzero(xb)
        
        # Überprüfe, ob eine der beiden Integrationsgrenzen von yb null ist
        if 0 in yb:
            
            # Obere oder untere Grenze von yb ungleich null?
            yind = np.flatnonzero(yb)
            
            # Rufe Funktion für Näherungslösung auf
            dg = topographie_naeherung(xb[xind],yb[yind],zb[zind],rho)
            # Ändere Vorzeichen, falls Integrationsgrenzen getauscht wurden
            dg = dg*(2*xind-1)*(2*yind-1)*(2*zind-1)
            
        else:
            
            # Zerlege Quader in Teilquader mit je einer Grenze von yb = 0
            
            # Rufe jeweils Funktion für Näherungslösung auf
            dg = ( topographie_naeherung(xb[xind],yb[1],zb[zind],rho) -
                  topographie_naeherung(xb[xind],yb[0],zb[zind],rho) )
            # Ändere Vorzeichen, falls Integrationsgrenzen getauscht wurden
            dg = dg*(2*xind-1)*(2*zind-1)
    
    # Überprüfe, ob eine der beiden Integrationsgrenzen von yb null ist
    # In diesem Fall sind obere und untere Grenze von xb ungleich null
    elif 0 in yb:
        
        # Obere oder unteregrenze von yb ungleich null?
        yind = np.flatnonzero(yb)
        
        # Zerlege Quader in Teilquader mit je einer Grenze von xb = 0
        
        # Rufe jeweils Funktion für Näherungslösung auf
        dg = ( topographie_naeherung(xb[1],yb[yind],zb[zind],rho) -
              topographie_naeherung(xb[0],yb[yind],zb[zind],rho) )
        # Ändere Vorzeichen, falls Integrationsgrenzen getauscht wurden
        dg = dg*(2*yind-1)*(2*zind-1)
        
    return dg

def topographie_naeherung(x,y,z,rho):

    """
    
    Diese Funktion berechnet den Wert einer Näherungslösung für die
    Schwerestörung eines Quaders homogener Dichte. Die untere
    Integrationsgrenze ist hierbei null, die obere Integrationsgrenze
    ungleich null
    
    D. Nagy, G. Papp, J. Benedek (2000)
    The gravitational potential and its derivatives for the prism
    Journal of Geodesy 74: 552-560
    
    Parameters
    ----------
    x, y, z : Tuple mit den Grenzen des Quaders in x-, y- und z-Richtung in
              Meter
    
    rho : Dichte des Quaders in kg/m^3

    Returns
    -------
    dg : Schwerestörung des Quaders im Ursprung in mGal

    """
    
    gamma = 6.6743e-6 # Gravitationskonstante in (mGal*m^2)/kg
    
    # Gleichung für die Näherungslösung des Integrals
    Ti = ( x*np.log(y+np.sqrt(x**2+y**2+z**2)) - 
          x*np.log(y+np.sqrt(x**2+y**2)) -
          x*np.log(np.sqrt(x**2+z**2)) +
          x*np.log(np.sqrt(x**2)) +
          y*np.log(x+np.sqrt(x**2+y**2+z**2)) -
          y*np.log(x+np.sqrt(x**2+y**2)) -
          y*np.log(np.sqrt(y**2+z**2)) +
          y*np.log(np.sqrt(y**2)) -
          z*np.arctan2(x*y,z*np.sqrt(x**2+y**2+z**2)) )
    
    # Berechnung der Schwerestörung
    dg = -rho*gamma*Ti
    
    return dg
    