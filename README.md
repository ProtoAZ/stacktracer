# STACKTRACER
Stacktracer é um puzzle game educativo baseado em texto e gráficos 2D minimalistas, renderizado com PyOpenGL e GLFW. A estética do jogo emula monitores CRT monocromáticos (fósforo verde) de mainframes antigos.

### STACKTRACER // MINIGAME 01: Linear Classifier
Regressão Linear: O objetivo é encontrar a melhor linha de ajuste para um conjunto de dados bidimensional. A reta obedece à equação fundamental $y = wx + b$, onde $w$ é o Peso (rotação/inclinação) e $b$ é o Viés (translação vertical).

O jogo possui um Sistema de Progressão contendo 3 setores de memória (fases). Cada fase injeta um novo dataset com distribuições de dados variadas (tendência positiva, negativa e íngreme).

#### Função de Perda (Loss Function)
O terminal inferior exibe em tempo real o cálculo do erro do jogador usando duas métricas:
- MSE (Mean Squared Error): Calcula a média dos quadrados das diferenças verticais entre os pontos reais e a predição da reta.
- Distância Euclidiana Ortogonal: Calcula a distância mais curta (perpendicular) entre cada ponto e a reta atual.

#### Otimização e Condição de Vitória (OLS)
O jogo utiliza o método dos Mínimos Quadrados Ordinários (Ordinary Least Squares) para calcular matematicamente a reta perfeita no momento em que a fase é carregada. Para vencer, o MSE do jogador deve atingir um limite de tolerância aceitável (2.5x o MSE ótimo), ensinando que modelos de ML buscam generalização satisfatória, e não necessariamente precisão absoluta (overfitting).

#### Interface
- Top Panel (Viewport Visual - 70%): Exibe a representação espacial dos dados normalizados. Os pontos e a reta escalam dinamicamente com a resolução da janela, mantendo a precisão visual e matemática.
- Bottom Panel (Terminal Log - 30%): Renderiza texto customizado usando uma matriz de fontes construída do zero com quadriláteros (GL_QUADS). Ele exibe a sequência de boot do sistema e atualiza os valores de perda (Loss) a cada frame.

#### Controles
O jogador interage diretamente com as variáveis da equação linear através do teclado:
- ↑ Seta para Cima: Aumenta o Viés (Bias). Translada a reta para cima.
- ↓ Seta para Baixo: Diminui o Viés (Bias). Translada a reta para baixo.
- ← Seta para Esquerda: Altera o Peso (Weight). Rotaciona a reta no sentido anti-horário em torno do seu centroide.
- → Seta para Direita: Altera o Peso (Weight). Rotaciona a reta no sentido horário.
- SPACE: Submeter Calibração. Aciona o cálculo de verificação (Validação OLS). Se o erro for baixo o suficiente, o módulo é destravado.
- ENTER: Próximo Setor. Avança para a próxima fase após submeter uma calibração válida.


#### MINIGAME 02: Logic Trees (Binary Search Tree) Estruturas de Dados:
 O objetivo é realocar os setores corrompidos de memória (nós) de volta à sua árvore de lógica estrutural. A árvore obedece à regra de ouro da Árvore Binária de Busca (BST): valores menores que a raiz são alocados à esquerda, e valores maiores à direita. O jogo possui 5 objetos  que compõem os dados do sistema.  
 Transformações Geométricas e SRU/SRO: O modelo foi todo desenvolvido utilizando matrizes de vértices no OpenGL. Para posicionar as peças pelo cenário, o jogo aplica conceitos de Computação Gráfica como SRU (Sistema de Referência do Universo): O painel superior mapeia o mundo entre as coordenadas -1.0 e 1.0. Uma escala global compensa a distorção do Aspect Ratio da tela.SRO (Sistema de Referência do Objeto): Cada nó (hexágono) é gerado a partir de sua própria origem local (0,0), permitindo que receba suas próprias matrizes de Translação, Rotação e Escala sem deformar os demais objetos na tela.  

 ##### Controles
O jogador interage diretamente com o estado das matrizes através do teclado:  

Teclas de numerais: Selecionam o nó corrompido que receberá as matrizes de transformação.

Setas Direcionais: Alteram as coordenadas X e Y da peça (Translação).

Q / E: Rotacionam o objeto no sentido anti-horário e horário (Rotação).

W / S: Alteram as proporções do objeto (Escala).

SPACE: Executa a submissão de dados. O terminal inferior cruza as posições e exibe o feedback de calibração ("Correto", ou erros específicos de posição/rotação/escala).
