import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900

# Создание окна игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("peace indrivers")

# Загрузка изображений
background_image = pygame.image.load("background.jpg")
player_image = pygame.image.load("player.png")
bullet_image = pygame.image.load("bullet.png")
enemy_image = pygame.image.load("enemy.png")
beam_image = pygame.image.load("beam.png")

# Загрузка звуков
beam_sound = pygame.mixer.Sound("laser.mp3")
kill_sound = pygame.mixer.Sound("enemykill.mp3")
next_stage_sound = pygame.mixer.Sound("next_stage.mp3")
gun_sound = pygame.mixer.Sound("gunshot.mp3")


# Размеры объектов
SHIP_SIZE = player_image.get_width()
BULLET_SIZE = bullet_image.get_size()
ENEMY_SIZE = enemy_image.get_width()
BEAM_SIZE = beam_image.get_size()

# Скорость движения объектов
SHIP_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 3
ENEMY_DROP_SPEED = 69   # )))
BEAM_SPEED = 2

clock = pygame.time.Clock()


# Класс для создания игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - SHIP_SIZE // 2
        self.rect.y = SCREEN_HEIGHT - SHIP_SIZE - 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= SHIP_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += SHIP_SPEED

        # Проверка на выход за границы экрана
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - SHIP_SIZE:
            self.rect.x = SCREEN_WIDTH - SHIP_SIZE


# Класс для создания пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        gun_sound.play()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.hit = False

    def update(self):
        if not self.hit:
            self.rect.y -= BULLET_SPEED
            if self.rect.y < 0:
                self.kill()


# Класс для создания врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED

        # Проверка на достижение края экрана
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - ENEMY_SIZE:
            self.direction *= -1
            self.rect.y += ENEMY_DROP_SPEED


# Класс для создания снарядов врагов
class Beam(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        beam_sound.play()
        self.image = beam_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += BEAM_SPEED
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()


# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
beams = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)


# Функция для создания врагов
def create_enemies(level):
    if level == 1:
        num_enemies = 20
        k = 4
    elif level == 2:
        num_enemies = 40
        k = 5
    elif level == 3:
        num_enemies = 60
        k = 6
    for i in range(k):
        for j in range(num_enemies // 10):
            enemy = Enemy(j * (ENEMY_SIZE + 5) + 50, i * (ENEMY_SIZE + 5) + 50)
            all_sprites.add(enemy)
            enemies.add(enemy)


# Переменная для хранения счета
score = 0

# Шрифт для отображения счета и сообщений
font = pygame.font.Font(None, 36)

def show_start_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    title_text = font.render("Peace indrivers", True, (255, 255, 255))
    start_text = font.render("Нажмите Enter, чтобы начать", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

# Отображение стартового экрана
def show_end_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    end_text = font.render("Конец игры", True, (255, 0, 0))
    restart_text = font.render("Нажмите Enter, чтобы выйти", True, (255, 255, 255))
    screen.blit(end_text, (SCREEN_WIDTH // 2 - end_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

# Отображение стартового экрана
show_start_screen()

# Ожидание нажатия клавиши Enter
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False
                score = 0
                level = 1
                create_enemies(level)
                show_start_screen()

# Ожидание нажатия клавиши Enter
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                waiting = False
# Уровень игры
level = 1
create_enemies(level)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not bullets.sprites():
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x + SHIP_SIZE // 2 - BULLET_SIZE[0] // 2
                    bullet.rect.y = player.rect.y - BULLET_SIZE[1]
                    all_sprites.add(bullet)
                    bullets.add(bullet)


    # Обновление спрайтов
    all_sprites.update()

    # Проверка столкновений пули с врагами
    for bullet in bullets:
        if not bullet.hit:
            enemy_collisions = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_collisions:
                kill_sound.play()
                bullet.hit = True
                bullet.kill()
                score += 10

    # Проверка столкновений врагов с игроком
    enemy_collisions = pygame.sprite.spritecollide(player, enemies, True)
    if enemy_collisions:
        running = False
        show_end_screen()
        pygame.display.flip()
        time.sleep(3)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        score = 0
                        level = 1
                        create_enemies(level)
                        show_start_screen()

    # Атака врагов снарядами
    for enemy in enemies:
        if random.randint(0, 1000) < 2 and len(beams) < 5:
            beam = Beam(enemy.rect.x + ENEMY_SIZE // 2 - BEAM_SIZE[0] // 2, enemy.rect.y + ENEMY_SIZE)
            all_sprites.add(beam)
            beams.add(beam)

    # Проверка столкновений снарядов врагов с игроком
    beam_collisions = pygame.sprite.spritecollide(player, beams, True)
    if beam_collisions:
        running = False
        show_end_screen()
        pygame.display.flip()
        time.sleep(3)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        score = 0
                        level = 1
                        create_enemies(level)
                        show_start_screen()
    # Проверка окончания уровня
    if len(enemies) == 0:
        next_stage_sound.play()
        if level == 3:
            running = False
            show_end_screen()
            pygame.display.flip()
            time.sleep(3)
        else:
            level += 1
            create_enemies(level)
            level_text = font.render("Этап " + str(level - 1) + " пройден", True, (255, 255, 255))
            screen.blit(level_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            time.sleep(3)

    # Отрисовка
    screen.blit(background_image, (0, 0))
    all_sprites.draw(screen)

    # Отрисовка счета и уровня
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    pygame.display.flip()

    clock.tick(60)


pygame.quit()

