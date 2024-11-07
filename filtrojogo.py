import cv2
import numpy as np
import pygame

# Links de referência:
# https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
# https://www.bluetin.io/opencv/opencv-color-detection-filtering-python/
# https://docs.opencv.org/4.x/d1/db7/tutorial_py_histogram_begins.html

# Inicializar captura de vídeo
captura = cv2.VideoCapture(0)

# Configuração dos limites para a primeira cor (baseado na primeira imagem - Vermelho)
limite_inferior_vermelho = np.array([167, 209, 0])
limite_superior_vermelho = np.array([179, 255, 255])

# Configuração dos limites para a segunda cor (agora Verde)
limite_inferior_verde = np.array([35, 94, 0])       # Hue = 35, Saturation = 94, Value = 0
limite_superior_verde = np.array([85, 255, 255])    # Ajuste conforme necessário

# Configuração do detector de blobs
parametros = cv2.SimpleBlobDetector_Params()
parametros.filterByArea = True
parametros.minArea = 1000
parametros.maxArea = 1000000
parametros.filterByCircularity = False
parametros.filterByConvexity = False
parametros.filterByInertia = False
detector = cv2.SimpleBlobDetector_create(parametros)

# Inicializar o Pygame para o jogo Pong
pygame.init()

# Dimensões da tela do Pong
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Pong com Rastreamento de Cor")

# Configurações das cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
COR_BARRA_1 = (255, 0, 0)  # Cor da primeira barra (vermelho)
COR_BARRA_2 = (0, 255, 0)  # Cor da segunda barra (verde)
COR_LINHA = (255, 255, 255)  # Cor das linhas de referência

# Variáveis das barras do Pong
largura_barra, altura_barra = 30, 150  # Aumentando largura e altura
velocidade_barra = 10
barra_1_y = ALTURA // 2 - altura_barra // 2
barra_2_y = ALTURA // 2 - altura_barra // 2

# Variáveis da bola do Pong
raio_bola = 15
bola_x, bola_y = LARGURA // 2, ALTURA // 2
velocidade_bola_x, velocidade_bola_y = 15, 15  # Velocidade triplicada

# Pontuação dos jogadores
pontuacao_1 = 0
pontuacao_2 = 0

# Fonte para exibir a pontuação
fonte = pygame.font.Font(None, 74)

# Função para desenhar elementos na tela do Pong
def desenhar_pong():
    tela.fill(PRETO)
    
    # Desenhar as barras
    pygame.draw.rect(tela, COR_BARRA_1, (20, barra_1_y, largura_barra, altura_barra))
    pygame.draw.rect(tela, COR_BARRA_2, (LARGURA - 50, barra_2_y, largura_barra, altura_barra))
    
    # Desenhar a bola
    pygame.draw.ellipse(tela, BRANCO, (bola_x - raio_bola, bola_y - raio_bola, raio_bola * 2, raio_bola * 2))
    
    # Desenhar a linha central
    pygame.draw.line(tela, COR_LINHA, (LARGURA // 2, 0), (LARGURA // 2, ALTURA), 2)
    
    # Desenhar linhas nas posições das barras
    pygame.draw.line(tela, COR_LINHA, (20 + largura_barra, 0), (20 + largura_barra, ALTURA), 2)
    pygame.draw.line(tela, COR_LINHA, (LARGURA - 50, 0), (LARGURA - 50, ALTURA), 2)
    
    # Exibir a pontuação dos jogadores
    texto_pontuacao = fonte.render(f"{pontuacao_1} - {pontuacao_2}", True, BRANCO)
    tela.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, 10))
    
    pygame.display.flip()

