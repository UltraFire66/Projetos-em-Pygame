import sys,math,pygame
sys.path.append('../func')
from func.draw_arrow import draw_arrow 

vector = pygame.math.Vector2

class Bolinha:

    centro = vector(0,0)

    vel = vector(5,5)
    acel = vector(0,0)
    atrito = vector(1,1)
    raioDeteccao = 100
    escalar_velocidade = 4

    def __init__(self,screen,centro,raio,alvo,parede,obstaculo):
        self.centro = centro
        self.raio = raio
        self.alvo = alvo
        self.screen = screen
        self.parede = parede
        self.obstaculo = obstaculo
        self.contador = 0 #apenas dedicado a testes e debug

    def update(self):


        distancia = (self.alvo.centro - self.centro)
        #print(distancia.length())

        if(distancia.length() > 0):
            self.direcao = distancia.normalize()
        else:
            self.direcao = vector(0,0)

               
        
        if(distancia.length() < self.raioDeteccao): ##se alvo estiver dentro do circulo vermelho, diminui velocidade gradualmente até parar no alvo
           self.vel = vector( self.escalar_velocidade * (distancia/self.raioDeteccao), self.escalar_velocidade * (distancia/self.raioDeteccao))
           if(self.vel.length() < 0.05): #previne de diminuir infinitamente
               self.vel = vector(0,0)
               self.alvo.update()
        else:   #se nao estiver dentro do circulo vermelho, bolinha tem velocidade constante
           self.vel = vector(self.escalar_velocidade,self.escalar_velocidade)       
        

        #Início do codigo referente a desviar de obstaculo

        distanciaObs = (self.centro - self.obstaculo.centro)
        direcaoObs = vector(0,0)

        resultante = ((self.vel.length()*10)*self.direcao)
        


        direcaoObs = vector.normalize(distanciaObs)
        distanciaBordaObs = (distanciaObs.length() - self.obstaculo.raio) - self.raio
       # print(distanciaBordaObs)
        fatorDistanciaObstaculo = ((self.raioDeteccao - distanciaBordaObs)/self.raioDeteccao) #porcentagem que indica o quão próximo do obstaculo a bolinha está (100% quando encostar)

        if(distanciaBordaObs < self.raioDeteccao): # gera o vetor resultante da atração e repulsao quando o obstaculo entra no raio
            #print(fatorDistanciaObstaculo)
            resultante += (self.vel.length()*10)*direcaoObs*fatorDistanciaObstaculo
            if(direcaoObs == -self.direcao):
                print("teste : %d",self.contador)
                self.contador += 1 #apenas um teste 
                self.centro += vector(-3,0)
        

        #Inicio do código referente a desviar de parede

       

        distanciaParede = vector(0,0) 
        
        if(self.centro.x < self.parede.p1 + self.parede.p3 and self.centro.x > self.parede.p1): #se horizontalmente a bolinha estiver entre as pontas da parede, deve olhar pra sua propria posicao horizontal
            distanciaParede.x = self.centro.x
        elif(self.centro.x > self.parede.p1 + self.parede.p3): #se estiver mais à direita, deve olhar para a ponta direita 
            distanciaParede.x = self.parede.p1 + self.parede.p3
        else:                                                  #se estiver mais à esquerda, deve olhar para a ponta esquerda
            distanciaParede.x = self.parede.p1


        #valem os mesmos comentarios em relação a altura da bolinha e a parede
        if(self.centro.y < self.parede.p2 + self.parede.p4 and self.centro.y > self.parede.p2): 
            distanciaParede.y = self.centro.y
        elif(self.centro.y > self.parede.p2 + self.parede.p4): 
            distanciaParede.y = self.parede.p2 + self.parede.p4
        else:                                                  
            distanciaParede.y = self.parede.p2

        distanciaParede =  self.centro - distanciaParede
        direcaoParede = vector.normalize(distanciaParede)
        fatorDistanciaParede = ((self.raioDeteccao - (distanciaParede.length()-self.raio))/self.raioDeteccao)
        
        if(distanciaParede.length() < self.raioDeteccao):
            resultante += + (self.vel.length()*10)*direcaoParede*fatorDistanciaParede
            
        else:
            direcaoResultante = self.direcao

        direcaoResultante = vector.normalize(resultante)
        print(distanciaParede.length() - self.raio)


        mouse_x,mouse_y = pygame.mouse.get_pos()

        self.centro  += self.vel.length() * direcaoResultante #oque faz a bolinha se movimentar
        #self.centro = vector(mouse_x,mouse_y)

        

        #desenhando tudo na tela
        pygame.draw.circle(self.screen,(255, 255, 0),self.centro,self.raio)
        pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raioDeteccao,3)
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*self.direcao,(255,0,0),(0,0,255))
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*12)*direcaoObs*fatorDistanciaObstaculo,(0,255,0),(0,255,0))
        #draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*12)*direcaoParede*fatorDistanciaParede,(0,255,0),(0,255,0))
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*direcaoResultante,(0,255,255),(0,255,255))



       


        
        