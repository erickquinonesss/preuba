import pygame
from ajustes import *

class Scoref:
    def __init__(self, screen):
        self.screen = screen
        self.scoref_mostrados = False

    def mostrar_scoref(self):
        scoref = pygame.image.load('imagenes/scoref.jpg')
        self.screen.blit(scoref, (0, 0))
        pygame.display.flip()
        self.scoref_mostrados = True
