import pygame
import random
import sys
import math
import matplotlib.pyplot as plt
import time

#
#PRESS P for plot and pause
#PRESS D for debug
#

DELAY = 0
DEBUG = True
SAVE_SCREENSHOT = False

RED= (255,0,0)
BLUE = (0,0,255)
GRAY = (127,127,127)
WHITE = (255,255,255)
BLACK = (0,0,0)

GRID_SIZE = 100
SCREEN_SIZE=800


#ASSIGNMENT PARAMETERS
"""
DELAY = 0
INIT_WOLVES=100
INIT_RABBITS=900
LIFE_RABBIT=100 #a) 100 #b) 50
LIFE_WOLF=50 #not eating
REPLICATE_PROBABILITY_RABBIT=0.02
REPLICATE_PROBABILITY_WOLF=0.02
EATING_DISTANCE=5
EATING_PROBABILITY=0.02
SIGMA=0.5 #a)5 #c) 0.5
"""



#TUNE PARAMETERS
"""
INIT_WOLVES=20
INIT_RABBITS=400
LIFE_RABBIT=90 
LIFE_WOLF= 90
REPLICATE_PROBABILITY_RABBIT=0.035
REPLICATE_PROBABILITY_WOLF=0.045
EATING_DISTANCE=5
EATING_PROBABILITY=0.15
SIGMA=0.5
"""

#cool
"""
INIT_WOLVES=100
INIT_RABBITS=600
LIFE_RABBIT=30
LIFE_WOLF=70
REPLICATE_PROBABILITY_RABBIT=0.09
REPLICATE_PROBABILITY_WOLF=0.016
EATING_DISTANCE=5
EATING_PROBABILITY=0.5
SIGMA=0.5
"""


#ok best

INIT_WOLVES=90
INIT_RABBITS=100
LIFE_RABBIT=80
LIFE_WOLF=100
REPLICATE_PROBABILITY_RABBIT=0.058
REPLICATE_PROBABILITY_WOLF=0.085
EATING_DISTANCE=5
EATING_PROBABILITY=0.21
SIGMA=0.5

#rounded
"""
INIT_WOLVES=90
INIT_RABBITS=100
LIFE_RABBIT=80
LIFE_WOLF=100
REPLICATE_PROBABILITY_RABBIT=0.06
REPLICATE_PROBABILITY_WOLF=0.085
EATING_DISTANCE=5
EATING_PROBABILITY=0.2
SIGMA=0.5
"""

"""
INIT_WOLVES=200
INIT_RABBITS=900
LIFE_RABBIT=100
LIFE_WOLF=50
REPLICATE_PROBABILITY_RABBIT=0.07
REPLICATE_PROBABILITY_WOLF=0.1
EATING_DISTANCE=5
EATING_PROBABILITY=0.03
SIGMA=0.5
"""


#init Cell lists
CL={}
#N_CELLS=GRID_SIZE
#CELL_SIZE=2*EATING_DISTANCE
CELL_SIZE=EATING_DISTANCE
N_CELLS = GRID_SIZE//CELL_SIZE
for x in range(N_CELLS):
    for y in range(N_CELLS):
        CL[(x,y)]={}

