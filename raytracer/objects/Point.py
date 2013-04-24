'''
Created on 16.04.2013

@author: soerenkroell
'''

from Vector import *

class Point(object):
    '''
    Operationen mit Punkt im 3D-Raum
    '''
    
    __p = [0,0,0]
    __p_e = [0,0,0]
    
    def __init__(self, point):
        #if len(point) == 2:
        #    __p = [0,0]
        #    self.__p = point
        #elif len(point) == 3:
         #   __p = [0,0,0]
         self.__p = point
    
    def __add__(self, vector):
        'Punkt und Vektor addieren -> neuer Punkt'
        return Point([self.__p[i] + vector.getVector()[i] for i in range(len(vector.getVector()))])
    
    def __sub__(self, point):
        'Punkte subtrahieren -> neuer Vektor'
        #print "punkt sub"
        #print [self.__p[0],self.__p[1],self.__p[2]]
        #print [point.getPoint()[0],point.getPoint()[1],point.getPoint()[2]]
        #print [point.getPoint()[i] for i in range (self.__p)]
        self.__p_e[0] = self.__p[0] - point.getPoint()[0]
        self.__p_e[1] = self.__p[1] - point.getPoint()[1]
        self.__p_e[2] = self.__p[2] - point.getPoint()[2]
        return Vector (self.__p_e)
        #return Vector([self.__p[i] - point.getPoint()[i] for i in range(len(self.__p))])  

    def getPoint(self):
        return Point(self.__p)
    
    def __repr__(self):
        return "Punkt: [{0}, {1}, {2}]".format(*self.__p)
    
    def __getitem__(self,index):
        return self.__p[index]
    
    def __len__(self):
        return len(self.__p)