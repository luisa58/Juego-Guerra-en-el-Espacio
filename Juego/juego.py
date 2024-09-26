import pygame
import random

# Inicialización de Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tamaño de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Jugador (Fortaleza)
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 20

# Cargar imágenes
background_image = pygame.image.load('space.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load('nave-extraterrestre.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

asteroid_image = pygame.image.load('platillo-volador.png')
asteroid_image = pygame.transform.scale(asteroid_image, (40, 40))

# Inicializar pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defensor de la Fortaleza")

# Clase Jugador (Fortaleza)
def draw_player(x, y):
    screen.blit(player_image, (x, y))

# Clase Bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()

# Clase Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - 40)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = random.randrange(-100, -40)
            self.rect.x = random.randrange(0, SCREEN_WIDTH - 40)

# Clase Menú
def show_menu(selected_option):
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 74)
    title = font.render("DEFENSOR DE LA FORTALEZA", True, WHITE)
    screen.blit(title, [50, 100])

    font = pygame.font.Font(None, 36)
    options = ["Iniciar Juego", "Controles", "Cómo Jugar", "Salir"]

    for i, option in enumerate(options):
        color = GREEN if i == selected_option else WHITE
        text = font.render(f"{i+1}. {option}", True, color)
        screen.blit(text, [200, 250 + i * 50])

    pygame.display.flip()

# Mostrar controles
def show_controls():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Controles: ", True, WHITE)
    screen.blit(text, [50, 50])
    text = font.render("Mover izquierda: Flecha izquierda", True, WHITE)
    screen.blit(text, [50, 100])
    text = font.render("Mover derecha: Flecha derecha", True, WHITE)
    screen.blit(text, [50, 150])
    text = font.render("Disparar: Barra espaciadora", True, WHITE)
    screen.blit(text, [50, 200])
    text = font.render("Presiona 'Esc' para volver", True, WHITE)
    screen.blit(text, [50, 300])
    pygame.display.flip()

    # Esperar a que el jugador presione 'Esc' para salir
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Mostrar cómo jugar
def show_how_to_play():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Cómo Jugar: ", True, WHITE)
    screen.blit(text, [50, 50])
    text = font.render("Defiende la fortaleza de los enemigos.", True, WHITE)
    screen.blit(text, [50, 100])
    text = font.render("Usa las teclas para moverte y disparar.", True, WHITE)
    screen.blit(text, [50, 150])
    text = font.render("Presiona 'Esc' para volver", True, WHITE)
    screen.blit(text, [50, 300])
    pygame.display.flip()

    # Esperar a que el jugador presione 'Esc' para salir
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# Función para pausar el juego
def pause_game():
    paused = True
    font = pygame.font.Font(None, 74)
    while paused:
        screen.blit(background_image, (0, 0))
        text = font.render("Juego Pausado", True, WHITE)
        screen.blit(text, [SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100])
        text = font.render("Presiona 'C' para continuar", True, WHITE)
        screen.blit(text, [SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2])
        text = font.render("Presiona 'Esc' para volver al menú", True, WHITE)
        screen.blit(text, [SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 100])
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    return True  # Volver al menú

# Función para el juego principal
def game_loop():
    # Variables del jugador
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
    player_speed = 5

    # Vidas del jugador
    lives = 5

    # Grupo de balas
    bullets = pygame.sprite.Group()

    # Grupo de enemigos
    enemies = pygame.sprite.Group()
    for i in range(5):  # Cantidad estándar de enemigos
        enemy = Enemy()
        enemies.add(enemy)

    # Contador de enemigos derrotados
    score = 0

    # Bucle principal del juego
    game_over = False
    clock = pygame.time.Clock()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausar el juego
                    if pause_game():
                        return  # Volver al menú si se presiona 'Esc' durante la pausa

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            bullet = Bullet(player_x + PLAYER_WIDTH // 2 - 2, player_y)
            bullets.add(bullet)

        # Actualizar balas y enemigos
        bullets.update()
        enemies.update()

        # Colisiones bala-enemigo
        for bullet in bullets:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in enemy_hit_list:
                bullets.remove(bullet)
                score += 1
                # Crear nuevo enemigo
                new_enemy = Enemy()
                enemies.add(new_enemy)

        # Colisiones enemigo-jugador
        for enemy in enemies:
            if enemy.rect.colliderect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT):
                enemies.remove(enemy)
                lives -= 1
                new_enemy = Enemy()
                enemies.add(new_enemy)
                if lives <= 0:
                    game_over = True

        # Dibujar todo
        screen.blit(background_image, (0, 0))
        draw_player(player_x, player_y)
        bullets.draw(screen)
        enemies.draw(screen)

        # Mostrar puntuación y vidas
        font = pygame.font.Font(None, 36)
        score_text = font.render("Puntuación: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])

        lives_text = font.render("Vidas: " + str(lives), True, WHITE)
        screen.blit(lives_text, [10, 50])

        pygame.display.flip()
        clock.tick(60)

# Menú de inicio
selected_option = 0
show_menu(selected_option)

# Esperar a que el jugador seleccione una opción del menú
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % 4
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % 4
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Iniciar juego
                    game_loop()
                elif selected_option == 1:  # Controles
                    show_controls()
                elif selected_option == 2:  # Cómo jugar
                    show_how_to_play()
                elif selected_option == 3:  # Salir
                    waiting = False
            show_menu(selected_option)

pygame.quit()
