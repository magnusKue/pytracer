import pygame, sys, time, datetime, os
from debug import Debug

class Rendertarget:
    def __init__(self) -> None:
        pass

    def push(self, col, x, y):
        pass

    def finish(self, deltaT):
        pass

class PPM(Rendertarget):
    def __init__(self, resolution, maxColorValue, path) -> None:
        super().__init__()
        self.maxColorVal = maxColorValue
        self.file = ""
        self.file += f"P3\n{resolution[0]} {resolution[1]} \n{self.maxColorVal}\n" # file header
        self.path = path
        self.resolution = resolution
        self.startTime = time.time()

        self.renderedPixels = 0
        self.pxRemaining = 0
        self.pxPerSec = 0
        self.est   = 0


    def push(self, x, y, col):
        super().push(col, x, y)
        self.file += str(col)

        # calculate progress information
        self.renderedPixels = (y * self.resolution[0]) +  x
        self.pxRemaining = (self.resolution[0] * self.resolution[1]) - self.renderedPixels
        self.pxPerSec =  round(self.renderedPixels / max(1, time.time() - self.startTime), 2)

        self.est = int(self.pxRemaining / max(self.pxPerSec, 1))

        # display them
        sys.stdout.write("\r{0}".format(f"pixels remaining: {self.pxRemaining}  px/s: {self.pxPerSec}  est: {datetime.timedelta(seconds=self.est)}                                 ")) # extra space to override old text
        sys.stdout.flush()
    
    def finish(self, deltaT):
        super().finish(deltaT)
        with open(self.path, "w") as fp:
            fp.write(self.file+"_"+str(deltaT))
        
        os.system('cls')
        deltaT = time.time() - self.startTime
        print(f"rendered {self.resolution[0]} x {self.resolution[1]} pixels in {str(datetime.timedelta(seconds=deltaT))}s")

class PygameWIN(Rendertarget):
    def __init__(self, resolution, maxColorValue, path) -> None:
        super().__init__()
        pygame.init()
        self.maxColorVal = maxColorValue

        self.winWidth = 1600
    	
        self.resolution = resolution
        ar = self.resolution[1]/self.resolution[0]
        self.winHeight = self.winWidth * ar
        self.root = pygame.display.set_mode([self.winWidth, self.winHeight])
        self.root.fill((87, 80, 89))

        self.renderTexture = pygame.Surface(resolution)
        self.renderTexture.fill((87, 80, 89))

        self.debugger = Debug(
            surface=self.root, 
            pos=pygame.Vector2(self.root.get_width() - 5, 5), 
            alignRight = True
        )
        
        pygame.display.set_caption("Pytracer")

        self.subtarget = PPM(resolution, maxColorValue, path)

        self.startTime = time.time()

    def push(self, x, y, color):
        super().push(color, x, y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.renderTexture.set_at((x, y), (color.r * self.maxColorVal, color.g * self.maxColorVal, color.b * self.maxColorVal))

        self.root.blit(pygame.transform.scale(self.renderTexture, [self.winWidth, self.winHeight]), (0,0))

        self.subtarget.push(x, y, color)

        # get progress information
        renderedPixels = self.subtarget.renderedPixels
        pxRemaining = self.subtarget.pxRemaining
        pxPerSec =  self.subtarget.pxPerSec
        est = self.subtarget.est

        # display them
        self.debugger.debug(f"px/sec: {pxPerSec}")
        self.debugger.debug(f"est: {datetime.timedelta(seconds=est)}")

        self.debugger.renderDebug()
        pygame.display.flip()

    def finish(self, deltaT):
        super().finish(deltaT)
        self.subtarget.finish(deltaT)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            pygame.display.flip()

            