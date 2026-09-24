import sys,math,pygame

def draw_arrow(screen,inicio, fim, corSeta,corLinha,widthLinha=4,widthSeta=0):

    if((fim-inicio).length() != 0):
        direcao = (fim - inicio).normalize()
    #else:
        #direcao = vector(0,0)
        post1 = fim
        post2 = fim - direcao.rotate(30) * 10
        post3 = fim - direcao.rotate(-30) * 10
        
        pygame.draw.line(screen,corLinha,inicio,fim-direcao*10,widthLinha)
        pygame.draw.polygon(screen,corSeta,[post1,post2,post3],widthSeta)