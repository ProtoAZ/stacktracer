"""
controles e resumo pra apresentação:

FASE 1: A Árvore do Conhecimento (BST)
Posicione os nós soltos respeitando a regra da Árvore Binária (menores à esquerda, maiores à direita).
- Controles: Teclas 1 a 5 (Seleciona), Setas (Translação), W/S (Escala), Q/E (Rotação), ESPAÇO (Validar).

FASE 2: O Despertar da IA (Perceptron / Separabilidade Linear)
Ajuste a reta (Weight e Bias) para separar os dados lineares (Vermelhos e Azuis).
- Controles: Setas Cima/Baixo (Move a reta / Bias), Q/E (Gira a reta / Weight), ESPAÇO (Validar).

FASE 3: O Enigma dos Pixels (Calibração de Padrões)
Recupere os "Macro-pixels" corrompidos ajustando posição, tamanho e rotação para formar a Cruz Sagrada.
- Controles: Teclas 1 a 5 (Seleciona), Setas, W/S, Q/E, ESPAÇO (Validar).

- ENTER avança para a próxima fase quando a atual for concluída!
"""

import glfw
from OpenGL.GL import *
import math
import sys

# ==============================================================================
# variaveis de estado
# ==============================================================================
fase_atual = 1 # Controle da máquina de estados (1, 2 ou 3)

# --- ESTADO DA FASE 1 (ÁRVORE BST) ---

# cada dicionário é um nó da árvore
nos = [
    {"id": 1, "valor": 50, "x": 0.0, "y": 0.6, "escala": 1.0, "rotacao": 0.0, "cor": (0.5, 0.5, 0.5), "alvo_x": 0.0, "alvo_y": 0.6, "pai": None, "fixo": True},
    {"id": 2, "valor": 30, "x": -0.8, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 0.0, 0.0), "alvo_x": -0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 3, "valor": 70, "x": -0.4, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (0.0, 0.5, 1.0), "alvo_x": 0.4, "alvo_y": 0.2, "pai": 1, "fixo": False},
    {"id": 4, "valor": 20, "x": 0.0, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 1.0, 0.0), "alvo_x": -0.6, "alvo_y": -0.2, "pai": 2, "fixo": False},
    {"id": 5, "valor": 60, "x": 0.4, "y": -0.8, "escala": 1.0, "rotacao": 0.0, "cor": (1.0, 0.0, 1.0), "alvo_x": 0.2, "alvo_y": -0.2, "pai": 3, "fixo": False},
]
no_ativo_idx = 1 # Começa controlando o nó 30

# --- ESTADO DA FASE 2 (PERCEPTRON) ---

reta_y = 0.0      #  Bias
reta_angulo = 0.0 # Representa o Weight 
fase2_vencida = False
pontos_vermelhos = [(-0.5, 0.5), (0.5, 0.8)]
pontos_azuis = [(-0.5, -0.5), (0.5, -0.8)]

# --- ESTADO DA FASE 3 (CALIBRAÇÃO) ---

# tem que formar uma cruz na tela, começa bagunçado
pixels = [
    {"id": 1, "x": -0.8, "y": 0.8, "escala": 0.5, "rotacao": 45.0, "alvo_x": 0.0, "alvo_y": 0.0, "fixo": False}, # Centro
    {"id": 2, "x": 0.8, "y": 0.8, "escala": 1.5, "rotacao": 15.0, "alvo_x": 0.0, "alvo_y": 0.3, "fixo": False}, # Cima
    {"id": 3, "x": -0.8, "y": -0.8, "escala": 0.3, "rotacao": 80.0, "alvo_x": 0.0, "alvo_y": -0.3, "fixo": False}, # Baixo
    {"id": 4, "x": 0.8, "y": -0.8, "escala": 1.8, "rotacao": 33.0, "alvo_x": -0.3, "alvo_y": 0.0, "fixo": False}, # Esquerda
    {"id": 5, "x": 0.0, "y": 0.8, "escala": 0.7, "rotacao": 66.0, "alvo_x": 0.3, "alvo_y": 0.0, "fixo": False}, # Direita
]
pixel_ativo_idx = 0


