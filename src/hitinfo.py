from vec import *
from ray import *
from math import sqrt

## A BASIC STRUCTURE TO HOLD INFORMATION ABOUT A COLLISION

class HitInfo:
    def __init__(self, didHit, t, hitPoint, hitNormal, hitMaterial, ray=None):
        self.didHit = didHit
        self.t = t
        self.hitPoint = hitPoint 
        self.hitNormal = hitNormal
        self.hitMaterial = hitMaterial
        self.ray = ray
    
    @staticmethod
    def zero():
        return HitInfo(False, None, None, None, None)