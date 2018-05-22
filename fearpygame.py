import pygame
import numpy as np
from numpy import random

N = 5000
A = 50


# EXIT=vector(0,A/2,0)


class Agent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.color = (0, 0, 0)
        self.image = pygame.Surface([10, 10])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        global N, A
        self.oxygen = 100
        self.speed = 5
        self.speedmax = 5
        self.radius = 5
        self.panic = N / A
        self.speedvector = np.array([1, 1])

    def GetPosition(self):
        return self.position

    def update(self,survivors,walls):
        self.rect.center = (self.speedvector[0] + self.rect.center[0], self.speedvector[1] + self.rect.center[1])
        collisions= pygame.sprite.spritecollide(self, walls, False)
        if( collisions):
            if(collisions[0].type == "horizont"):
                self.speedvector= self.speedvector * ([1,-1])
            if(collisions[0].type == "vertical"):
                self.speedvector = self.speedvector * ([-1,1])
    def move(self):
        self.rect.center = (self.speedvector[0] + self.rect.center[0], self.speedvector[1] + self.rect.center[1])


class Wall(pygame.sprite.Sprite):
    def __init__(self,x,y,xsize,ysize,type):
        pygame.sprite.Sprite.__init__(self)
        self.color = (15, 125, 125)
        self.image = pygame.Surface([xsize, ysize])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type


pygame.init()
screen = pygame.display.set_mode((800, 400))
survivors = pygame.sprite.Group()
walls = pygame.sprite.Group()
exits = pygame.sprite.Group()

walls.add(Wall(400,50,500,10,"horizont"))
walls.add(Wall(400,350,500,10,"horizont"))

walls.add(Wall(150,200,10,300,"vertical"))
walls.add(Wall(650,200,10,300,"vertical"))
exits.add(Wall(650,200,10,150,"vertical"))
for i in exits:
    i.image.fill(250,250,250)

# survivors.add(Agent(10, 10))
#losowanie polozenia dla Agentow
for i in range(N):
    x = random.randint(170, 600)
    y = random.randint(100, 300)
    survivors.add(Agent(x, y))

# randomowy wektor poruszania
for person in survivors:
    a = random.choice([-1, 1])
    b = random.choice([-1, 1])
    person.speedvector = person.speedvector * np.array([a, b])

clock = pygame.time.Clock()
while True:
    screen.fill((255, 255, 255))
    survivors.draw(screen)
    walls.draw(screen)
    exits.draw(screen)
    for agent in survivors:
        agent.update(survivors,walls)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #sys.exit()
    pygame.display.update()
    clock.tick(20)
