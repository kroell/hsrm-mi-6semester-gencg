'''
Created on 12.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

# Klasse zum Erstellen eines Strahlobjekts      
class Ray(object):
    
    def __init__(self, origin, direction):
        'Konstruktor unter Mitgabe von origin und direction'
        # point
        self.origin = origin 
        # vector
        self.direction = direction.normalize() 
        #self.direction = direction # vector

    def __repr__(self):
        'Gibt Origin und Direction des Strahls zurueck'
        return 'Ray(%s,%s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)
    