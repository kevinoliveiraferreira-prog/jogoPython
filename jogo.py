import pygame
import random
import sys

pygame.init()
LARGURA, ALTURA = 800, 600
CHAO_Y = 520
FPS = 60

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pular e Coletar - 20 Pontos")
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("arial", 28, bold=True)
fonte_grande = pygame.font.SysFont("arial", 46, bold=True)

# Cores
CEU = (107, 140, 255)
TERRA = (139, 69, 19)
GRAMA = (34, 177, 76)
MOEDA_COR = (255, 215, 0)
BRANCO = (255, 255, 255)

# Jogador
jogador = pygame.Rect(384, CHAO_Y - 38, 32, 38)
vel_y = 0
no_chao = True


def nova_moeda(jogador_x):
    while True:
        x = random.randint(40, LARGURA - 60)
        if abs(x - jogador_x) > 80:
            break
    y = random.randint(CHAO_Y - 150, CHAO_Y - 50)
    return pygame.Rect(x, y, 22, 22)


moeda = nova_moeda(jogador.x)
pontos = 0
venceu = False

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and venceu:
            jogador.x, jogador.y = 384, CHAO_Y - 38
            vel_y = 0
            pontos = 0
            moeda = nova_moeda(jogador.x)
            venceu = False

    if not venceu:
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.x -= 6
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.x += 6
        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and no_chao:
            vel_y = -14
            no_chao = False

        # Limites da tela
        jogador.x = max(0, min(LARGURA - jogador.width, jogador.x))

        # Gravidade e chão
        vel_y += 0.6
        jogador.y += int(vel_y)
        if jogador.bottom >= CHAO_Y:
            jogador.bottom = CHAO_Y
            vel_y = 0
            no_chao = True

        # Coletar moeda
        if jogador.colliderect(moeda):
            pontos += 1
            if pontos >= 20:
                venceu = True
            else:
                moeda = nova_moeda(jogador.x)

    # Desenho
    tela.fill(CEU)

    if not venceu:
        # Chão reto
        pygame.draw.rect(tela, TERRA, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
        pygame.draw.rect(tela, GRAMA, (0, CHAO_Y, LARGURA, 12))

        # Moeda
        pygame.draw.ellipse(tela, MOEDA_COR, moeda)

        # Personagem
        x, y = jogador.x, jogador.y
        pygame.draw.rect(tela, (220, 20, 60), (x + 2, y, 28, 8))
        pygame.draw.rect(tela, (255, 200, 150), (x + 4, y + 8, 24, 12))
        pygame.draw.rect(tela, (220, 20, 60), (x + 2, y + 20, 28, 8))
        pygame.draw.rect(tela, (30, 80, 220), (x + 4, y + 24, 24, 14))

        # Placar
        texto = fonte.render(f"Pontos: {pontos} / 20", True, BRANCO)
        tela.blit(texto, (20, 20))
    else:
        tela.fill((25, 25, 112))
        t1 = fonte_grande.render("VOCÊ FEZ 20 PONTOS!", True, MOEDA_COR)
        t2 = fonte.render("Pressione R para jogar novamente", True, BRANCO)
        tela.blit(t1, t1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 25)))
        tela.blit(t2, t2.get_rect(center=(LARGURA // 2, ALTURA // 2 + 30)))

    pygame.display.flip()
    relogio.tick(FPS)