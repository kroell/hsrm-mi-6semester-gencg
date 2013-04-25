'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''
     
class Ray(object):
    '''
    Klasse zum Erstellen eines Strahls
    '''
    
    def __init__(self, origin, direction):
        'Konstruktor unter Mitgabe von origin und direction'
        # point
        self.origin = origin 
        # normalisierter vector
        self.direction = direction.normalize() 

    def __repr__(self):
        'Gibt Origin und Direction des Strahls zurueck'
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)
    