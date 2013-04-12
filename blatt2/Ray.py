'''
Created on 12.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''


# Klasse zum Erstellen eines Strahlobjekts
class Ray(object):
    
    # Konstruktor
    def __init__(self, origin, direction):
        # Ausgangspunkt
        self.origin = origin
        # normalisierter Vektor
        self.direction = direction.normalized()
    
    def __repr__(self):
        pass
    
    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)
    
    # jede Komponente durch die Laenge des Vektors
    # normalisieren
    def normalized(self):
        pass
    
    # skalieren
    def scale(self,t):
        pass