# ==============================================================================
# funções desenho
# ==============================================================================

# --- funções fase 1 ---
def desenhar_hexagono(r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    for i in range(6):
        angulo = 2 * math.pi * i / 6
        glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    glEnd()

def desenhar_linha_conexao(x1, y1, x2, y2):
    glColor3f(1.0, 1.0, 1.0) # linha branca
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()

def desenhar_silhueta(tipo="hexagono"):
    """ Modificado para aceitar diferentes formas (hexagono ou quadrado) """
    glColor3f(0.4, 0.4, 0.4) # cinza 
    glLineWidth(2.0)
    glEnable(GL_LINE_STIPPLE)
    glLineStipple(1, 0x0F0F)
    glBegin(GL_LINE_LOOP)
    if tipo == "hexagono":
        for i in range(6):
            angulo = 2 * math.pi * i / 6
            glVertex2f(0.15 * math.cos(angulo), 0.15 * math.sin(angulo))
    elif tipo == "quadrado":
        glVertex2f(-0.15, -0.15)
        glVertex2f( 0.15, -0.15)
        glVertex2f( 0.15,  0.15)
        glVertex2f(-0.15,  0.15)
    glEnd()
    glDisable(GL_LINE_STIPPLE)

def desenhar_digito(d):
    segmentos = {
        'T':  ((-0.04,  0.08), ( 0.04,  0.08)),  'M':  ((-0.04,  0.00), ( 0.04,  0.00)),
        'B':  ((-0.04, -0.08), ( 0.04, -0.08)),  'TL': ((-0.04,  0.08), (-0.04,  0.00)),
        'BL': ((-0.04,  0.00), (-0.04, -0.08)),  'TR': (( 0.04,  0.08), ( 0.04,  0.00)),
        'BR': (( 0.04,  0.00), ( 0.04, -0.08)),
    }
    mapa_digitos = {
        '0': ['T','B','TL','BL','TR','BR'], '1': ['TR','BR'], '2': ['T','M','B','TR','BL'],
        '3': ['T','M','B','TR','BR'], '4': ['M','TL','TR','BR'], '5': ['T','M','B','TL','BR'],
        '6': ['T','M','B','TL','BL','BR'], '7': ['T','TR','BR'], '8': ['T','M','B','TL','BL','TR','BR'],
        '9': ['T','M','B','TL','TR','BR']
    }
    glBegin(GL_LINES)
    for seg in mapa_digitos[str(d)]:
        p1, p2 = segmentos[seg]
        glVertex2f(p1[0], p1[1])
        glVertex2f(p2[0], p2[1])
    glEnd()

def desenhar_numero(numero):
    texto = str(numero)
    espacamento = 0.12 
    inicio_x = -(len(texto) * espacamento) / 2.0 + (espacamento / 2.0)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)         
    glPushMatrix()
    glTranslatef(inicio_x, 0.0, 0.0)
    for char in texto:
        desenhar_digito(char)
        glTranslatef(espacamento, 0.0, 0.0)
    glPopMatrix() 

# --- funções fase 2 e 3 ---
def desenhar_ponto_fixo(x, y, r, g, b):
    """ Usado na Fase 2 para os dados do Perceptron """
    glPushMatrix()
    glTranslatef(x, y, 0.0)
    glColor3f(r, g, b)
    glBegin(GL_POLYGON) # faz um losango aq
    glVertex2f(0.0, 0.05); glVertex2f(0.05, 0.0); glVertex2f(0.0, -0.05); glVertex2f(-0.05, 0.0)
    glEnd()
    glPopMatrix()

