import pygame
import numpy as np
from numpy import random

N = 1
A = 50


# EXIT=vector(0,A/2,0)


class Agent(pygame.Rect):
    def __init__(self, x, y):
        global N, A
        self.color = (0, 0, 0)
        super(Agent, self).__init__(x, y, 3, 3)
        self.oxygen = 100
        self.speed = 5
        self.speedmax = 5
        self.radius = 5
        self.panic = N / A
        self.speedvector = np.array([1, 1, 0])

    def GetPosition(self):
        return self.position

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self, 0)


#   def check(self):
#     if (self.x == 0 or self.x == A):
#       self.speedvector = self.speedvector * ([-1, 1, 1])
#     if (self.y == 0 or self.y == A):
#       self.speedvector = self.speedvector * ([1, -1, 1])


# class Wall(pygame.Rect):
#     def __init__(self,x,y):
#         self.color = (5, 5, 5)
#         super(Wall,self).__init__(x,y)
#
#     def draw(self,screen,color,fill):
#         pygame.draw.rect(screen, color, self,fill)


pygame.init()
screen = pygame.display.set_mode((450, 450))

survivors = []

#losowanie polozenia dla Agentow
for i in range(10):
    x = random.randint(-A + 1, A - 1)
    y = random.randint(-A + 1, A - 1)
    survivors.append(Agent(x, y))

# randomowy wektor poruszania
for person in survivors:
    a = random.randint(-1, 1)
    b = random.randint(-1, 1)
    print(person.speedvector, a, b)
    person.speedvector = person.speedvector * np.array([a, b, 0])
    print(person.speedvector)

clock = pygame.time.Clock()
while True:
    screen.fill((255, 255, 255))
    for e in survivors:
        e.draw(screen)
    pygame.display.update()
    clock.tick(20)
