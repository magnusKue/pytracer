from vec import *
from ray import *
from math import sqrt


class HitInfo:
    def __init__(self, didHit, t, hitPoint, hitNormal, hitMaterial):
        self.didHit = didHit
        self.t = t
        self.hitPoint = hitPoint 
        self.hitNormal = hitNormal
        self.hitMaterial = hitMaterial
    
    @staticmethod
    def zero():
        return HitInfo(False, None, None, None, None)