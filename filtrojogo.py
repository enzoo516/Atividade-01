import cv2
import numpy as np
import pygame

# Função de callback vazia para as trackbars
def callback(_):
    pass

# Inicializar captura de vídeo
captura = cv2.VideoCapture(0)

# Criar janela para os filtros e trackbars
cv2.namedWindow('Filtros')
cv2.resizeWindow('Filtros', 1080, 720)

# Criar trackbars para a primeira cor (Cor1)
cv2.createTrackbar("LH1", "Filtros", 167, 179, callback)  # Hue Inferior
cv2.createTrackbar("LS1", "Filtros", 209, 255, callback)  # Saturação Inferior
cv2.createTrackbar("LV1", "Filtros", 0, 255, callback)    # Valor Inferior
cv2.createTrackbar("UH1", "Filtros", 179, 179, callback)  # Hue Superior
cv2.createTrackbar("US1", "Filtros", 255, 255, callback)  # Saturação Superior
cv2.createTrackbar("UV1", "Filtros", 255, 255, callback)  # Valor Superior

# Criar trackbars para a segunda cor (Cor2)
cv2.createTrackbar("LH2", "Filtros", 35, 179, callback)   # Hue Inferior
cv2.createTrackbar("LS2", "Filtros", 63, 255, callback)   # Saturação Inferior
cv2.createTrackbar("LV2", "Filtros", 82, 255, callback)    # Valor Inferior
cv2.createTrackbar("UH2", "Filtros", 85, 179, callback)   # Hue Superior
cv2.createTrackbar("US2", "Filtros", 255, 255, callback)  # Saturação Superior
cv2.createTrackbar("UV2", "Filtros", 255, 255, callback)  # Valor Superior

# Inicializar o Pygame para o jogo Pong
pygame.init()

# Dimensões da tela do Pong
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Pong com Rastreamento de Cor")

# Configurações das cores para Pygame
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
COR_LINHA = (255, 255, 255)  # Branco

# Variáveis das barras do Pong
largura_barra, altura_barra = 30, 150
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

# Função para converter HSV para RGB
def hsv_para_rgb(h, s, v):
    # OpenCV usa H de 0-179, S e V de 0-255
    hsv = np.uint8([[[h, s, v]]])
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return tuple(int(c) for c in rgb[0][0])

