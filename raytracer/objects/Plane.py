'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import Material

class Plane(object):
    '''
    Klasse zum Erstellen einer Ebene
    '''
    
    def __init__(self, point, normal, material):
        self.point = point # point
        self.normal = normal.normalize() # vector
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
        '''
        Gibt den normalen Vektor an Punkt p zurueck
        '''
        return self.normal
    