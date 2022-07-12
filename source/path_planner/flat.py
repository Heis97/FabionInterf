import abc
from polygon import Point3D


class Flat3D(object):
    abc:Point3D
    d:float
    def __init__(self,_abc:Point3D,_d:Point3D) -> None:
        abc = _abc
        d = _d

    def compFlat(p1:Point3D,p2:Point3D,p3:Point3D):
        v1 = p2 - p1
        v2 = p3 - p1
        abc = (v1*v2).normalyse()
        d = -abc**p1
        return Flat3D(abc,d)