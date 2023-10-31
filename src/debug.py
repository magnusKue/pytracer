import pygame

class Debug:
	def __init__(self, surface=pygame.display.get_surface(), pos=pygame.Vector2(50,50), alignRight=False):
		self.pos = pos
		self.surface = surface
		self.content = []
		self.font = pygame.font.SysFont(pygame.font.get_fonts()[0], 20)
		self.alignRight = True

	def debug(self, info):
		self.content.append(str(info))

	def renderDebug(self):
		for index, item in enumerate(self.content):
			if type(item) == pygame.Vector2:
				item = str("(" + item.x + " : " + item.y + ")")
			itemText = self.font.render(item, 2, (200,200,200))
			pygame.draw.rect(self.surface, (0,0,0), pygame.Rect((self.pos.x- self.alignRight * itemText.get_width(), self.pos.y + index*itemText.get_height()), (itemText.get_width(), itemText.get_height())))
			self.surface.blit(itemText, (self.pos.x - self.alignRight * itemText.get_width(), self.pos.y + index*itemText.get_height()))
		self.content = []