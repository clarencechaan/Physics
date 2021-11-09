import pygame, random, math


def dist(x1, x2, y1, y2):
    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return d


class Ball:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.r, 1)

    def move(self):
        self.vy *= .99
        self.vx *= .99

        # print(b.ay, b.vy, b.y)
        self.vy += self.ay/FPS
        if abs(self.vy) > TERM_V:
            if self.vy >= TERM_V:
                self.vy = TERM_V
            elif self.vy < TERM_V:
                self.vy = -TERM_V
        self.y += self.vy/FPS

        # print(b.ax, b.vx, b.x)
        self.vx += self.ax/FPS
        if abs(self.vx) > TERM_V:
            if self.vx >= TERM_V:
                self.vx = TERM_V
            elif self.vx < TERM_V:
                self.vx = -TERM_V
        self.x += self.vx/FPS

        self.eat()

    def eat(self):
        for j in range(0, 20):
            if dist(star_list[j].x, self.x, star_list[j].y, self.y) < self.r:
                star_list[j].renew()
                self.r += 1


class Star:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.r, 0)

    def renew(self):
        while dist(self.x, b.x, self.y, b.y) < b.r:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
        self.draw()

# dimensions in pixels
HEIGHT = 480
WIDTH = 640
TERM_V = 200.0
WHITE = (255, 255, 255)
SCORE = 0

pygame.init()
screen=pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
background = background.convert()
screen.blit(background, (0, 0))
clock = pygame.time.Clock()

mainloop = True
FPS = 60
playtime = 0.0

b = Ball(WIDTH/2, HEIGHT/2, 10)

star_list = [None] * 20
for i in range(0, 20):
    star_list[i] = Star(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(0, 3))

while mainloop:
    milliseconds = clock.tick(FPS)
    playtime += milliseconds / 1000.0

    for event in pygame.event.get():
        # User presses QUIT-button.
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            # User presses ESCAPE-Key
            if event.key == pygame.K_ESCAPE:
                mainloop = False

    b.ay = 0
    b.ax = 0
    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_UP]:
        b.ay = -480
    if keys[pygame.K_DOWN]:
        b.ay = 480
    if keys[pygame.K_LEFT]:
        b.ax = -480
    if keys[pygame.K_RIGHT]:
        b.ax = 480

    screen.blit(background, (0, 0))
    b.move()
    b.draw()

    for i in range(0, 20):
        star_list[i].draw()

    # Print frame-rate and playtime in title-bar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    # Update PyGame display.
    pygame.display.flip()

pygame.quit()
