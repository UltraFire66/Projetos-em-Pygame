import sys,math,pygame

class Alvo:
    def __init__(self,screen,posicoes,raio,cor=(0, 255, 0)):
        self.posicoes = posicoes
        self.screen = screen
        self.centro = posicoes[0]
        self.contador = 0
        self.raio = raio
        self.cor = cor

    def update(self):
        self.contador += 1
        #print(self.contador)
        if(self.contador < len(self.posicoes)):
            self.centro = self.posicoes[self.contador]

    def draw(self):
        pygame.draw.circle(self.screen,self.cor,self.centro,self.raio)