import math

class vec3:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, o):
        return vec3(
            self.x + o.x,
            self.y + o.y,
            self.z + o.z
        )
    
    def __iadd__(self, o):
        return self + o

    def __sub__(self, o):
        return vec3(
            self.x - o.x,
            self.y - o.y,
            self.z - o.z
        )
    
    def __isub__(self, o):
        return self - o
    
    def __mul__(self, o):
        if isinstance(o, self.__class__):
            return vec3(
                self.x * o.x,
                self.y * o.y,
                self.z * o.z
            )
        elif isinstance(o, int) or isinstance(o, float):
            return vec3(
                self.x * o,
                self.y * o,
                self.z * o
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
        return f"({self.x}|{self.y}|{self.z})"

    def lengthSquared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def length(self) -> float:
        return math.sqrt(self.lengthSquared())

def unitize(vec:vec3):
    return vec/vec.length()

def dot(vec1, vec2) -> float:
    return vec1.x * vec2.x + vec1.y * vec2.y + vec1.z * vec2.z

def cross(vec1, vec2) -> vec3:
    return vec3(
        vec1.y * vec2.z - vec1.z * vec2.y,
        vec1.z * vec2.x - vec1.x * vec2.z,
        vec1.x * vec2.y - vec1.y * vec2.x
    )

class point3(vec3):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z)