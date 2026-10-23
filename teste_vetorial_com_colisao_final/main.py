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




a1 = Alvo(screen,[vector(30,30),vector(400,400),(30,400),(400,30)],7,(0,255,0))
a2 = Alvo(screen,[vector(470,470),vector(100,100),(30,400),(400,30)],7)
a3 = Alvo(screen,[vector(50,250)],7)
p1 = Parede(screen,150,70,50,120)
p2 = Parede(screen,250,180,50,120)
p3 = Parede(screen,200,180,90,120)
o1 = Obstaculo(screen,(150,200),50)
o2 = Obstaculo(screen,(150,300),50)
o3 = Obstaculo(screen,(250,250),50)
b1 = Bolinha(screen,vector(400,450),10,a1,[],[o3],100)
b2 = Bolinha(screen,vector(25,50),30,a2,[],[o3],130)
t1 = Triangulo(screen, vector(50,50),15,100,4)
t2 = Triangulo(screen, vector(450,470),15,100,4)
t3 = Triangulo(screen, vector(470,470),15,100,4)
t4 = Triangulo(screen, vector(450,250),15,100,3)



iniciar = True #trocar pra false caso queira que o jogo inicie quando clique espaço


while True:

    for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()


    if(iniciar):

        mouse_x,mouse_y = pygame.mouse.get_pos()
        mouse = vector(mouse_x,mouse_y)
        
        agenteMouse = Triangulo(screen,mouse,15,100,3)
        #agenteMouse.orientacao = math.pi/4
        agenteMouse.orientacao = math.pi/2
        #criando um alvo no local onde o mouse esta
        alvoMouse = Alvo(screen,[pygame.mouse.get_pos()],10,(255,0,0)) 
        teclas = pygame.key.get_pressed()

        screen.fill(black)

       

        #t1.chegada(a2)

        #t1.evitaParede([p2])

        #t1.draw()
               
        #t1.update()

        #p2.draw()

        #a2.draw()

        #agenteMouse.draw()
        #agenteMouse.evitaParede([p2])

        t4.chegada(a3)
        t4.evitaParede([p3])

        t4.update()
        t4.draw()
        p3.draw()
        a3.draw()
        
        pygame.display.flip()

    clock.tick(framerate)