# Função para desenhar elementos na tela do Pong
def desenhar_pong(cor_barra1, cor_barra2):
    tela.fill(PRETO)
    
    # Desenhar as barras
    pygame.draw.rect(tela, cor_barra1, (20, barra_1_y, largura_barra, altura_barra))
    pygame.draw.rect(tela, cor_barra2, (LARGURA - 50, barra_2_y, largura_barra, altura_barra))
    
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

    # Obter valores das trackbars para a primeira cor (Cor1)
    lh1 = cv2.getTrackbarPos("LH1", "Filtros")
    ls1 = cv2.getTrackbarPos("LS1", "Filtros")
    lv1 = cv2.getTrackbarPos("LV1", "Filtros")
    uh1 = cv2.getTrackbarPos("UH1", "Filtros")
    us1 = cv2.getTrackbarPos("US1", "Filtros")
    uv1 = cv2.getTrackbarPos("UV1", "Filtros")

    # Obter valores das trackbars para a segunda cor (Cor2)
    lh2 = cv2.getTrackbarPos("LH2", "Filtros")
    ls2 = cv2.getTrackbarPos("LS2", "Filtros")
    lv2 = cv2.getTrackbarPos("LV2", "Filtros")
    uh2 = cv2.getTrackbarPos("UH2", "Filtros")
    us2 = cv2.getTrackbarPos("US2", "Filtros")
    uv2 = cv2.getTrackbarPos("UV2", "Filtros")

    # Atualizar os limites de cor
    limite_inferior_cor1 = np.array([lh1, ls1, lv1])
    limite_superior_cor1 = np.array([uh1, us1, uv1])

    limite_inferior_cor2 = np.array([lh2, ls2, lv2])
    limite_superior_cor2 = np.array([uh2, us2, uv2])

    # Criar máscaras para as duas cores usando os limites atualizados
    mascara_cor1 = cv2.inRange(hsv, limite_inferior_cor1, limite_superior_cor1)
    mascara_cor2 = cv2.inRange(hsv, limite_inferior_cor2, limite_superior_cor2)

    # Aplicar operações de morfologia para remover ruídos
    mascara_cor1 = cv2.erode(mascara_cor1, None, iterations=2)
    mascara_cor1 = cv2.dilate(mascara_cor1, None, iterations=2)

    mascara_cor2 = cv2.erode(mascara_cor2, None, iterations=2)
    mascara_cor2 = cv2.dilate(mascara_cor2, None, iterations=2)

    # Encontrar contornos para determinar as posições das barras
    contornos_cor1, _ = cv2.findContours(mascara_cor1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_cor2, _ = cv2.findContours(mascara_cor2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Atualizar a posição da primeira barra (Cor1)
    if len(contornos_cor1) > 0:
        maior_contorno_cor1 = max(contornos_cor1, key=cv2.contourArea)
        if cv2.contourArea(maior_contorno_cor1) > 1000:  # Garantir que o contorno não seja muito pequeno
            _, y, _, h = cv2.boundingRect(maior_contorno_cor1)
            barra_1_y = y * 2 if y * 2 > 0 else 0
            barra_1_y = min(barra_1_y, ALTURA - altura_barra)
    else:
        # Manter a barra no meio se não houver rastreamento
        barra_1_y = ALTURA // 2 - altura_barra // 2

    # Atualizar a posição da segunda barra (Cor2)
    if len(contornos_cor2) > 0:
        maior_contorno_cor2 = max(contornos_cor2, key=cv2.contourArea)
        if cv2.contourArea(maior_contorno_cor2) > 1000:  # Garantir que o contorno não seja muito pequeno
            _, y, _, h = cv2.boundingRect(maior_contorno_cor2)
            barra_2_y = y * 2 if y * 2 > 0 else 0
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

    # Calcular cores das barras a partir dos limites HSV
    # Representativo para a primeira cor (Cor1)
    h_cor1 = (lh1 + uh1) // 2
    s_cor1 = (ls1 + us1) // 2
    v_cor1 = (lv1 + uv1) // 2
    cor_barra1 = hsv_para_rgb(h_cor1, s_cor1, v_cor1)

    # Representativo para a segunda cor (Cor2)
    h_cor2 = (lh2 + uh2) // 2
    s_cor2 = (ls2 + us2) // 2
    v_cor2 = (lv2 + uv2) // 2
    cor_barra2 = hsv_para_rgb(h_cor2, s_cor2, v_cor2)

    # Desenhar os elementos do jogo com cores atualizadas
    desenhar_pong(cor_barra1, cor_barra2)

    # Criar a imagem para exibir na janela "Filtros"
    # Para a primeira cor (Cor1)
    resultado_cor1 = cv2.bitwise_and(frame, frame, mask=mascara_cor1)
    keypoints_cor1 = cv2.findContours(mascara_cor1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for kp in keypoints_cor1:
        (x, y), radius = cv2.minEnclosingCircle(kp)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(resultado_cor1, center, radius, (255, 255, 255), 3)

    # Para a segunda cor (Cor2)
    resultado_cor2 = cv2.bitwise_and(frame, frame, mask=mascara_cor2)
    keypoints_cor2 = cv2.findContours(mascara_cor2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for kp in keypoints_cor2:
        (x, y), radius = cv2.minEnclosingCircle(kp)
        center = (int(x), int(y))
        radius = int(radius)
        cv2.circle(resultado_cor2, center, radius, (255, 255, 255), 3)

    # Combinar as duas imagens lado a lado
    resultado_combinado = np.hstack((resultado_cor1, resultado_cor2))
    resultado_combinado = cv2.resize(resultado_combinado, (1080, 480))
    cv2.imshow("Filtros", resultado_combinado)

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
