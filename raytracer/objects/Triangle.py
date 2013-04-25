'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

class Triangle(object):
    '''
    Klasse zum Erstellen eines Dreiecks
    '''

    def __init__(self, a, b, c, color):
        self.a = a # point
        self.b = b # point
        self.c = c # point
        self.__color = color
        self.u = self.b - self.a # direction vector
        self.v = self.c - self.a # direction vector

    def __repr__(self):
        return 'Triangle(%s,%s,%s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0<=r and r<=1 and 0<=s and s<=1 and r+s <=1:
            return wu.dot(self.v) / dvu
        else:
            return None
         
    def normalAt(self, p):
        return self.u.cross(self.v).normalize()
    
    def color(self):
        return self.__color