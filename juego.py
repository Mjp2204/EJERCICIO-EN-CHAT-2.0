import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Snake Game")

# Clase para la serpiente
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)  # Superficie transparente para el círculo
        pygame.draw.circle(self.image, WHITE, (10, 10), 10)  # Dibujar el círculo
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 8  # Velocidad inicial de la serpiente
        self.speed_x = 0
        self.speed_y = 0
        self.body = []  # Lista para almacenar los segmentos de la serpiente
        self.max_body_length = 1  # Longitud inicial del cuerpo de la serpiente

    def update(self):
        # Actualizar la posición de la cabeza
        self.rect.x += self.speed_x * self.speed
        self.rect.y += self.speed_y * self.speed

        # Comprobar los límites de la pantalla
        if self.rect.right < 0:
            self.rect.left = screen_width
        elif self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.bottom < 0:
            self.rect.top = screen_height
        elif self.rect.top > screen_height:
            self.rect.bottom = 0

        # Actualizar la posición de los segmentos del cuerpo
        self.body.insert(0, list(self.rect.center))  # Agregar la posición actual de la cabeza al principio de la lista

        # Ajustar la longitud del cuerpo
        if len(self.body) > self.max_body_length:
            self.body.pop()  # Eliminar el último segmento si la longitud del cuerpo es mayor que el máximo

    def grow(self):
        self.max_body_length += 1  # Incrementar la longitud máxima del cuerpo

    def increase_speed(self):
        self.speed += 1  # Aumentar la velocidad de la serpiente

# Clase para las bolitas
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Superficie para la bolita
        self.image.fill(RED)  # Color rojo para la bolita
        self.rect = self.image.get_rect()
        self.place_food()  # Colocar la bolita en una posición aleatoria

    def place_food(self):
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = random.randrange(0, screen_height - self.rect.height)

# Crear la serpiente
snake = Snake()

# Grupo de sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(snake)

# Grupo de bolitas
food = Food()
all_sprites.add(food)

# Puntaje inicial
score = 0

# Fuente de texto
font = pygame.font.Font(None, 36)

# Bucle principal del juego
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Manejar eventos de teclado para mover la serpiente
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake.speed_x = -1
                snake.speed_y = 0
            elif event.key == pygame.K_RIGHT:
                snake.speed_x = 1
                snake.speed_y = 0
            elif event.key == pygame.K_UP:
                snake.speed_y = -1
                snake.speed_x = 0
            elif event.key == pygame.K_DOWN:
                snake.speed_y = 1
                snake.speed_x = 0

    # Comprobar colisiones entre la serpiente y la bolita
    if pygame.sprite.collide_rect(snake, food):
        score += 1  # Incrementar el puntaje al comer una bolita
        snake.grow()  # Hacer crecer la serpiente
        snake.increase_speed()  # Aumentar la velocidad de la serpiente
        food.place_food()  # Colocar una nueva bolita

    # Actualizar los sprites
    all_sprites.update()

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar todos los sprites
    all_sprites.draw(screen)

    # Mostrar el puntaje en la pantalla
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Dibujar el cuerpo de la serpiente
    for segment in snake.body:
        pygame.draw.circle(screen, WHITE, segment, 10)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(15)  # Aumentamos la velocidad del juego

# Salir de Pygame
pygame.quit()
sys.exit()