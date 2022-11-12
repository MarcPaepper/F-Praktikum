def count2mgal(ct):
    """
    
    Mithilfe dieser Funktion kann die analoge Anzeige des Lacoste-Romberg-
    Gravimeters (cr) in eine Gravitationsbeschleungigung in mGal umgerechnet
    werden. Die Umrechnung basiert auf der Kalibrierung vom 03.06.2008.
    
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
        # Rekursiver Aufruf fÃ¼r Umrechnung einzelner Zahlen
        mgal = count2mgal([ct])
    elif isinstance(ct,(list,tuple)):
        mgal = [None]*len(ct)
    
        for ii in range(0,len(ct)):
        
            cr = ct[ii]
            
            # Fehlermeldungen fÃ¼r Werte auÃerhalb der Anzeige
            if cr < 0:
                raise ValueError("Counter Reading muss grÃ¶Ãer als null sein.")
            elif cr > 7000:
                raise ValueError("Counter Reading darf maximal 7000 sein.")
            
            # Werte aus der Kalibrierungstabelle, in 100-Counts-Intervallen
            
            # Gravitationsbeschleunigung pro 100 Counts
            
            val_100 = [0, 102.16, 204.31, 306.46, 408.6, 510.74, 612.38, 715.02,
                       817.17, 919.32, 1021.48, 1123.65, 1225.82, 1328, 1430.19,
                       1532.39, 1634.6, 1736.92, 1839.04, 1941.28, 2043.54, 
                       2145.8, 2249.08, 2350.37, 2452.67, 2554.99, 2657.32,
                       2759.67, 2862.03, 2964.4, 3066.78, 3169.15, 3271.59,
                       3374, 3476.43, 3578.87, 3681.32, 3783.78, 3889.25, 
                       3989.73, 4091.21, 4193.71, 4296.21, 4398.72, 4501.24,
                       4603.77, 4706.3, 4808.83, 4911.37, 5013.91, 5116.45,
                       5218.99, 5321.53, 5424.07, 5526.61, 5629.14, 5731.67,
                       5834.2, 5936.72, 6039.23, 6141.73, 6244.22, 6346.68,
                       6449.14, 6551.57, 6653.98, 6756.37, 6858.73, 6961.07,
                       7063.38, 7165.66]
            
            # Intervall pro Count zwischen 100 Counts
            
            val_int = [1.02162, 1.02151, 1.02145, 1.02141, 1.0214, 1.02141, 
                       1.02144, 1.02147, 1.02153, 1.02159, 1.02165, 1.02173,
                       1.02181, 1.02189, 1.02198, 1.02208, 1.02218, 1.02228,
                       1.0224, 1.02252, 1.02264, 1.02276, 1.0229, 1.02304,
                       1.02319, 1.02332, 1.02346, 1.02359, 1.02372, 1.02384,
                       1.02396, 1.02408, 1.02419, 1.02429, 1.02439, 1.0245,
                       1.02459, 1.02468, 1.02478, 1.02487, 1.02495, 1.02503,
                       1.02511, 1.02518, 1.02525, 1.0253, 1.02533, 1.02538,
                       1.02541, 1.0254, 1.02539, 1.02537, 1.02535, 1.02531, 
                       1.02526, 1.02519, 1.02512, 1.02501, 1.02486, 1.02468,
                       1.02451, 1.02432, 1.02411, 1.02389, 1.02365, 1.02339,
                       1.02309, 1.02275, 0]
    
            # Berechnung der Gravitationsbeschleunigung
            # Einser- und Zehnerstellen des Counters
            cr_int = cr%100
            # Index des 100er-Intervalls des Counters
            ind = int((cr-cr_int)/100)
            # Auslesen des Wertes des 100er-Intervalls, Interpolation
            mgal[ii] = val_100[ind]+val_int[ind]*cr_int
    else:
        # Fehermeldung fÃ¼r falschen Datentyp
        raise TypeError("Datentyp muss Liste oder Tupel sein.")
    # Ausgabe des Schwerewertes
    return mgal