class Cell:
    
    #n_wolves=0
    #n_rabbits=0

    #allCells=[]
    #wolves=[]
    #rabbits=[]

    #maybe faster with dictionary
    ids=0
    allCells={}
    wolves={}
    rabbits={}

    RABBIT = 0
    WOLF = 1
    
    SIZE= SCREEN_SIZE//GRID_SIZE
    #SIZE=10
    
    ADJACENCY_DISTANCE=1 

    def __init__(self, posX, posY, type):
        self.id=Cell.ids+1
        Cell.ids+=1
        self.type=type
        self.posX=posX
        self.posY=posY
        self.age=0
        self.ate=0
        #if(type==Cell.EMPTY):
        #    self.color = (0,0,0)
        if(type==Cell.WOLF):
            self.color = RED
            #Cell.n_wolves+=1
            #Cell.wolves.append(self)
            Cell.wolves[self.id]=self

        if(type==Cell.RABBIT):
            self.color = BLUE
            self.age=random.randint(1,LIFE_RABBIT)
            #Cell.rabbits.append(self)
            #Cell.n_rabbits+=1
            Cell.rabbits[self.id]=self
            
        
        #Cell.allCells.append(self)
        Cell.allCells[self.id]=self
        #print(posX,posY)
        CL[(posX//CELL_SIZE,posY//CELL_SIZE)][self.id]=self
        
        #print(CL)
        
    def die(self):
        if(self.type==Cell.WOLF):
            #Cell.n_wolves-=1
            #Cell.wolves.remove(self)
            Cell.wolves.pop(self.id)
        if(self.type==Cell.RABBIT):
            #Cell.n_rabbits-=1
            #Cell.rabbits.remove(self)
            Cell.rabbits.pop(self.id)
        #Cell.allCells.remove(self)
        Cell.allCells.pop(self.id)
        CL[(self.posX//CELL_SIZE,self.posY//CELL_SIZE)].pop(self.id)

    def survive(self):
        if(self.type==Cell.WOLF):
            if(self.age>=LIFE_WOLF):
                self.die()
        
        if(self.type==Cell.RABBIT):
            if(self.age>=LIFE_RABBIT):
                self.die()

        self.age+=1
    
    def moveRandomly(self):
        #dx=random.choice([-1,0,1])
        #dy=random.choice([-1,0,1])
        
        dx = random.gauss(0,SIGMA)
        dy = random.gauss(0,SIGMA)
        new_posX = (self.posX + dx) % GRID_SIZE
        new_posY = (self.posY + dy) % GRID_SIZE

        if((self.posX//CELL_SIZE,self.posY//CELL_SIZE) != (new_posX//CELL_SIZE,new_posY//CELL_SIZE)):
            CL[(self.posX//CELL_SIZE,self.posY//CELL_SIZE)].pop(self.id)
            CL[(new_posX//CELL_SIZE,new_posY//CELL_SIZE)][self.id]=self

        self.posX=new_posX
        self.posY=new_posY

    def replicate(self):
        if(self.type==Cell.WOLF):
            for _ in range(self.ate):
                if(random.random()<=REPLICATE_PROBABILITY_WOLF):
                    Cell(self.posX, self.posY, self.type)

            self.ate=0
        if(self.type==Cell.RABBIT):
            if(random.random()<=REPLICATE_PROBABILITY_RABBIT):
                Cell(self.posX, self.posY, self.type)

    def eat(self):

        #NAIVE IMPLEMENTATION
        """
        #if(self.type==Cell.WOLF):
            for cell in Cell.rabbits:
                #if(cell.type==Cell.RABBIT and math.dist((self.posX,self.posY),(cell.posX,cell.posY))<EATING_DISTANCE and random.random()<EATING_PROBABILITY):
                if(math.dist((self.posX,self.posY),(cell.posX,cell.posY))<EATING_DISTANCE and random.random()<EATING_PROBABILITY):
                    cell.die()
                    self.ate+=1
                    self.age=0
        """
        #OPTIMIZED IMPLEMENTATION
        clx = self.posX//CELL_SIZE
        cly = self.posY//CELL_SIZE
        neighbours = {}#CL[(clx,cly)]

        for dx in range(-Cell.ADJACENCY_DISTANCE, Cell.ADJACENCY_DISTANCE+1):
            for dy in range(-Cell.ADJACENCY_DISTANCE, Cell.ADJACENCY_DISTANCE+1):
                  
                    x = (clx + dx) % N_CELLS
                    y = (cly + dy) % N_CELLS

                    #neighbours.extend(CL[(x,y)])
                    neighbours.update(CL[(x,y)])

        for _,cell in neighbours.copy().items() :
            distX=self.posX-cell.posX
            distY=self.posY-cell.posY
            if(distX>GRID_SIZE/2):
                distX=distX-GRID_SIZE
            elif(distX<=-GRID_SIZE/2):
                distX=distX+GRID_SIZE
            if(distY>GRID_SIZE/2):
                distY=distY-GRID_SIZE
            elif(distY<=-GRID_SIZE/2):
                distY=distY+GRID_SIZE
            dist=math.sqrt(distX**2+distY**2)
            #if(cell.type==Cell.RABBIT and math.dist((self.posX,self.posY),(cell.posX,cell.posY))<EATING_DISTANCE and random.random()<EATING_PROBABILITY):
            if(cell.type==Cell.RABBIT and dist<=EATING_DISTANCE and random.random()<EATING_PROBABILITY):
                cell.die()
                self.ate+=1
                self.age=0

   
###########
pygame.init()
pygame.display.set_caption('Press P or D')
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), 0)
#WHITE = (255,255,255)

for n in range(INIT_WOLVES):
    x=random.randint(0, GRID_SIZE-1)
    y=random.randint(0, GRID_SIZE-1)
    Cell(x,y,Cell.WOLF)

for n in range(INIT_RABBITS):
    x=random.randint(0, GRID_SIZE-1)
    y=random.randint(0, GRID_SIZE-1)
    Cell(x,y,Cell.RABBIT)

n_iterations=0
plot_wolves=[]
plot_rabbits=[]
#plt.ion()
#fig=plt.figure()

end=False
start_time= time.time()
tot_time=0
while(not end):
    iter_time = time.time()
    n_iterations+=1
    
    #plot stuff
    
    plot_rabbits.append(len(Cell.rabbits))
    plot_wolves.append(len(Cell.wolves))
    
    #draw stuff
    draw_time = time.time()
    screen.fill(0)
    for _,cell in Cell.allCells.items():
        pygame.draw.rect(screen,cell.color,(cell.posX*cell.SIZE, cell.posY*Cell.SIZE, Cell.SIZE, Cell.SIZE))

    if(DEBUG):
        #draw wolf fov
        for _,cell in Cell.allCells.items():
            if(cell.type==Cell.WOLF):
                pygame.draw.circle(screen, GRAY, (cell.posX*Cell.SIZE+Cell.SIZE//2, cell.posY*Cell.SIZE+Cell.SIZE//2), EATING_DISTANCE*Cell.SIZE, 1)

        #draw cl
        for x,y in CL.keys():
            pygame.draw.rect(screen, GRAY, (x*CELL_SIZE*Cell.SIZE, y*CELL_SIZE*Cell.SIZE, CELL_SIZE*Cell.SIZE, CELL_SIZE*Cell.SIZE), width=1)
    draw_time = time.time() - draw_time
    
    time_move = time.time()     
    for _,cell in Cell.allCells.items():
        cell.moveRandomly()
    time_move = time.time() - time_move

    time_eat = time.time()
    for _,cell in Cell.wolves.items():
        cell.eat()
    time_eat = time.time() - time_eat

    time_replicate = time.time()
    for _,cell in Cell.allCells.copy().items():
        cell.replicate()
    time_replicate = time.time() - time_replicate

    time_survive = time.time()
    for _,cell in Cell.allCells.copy().items():
        cell.survive()
    time_survive = time.time() - time_survive
        
    #events
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            pygame.display.quit()
            pygame.quit()
            end=True
            #sys.exit()
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_UP):           
                DELAY-=10                
            if(event.key == pygame.K_DOWN):            
                DELAY+=10
            if(event.key == pygame.K_SPACE):
                 pygame.image.save(screen, f"-Iteration{n_iterations}-N_WOLVES={len(Cell.wolves)}-N_RABBITS={len(Cell.rabbits)}.jpg") 
            if(event.key == pygame.K_d):
                DEBUG=not DEBUG
            if(event.key == pygame.K_p):
                plt.figure()
                plt.plot(range(n_iterations),plot_rabbits,label='Rabbits')
                plt.plot(range(n_iterations),plot_wolves,label='Wolves')
                plt.legend()
                plt.show()
                
        if(event.type == pygame.MOUSEBUTTONDOWN):
            mousePosX,mousePosY= pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            Cell(mousePosX//Cell.SIZE, mousePosY//Cell.SIZE, Cell.WOLF)
            for _ in range(10):
                Cell((mousePosX//Cell.SIZE)+EATING_DISTANCE*2, mousePosY//Cell.SIZE, Cell.RABBIT)

    iter_time=time.time()-iter_time
    tot_time= time.time()-start_time
    print(f'Iteration:{n_iterations} N_WOLVES={len(Cell.wolves)} N_RABBITS={len(Cell.rabbits)} -TIMING: sim={tot_time/60:.2f}m iter={iter_time:.3f}s : draw={draw_time:.3f}s move={time_move:.3f}s eat={time_eat:.3f}s repr={time_replicate:.3f}s surv={time_survive:.3f}s      ', end='\r')
    
    if(not end):
        pygame.display.update()     
        pygame.time.delay(DELAY)

    







