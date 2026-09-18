import sys,math,pygame

pygame.init

vector = pygame.math.Vector2

clock = pygame.time.Clock()

black = 0,0,0
screen = pygame.display.set_mode((500,500))
print("startou\n")




def draw_arrow(inicio, fim, corSeta,corLinha,widthLinha=4,widthSeta=0):

    if((fim-inicio).length() != 0):
        direcao = (fim - inicio).normalize()
    #else:
        #direcao = vector(0,0)
        post1 = fim
        post2 = fim - direcao.rotate(30) * 10
        post3 = fim - direcao.rotate(-30) * 10
        
        pygame.draw.line(screen,corLinha,inicio,fim-direcao*10,widthLinha)
        pygame.draw.polygon(screen,corSeta,[post1,post2,post3],widthSeta)

class alvo:
    def __init__(self,centro):
        self.centro = centro

    def update(self):
        pygame.draw.circle(screen,(0, 255, 0),self.centro,5)
        

class parede:

    p1 = 0
    p2 = 0
    p3 = 0
    p4 = 0
    

    def __init__(self,p1,p2,p3,p4):
            self.p1=p1
            self.p2=p2
            self.p3=p3
            self.p4=p4
            self.rect = pygame.Rect(p1,p2,p3,p4)

    def update(self):
        pygame.draw.rect(screen,(255,0,0),self.rect)
 


class bolinha:

    centro = vector(0,0)

    vel = vector(5,5)
    acel = vector(0,0)
    atrito = vector(1,1)

    escalar_velocidade = 2

    def __init__(self,centro,alvo,parede):
        self.centro = centro
        self.alvo = alvo
        self.parede = parede

    def update(self):


        distancia = (self.alvo - self.centro)
        print(distancia.length())

        if(distancia.length() > 0):
            direcao = distancia.normalize()
        else:
            direcao = vector(0,0)

               
        
        if(distancia.length() < 100): ##se alvo estiver dentro do circulo vermelho, diminui velocidade gradualmente até parar no alvo
           self.vel = vector( self.escalar_velocidade * (distancia/100), self.escalar_velocidade * (distancia/100))
           if(self.vel.length() < 0.05): #previne de diminuir infinitamente
               self.vel = vector(0,0)
        else:   #se nao estiver dentro do circulo vermelho, bolinha tem velocidade constante
           self.vel = vector(self.escalar_velocidade,self.escalar_velocidade)       
        
        
        
        
        #Inicio do codigo referente à afastar de paredes  

        distanciaParede = vector(0,0) 

        if(self.centro.x < self.parede.p1 + self.parede.p3 and self.centro.x > self.parede.p1): #Se horizontalmente a bolinha estiver entre as pontas da parede, deve olhar pra sua propria posicao horizontal
            distanciaParede.x = self.centro.x
        elif(self.centro.x > self.parede.p1 + self.parede.p3): #Se estiver mais à direita, deve olhar para a ponta direita 
            distanciaParede.x = self.parede.p1 + self.parede.p3
        else:                                                  #Se estiver mais à esquerda, deve olhar para a ponta esquerda
            distanciaParede.x = self.parede.p1


        #Valem os mesmos comentarios em relação a altura da bolinha e a parede
        if(self.centro.y < self.parede.p2 + self.parede.p4 and self.centro.y > self.parede.p2): 
            distanciaParede.y = self.centro.y
        elif(self.centro.y > self.parede.p2 + self.parede.p4): 
            distanciaParede.y = self.parede.p2 + self.parede.p4
        else:                                                  
            distanciaParede.y = self.parede.p2

        
        #Agora encontrando a distancia da bolinha para a extremidade mais proxima da parede
        distanciaParede = distanciaParede - self.centro
        

        if(distanciaParede.length() < 100):
            if(distanciaParede.x > self.escalar_velocidade): #evita divisao por zero
                self.vel.x -= (self.escalar_velocidade*1.5)/(distanciaParede.x*100)
            if(distanciaParede.y > self.escalar_velocidade):
                self.vel.y -= (self.escalar_velocidade*1.5)/(distanciaParede.y*100)

            direcao = (distancia-distanciaParede).normalize()
     
        self.centro += self.vel.length() * direcao #oque faz a bolinha se movimentar

        pygame.draw.circle(screen,(255, 255, 0),self.centro,10)
        pygame.draw.circle(screen,(255, 0, 0),self.centro,100,3)
        draw_arrow(self.centro,self.centro+(self.vel.length()*10)*direcao,(255,0,0),(0,0,255))
        


       

a1 = alvo(vector(30,30)) 
p1 = parede(150,150,50,120)
b1 = bolinha(vector(400,400),a1.centro,p1) 
iniciar = False #trocar pra false caso queira que o jogo inicie quando clique espaço


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE: #feito para quando se quer iniciar o jogo clicando espaço
                print("iniciou")
                iniciar = True


    if(iniciar):
        screen.fill(black)
        bolinha.update(b1)
        alvo.update(a1)
        parede.update(p1)
        
        pygame.display.flip()

    clock.tick(40)