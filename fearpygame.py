# from __future__ import division
import pygame
import numpy as np
from numpy import random
import math

N = 50
A = 50 * 30
T = 1000
Time = 0
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
        self.speed = 1
        self.speedmax = 5
        self.radius = 20
        self.panic = N / A
        self.speedvector = np.array([1.0, 1.0])
        self.point = [0, 0]
        self.iteration=random.randint(10,50)


    def computeVector(self):
        # print((float)(self.point[0] - self.GetPosition()[0]+ 0.0) / (self.point[0]+ 0.0))
        # self.speedvector[0] = (float)(self.point[0] - self.GetPosition()[0]+ 0.0) / (self.point[0]+ 0.0)
        # self.speedvector[1] = (float)(self.point[1] - self.GetPosition()[1]+ 0.0) / (self.point[0]+ 0.0)
        self.speedvector[0] = (float)(self.point[0] - self.GetPosition()[0]+ 0.0) / 100.0
        self.speedvector[1] = (float)(self.point[1] - self.GetPosition()[1]+ 0.0) / 100.0

    def GetPosition(self):
        pos = np.array([self.rect.center[0],self.rect.center[1]])
        return pos

    def update(self, survivors, walls, exits):
        global ESCAPED
        global N
        global A
        self.oxygen = self.oxygen - 1
        print(self.point, self.GetPosition(), self.speedvector)
        self.computeVector()
        self.move()
        self.iteration -= 1
        if(self.iteration<0):
            self.iteration = random.randint(10, 50)
            x = random.randint(170, 600)
            y = random.randint(100, 300)
            self.point = [x,y]

        suma = 0
        n = 0

        neighbours = list(survivors)
        neighbours.remove(self)

        for neighbour in neighbours:
            if (pygame.sprite.collide_circle(self, neighbour) == True):
                if (neighbour.state != "dead"):
                    self.speedvector = self.speedvector * -1
                    suma = suma + neighbour.speedvector
                    n = n + 1

        collisions = pygame.sprite.spritecollide(self, walls, False)
        escapes = pygame.sprite.spritecollide(self, exits, False)

        survivorscollisions = pygame.sprite.spritecollide(self, walls, False)

        if (escapes):
            if (escapes[0].GetPosition()[0] - self.GetPosition()[0] < 0):
                self.speedvector[0] = -1
            else:
                self.speedvector[0] = 1
            if (escapes[0].GetPosition()[1] - self.GetPosition()[1] < 0):
                self.speedvector[1] = -1
            else:
                self.speedvector[1] = 1
            ESCAPED = ESCAPED + 1
            self.state = "found"
            # survivors.remove(self)

        #        if(n>0):
        #
        # suma = suma.round()
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
            self.state = "dead"
            self.image.fill((250, 0, 0))
            self.speedvector = self.speedvector * ([0, 0])
            # walls.add(Wall(self.GetPosition()[0],self.GetPosition()[1], 10, 10, "dead", (250, 0, 0)))
            # survivors.remove(self)

        if (self.oxygen <= T / 2 and self.oxygen > 0 and self.state != "found"):
            self.image.fill((0, 150, 0))
            self.state = "ill"

    def move(self):
        self.rect.center = (self.speed* round(self.speedvector[0],2) + self.rect.center[0],self.speed* round(self.speedvector[1],2) + self.rect.center[1])


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

    def GetPosition(self):
        return self.rect.center


survivors = pygame.sprite.Group()
walls = pygame.sprite.Group()
exits = pygame.sprite.Group()

walls.add(Wall(400, 50, 500, 10, "horizont", (15, 125, 125)))
walls.add(Wall(400, 350, 500, 10, "horizont", (15, 125, 125)))
walls.add(Wall(150, 200, 10, 300, "vertical", (15, 125, 125)))
walls.add(Wall(650, 200, 10, 300, "vertical", (15, 125, 125)))

# sprawdzanie odleglosci 20 jednostek do ok exit
exits.add(Wall(650, 200, 10, 70, "exit", (15, 125, 125)))
exits.add(Wall(150, 200, 10, 70, "exit", (15, 125, 125)))

exits.add(Wall(650, 200, 20, 50, "exit", (250, 250, 250)))
exits.add(Wall(150, 200, 20, 50, "exit", (250, 250, 250)))

# survivors.add(Agent(10, 10))

# losowanie polozenia dla Agentow
for i in range(N):
    x = random.randint(170, 600)
    y = random.randint(100, 300)
    t = random.randint(T - 300, T)
    survivors.add(Agent(x, y, t))

# randomowy wektor poruszania
for person in survivors:
    x = random.randint(170, 600)
    y = random.randint(100, 300)
    person.point =np.array([x, y])

while True:
    screen.fill((255, 255, 255))
    walls.draw(screen)
    exits.draw(screen)
    survivors.draw(screen)

    label = myfont.render("Time: " + str(Time), 1, (0, 0, 0))
    screen.blit(label, (10, 20))
    label = myfont.render("Escaped: " + str(ESCAPED), 1, (0, 0, 0))
    screen.blit(label, (10, 40))
    label = myfont.render("Died: " + str(DIED), 1, (0, 0, 0))
    screen.blit(label, (10, 60))

    Time = Time + 1
    for agent in survivors:
        if (agent.oxygen >= 0):
            if (agent.state != "found"):
                agent.update(survivors, walls, exits)
            else:
                agent.move()
    if (Time == T):
        pygame.quit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # sys.exit()
    pygame.display.update()
    clock.tick(30)
