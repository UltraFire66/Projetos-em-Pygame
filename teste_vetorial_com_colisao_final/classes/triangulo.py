import sys,math,pygame,random
from datetime import datetime
sys.path.append('../func')
from func.draw_arrow import draw_arrow
from classes.alvo import Alvo

vector = pygame.math.Vector2

class Triangulo:

    def __init__(self,screen,centro,tamanho,raioDeteccao,velocidadeMax):
        self.screen = screen
        self.centro = centro
        self.orientacao = math.pi #começa com o triangulo apontado para cima
        self.velocidade = vector(0,0)
        self.rotacao = 0
        self.aceleracao = vector(0,0)
        self.aceleracaoMax = 2
        self.acelAngular = 0
        self.acelAngularMax = math.pi/20
        self.tamanho = tamanho
        self.raioDeteccao = raioDeteccao
        self.velocidadeMax = velocidadeMax
        self.rotacaoMax = math.pi/10



    def limitar_vel(self):
        if(self.velocidade.length() > self.velocidadeMax):
            self.velocidade = self.velocidade.normalize()
            self.velocidade *= self.velocidadeMax


    def limitar_acel(self):
        if(self.aceleracao.length() > self.aceleracaoMax):
            self.aceleracao = self.aceleracao.normalize()
            self.aceleracao *= self.aceleracaoMax

    def limitar_rot(self):
        if(abs(self.rotacao) > self.rotacaoMax):
            if(self.rotacao > 0):
                self.rotacao = self.rotacaoMax
            else:
                self.rotacao = -self.rotacaoMax

    def limitar_acel_Angular(self):
            if(abs(self.acelAngular) > self.acelAngularMax):
                if(self.acelAngular > 0):
                    self.acelAngular = self.acelAngularMax
                else:
                    self.acelAngular = -self.acelAngularMax
            

    def novaOrientação(self):
        if(self.velocidade.length() > 0):
            self.orientacao = math.atan2(self.velocidade.x,self.velocidade.y)


    #persegue o mouse (ou um alvo) com velocidade maxima e com orientação baseada na velocidade
    def procurar(self,alvo):

        distancia = alvo.centro - self.centro
        direcao = distancia.normalize()

        if(distancia.length() < alvo.raio):
            return 0

        self.aceleracao = self.aceleracaoMax * direcao
        

        #alterando a orientação com base na velocidade
        self.novaOrientação()

        self.velocidade = (0,0)

        #atualizando posicao e velocidade
        self.centro += self.velocidade
        self.velocidade += self.aceleracao
        self.limitar_vel()

 
    #foge do mouse (ou um alvo) com velocidade maxima e com orientação baseada na velocidade
    def fugir(self,alvo):
    
        mouse_x,mouse_y = pygame.mouse.get_pos()

        self.velocidade = self.centro - alvo

        self.limitar_vel()
        self.novaOrientação()
        
        
        self.centro += self.velocidade


    #vaga pela tela randomicamente 
    def vagar(self):
        random.seed(datetime.now().timestamp())
        #anda com velocidade máxima na posição em que está orientado
        direcao = vector(math.sin(self.orientacao),math.cos(self.orientacao))
        self.velocidade = self.velocidadeMax * direcao

        #olha para uma nova posição randomicamente
        self.rotacao = random.uniform(-1, 1) * self.rotacaoMax
        
        #atualiza posicao e orientação
        if((self.centro+self.velocidade).x < 500 and (self.centro+self.velocidade).x > 0):
            self.centro.x += self.velocidade.x

        if((self.centro+self.velocidade).y < 500 and (self.centro+self.velocidade).y > 0):
            self.centro.y += self.velocidade.y
        
        
        self.orientacao += self.rotacao


    #chega a um dado alvo, desacelerando e parando ao chegar perto dele
    def chegada(self,alvo):

        # tempo que a velocidade tem para se tornar a velocidade alvo por meio de desaceleração
        tempo = 0.2

        # descobre a direção e distância para o alvo
        distancia = alvo.centro - self.centro
        direcao = distancia.normalize()
        

        #se ja estiver no alvo, não faz nada
        if(distancia.length() < alvo.raio):
            self.velocidade = vector(0,0)
            self.aceleracao = vector(0,0)
            return 0

        #se alvo não estiver no raio de detecção, usa velocidade máxima
        if(distancia.length() > self.raioDeteccao):
            velalvo = self.velocidadeMax

        else:
            velalvo = self.velocidadeMax * distancia.length()/self.raioDeteccao

        velalvo *= direcao


        self.aceleracao = (velalvo - self.velocidade)/tempo


        #alterando a orientação com base na velocidade
        self.novaOrientação()

        self.limitar_vel()
        self.limitar_acel()

        #atualizando posicao e velocidade
        self.centro += self.velocidade
        self.velocidade += self.aceleracao

    def alinhar(self,alvo):

        # tempo que a rotação tem para se tornar a rotação alvo por meio de aceleração
        tempo = 0.2

        #determina a distancia em que a rotação começara a diminuir para alcançar a orientação exata
        raioDeLentidao = math.pi/4

        
        ori = alvo - self.orientacao

        #precisamos mapear esse valor da orientação para o intervalo de [-pi,pi]
        if(ori > 0):
            while(ori > math.pi):
                ori -= 2*math.pi
        else:
            while(ori < (-math.pi)):
                ori += 2*math.pi

        print(ori)

        #se os dois já estiverem alinhados, não faz nada
        if(abs(ori)< math.pi/20):
            self.rotacao = 0
            self.acelAngular = 0
            return 0

        #se não está no raio de lentidão, usa rotação máxima
        if(abs(ori) > raioDeLentidao):
            if(ori > 0):
                rotacaoAlvo = self.rotacaoMax
            else:
                rotacaoAlvo = -self.rotacaoMax


        #se está, escalona uma rotação
        else:
            rotacaoAlvo = self.rotacaoMax * ori/raioDeLentidao

        self.acelAngular = (rotacaoAlvo - self.rotacao)/tempo

        self.limitar_rot()
        self.limitar_acel_Angular()

        self.orientacao += self.rotacao
        self.rotacao += self.acelAngular

        
    
    def perseguir(self,alvo):

        #tempo máximo de predição, se não conseguir alcançar o alvo dentro desse tempo, usa aceleração máxima
        predicaoMax = 0.5    

        distancia = alvo.centro - self.centro

        if(self.velocidade.length() < (distancia.length()/predicaoMax)):
            predicao = predicaoMax
        else:
            predicao = (distancia.length()/self.velocidade.length())

        localAlvo = alvo.centro + (alvo.velocidade * predicao)

        alvoProcurar = Alvo(self.screen,[localAlvo],5,(0,0,0))

        self.procurar(alvoProcurar)


    def draw(self):
        direcao = vector(math.sin(self.orientacao),math.cos(self.orientacao))
        post1 = self.centro + direcao*self.tamanho
        post2 = self.centro + direcao.rotate(135) * self.tamanho
        post3 = self.centro + direcao.rotate(225) * self.tamanho
        pygame.draw.polygon(self.screen,(173, 216, 230),[post1,post2,post3])
        #pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raioDeteccao,3)
