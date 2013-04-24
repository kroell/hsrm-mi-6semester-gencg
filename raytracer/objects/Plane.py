'''
Created on 16.04.2013

@author: soerenkroell
'''

from Material import *

class Plane(object):
    def __init__(self, point, normal, color, material):
        self.point = point # point
        self.normal = normal.normalize() # vector
        self.__color = color
        self.material = material if material else Material()

    def __repr__(self):
        return 'Plane(%s,%s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a/b
        else:
            return None

    def normalAt(self, p):
        return self.normal
    
    def color(self):
        return self.__color