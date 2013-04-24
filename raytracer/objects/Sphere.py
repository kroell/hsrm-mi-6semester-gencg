'''
Created on 12.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

import math
from Point import *
from Material import *

class Sphere(object):
    def __init__(self, center, radius, color, material):
        # point
        self.center = center 
        # scalar
        self.radius = radius 
        self.__color = color
        self.material = material if material else Material()

    def __repr__(self):
        return 'Sphere(%s,%s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        #print "v", v
        discriminant = (self.radius * self.radius) - (co.dot(co) - v*v)
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalize()
    
    def color(self):
        return self.__color

    def getCenter(self):
        return Point(self.center)