def desenhar_reta():
    """ Usado na Fase 2 para a separação linear """
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex2f(-2.0, 0.01) 
    glVertex2f( 2.0, 0.01)
    glVertex2f( 2.0, -0.01)
    glVertex2f(-2.0, -0.01)
    glEnd()

def desenhar_quadrado(r, g, b):
    """ Usado na Fase 3 para os Macro-pixels """
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    glVertex2f(-0.15, -0.15)
    glVertex2f( 0.15, -0.15)
    glVertex2f( 0.15,  0.15)
    glVertex2f(-0.15,  0.15)
    glEnd()
    # Contorno
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-0.15, -0.15); glVertex2f(0.15, -0.15); glVertex2f(0.15, 0.15); glVertex2f(-0.15, 0.15)
    glEnd()


# ==============================================================================
# teclado e logica de fases
# ==============================================================================
def verificar_arvore_completa():
    for no in nos:
        if not no["fixo"]: return False
    return True

def verificar_pixels_completos():
    for px in pixels:
        if not px["fixo"]: return False
    return True

def verificar_separacao_linear():       
    """ Lógica matemática (Matriz/Produto Escalar) para detectar separação """
    global fase2_vencida
    rad = math.radians(reta_angulo)
    nx = -math.sin(rad) # Normal X
    ny = math.cos(rad)  # Normal Y
    
    vermelhos_corretos = True
    azuis_corretos = True
    
    # escala com margem pra n enconstar nos pontos na fase 2
    for px, py in pontos_vermelhos:
        py_relativo = py - reta_y
        # Exige que fique a uma distância mínima de 0.05 da reta
        if (px * nx) + (py_relativo * ny) <= 0.05: vermelhos_corretos = False
            
    for px, py in pontos_azuis:
        py_relativo = py - reta_y
        # Exige que fique a uma distância mínima de 0.05 da reta pra n ficar feio
        if (px * nx) + (py_relativo * ny) >= -0.05: azuis_corretos = False
            
    if vermelhos_corretos and azuis_corretos:
        print("\n>>> FASE 2 CONCLUÍDA! PERCEPTRON TREINADO! <<<")
        print("Pressione ENTER para ir à Fase 3.")
        fase2_vencida = True
    else:
        print("ERRO: Os dados ainda não estão separados linearmente.")

