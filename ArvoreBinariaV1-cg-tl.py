"""
colocar essa descrição irada maneira crazy pra apresentação:


Desafio da Árvore Binária de Busca (BST). O usuário deve posicionar os nós 
soltos em suas posições corretas respeitando a regra da BST (menores à esquerda, 
maiores à direita).

Controles:
- Teclas 1 a 5: Selecionam qual nó você quer controlar.
- Setas do teclado (Cima, Baixo, Esquerda, Direita): Translação do nó selecionado.
- Teclas 'Q' e 'E': Rotação do nó ativo.
- Teclas 'W' e 'S': Escala do nó ativo.
- Tecla 'ESPAÇO': Verifica se o nó está na posição correta da árvore.
"""

import glfw
from OpenGL.GL import *
import math
import sys


# cada dicionário é um nó da árvore
# 50 começa fixa os outros tu muda no jogo
nos = [
    # id, valor, x, y atual, escala, rotacao, cor(R,G,B), alvo_x, alvo_y, id_pai, fixo
    {"id": 1, "valor": 50, "x": 0.0, "y": 0.6, "escala": 1.0, "rotacao": 0.0, "cor": (0.5, 0.5, 0.5), "alvo_x": 0.0, "alvo_y": 0.6, "pai": None, "fixo": True},   # Raiz (Cinza)
    {"id": 2, "valor": 30, "x": -0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 0.0, 0.0), "alvo_x": -0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},  # Vermelho
    {"id": 3, "valor": 70, "x": -0.4, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (0.0, 0.5, 1.0), "alvo_x": 0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},   # Azul
    {"id": 4, "valor": 20, "x": 0.0, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 1.0, 0.0), "alvo_x": -0.6, "alvo_y": -0.2, "pai": 2, "fixo": False},  # Amarelo
    {"id": 5, "valor": 60, "x": 0.4, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 0.0, 1.0), "alvo_x": 0.2, "alvo_y": -0.2, "pai": 3, "fixo": False},   # Magenta
]

no_ativo_idx = 1 # Começa controlando o nó 30 (índice 1 da lista)



#------- FUNÇÕES DO DESENHO (Modelagem por vértices) --------



def desenhar_hexagono(r, g, b):
    """
    Desenha um objeto através de vértices, gerando um hexágono.
    SRU: Sistema de Referência do Universo padrão (-1.0 a 1.0)
    SRO: Origem no centro geométrico do hexágono.
    """
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        # Raio base de 0.15 unidades
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()
    
    # contorno preto
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()

def desenhar_linha_conexao(x1, y1, x2, y2):
    """ Desenha a linha ligando um nó pai ao nó filho """
    glColor3f(1.0, 1.0, 1.0) # linha branca
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def desenhar_silhueta():
    """ Desenha um contorno tracejado indicando onde a peça deve encaixar """
    glColor3f(0.4, 0.4, 0.4) # cinza 
    glLineWidth(2.0)
    
    glEnable(GL_LINE_STIPPLE)     #  tracejado
    glLineStipple(1, 0x0F0F)      # padrão do tracejado
    
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()
    
    glDisable(GL_LINE_STIPPLE)    # tem que desativar pra n afetar tudo

def desenhar_digito(d):
    """ Desenha um único dígito (0-9) usando linhas vetoriais (estilo display de 7 segmentos) """
    segmentos = {
        'T':  ((-0.04,  0.08), ( 0.04,  0.08)),  # Top (Cima)
        'M':  ((-0.04,  0.00), ( 0.04,  0.00)),  # Middle (Meio)
        'B':  ((-0.04, -0.08), ( 0.04, -0.08)),  # Bottom (Baixo)
        'TL': ((-0.04,  0.08), (-0.04,  0.00)),  # Top-Left (Cima-Esquerda)
        'BL': ((-0.04,  0.00), (-0.04, -0.08)),  # Bottom-Left (Baixo-Esquerda)
        'TR': (( 0.04,  0.08), ( 0.04,  0.00)),  # Top-Right (Cima-Direita)
        'BR': (( 0.04,  0.00), ( 0.04, -0.08)),  # Bottom-Right (Baixo-Direita)
    }
    
    mapa_digitos = {
        '0': ['T', 'B', 'TL', 'BL', 'TR', 'BR'],
        '1': ['TR', 'BR'],
        '2': ['T', 'M', 'B', 'TR', 'BL'],
        '3': ['T', 'M', 'B', 'TR', 'BR'],
        '4': ['M', 'TL', 'TR', 'BR'],
        '5': ['T', 'M', 'B', 'TL', 'BR'],
        '6': ['T', 'M', 'B', 'TL', 'BL', 'BR'],
        '7': ['T', 'TR', 'BR'],
        '8': ['T', 'M', 'B', 'TL', 'BL', 'TR', 'BR'],
        '9': ['T', 'M', 'B', 'TL', 'TR', 'BR']
    }
    
    glBegin(GL_LINES)
    for seg in mapa_digitos[str(d)]:
        p1, p2 = segmentos[seg]
        glVertex2f(p1[0], p1[1])
        glVertex2f(p2[0], p2[1])
    glEnd()

