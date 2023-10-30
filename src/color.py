import math

class col:
    def __init__(self, r, g, b) -> None:
        self.r = r
        self.g = g
        self.b = b
    
    def __add__(self, o):
        return col(
            self.r + o.r,
            self.g + o.g,
            self.b + o.b
        )
    
    def __iadd__(self, o):
        return self + o

    def __sub__(self, o):
        return col(
            self.r + o.r,
            self.g + o.g,
            self.b + o.b
        )
    
    def __isub__(self, o):
        return self - o
    
    def __mul__(self, o):
        if isinstance(o, self.__class__):
            return col(
                self.r * o.r,
                self.g * o.g,
                self.b * o.b
            )
        elif isinstance(o, int) or isinstance(o, float):
            return col(
                self.r * o,
                self.g * o,
                self.b * o
            )
        else:
            raise TypeError("vector multiplication only supports other vectors, integers or floats") 
    
    __rmul__ = __mul__

    def __imul__(self, o):
        return self * o

    def __truediv__(self, o:int | float):
        return (1/o) * self
    
    def __itruediv__(self, o):
        return self / o
    
    def __str__(self) -> str:
        return f"{255.999*self.r} {255.999*self.g} {255.999*self.b}\n"
    
    def componentToGamma(self, comp):
        return math.sqrt(comp)

    def colToGammaSpace(self):
        return col(
            self.componentToGamma(self.r),
            self.componentToGamma(self.g),
            self.componentToGamma(self.b)
        )


class Material:
    def __init__(self, color:col):
        self.color = color