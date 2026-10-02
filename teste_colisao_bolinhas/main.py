import sys,math,pygame
from classes.alvo import Alvo
from classes.bolinha import Bolinha
from classes.parede import Parede
from classes.obstaculo import Obstaculo
from func.draw_arrow import draw_arrow 


pygame.init

vector = pygame.math.Vector2

clock = pygame.time.Clock()

black = 0,0,0
screen = pygame.display.set_mode((500,500))
print("startou\n")




a1 = Alvo(screen,[vector(30,30),vector(400,400),(30,400),(400,30)])
a2 = Alvo(screen,[vector(470,470),vector(100,100),(30,400),(400,30)]) 
p1 = Parede(screen,150,70,50,120)
o1 = Obstaculo(screen,(150,200),50)
o2 = Obstaculo(screen,(150,300),50)
o3 = Obstaculo(screen,(250,250),50)
b1 = Bolinha(screen,vector(400,450),10,a1,[],[o3],100)
b2 = Bolinha(screen,vector(25,50),30,a2,[],[o3],130)
iniciar = True #trocar pra false caso queira que o jogo inicie quando clique espaço


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE: #feito para quando se quer iniciar o jogo clicando espaço
                print("iniciou")
                iniciar = True


    if(iniciar):
        screen.fill(black)
        b1.update([b2])
        b2.update([b1])


        a1.draw()
        a2.draw()
        #p1.draw()
        #o1.draw()
        #o2.draw()
        o3.draw()
        pygame.display.flip()

    clock.tick(40)