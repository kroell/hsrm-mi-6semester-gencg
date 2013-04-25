'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import *
import math

class Sphere(object):
    '''
    Klasse zum Erstellen eines Kreises
    '''
    
    def __init__(self, center, radius, material):
        # point
        self.center = center 
        # scalar
        self.radius = radius 
        self.material = material if material else Material()

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = (self.radius * self.radius) - (co.dot(co) - v*v)
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        '''
        Gibt den Normalenvektor an Punkt p zurueck
        '''
        return (p - self.center).normalize()

    def getCenter(self):
        '''
        Gibt den Mittelpunkt der Ebene zurueck
        '''
        return Point(self.center)