def teclado_callback(window, key, scancode, action, mods):
    global fase_atual, no_ativo_idx, reta_y, reta_angulo, pixel_ativo_idx
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        
        # --- CONTROLES DA FASE 1 ---
        if fase_atual == 1:
            if glfw.KEY_1 <= key <= glfw.KEY_5:
                idx = key - glfw.KEY_1
                if not nos[idx]["fixo"]:
                    no_ativo_idx = idx
                    print(f"-> FASE 1: Controlando o Nó: {nos[idx]['valor']}")

            no_atual = nos[no_ativo_idx]
            if not no_atual["fixo"]:
                if key == glfw.KEY_RIGHT: no_atual["x"] += 0.05
                elif key == glfw.KEY_LEFT: no_atual["x"] -= 0.05
                elif key == glfw.KEY_UP: no_atual["y"] += 0.05
                elif key == glfw.KEY_DOWN: no_atual["y"] -= 0.05
                elif key == glfw.KEY_Q: no_atual["rotacao"] += 10.0
                elif key == glfw.KEY_E: no_atual["rotacao"] -= 10.0
                elif key == glfw.KEY_W: no_atual["escala"] += 0.1
                elif key == glfw.KEY_S: no_atual["escala"] = max(0.2, no_atual["escala"] - 0.1)
                
                elif key == glfw.KEY_SPACE:
                    distancia = math.sqrt((no_atual["x"] - no_atual["alvo_x"])**2 + (no_atual["y"] - no_atual["alvo_y"])**2)
                    if distancia < 0.15:
                        print(f"CORRETO! O Nó {no_atual['valor']} foi encaixado.")
                        no_atual["x"], no_atual["y"], no_atual["escala"], no_atual["rotacao"] = no_atual["alvo_x"], no_atual["alvo_y"], 1.0, 360.0
                        no_atual["cor"], no_atual["fixo"] = (0.0, 1.0, 0.0), True
                        if verificar_arvore_completa():
                            print("\n>>> FASE 1 CONCLUÍDA! Pressione ENTER para ir à Fase 2. <<<")
                    else:
                        print("ERRO: Posição incorreta na Árvore.")
            
            # Avançar para a próxima fase se apertar ENTER e tiver ganho
            if key == glfw.KEY_ENTER and verificar_arvore_completa():
                fase_atual = 2
                print("\n=== INICIANDO FASE 2: SEPARABILIDADE LINEAR ===")
        
        # --- CONTROLES DA FASE 2 ---
        elif fase_atual == 2:
            if not fase2_vencida:
                if key == glfw.KEY_UP: reta_y += 0.05       # Altera o Bias
                elif key == glfw.KEY_DOWN: reta_y -= 0.05
                elif key == glfw.KEY_Q: reta_angulo += 5.0  # Altera o Weight
                elif key == glfw.KEY_E: reta_angulo -= 5.0
                
                elif key == glfw.KEY_SPACE:
                    verificar_separacao_linear()
            
            if key == glfw.KEY_ENTER and fase2_vencida:
                fase_atual = 3
                print("\n=== INICIANDO FASE 3: CALIBRAÇÃO DE PIXELS ===")

        # --- CONTROLES DA FASE 3 ---
        elif fase_atual == 3:
            if glfw.KEY_1 <= key <= glfw.KEY_5:
                idx = key - glfw.KEY_1
                if not pixels[idx]["fixo"]:
                    pixel_ativo_idx = idx
                    print(f"-> FASE 3: Controlando o Pixel {idx + 1}")

            px_atual = pixels[pixel_ativo_idx]
            if not px_atual["fixo"]:
                if key == glfw.KEY_RIGHT: px_atual["x"] += 0.05
                elif key == glfw.KEY_LEFT: px_atual["x"] -= 0.05
                elif key == glfw.KEY_UP: px_atual["y"] += 0.05
                elif key == glfw.KEY_DOWN: px_atual["y"] -= 0.05
                elif key == glfw.KEY_Q: px_atual["rotacao"] += 5.0
                elif key == glfw.KEY_E: px_atual["rotacao"] -= 5.0
                elif key == glfw.KEY_W: px_atual["escala"] += 0.1
                elif key == glfw.KEY_S: px_atual["escala"] -= 0.1
                
                elif key == glfw.KEY_SPACE:
                    dist = math.sqrt((px_atual["x"] - px_atual["alvo_x"])**2 + (px_atual["y"] - px_atual["alvo_y"])**2)
                    esc_ok = 0.8 < px_atual["escala"] < 1.2
                    # aq ele deixa uma margem de erro nos quadrados pra nao ficar mt ruim de encaixar
                    rot_ok = (px_atual["rotacao"] % 90) <= 15 or (px_atual["rotacao"] % 90) >= 75
                    
                    if dist < 0.15 and esc_ok and rot_ok:
                        print(f"CORRETO! O Pixel {pixel_ativo_idx + 1} foi calibrado e travado.")
                        px_atual["x"], px_atual["y"], px_atual["escala"], px_atual["rotacao"] = px_atual["alvo_x"], px_atual["alvo_y"], 1.0, 0.0
                        px_atual["fixo"] = True
                        if verificar_pixels_completos():
                            print("\n🎉 PARABÉNS! VOCÊ ZEROU O JOGO! 🎉")
                    else:
                        # aqui ele diz se precisa diminuir ou aumentar o tamanho ou mudar o lugar do quadrado pra ser mais facil
                        print(f"--- ANALISANDO PIXEL {pixel_ativo_idx + 1} ---")
                        if dist >= 0.15:
                            print("ERRO: A Posição está errada (Mova com as Setas).")
                        if not esc_ok:
                            print("ERRO: O Tamanho está errado (Use W/S para ajustar a escala).")
                        if not rot_ok:
                            print("ERRO: O Ângulo está torto (Use Q/E para deixar o quadrado reto).")


