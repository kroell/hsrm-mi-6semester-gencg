'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import *
from Color import *

class Light(object):
    '''
    Klasse zum Erstellen einer Lichtquelle
    '''
    
    def __init__(self, position, color ):
        self.__position = position #Point
        self.color = color
    
    def getPosition(self):
        '''
        Gibt die Position der Lichtquelle zurueck
        '''
        return Point(self.__position)
    
    def getColor(self):
        '''
        Gibt den Farbwert der Lichquelle zurueck
        '''
        return Color(self.color)
    