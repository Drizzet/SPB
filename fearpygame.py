import pygame
import numpy as np
from numpy import random

N = 50
A = 50 * 30
T = 500
ESCAPED = 0
DIED = 0
pygame.init()
screen = pygame.display.set_mode((800, 400))
myfont = pygame.font.SysFont("monospace", 15)
clock = pygame.time.Clock()


class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y, t):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0, 0, 0)
        self.image = pygame.Surface([10, 10])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.state = "alive"
        global N, A
        self.oxygen = t
        self.speed = 5
        self.speedmax = 5
        self.radius = 10
        self.panic = N / A
        self.speedvector = np.array([1, 1])

    def GetPosition(self):
        return self.rect.center

    def update(self, survivors, walls, exits):
        global ESCAPED
        global N
        global A
        self.oxygen = self.oxygen - 1
        self.move()

        suma = 0
        n = 0
        for neighbour in survivors:
            if (pygame.sprite.collide_circle(self, neighbour) == True):
                # h = (3.14 * self.radius * self.radius * ((N-ESCAPED)/A))
                suma = suma + neighbour.speedvector
                n = n + 1

        collisions = pygame.sprite.spritecollide(self, walls, False)
        escapes = pygame.sprite.spritecollide(self, exits, False)

        if (escapes):
            ESCAPED = ESCAPED + 1
            survivors.remove(self)

        #        if(n>0):
        #                 suma = suma.round()
        #               if ((suma / ([n,n])) != ([0,0])).all() :
        #                   self.speedvector = suma / ([n,n])
        #                   print(self.speedvector,suma,n)

        if (collisions):
            if (collisions[0].type == "horizont"):
                self.speedvector = self.speedvector * ([1, -1])
            if (collisions[0].type == "vertical"):
                self.speedvector = self.speedvector * ([-1, 1])
            if (collisions[0].type == "dead"):
                self.speedvector = self.speedvector * ([-1, -1])

        if (self.oxygen == 0):
            global DIED
            DIED = DIED + 1
            self.image.fill((250, 0, 0))
            self.speedvector = self.speedvector * ([0, 0])
            # walls.add(Wall(self.GetPosition()[0],self.GetPosition()[1], 10, 10, "dead", (250, 0, 0)))
            # survivors.remove(self)

        if (self.oxygen <= T / 2 and self.oxygen > 0):
            self.image.fill((0, 150, 0))
            self.state = "ill"

    def move(self):
        self.rect.center = (self.speedvector[0] + self.rect.center[0], self.speedvector[1] + self.rect.center[1])


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, xsize, ysize, type, color):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.image = pygame.Surface([xsize, ysize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type


survivors = pygame.sprite.Group()
walls = pygame.sprite.Group()
exits = pygame.sprite.Group()

walls.add(Wall(400, 50, 500, 10, "horizont", (15, 125, 125)))
walls.add(Wall(400, 350, 500, 10, "horizont", (15, 125, 125)))
walls.add(Wall(150, 200, 10, 300, "vertical", (15, 125, 125)))
walls.add(Wall(650, 200, 10, 300, "vertical", (15, 125, 125)))

exits.add(Wall(650, 200, 10, 50, "exit", (125, 125, 125)))
exits.add(Wall(150, 200, 10, 50, "exit", (125, 125, 125)))
# survivors.add(Agent(10, 10))
# losowanie polozenia dla Agentow
for i in range(N):
    x = random.randint(170, 600)
    y = random.randint(100, 300)
    t = random.randint(T - 300, T)
    survivors.add(Agent(x, y, t))

# randomowy wektor poruszania
for person in survivors:
    a = random.choice([-1, 1])
    b = random.choice([-1, 1])
    person.speedvector = person.speedvector * np.array([a, b])

while True:
    screen.fill((255, 255, 255))
    survivors.draw(screen)
    walls.draw(screen)
    exits.draw(screen)
    label = myfont.render("Escaped: " + str(ESCAPED), 1, (0, 0, 0))
    screen.blit(label, (10, 100))
    label = myfont.render("Died: " + str(DIED), 1, (0, 0, 0))
    screen.blit(label, (10, 120))
    for agent in survivors:
        if(agent.oxygen >= 0):
            agent.update(survivors, walls, exits)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()
    pygame.display.update()
    clock.tick(20)
