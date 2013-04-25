'''
Created on 25.04.2013

Generative Computergrafik, Uebungsblatt 2, Aufgabe 1
RAYTRACER
Hochschule RheinMain, Medieninformatik

@author: Soeren Kroell
'''

from raytracer.objects import Vector


class Point(object):
    '''
    Klasse zum Erstellen einers Punkts mit den dazugehoerigen Operationen im 3D-Raum
    '''
    
    __p = [0,0,0]
    __p_e = [0,0,0]
    
    def __init__(self, point):
        self.__p = point
    
    def __add__(self, vector):
        'Punkt und Vektor addieren -> neuer Punkt'
        return Point([self.__p[i] + vector.getVector()[i] for i in range(len(vector.getVector()))])
    
    def __sub__(self, point):
        'Punkte subtrahieren -> neuer Vektor'
        self.__p_e[0] = self.__p[0] - point.getPoint()[0]
        self.__p_e[1] = self.__p[1] - point.getPoint()[1]
        self.__p_e[2] = self.__p[2] - point.getPoint()[2]
        return Vector (self.__p_e)

    def getPoint(self):
        'Gibt den Punkt zurueck'
        return Point(self.__p)
    
    def __repr__(self):
        return "Punkt: [{0}, {1}, {2}]".format(*self.__p)
    
    def __getitem__(self,index):
        return self.__p[index]
    
    def __len__(self):
        return len(self.__p)