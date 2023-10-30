import pygame, sys


class Rendertarget:
    def __init__(self) -> None:
        pass

    def push(self, col, x, y):
        pass

    def finish(self):
        pass

class PPM(Rendertarget):
    def __init__(self, resolution, maxColorValue, path) -> None:
        super().__init__()
        self.maxColorVal = maxColorValue
        self.file = ""
        self.file += f"P3\n{resolution[0]} {resolution[1]} \n{self.maxColorVal}\n" # file header
        self.path = path

    def push(self, x, y, col):
        super().push(col, x, y)
        self.file += str(col)
    
    def finish(self):
        super().finish()
        with open(self.path, "w") as fp:
            fp.write(self.file)

class PygameWIN(Rendertarget):
    def __init__(self, resolution, maxColorValue, path) -> None:
        super().__init__()
        pygame.init()
        self.maxColorVal = maxColorValue

        self.winWidth = 1600

        ar = resolution[1]/resolution[0]
        self.winHeight = self.winWidth * ar
        self.root = pygame.display.set_mode([self.winWidth, self.winHeight])
        self.root.fill((87, 80, 89))

        self.renderTexture = pygame.Surface(resolution)
        self.renderTexture.fill((87, 80, 89))

        
        pygame.display.set_caption("Pytracer")

        self.subtarget = PPM(resolution, maxColorValue, path)

    def push(self, x, y, color):
        super().push(color, x, y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.renderTexture.set_at((x, y), (color.r * self.maxColorVal, color.g * self.maxColorVal, color.b * self.maxColorVal))

        self.root.blit(pygame.transform.scale(self.renderTexture, [self.winWidth, self.winHeight]), (0,0))
        pygame.display.flip()

        self.subtarget.push(x, y, color)

    def finish(self):
        super().finish()
        self.subtarget.finish()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            pygame.display.flip()
            