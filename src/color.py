import vec

class col(vec.vec3):
    def __init__(self, x, y, z) -> None:
        super().__init__(x, y, z)

    def __str__(self) -> str:
        return f"{255.999*self.x} {255.999*self.y} {255.999*self.z}\n"