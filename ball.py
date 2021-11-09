import pygame, random, math, numpy as np


def dist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u = ((x3 - x1) * px + (y3 - y1) * py) / something

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    d = math.sqrt(dx*dx + dy*dy)

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

        #print(b.ay, b.vy, b.y)
        self.vy += self.ay/FPS
        if abs(self.vy) > TERM_V:
            if self.vy >= TERM_V:
                self.vy = TERM_V
            elif self.vy < TERM_V:
                self.vy = -TERM_V
        self.y += self.vy/FPS

        #print(b.ax, b.vx, b.x)
        self.vx += self.ax/FPS
        if abs(self.vx) > TERM_V:
            if self.vx >= TERM_V:
                self.vx = TERM_V
            elif self.vx < TERM_V:
                self.vx = -TERM_V
        self.x += self.vx/FPS


class Laser:

    def __init__(self):
        x_len = random.randint(-50, 50)
        y_len = math.sqrt(50 ** 2 - x_len ** 2)
        y_len = random.choice([y_len, -y_len])

        lw = (0, random.randint(0, HEIGHT))
        rw = (WIDTH, random.randint(0, HEIGHT))
        tw = (random.randint(0, WIDTH), 0)
        bw = (random.randint(0, WIDTH), HEIGHT)

        (x, y) = random.choice([lw, rw, tw, bw])

        if x_len > 0 and y_len > 0:
            (x, y) = random.choice([lw, tw])
        elif x_len < 0 and y_len > 0:
            (x, y) = random.choice([rw, tw])
        elif x_len > 0 and y_len < 0:
            (x, y) = random.choice([lw, bw])
        elif x_len < 0 and y_len < 0:
            (x, y) = random.choice([rw, bw])

        self.x = x
        self.y = y
        self.x_len = x_len
        self.y_len = y_len

    def draw(self):
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x - self.x_len, self.y - self.y_len), 1)

    def move(self):
        self.x += self.x_len/20.0
        self.y += self.y_len/20.0

    def out_of_range(self):
        # print(self.x, self.y)
        return (self.x - self.x_len > WIDTH + 100
                or self.y - self.y_len > HEIGHT + 100
                or self.x - self.x_len < -100
                or self.y - self.y_len < -100)

    def check_hit(self, x, y):
        d = dist(self.x, self.y, self.x - self.x_len, self.y - self.y_len, x, y)
        if d < 9:
            print("Score: " + str(SCORE))
            pygame.quit()

# dimensions in pixels
HEIGHT = 480
WIDTH = 640
TERM_V = 200.0
WHITE = (255, 255, 255)
NUM_LASERS = 20
SCORE = 0

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
background = pygame.Surface(screen.get_size())
background.fill((0, 0, 0))
background = background.convert()
screen.blit(background, (0,0))
clock = pygame.time.Clock()

mainloop = True
FPS = 60
playtime = 0.0

b = Ball(WIDTH/2, HEIGHT/2, 10)

laser_list = [None] * NUM_LASERS
for i in range(0, NUM_LASERS):
    laser_list[i] = Laser()

myfont = pygame.font.SysFont("Monospace", 20)

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
    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP]:
        b.ay = -480
    if keys[pygame.K_DOWN]:
        b.ay = 480
    if keys[pygame.K_LEFT]:
        b.ax = -480
    if keys[pygame.K_RIGHT]:
        b.ax = 480

    screen.blit(background, (0, 0))
    label = myfont.render("Score: " + str(SCORE), 1, (255, 255, 255))
    screen.blit(label, (260, 10))
    b.move()
    b.draw()
    for i in range(0, NUM_LASERS):
        if laser_list[i].out_of_range():
            SCORE += 5
            laser_list[i] = Laser()
        laser_list[i].move()
        laser_list[i].draw()
        laser_list[i].check_hit(b.x, b.y)

    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(text)

    # Update Pygame display.
    pygame.display.flip()

pygame.quit()