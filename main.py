import pygame

pygame.init()

back = (200, 255, 255)
mw = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Гра")


mw.fill(back)
clock = pygame.time.Clock()

game_over = False
you_win = False  # Додано для визначення перемоги

class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def outline(self, frame_color, thickness):
        pygame.draw.rect(mw, frame_color, self.rect, thickness)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)

class Picture(Area):
    def __init__(self, filename, x, y, width, height):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))

racket_x = 200
racket_y = 330
ball = Picture('ball.png', 160, 200, 50, 50)
platform = Picture('platform.png', racket_x, racket_y, 100, 30)

start_x = 5
start_y = 5
count = 9
monsters = []

for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Picture('enemy.png', x, y, 50, 50)
        monsters.append(d)
        x = x + 55
    count = count - 1

ball_speed_x = 5
ball_speed_y = 5

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Рух платформи
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and platform.rect.x > 0:
        platform.rect.x -= 5
    elif keys[pygame.K_RIGHT] and platform.rect.x < 400:
        platform.rect.x += 5

    # Швидкість м'яча
    ball.rect.x += ball_speed_x
    ball.rect.y += ball_speed_y

    # Зіткнення м'яча зі стінками
    if ball.rect.x <= 0 or ball.rect.x >= 450:
        ball_speed_x = -ball_speed_x

    if ball.rect.y <= 0:
        ball_speed_y = -ball_speed_y

    if ball.rect.colliderect(platform.rect):
        ball_speed_y = -ball_speed_y

    mw.fill(back)

    # Зіткнення м'яча з ворогом
    for m in monsters:
        if ball.rect.colliderect(m.rect):
            monsters.remove(m)
            ball_speed_y = -ball_speed_y
            

    # Оновлення позицій монстрів та м'яча
    for m in monsters:
        m.draw()

    platform.draw()
    ball.draw()

    # Вивід повідомлення про перемогу
    if not monsters:
        you_win = True
        font = pygame.font.Font(None, 36)
        text = font.render("YOU WIN!", True, (0, 0, 0))
        mw.blit(text, (200, 250))
        pygame.display.update()
        pygame.time.delay(2000)  # Затримка 2 секунди перед завершенням гри
        game_over = True



    if ball.rect.y > (platform.rect.y +20):
        font = pygame.font.Font(None, 36)
        text = font.render("YOU LOSE!", True, (255, 0, 0))
        mw.blit(text, (200, 250))
        pygame.display.update()
        pygame.time.delay(2000)  # Затримка 2 секунди перед завершенням гри
        game_over = True


    pygame.display.update()
    clock.tick(40)

pygame.quit()