# Loop principal
executando = True
while executando:
    # Capturar frame da câmera
    ret, frame = captura.read()
    if not ret:
        break

    # Converter para o espaço de cor HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Criar máscaras para as duas cores
    mascara_vermelho = cv2.inRange(hsv, limite_inferior_vermelho, limite_superior_vermelho)
    mascara_verde = cv2.inRange(hsv, limite_inferior_verde, limite_superior_verde)

    # Combinar as duas máscaras
    mascara_combinada = cv2.bitwise_or(mascara_vermelho, mascara_verde)

    # Aplicar a máscara combinada na imagem original
    resultado = cv2.bitwise_and(frame, frame, mask=mascara_combinada)
    mascara_invertida = cv2.bitwise_not(mascara_combinada)
    keypoints = detector.detect(mascara_invertida)
    frame_com_keypoints = cv2.drawKeypoints(resultado, keypoints, np.array([]), (0, 255, 255),
                                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Redimensionar as imagens para exibição
    frame_com_keypoints = cv2.resize(frame_com_keypoints, (1080, 720))
    
    # Mostrar o resultado da detecção na janela de log
    cv2.imshow("Filtros", frame_com_keypoints)

    # Atualizar o Pygame com o rastreamento
    # Encontrar contornos para determinar as posições das barras
    contornos_vermelho, _ = cv2.findContours(mascara_vermelho, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_verde, _ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Atualizar a posição da primeira barra (vermelha)
    if len(contornos_vermelho) > 0:
        maior_contorno_vermelho = max(contornos_vermelho, key=cv2.contourArea)
        _, y, _, h = cv2.boundingRect(maior_contorno_vermelho)
        barra_1_y = (y - (altura_barra // 2)) * 2 if (y - (altura_barra // 2)) * 2 > 0 else 0
        barra_1_y = min(barra_1_y, ALTURA - altura_barra)
    else:
        # Manter a barra no meio se não houver rastreamento
        barra_1_y = ALTURA // 2 - altura_barra // 2

    # Atualizar a posição da segunda barra (verde)
    if len(contornos_verde) > 0:
        maior_contorno_verde = max(contornos_verde, key=cv2.contourArea)
        _, y, _, h = cv2.boundingRect(maior_contorno_verde)
        barra_2_y = (y - (altura_barra // 2)) * 2 if (y - (altura_barra // 2)) * 2 > 0 else 0
        barra_2_y = min(barra_2_y, ALTURA - altura_barra)
    else:
        # Manter a barra no meio se não houver rastreamento
        barra_2_y = ALTURA // 2 - altura_barra // 2

    # Atualizar a posição da bola
    bola_x += velocidade_bola_x
    bola_y += velocidade_bola_y

    # Verificar colisão com as paredes superior e inferior
    if bola_y - raio_bola <= 0 or bola_y + raio_bola >= ALTURA:
        velocidade_bola_y *= -1

    # Verificar colisão com as barras
    # Colisão com a primeira barra (esquerda)
    if (velocidade_bola_x < 0 and bola_x - raio_bola <= 20 + largura_barra and barra_1_y <= bola_y <= barra_1_y + altura_barra):
        velocidade_bola_x *= -1
        bola_x = 20 + largura_barra + raio_bola  # Ajustar posição para evitar sobreposição
    # Colisão com a segunda barra (direita)
    elif (velocidade_bola_x > 0 and bola_x + raio_bola >= LARGURA - 50 - largura_barra and barra_2_y <= bola_y <= barra_2_y + altura_barra):
        velocidade_bola_x *= -1
        bola_x = LARGURA - 50 - largura_barra - raio_bola  # Ajustar posição para evitar sobreposição

    # Verificar se a bola passou das barras (pontuação)
    if bola_x - raio_bola < 0:
        pontuacao_2 += 1
        bola_x, bola_y = LARGURA // 2, ALTURA // 2
        velocidade_bola_x *= -1
    elif bola_x + raio_bola > LARGURA:
        pontuacao_1 += 1
        bola_x, bola_y = LARGURA // 2, ALTURA // 2
        velocidade_bola_x *= -1

    # Desenhar os elementos do jogo
    desenhar_pong()

    # Eventos do Pygame
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False

    # Tecla para sair do OpenCV
    if cv2.waitKey(1) & 0xFF == ord('q'):
        executando = False

# Liberar recursos
captura.release()
cv2.destroyAllWindows()
pygame.quit()
