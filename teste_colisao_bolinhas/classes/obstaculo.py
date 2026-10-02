import sys,math,pygame
sys.path.append('../func')
from func.draw_arrow import draw_arrow 

vector = pygame.math.Vector2


class Obstaculo:

    def __init__(self,screen,centro,raio):
        self.centro = centro
        self.raio = raio
        self.screen = screen


    def draw(self):
        pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raio)

