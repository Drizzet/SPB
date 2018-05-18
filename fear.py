from vpython import *
N=1
A=50
EXIT=vector(0,A/2,0)







class Agent():
    def __init__(self,pos):
        global N,A
        self.position = pos
        self.body = sphere(pos=pos, radius=1,  color=color.white)
        self.oxygen=100
        self.speed=5
        self.speedmax=5
        self.radius=5
        self.panic=N/A
        self.speedvector=vector(1,1,0)
    def GetPosition(self):
        return self.position

    def Neighborhood(self):
        b = self.position
        n = []
        for j in range(len(walls)):
            x = walls[j].pos
            diff = b - x
            if (sqrt(pow(diff.x, 2) + pow(diff.y, 2) + pow(diff.z, 2)) < self.radius):
                n.append(j)
        return n


    def update(self):
        print(self.Neighborhood())
        self.position=self.position+self.speedvector*(0.00005)
        self.body.pos=self.position

class Wall(box):
    def __init__(self,position):
        box.__init__(self,pos=position, color=color.red)


walls=[]

for i in range (A+1):
    walls.append(Wall(vector(i,0,0)))
    if(i>((A/2)+1) or i<((A/2)-1)):
        walls.append(Wall(vector(0,i,0)))
    walls.append(Wall(vector(A,i,0)))
    walls.append(Wall(vector(i,A,0)))


survivors=[]
survivors.append(Agent(vector(5,5,0)))

while True:
    for e in survivors:
        rate(500)
        e.update()