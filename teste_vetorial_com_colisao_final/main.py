import sys,math,pygame
from classes.alvo import Alvo
from classes.bolinha import Bolinha
from classes.triangulo import Triangulo
from classes.parede import Parede
from classes.obstaculo import Obstaculo
from func.draw_arrow import draw_arrow 



pygame.init()

vector = pygame.math.Vector2

clock = pygame.time.Clock()

black = 0,0,0
screen = pygame.display.set_mode((500,500))
framerate = 40

print("startou\n")




a1 = Alvo(screen,[vector(30,30),vector(400,400),(30,400),(400,30)],5)
a2 = Alvo(screen,[vector(470,470),vector(100,100),(30,400),(400,30)],5) 
p1 = Parede(screen,150,70,50,120)
o1 = Obstaculo(screen,(150,200),50)
o2 = Obstaculo(screen,(150,300),50)
o3 = Obstaculo(screen,(250,250),50)
b1 = Bolinha(screen,vector(400,450),10,a1,[],[o3],100)
b2 = Bolinha(screen,vector(25,50),30,a2,[],[o3],130)
t1 = Triangulo(screen, vector(200,250),15,100,8)
t2 = Triangulo(screen, vector(300,250),15,100,5)

iniciar = True #trocar pra false caso queira que o jogo inicie quando clique espaço


while True:

    for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


    if(iniciar):

        #criando um alvo no local onde o mouse esta
        alvoMouse =Alvo(screen,[pygame.mouse.get_pos()],10,(255,0,0)) 
        teclas = pygame.key.get_pressed()

        screen.fill(black)

        #if teclas[pygame.K_SPACE]:
        
        t1.draw()
        t2.draw()
        t1.procurar(alvoMouse)

        #if teclas[pygame.K_SPACE]:
        t2.alinhar(t1.orientacao)
        
                       
        
        
        pygame.display.flip()

    clock.tick(framerate)