# ==============================================================================
# FUNÇÃO PRINCIPAL / RENDERIZAÇÃO
# ==============================================================================
def main():
    if not glfw.init(): sys.exit()
    
    window = glfw.create_window(800, 600, "Trabalho G1 - Computação Gráfica", None, None)
    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)
    glfw.set_key_callback(window, teclado_callback)
    
    print("=== JOGO DA ÁRVORE BINÁRIA DE BUSCA (FASE 1) ===")

    while not glfw.window_should_close(window):
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        glScalef(600.0 / 800.0, 1.0, 1.0) # isso é pra n causar distorção e os quadrados da fase 3 funcionar
        
        # ---------------- FASE 1 ----------------
        if fase_atual == 1:
            for no in nos:
                if not no["fixo"]:
                    glPushMatrix()
                    glTranslatef(no["alvo_x"], no["alvo_y"], 0.0)
                    desenhar_silhueta("hexagono")
                    glPopMatrix()
            
            for no in nos:
                if no["fixo"] and no["pai"] is not None:
                    pai = next(p for p in nos if p["id"] == no["pai"])
                    desenhar_linha_conexao(no["x"], no["y"], pai["x"], pai["y"])

            for i, no in enumerate(nos):
                glPushMatrix() 
                glTranslatef(no["x"], no["y"], 0.0)
                glRotatef(no["rotacao"], 0.0, 0.0, 1.0)
                
                if i == no_ativo_idx and not no["fixo"]:
                    glScalef(no["escala"] * 1.2, no["escala"] * 1.2, 1.0)
                else:
                    glScalef(no["escala"], no["escala"], 1.0)
                
                desenhar_hexagono(no["cor"][0], no["cor"][1], no["cor"][2])
                desenhar_numero(no["valor"])
                glPopMatrix()

        # ---------------- FASE 2 ----------------
        elif fase_atual == 2:
            # desenha os dados, vermelho em cima azul em baixo
            for x, y in pontos_vermelhos: desenhar_ponto_fixo(x, y, 1.0, 0.0, 0.0)
            for x, y in pontos_azuis: desenhar_ponto_fixo(x, y, 0.0, 0.5, 1.0)
            
            #tranformacoes na reta
            glPushMatrix()
            if fase2_vencida: glColor3f(0.0, 1.0, 0.0) # Fica verde se vencer
            glTranslatef(0.0, reta_y, 0.0)
            glRotatef(reta_angulo, 0.0, 0.0, 1.0)
            desenhar_reta()
            glPopMatrix()

        # ---------------- FASE 3 ----------------
        elif fase_atual == 3:
            # desenha as silhuetas dos quadrados
            for px in pixels:
                if not px["fixo"]:
                    glPushMatrix()
                    glTranslatef(px["alvo_x"], px["alvo_y"], 0.0)
                    desenhar_silhueta("quadrado")
                    glPopMatrix()

            # faz os proprios quadrados
            for i, px in enumerate(pixels):
                glPushMatrix()
                glTranslatef(px["x"], px["y"], 0.0)
                glRotatef(px["rotacao"], 0.0, 0.0, 1.0)
                
                escala_extra = 1.2 if (i == pixel_ativo_idx and not px["fixo"]) else 1.0
                glScalef(px["escala"] * escala_extra, px["escala"] * escala_extra, 1.0)
                
                cor = (0.0, 1.0, 0.0) if px["fixo"] else (0.8, 0.8, 0.8) # Verde quando acerta
                desenhar_quadrado(cor[0], cor[1], cor[2])
                glPopMatrix()

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()