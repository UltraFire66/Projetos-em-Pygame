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
        

        
        distanciaObs = (self.centro - self.obstaculo.centro)
        direcaoObs = vector(0,0)

        direcaoObs = vector.normalize(distanciaObs)
        distanciaBordaObs = (distanciaObs.length() - self.obstaculo.raio) - self.raio
        #print(distanciaBordaObs)
        fatorDistancia = ((self.raioDeteccao - distanciaBordaObs)/self.raioDeteccao)*1.2 #porcentagem que indica o quão próximo do obstaculo a bolinha está (100% quando encostar)

        if(distanciaBordaObs < self.raioDeteccao): # gera o vetor resultante da atração e repulsao quando o obstaculo entra no raio
            #print(fatorDistancia)
            resultante = ((self.vel.length()*10)*self.direcao) + (self.vel.length()*12)*direcaoObs*fatorDistancia
            direcaoResultante = vector.normalize(resultante)
            if(direcaoObs == -self.direcao):
                #print("teste : %d",self.contador)
                #self.contador += 1 #apenas um teste 
                self.centro += vector(-3,0)
        else:
            direcaoResultante = self.direcao
            

        mouse_x,mouse_y = pygame.mouse.get_pos()

        self.centro  += self.vel.length() * direcaoResultante #oque faz a bolinha se movimentar
        #self.centro = vector(mouse_x,mouse_y)

        

        #desenhando tudo na tela
        pygame.draw.circle(self.screen,(255, 255, 0),self.centro,self.raio)
        pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raioDeteccao,3)
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*self.direcao,(255,0,0),(0,0,255))
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*12)*direcaoObs*fatorDistancia,(0,255,0),(0,255,0))
        draw_arrow(self.screen,self.centro,self.centro+(self.vel.length()*10)*direcaoResultante,(0,255,255),(0,255,255))



       


        
        