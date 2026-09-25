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




        

a1 = Alvo(screen,[vector(30,30),vector(400,400)]) 
p1 = Parede(screen,150,200,50,120)
o1 = Obstaculo(screen,(150,150),50)
b1 = Bolinha(screen,vector(400,400),10,a1,p1,o1)
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
        b1.update()      

        
        a1.draw()
        p1.draw()
        o1.draw()
        pygame.display.flip()

    clock.tick(40)