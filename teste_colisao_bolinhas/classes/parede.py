import sys,math,pygame


class Parede:

    def __init__(self,screen,p1,p2,p3,p4):
            self.p1=p1
            self.p2=p2
            self.p3=p3
            self.p4=p4
            self.screen = screen
            self.rect = pygame.Rect(p1,p2,p3,p4)

    def draw(self):
        pygame.draw.rect(self.screen,(255,0,0),self.rect)