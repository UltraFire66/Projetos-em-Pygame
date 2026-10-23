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
        #raio de um circulo que passa nas 3 pontas dele
        self.raio = 20
        #orientação referente a função wander, que precisa se manter estatica entre iterações
        self.orientacaoVagar = 0
        



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
            

    def OrientacaoVel(self):
        if(self.velocidade.length() > 2):
            self.alinhar(math.atan2(self.velocidade.x,self.velocidade.y))
        else:
         
            self.rotacao = 0
            self.acelAngular = 0

    def encontraDistanciaParede(self,pos,parede):
        distanciaParede = vector(0,0) 
                    
        if(pos.x < parede.p1 + parede.p3 and pos.x > parede.p1): #se horizontalmente o agente estiver entre as pontas da parede, deve olhar pra sua propria posicao horizontal
            distanciaParede.x = pos.x
        elif(pos.x > parede.p1 + parede.p3): #se estiver mais à direita, deve olhar para a ponta direita 
            distanciaParede.x = parede.p1 + parede.p3
        else:                                                  #se estiver mais à esquerda, deve olhar para a ponta esquerda
            distanciaParede.x = parede.p1


        #valem os mesmos comentarios em relação a altura do agente e a parede
        if(pos.y < parede.p2 + parede.p4 and pos.y > parede.p2): 
            distanciaParede.y = pos.y
        elif(pos.y > parede.p2 + parede.p4): 
            distanciaParede.y = parede.p2 + parede.p4
        else:                                                  
            distanciaParede.y = parede.p2

        distanciaParede =  pos - distanciaParede
        return distanciaParede

    #persegue o mouse (ou um alvo) com velocidade maxima e com orientação baseada na velocidade
    def procurar(self,alvo):

        distancia = alvo.centro - self.centro
        direcao = distancia.normalize()

        if(distancia.length() < alvo.raio):
            self.velocidade = vector(0,0)
            self.aceleracao = vector(0,0)
            self.rotacao = 0
            self.acelAngular = 0
            return 0

        self.aceleracao = self.aceleracaoMax * direcao
        

        
        

 
    #foge do mouse (ou um alvo) com velocidade maxima e com orientação baseada na velocidade
    def fugir(self,alvo):
    
        mouse_x,mouse_y = pygame.mouse.get_pos()

        self.velocidade = self.centro - alvo

        self.limitar_vel()
        self.OrientacaoVel()
        
        
        self.centro += self.velocidade


    #vaga pela tela randomicamente em velocidade constante
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
            self.acelAngular = 0
            self.rotacao = 0
            return 0

        #se alvo não estiver no raio de detecção, usa velocidade máxima
        if(distancia.length() > self.raioDeteccao):
            velalvo = self.velocidadeMax

        else:
            velalvo = self.velocidadeMax * distancia.length()/self.raioDeteccao

        velalvo *= direcao


        self.aceleracao = (velalvo - self.velocidade)/tempo
        self.limitar_acel()

        #alterando a orientação para sempre olhar para o alvo
        #self.alinhar(math.atan2(distancia.x,distancia.y))


    def alinhar(self,alvo):

        # tempo que a rotação tem para se tornar a rotação alvo por meio de aceleração
        tempo = 10

        #determina a distancia em que a rotação começara a diminuir para alcançar a orientação exata
        raioDeLentidao = math.pi/2

        
        ori = alvo - self.orientacao

        #precisamos mapear esse valor da orientação para o intervalo de [-pi,pi]
        if(ori > 0):
            while(ori > math.pi):
                ori -= 2*math.pi
        else:
            while(ori < (-math.pi)):
                ori += 2*math.pi

        

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
        self.limitar_acel_Angular()

        
    
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


    #algoritmo de vagar melhorado para funcionar com novas funções e aceleração
    def vagar2(self):

        random.seed(datetime.now().timestamp())

        #raio e offset do circulo de vagar
        raioVagar = self.raio+10
        offset = self.raio+5

        #cria o circulo de vagar na direção em que o agente está orientado
        orientacaoAgente = vector(math.sin(self.orientacao),math.cos(self.orientacao))

        centroCirculoVagar = self.centro+(orientacaoAgente*offset)

      


        #pygame.draw.circle(self.screen,(255,0,0),centroCirculoVagar,raioVagar,5)


        #guarda a maxima taxa em que a orientação pode mudar em um dado frame
        taxaMudanca = math.pi/4

        #move o alvo dentro do circulo vagar um numero aleatorio de vezes
        self.orientacaoVagar += random.uniform(-1, 1) * taxaMudanca

        orientacaoAlvo = self.orientacao + self.orientacaoVagar

        alvoVagar = centroCirculoVagar + (raioVagar * vector(math.sin(orientacaoAlvo),math.cos(orientacaoAlvo)))

        #a1 = Alvo(self.screen,[alvoVagar],7)
        
        #a1.draw()

        self.aceleracao += self.aceleracaoMax * vector(math.sin(orientacaoAlvo),math.cos(orientacaoAlvo))

    
    def separar(self,agentes):

        #define quando o agente vai começar a receber a repulsão do outro agente
        limite = self.raio+30
        k = 250

        #para cada agente fornecido
        for agente in agentes:
            #descobre a distancia entre eles
            distancia = (agente.centro) - (self.centro)
            distanciaEntre =  distancia.length() - (self.raio + agente.raio)


            if(distanciaEntre < 0):
                distanciaEntre = -distanciaEntre
                direcao = distancia.normalize()
                #dividindo a distancia por dois pois a correção é feita uma vez por cada agente
                self.centro -= (distanciaEntre/2) * direcao 

            if(distanciaEntre < limite  and distanciaEntre != 0):
                #print("entrei aqui, a acel de repulsao eh : ")
                direcao  = distancia.normalize()
                #gera força (aceleração) de repulsão
                repulsao = k/(distancia.length()*distancia.length())
                #print(str(k) + " sobre " + str(distancia.length()*distancia.length()) + " eh " + str(repulsao))
                #print(distancia.length())
                self.aceleracao -= repulsao*direcao


    def evitarColisao(self,agentes):

        menorTempo = 200
        primeiroAgente = None #Começa supondo que não existe um alvo para desviar

        #o objetivo desse for é encontrar com qual agente este vai colidir primeiro
        for agente in agentes:

            #calcula tempo até a colisão
            dp = agente.centro - self.centro

            if(dp.length() > 120): return None

            dv = agente.velocidade - self.velocidade

            if(dv.length() == 0):
                continue
            
            tempoColisao =  - (dp * dv)/(dv.length()*dv.length())

            #checa se vai ter uma colisao
            distancia = dp.length()
            separacaoMinima = distancia - (dv.length() * menorTempo)

            #se essa separação for maior que a soma do raio dos dois, eles não vão colidir, então passa para o próximo agente
            if(separacaoMinima > (self.raio + agente.raio)):
                continue

            #caso o agente vá colidir com este e no menor tempo, guarda as informações dele
            
            if(tempoColisao > 0 and tempoColisao < menorTempo ):
                menorTempo = tempoColisao
                primeiroAgente = agente
                primeiroSeparacaoMinima = separacaoMinima
                primeiroDistancia = distancia
                primeiroDp = dp
                primeiroDv = dv

        if not primeiroAgente: return None

        #se ja esta colidindo, foge de onde está
        if(primeiroSeparacaoMinima <= 0 or primeiroDistancia < (self.raio + primeiroAgente.raio)):
            dp = primeiroDp
            #pygame.draw.circle(self.screen,(255,0,0),dp,5)

        #se não, caucula onde terá colisao e evita ela
        else:
            dp = primeiroDp + (primeiroDv * menorTempo)
            #pygame.draw.circle(self.screen,(255,0,0),self.centro+dp,5)

        #evita o alvo
        dp = dp.normalize()

     
        if(dp == self.velocidade.normalize()):
          self.vagar2()  
        else:
            self.aceleracao = -self.aceleracaoMax*dp
        #self.alinhar(math.atan2(self.velocidade.x,self.velocidade.y))
        

    def evitaParede(self,paredes):

        #distancia que o agente manterá de uma parede
        distanciaMinima = 40

        #distancia do raio que o agente dispara de seu centro para detectar paredes proximas (serve de sensor)
        
        orient = vector(math.sin(self.orientacao),math.cos(self.orientacao))
        raycastCentro = (self.raio+37)*orient
        raycastDireita = (self.raio+37)*orient.rotate(45)
        raycastEsquerda = (self.raio+37)*orient.rotate(-45)
        

        
        draw_arrow(self.screen,self.centro+(self.raio*orient),self.centro + raycastCentro,(0,0,255),(0,0,255))
        draw_arrow(self.screen,self.centro+(self.raio*orient.rotate(45)),self.centro + raycastDireita,(0,0,255),(0,0,255))
        draw_arrow(self.screen,self.centro+(self.raio*orient.rotate(-45)),self.centro + raycastEsquerda,(0,0,255),(0,0,255))

        for parede in paredes:

            #checa se o alvo vai colidir com a parede supondo que ele vá continuar se movendo com velocidade constante
            checaColisaoCentro = self.encontraDistanciaParede(self.centro+(self.raio*orient)+raycastCentro,parede)
            checaColisaoDireita = self.encontraDistanciaParede(self.centro+(self.raio*orient.rotate(45))+raycastDireita,parede)
            checaColisaoEsquerda = self.encontraDistanciaParede(self.centro+(self.raio*orient.rotate(-45))+raycastEsquerda,parede)
            normal = self.encontraDistanciaParede(self.centro,parede)
            if(normal.length()>0):
                normal = normal.normalize()
            
            #agente colidirá com a parede
            if(checaColisaoCentro.length() == 0):

                #checando se está na condição do minimo comum
                if((normal-orient).length()<2):
                    print("entrei")
                    #self.vagar2()
                    self.orientacao += math.pi/20
                    #posicaoAlvo = (self.centro+raycastCentro) + distanciaMinima*normal
                    #posicaoAlvo.y += 10
                else:
                    #criando o alvo e delegando para a função procurar
                    posicaoAlvo = (self.centro+raycastCentro) + distanciaMinima*normal
                    
                    #desenhando a seta da força normal
                    draw_arrow(self.screen,self.centro+(raycastCentro),posicaoAlvo,(144,233,255),(144,233,255))

                    a1 = Alvo(self.screen,[posicaoAlvo],7,(0,255,0))
                    a1.draw()
                    self.procurar(a1)
                
            #agente colidirá com a parede
            elif(checaColisaoEsquerda.length() == 0):
                #criando o alvo e delegando para a função procurar
                posicaoAlvo = (self.centro+raycastDireita) 
                
                #desenhando a seta da força normal
                draw_arrow(self.screen,self.centro+(raycastDireita),posicaoAlvo,(144,233,255),(144,233,255))

                a1 = Alvo(self.screen,[posicaoAlvo],7,(0,255,0))
                a1.draw()
                self.procurar(a1)


            #agente colidirá com a parede
            elif(checaColisaoDireita.length() == 0):
                #criando o alvo e delegando para a função procurar
                posicaoAlvo = (self.centro+raycastEsquerda) 
                
                #desenhando a seta da força normal
                draw_arrow(self.screen,self.centro+(raycastEsquerda),posicaoAlvo,(144,233,255),(144,233,255))

                a1 = Alvo(self.screen,[posicaoAlvo],7,(0,255,0))
                a1.draw()
                self.procurar(a1)

            self.limitar_acel()
         
            
            

                
                
               

            
            
                
            

    def update(self):

        #checando se passa das paredes
        if((self.centro + self.velocidade).x > 0 and (self.centro + self.velocidade).x < 500 ):
            self.centro.x += self.velocidade.x

        if((self.centro + self.velocidade).y > 0 and (self.centro + self.velocidade).y < 500 ):
            self.centro.y += self.velocidade.y
        
        self.orientacao += self.rotacao

        self.velocidade += self.aceleracao
        self.rotacao += self.acelAngular
        self.limitar_vel()     
        self.limitar_rot()
        self.OrientacaoVel()
        
    

    def draw(self):
        direcao = vector(math.sin(self.orientacao),math.cos(self.orientacao))
        post1 = self.centro + direcao*self.tamanho
        post2 = self.centro + direcao.rotate(135) * self.tamanho
        post3 = self.centro + direcao.rotate(225) * self.tamanho
        pygame.draw.polygon(self.screen,(173, 216, 230),[post1,post2,post3])
        #pygame.draw.circle(self.screen,(255, 0, 0),self.centro,self.raio,3)
