def count2mgal(ct):
    """
    
    Mithilfe dieser Funktion kann die analoge Anzeige des Lacoste-Romberg-
    Gravimeters (cr) in eine Gravitationsbeschleungigung in mGal umgerechnet
    werden. Die Umrechnung basiert auf der Kalibrierung vom 14.12.1993.
    
    Parameters
    ----------
    ct : Analoge Anzeige des Gravimeters (Counter Readin), angegeben als 
         Array, im Wertebereich 0 < ct < 7000

    Returns
    -------
    mgal : Gravitationsbeschleunigung in mGal gemäß der Kalibrierung des
           Gravimeters.

    """
    
        
    if isinstance(ct,(float,int)):
        # Rekursiver Aufruf fuer Umrechnung einzelner Zahlen
        mgal = count2mgal([ct])
    elif isinstance(ct,(list,tuple)):
        mgal = [None]*len(ct)
    
        for ii in range(0,len(ct)):
        
            cr = ct[ii]
            
            # Fehlermeldungen fuer Werte ausserhalb der Anzeige
            if cr < 0:
                raise ValueError("Counter Reading muss groesser als null sein.")
            elif cr > 7000:
                raise ValueError("Counter Reading darf maximal 7000 sein.")
            
            # Werte aus der Kalibrierungstabelle, in 100-Counts-Intervallen
            
            # Gravitationsbeschleunigung pro 100 Counts
            
            val_100 = [0, 102.12, 204.22, 306.3, 408.36, 510.41, 612.44, 714.45,
                   816.45, 918.43, 1020.4, 1122.36, 1224.31, 1326.25, 1428.18,
                   1530.1, 1632.01, 1733.92, 1835.83, 1937.73, 2039.62, 2141.52,
                   2243.41, 2345.31, 2447.2, 2549.1, 2651, 2752.9, 2854.8,
                   2956.7, 3058.61, 3160.52, 3262.44, 3364.36, 3466.28, 3568.21,
                   3670.14, 3772.08, 3874.02, 3975.96, 4077.9, 4179.85, 4281.8,
                   4383.75, 4485.71, 4587.66, 4689.62, 4791.58, 4893.54, 4995.5,
                   5097.45, 5199.4, 5301.35, 5403.28, 5505.21, 5607.14, 5709.05,
                   5810.94, 5912.83, 6014.7, 6116.56, 6218.41, 6320.24, 6422.06,
                   6523.86, 6625.86, 6727.4, 6829.18, 6930.91, 7032.61, 7134.29]
            
            # Intervall pro Count zwischen 100 Counts
            
            val_int = [1.02119, 1.021, 1.02082, 1.02064, 1.02046, 1.02028, 1.02011,
                   1.01995, 1.01982, 1.0197, 1.01959, 1.01949, 1.0194, 1.01931,
                   1.01923, 1.01916, 1.01909, 1.01905, 1.019, 1.01898, 1.01896,
                   1.01894, 1.01894, 1.01895, 1.01897, 1.01898, 1.019, 1.01903,
                   1.01906, 1.01908, 1.01912, 1.01917, 1.01921, 1.01924, 1.01928,
                   1.01931, 1.01936, 1.01938, 1.01942, 1.01945, 1.01948, 1.0195,
                   1.01953, 1.01954, 1.01956, 1.01958, 1.01958, 1.01958, 1.01958,
                   1.01956, 1.01951, 1.01945, 1.01938, 1.0193, 1.01921, 1.01911,
                   1.01895, 1.01887, 1.01874, 1.01861, 1.01847, 1.01832, 1.01816,
                   1.01799, 1.0178, 1.01762, 1.01784, 1.01724, 1.01704, 1.01638, 0]
    
            # Berechnung der Gravitationsbeschleunigung
            # Einser- und Zehnerstellen des Counters
            cr_int = cr%100
            # Index des 100er-Intervalls des Counters
            ind = int((cr-cr_int)/100)
            # Auslesen des Wertes des 100er-Intervalls, Interpolation
            mgal[ii] = val_100[ind]+val_int[ind]*cr_int
    else:
        # Fehermeldung fuer falschen Datentyp
        raise TypeError("Datentyp muss Liste oder Tupel sein.")
    # Ausgabe des Schwerewertes
    return mgal
