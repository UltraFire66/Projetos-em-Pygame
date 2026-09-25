import sys,math,pygame

class Alvo:
    def __init__(self,screen,posicoes):
        self.posicoes = posicoes
        self.screen = screen
        self.centro = posicoes[0]
        self.contador = 0

    def update(self):
        self.contador += 1
        #print(self.contador)
        if(self.contador < len(self.posicoes)):
            self.centro = self.posicoes[self.contador]

    def draw(self):
        pygame.draw.circle(self.screen,(0, 255, 0),self.centro,5)