'''
Created on 12.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: soerenkroell
'''

import math

class Vector(object):
    '''
    Operationen mit Punkt im 3D-Raum
    '''
    
    __v = [0,0,0]
    __v_e = [0,0,0]
    
    def __init__ (self, vector):
        self.__v = vector
        #self.x = vector[0]
        #self.y = vector[1]
        #self.z = vector[2]

    def __add__(self, vector):
        'Zwei Vektoren addieren'
        #print "vektor add"
        return Vector([self.__v[i] + vector.getVector()[i] for i in range(len(self.__v))])

    def __sub__(self, vector):
        'Zwei Vektoren subtrahieren'
        print "vektor sub"
        return Vector([self.__v[i] - vector.getVector()[i] for i in range(len(self.__v))])
    
    def __mul__(self, scalar):
        'Skalarprodukt'
        self.scale(scalar) 
    
    def __div__(self, scalar):
        'Division Vektor durch Skalar'
        return Vector([self.__v[i] / scalar for i in range (len(self.__v))])
    
    def dot(self, vector):
        'Skalarprodukt -> passt'
        #print "vektor dot"
        return float(sum(self.__v[i] * vector.getVector()[i] for i in range (len(self.__v))))
    
    def cross(self, vector):
        'Kreuzprodukt zweier Vektoren im 3-dimensionalen Raum'
        self.__v_e[0] = self.__v[1] * vector.getVector()[2] - self.__v[2] * vector.getVector()[1]
        self.__v_e[1] = self.__v[2] * vector.getVector()[0] - self.__v[0] * vector.getVector()[2]
        self.__v_e[2] = self.__v[0] * vector.getVector()[1] - self.__v[1] * vector.getVector()[0]
        return Vector(self.__v_e)
        
    def scale(self, scalar):
        'Skalarmultiplikation. Skalar mit Vektor --> denke es passt'
        #print "vektor scale"
        return Vector([scalar * self.__v[i] for i in range (len(self.__v))])
        
    def norm(self):
        'Norm des Vektors berechnen -> passt'
        return math.sqrt(sum(math.pow(self.__v[i],2)for i in range(len(self.__v))))
    
    def normalize(self):
        'Vektor normalisieren. Jede Komponente wird durch die Norm des Vektors geteilt'
        normVector = self.norm()
        return Vector([self.__v[i]/ normVector for i in range(len(self.__v))])
    
    def getVector(self):
        'Gibt Vektor zurueck'
        return Vector(self.__v)
    
    
    def __repr__(self):
        return "Vector: [{0}, {1}, {2}]".format(*self.__v)
    
    def __len__(self):
        return len(self.__v)
    
    def __getitem__(self,index):
        return self.__v[index]
    