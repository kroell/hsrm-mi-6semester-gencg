'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import Vector


class Color(Vector):
    '''
    Vektor welcher die Farbbereiche repraensentiert. 
    Anstelle von 0 - 255 gehen die Werte von 0 bis 1. 
    0 = Schwarz und 1 = Weiss
    '''
    
    __colorVector = [0,0,0]
    
    def __init__(self, colorVector):
        self.__colorVector = Vector.__init__(self, colorVector)
            
    def colorToRGBTuple(self):
        'wandelt den Color-Vector in ein Tupel mit RGB Werten um und gibt dieses Tupel zurueck'
        return tuple([255 if x > 255 else int(255 * x) for x in self])
    
    def __repr__(self):
        return "Color-Vector: [{0}, {1}, {2}]".format(*self.__colorVector)