def desenhar_numero(numero):
    """ Pega um número inteiro, centraliza e desenha dígito por dígito """
    texto = str(numero)
    espacamento = 0.12 #distancia entre eles
    
    #isso ve pra ficar centralizado no hexagono
    inicio_x = -(len(texto) * espacamento) / 2.0 + (espacamento / 2.0)
    
    glColor3f(1.0, 1.0, 1.0) # branco no numeros
    glLineWidth(2.0)         # Espessura da linha do número
    
    glPushMatrix() # tem que salvar matriz pra n afetar o resto
    glTranslatef(inicio_x, 0.0, 0.0) # Move para a posição inicial do texto
    
    for char in texto:
        desenhar_digito(char)
        glTranslatef(espacamento, 0.0, 0.0) # mexe um pouco pro lado pra digitar o outro numero
        
    glPopMatrix() # 




#----- INTERAÇÃO (Teclado)-----

def teclado_callback(window, key, scancode, action, mods):
    global no_ativo_idx, nos
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        # seleção de objeto (teclas 1 a 5)
        if glfw.KEY_1 <= key <= glfw.KEY_5:
            idx = key - glfw.KEY_1
            if not nos[idx]["fixo"]:
                no_ativo_idx = idx
                print(f"-> Controlando o Nó com valor: {nos[idx]['valor']}")
            else:
                print(f"-> O Nó {nos[idx]['valor']} já está fixo na árvore!")

        # só transforma se o nó não tiver fixo na resposta
        no_atual = nos[no_ativo_idx]
        if not no_atual["fixo"]:
            # Translação
            if key == glfw.KEY_RIGHT: no_atual["x"] += 0.05
            elif key == glfw.KEY_LEFT: no_atual["x"] -= 0.05
            elif key == glfw.KEY_UP: no_atual["y"] += 0.05
            elif key == glfw.KEY_DOWN: no_atual["y"] -= 0.05
            
            # Rotação
            elif key == glfw.KEY_Q: no_atual["rotacao"] += 10.0
            elif key == glfw.KEY_E: no_atual["rotacao"] -= 10.0
            
            # Escala
            elif key == glfw.KEY_W: no_atual["escala"] += 0.1
            elif key == glfw.KEY_S: no_atual["escala"] = max(0.2, no_atual["escala"] - 0.1)
            
            # validação pra ver se ta tudo ok (Aperte Espaço)
            elif key == glfw.KEY_SPACE:
                distancia = math.sqrt((no_atual["x"] - no_atual["alvo_x"])**2 + (no_atual["y"] - no_atual["alvo_y"])**2)
                # verifica se o hexagono ta perto do lugar certo
                if distancia < 0.15:
                    print(f"CORRETO! O Nó {no_atual['valor']} foi encaixado.")
                    no_atual["x"] = no_atual["alvo_x"]
                    no_atual["y"] = no_atual["alvo_y"]
                    no_atual["escala"] = 1.0
                    no_atual["rotacao"] = 360.0 # animação de sucesso
                    no_atual["cor"] = (0.0, 1.0, 0.0) # aqui ele fica verde
                    no_atual["fixo"] = True
                else:
                    print(f"ERRO: Esta não é a posição do {no_atual['valor']} na Árvore de Busca.")




#------- FUNÇÃO PRINCIPAL ---------

def main():
    if not glfw.init():
        sys.exit()
    
    # cria janela
    window = glfw.create_window(800, 600, "Trabalho G1 - ArvoreBinariaV1", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado_callback)
    
    print("=== JOGO DA ÁRVORE BINÁRIA DE BUSCA ===")
    print("Regra: Menores à esquerda, Maiores à direita da Raiz (50).")
    print("Controles no teclado: Setas, Q/E, W/S. Espaço para confirmar posição.")
    print(f"-> Controlando o Nó com valor: {nos[no_ativo_idx]['valor']}")

    # renderização
    while not glfw.window_should_close(window):
        # cor do fundo
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        
        # desenha silhueta dos alvos pra colocar hexagonos
        for no in nos:
            if not no["fixo"]: # ele desenha se a peça n está la
                glPushMatrix()
                glTranslatef(no["alvo_x"], no["alvo_y"], 0.0)
                desenhar_silhueta()
                glPopMatrix()
        
    

        # linhas de conexão para os nós que já tão fixos
        for no in nos:
            if no["fixo"] and no["pai"] is not None:
                pai = next(p for p in nos if p["id"] == no["pai"])
                desenhar_linha_conexao(no["x"], no["y"], pai["x"], pai["y"])

        # desenha nós fazendo as transformações geométricas
        for i, no in enumerate(nos):
            glPushMatrix() # salva a matriz atual 
            # aplica as transformações como a translação
            glTranslatef(no["x"], no["y"], 0.0)
            glRotatef(no["rotacao"], 0.0, 0.0, 1.0)
            
            # da um destaque de escala se for o nó ativo e não tiver fixo
            if i == no_ativo_idx and not no["fixo"]:
                # escala manual
                glScalef(no["escala"] * 1.2, no["escala"] * 1.2, 1.0)
            else:
                glScalef(no["escala"], no["escala"], 1.0)
            
            desenhar_hexagono(no["cor"][0], no["cor"][1], no["cor"][2])
            
            desenhar_numero(no["valor"])
            
            glPopMatrix() # restaura a matriz
        
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()