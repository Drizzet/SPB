import pygame
N=1
A=50
# EXIT=vector(0,A/2,0)







class Agent(pygame.Rect):
    def __init__(self,x,y):
        global N,A
        self.color = (0, 0, 0)
        super(Agent, self).__init__(x, y,3,3)
        self.oxygen=100
        self.speed=5
        self.speedmax=5
        self.radius=5
        self.panic=N/A
        # self.speedvector=vector(1,1,0)
    def GetPosition(self):
        return self.position
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self,(0,0,0))



# class Wall(pygame.Rect):
#     def __init__(self,x,y):
#         self.color = (5, 5, 5)
#         super(Wall,self).__init__(x,y)
#
#     def draw(self,screen,color,fill):
#         pygame.draw.rect(screen, color, self,fill)



pygame.init()
screen = pygame.display.set_mode((450, 450))

survivors=[]

survivors.append(Agent(5,5))

while True:
    screen.fill((255, 255, 255))
    for e in survivors:
        e.draw(screen)
