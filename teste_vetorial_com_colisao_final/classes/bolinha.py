import sys,math,pygame
sys.path.append('../func')
from func.draw_arrow import draw_arrow 

vector = pygame.math.Vector2

class Bolinha:


    def __init__(self,screen,centro,raio,alvo,paredes,obstaculos,raiodeteccao):
        self.centro = centro
        self.raio = raio
        self.alvo = alvo
        self.screen = screen
        self.paredes = paredes
        self.obstaculos = obstaculos
        self.contador = 0 #apenas dedicado a testes e debug
        self.acelAtracao = 0.05
        self.acelRepulsao = 0.05
        self.raioDeteccao = raiodeteccao
        self.escalar_velocidade = 4
        self.vel = vector(0,0)

    def update(self,agentes):

       
        #pegando a altura e largura da tela
        Screenwidth, Screenheight = pygame.display.get_surface().get_size()


        distancia = (self.alvo.centro - self.centro)
        #print(distancia.length())

        if(distancia.length() > 0):
            self.direcao = distancia.normalize()
        else:
            self.direcao = vector(0,0)
        

        #codigo referente a diminuir  a velocidade da bolinha quando estiver se aproximando do alvo
        
        #if(distancia.length() < self.raioDeteccao): ##se alvo estiver dentro do circulo vermelho, diminui velocidade gradualmente até parar no alvo
           #self.vel = vector( self.escalar_velocidade * (distancia/self.raioDeteccao), self.escalar_velocidade * (distancia/self.raioDeteccao))
           #if(self.vel.length() < 0.05): #previne de diminuir infinitamente
               #self.vel = vector(0,0)
               #self.alvo.update()
        #else:   #se nao estiver dentro do circulo vermelho, agente é atraído pelo alvo
           # self.vel = self.vel + self.acel     




        #Início do codigo referente a quicar quando atingir outro agente

        for agente in agentes:
            distanciaAG = self.centro - agente.centro
            direcaoAG = vector(0,0)
            if(distanciaAG.length() > 0):
                direcaoAG = vector.normalize(distanciaAG)
            
            #caso colidam, inverte a velocidade dos dois (colisão perfeita elástica)
            if(distanciaAG.length() <= (self.raio+agente.raio)):
                veloc = self.vel.length() + agente.vel.length() #guardando a soma das velocidades para dividir no momento da colisão
                self.vel = (veloc * (agente.raio/(agente.raio+self.raio)))*direcaoAG #não conserva energia cinética, só distribui a velocidade final de forma inversamente proporcional à massa(apenas para testes)
                agente.vel = (veloc * (self.raio/(agente.raio+self.raio)))*(-direcaoAG)
                
                



        #Início do codigo referente a desviar de obstaculo

        direcaoObs = vector(0,0)

        fatorDistanciaAlvo =  distancia.length() / math.sqrt(pow(Screenwidth,2) + pow(Screenheight,2))

        resultante = ((self.acelAtracao * fatorDistanciaAlvo)*self.direcao)  #força de atração para o alvo
        
        
        for obstaculo in self.obstaculos:
            distanciaObs = (self.centro - obstaculo.centro)
            direcaoObs = vector.normalize(distanciaObs)
            distanciaBordaObs = (distanciaObs.length() - obstaculo.raio) - self.raio
            # print(distanciaBordaObs)
            fatorDistanciaObstaculo = ((self.raioDeteccao - distanciaBordaObs)/self.raioDeteccao) #porcentagem que indica o quão próximo do obstaculo a bolinha está (100% quando encostar)

            #conferindo se a bolinha está colidindo com o obstaculo e não deixando ela avançar
            if(distanciaBordaObs <= 0):
                self.centro = self.centro + distanciaObs - (obstaculo.raio*direcaoObs)

            
            if(distanciaBordaObs < self.raioDeteccao): # gera o vetor resultante da atração e repulsao quando o obstaculo entra no raio
                #print(fatorDistanciaObstaculo)
                resultante += self.acelRepulsao*direcaoObs*fatorDistanciaObstaculo
                if(direcaoObs == -self.direcao):
                    print("teste : %d",self.contador)
                    self.contador += 1 #apenas um teste 
                    self.centro += vector(-3,0)
            

        #Inicio do código referente a desviar de parede
        
        for parede in self.paredes:
            distanciaParede = vector(0,0) 

            if(self.centro.x < parede.p1 + parede.p3 and self.centro.x > parede.p1): #se horizontalmente a bolinha estiver entre as pontas da parede, deve olhar pra sua propria posicao horizontal
                distanciaParede.x = self.centro.x
            elif(self.centro.x > parede.p1 + parede.p3): #se estiver mais à direita, deve olhar para a ponta direita 
                distanciaParede.x = parede.p1 + parede.p3
            else:                                                  #se estiver mais à esquerda, deve olhar para a ponta esquerda
                distanciaParede.x = parede.p1


            #valem os mesmos comentarios em relação a altura da bolinha e a parede
            if(self.centro.y < parede.p2 + parede.p4 and self.centro.y > parede.p2): 
                distanciaParede.y = self.centro.y
            elif(self.centro.y > parede.p2 + parede.p4): 
                distanciaParede.y = parede.p2 + parede.p4
            else:                                                  
                distanciaParede.y = parede.p2

            distanciaParede =  self.centro - distanciaParede
            direcaoParede = vector.normalize(distanciaParede)
            fatorDistanciaParede = ((self.raioDeteccao - (distanciaParede.length()-self.raio))/self.raioDeteccao)
            
            if(distanciaParede.length() < self.raioDeteccao):
                resultante += + (self.vel.length()*10)*direcaoParede*fatorDistanciaParede

        if(resultante.length() != 0):
            direcaoResultante = vector.normalize(resultante)
        else:
            direcaoResultante = vector(0,0)


        #codigo para fazer a bolinha quicar nas bordas
        if(self.centro.x > Screenwidth or self.centro.x < 0):
            self.vel.x = -self.vel.x
            resultante.x = - resultante.x
                
        if(self.centro.y > Screenheight or self.centro.y < 0):
            self.vel.y = -self.vel.y
            resultante.y = - resultante.y


        mouse_x,mouse_y = pygame.mouse.get_pos()

        if(distancia.length() < self.raioDeteccao): #se alvo estiver dentro do circulo vermelho, diminui velocidade gradualmente até parar no alvo
            self.vel = vector( self.escalar_velocidade * (distancia/self.raioDeteccao), self.escalar_velocidade * (distancia/self.raioDeteccao))
            if(self.vel.length() < 0.05): #previne de diminuir infinitamente
                self.vel = vector(0,0)
                self.alvo.update()
        else:   #se nao estiver dentro do circulo vermelho, agente é atraído pelo alvo
           self.vel += resultante    

        self.centro  += self.vel #oque faz a bolinha se movimentar

        #self.centro = vector(mouse_x,mouse_y)
        
        #limita a velocidade total da bolinha
        if(self.vel.length()>3):
            self.vel = vector.normalize(self.vel) * 3
        

        #desenhando tudo na tela
        pygame.draw.circle(self.screen,(255, 255, 0),self.centro,self.raio)
        pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raioDeteccao,3)
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*self.direcao,(255,0,0),(0,0,255))
        #draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*12)*direcaoObs*fatorDistanciaObstaculo,(0,255,0),(0,255,0))
        #draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*12)*direcaoParede*fatorDistanciaParede,(0,255,0),(0,255,0))
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*direcaoResultante,(0,255,255),(0,255,255))



       


        
        