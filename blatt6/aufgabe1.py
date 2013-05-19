'''
Created on 19.05.2013

Berechnung der Linienpunkte aus Blatt 6 Aufgabe 1

@author: soerenkroell
'''


def bresenham(p,q):
    """ draw a line using bresenhams algorithm """
    x0,y0 = p[0],p[1]
    x1,y1 = q[0],q[1] 
    
    a,b = y1 - y0, x0 - x1
    d = 2 * a + b 
    incE = 2 * a
    incNE = 2 * (a+b)
    y = y0
    i = 1
    
    for x in range(x0, x1+1):
        print i, ":" , x, y
        i += 1
        if d <= 0: 
            d += incE
        else:
            d += incNE
            y += 1


if __name__ == "__main__":
    p = [5,5]
    q = [22,12]
    bresenham(p,q)