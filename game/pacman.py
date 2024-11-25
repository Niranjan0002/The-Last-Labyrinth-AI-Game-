from board import boards
import math
import pygame
import time
pygame.init()
from collections import deque
import heapq
#<------------------INITIALISATION START------------------------>
WIDTH=600
HEIGHT=650

screen=pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps=60  #max speed
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'darkgreen'
PI = math.pi
player_images=[]
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'./player/{i}.png'),(30,30)))
ghost_speeds = [2, 2, 2, 2]
#<-------------BLINKY GHOST (RED)------------------------------------------>
blinky_img = pygame.transform.scale(pygame.image.load(f'./ghost/red.png'),(30,30))
blinky_box = False
player_x = 35
player_y = 28
blinky_xc= 2#530
blinky_yc= 26#31
blinky_direction=0
#<----------------------------------------------------------------------------->



direction=0
counter=0
flicker =False
turns_allowed =  [False , False , False , False]
direction_command = 0
player_speed = 2
downtime = 0 #time when fps 40 is triggered
stoptime = 0 #time when stop is triggered
score=0
targets=[(player_x,player_y)]        #target of each reaper
#<------------------INITIALISATION END------------------------>

class Ghost:
    def __init__(self,x_cord,y_cord,target,speed,img,direction,box,id):
        self.x_pos = x_cord   #xyc
        self.y_pos = y_cord   #xyc
        self.center_x = self.x_pos*15 + 15
        self.center_y = self.y_pos*20 + 15
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.in_box = box
        self.id = id
        self.turns, self.in_box = self.check_collisions()
        #self.rect = self.draw() 

    def draw(self):
        screen.blit(self.img, (self.y_pos*20, self.x_pos*20))

    def check_collisions(self):
        # R, L, U, D
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box )):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box )):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box )):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box )):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 6 <= self.center_x % num2 <= 15:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box )):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box )):
                        self.turns[2] = True
                if 6 <= self.center_y % num1 <= 15:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box )):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 6 <= self.center_x % num2 <= 15:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box )):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box )):
                        self.turns[2] = True
                if 6 <= self.center_y % num1 <= 15:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box )):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box


    def createAdjacencyDict(self):
        adjacent_dict = {}
        rows = len(level)
        cols = len(level[0])
        
        for x in range(rows-2):
            for y in range(cols-1):
                # Only consider cells that are not walls
                if level[x][y] <= 2:
                    # Initialize the adjacency list for this cell
                    adjacent_dict[(x, y)] = []
                    
                    # Check the four adjacent positions
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # up, down, left, right
                        nx, ny = x + dx, y + dy
                        # Check boundaries and if the adjacent cell is not a wall
                        if 0 <= nx < rows and 0 <= ny < cols and level[nx][ny] <= 2:
                            adjacent_dict[(x, y)].append((nx, ny))
        #print(adjacent_dict)
        return adjacent_dict
    
    

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def move_blinky(self):
        # Get the current position of the ghost in grid coordinates
        #print(player_x,player_y)
        #time.sleep(0.1)
        ghost_pos = (blinky_xc,blinky_yc)  # (row, col)
        pacman_pos = (player_y // 15, player_x // 20)
        #print(ghost_pos)

        adjacency_dict = self.createAdjacencyDict()  # Get the adjacency dictionary

        # Get adjacent positions of the ghost
        adjacent_positions = adjacency_dict.get(ghost_pos, [])
        print(adjacent_positions)
        # Find the next position that is closest to Pacman
        next_move = None
        min_distance = float('inf')  # Set initial distance to infinity

        for neighbor in adjacent_positions:
            distance = self.heuristic(neighbor, pacman_pos)
            #print(distance)
            if distance < min_distance:
                min_distance = distance
                next_move = neighbor
        #print(next_move)
        # Move the ghost to the next position if valid
        self.x_pos += (next_move[0] - ghost_pos[0]) * 0.5 # Assuming id corresponds to the ghost's index
        self.y_pos += (next_move[1] - ghost_pos[1]) * 0.5
        #print("updated next move ",next_move[0],next_move[1])

        #print(pacman_pos, next_move)
        # Redraw the ghost at its new position
        self.draw()

        return next_move[0],next_move[1]

       
        



def draw_misc():
    score_text = font.render(f'Score : {score}',True,'white')
    screen.blit(score_text,(10,600))




def draw_board():
    num1 = ((HEIGHT - 50 )//32)   #50 is the padding , 32 rows
    num2 = ((WIDTH)//30)          #30 columns
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j]==-1:   #slow down ticket
                pygame.draw.circle(screen, 'red' , (j*num2+ (0.5*num2), i*num1 + (0.5*num1)) , 10)

            if level[i][j] == -2:
                pygame.draw.circle(screen, 'white' , (j*num2+ (0.5*num2), i*num1 + (0.5*num1)) , 10)

                
            if level[i][j]==1:
                pygame.draw.circle(screen, ' gold' , (j*num2+ (0.5*num2), i*num1 + (0.5*num1)) , 4)
            if level[i][j]==2 and not flicker:
                pygame.draw.circle(screen, ' gold' , (j*num2+ (0.5*num2), i*num1 + (0.5*num1)) , 8)
            if level[i][j]==3:
                pygame.draw.line(screen ,  color , (j * num2 + (0.5 * num2) , i*num1), (j * num2 + (0.5 * num2) , i*num1+num1 ), 3)
            if level[i][j]==4:
                pygame.draw.line(screen ,  color , (j * num2 , i*num1 + (0.5*num1)), (j * num2 + num2 , i*num1+(0.5*num1) ), 3)
            if level[i][j]==5:
                pygame.draw.arc(screen , color ,  [(j*num2 - (num2*0.3)) - 4 , (i*num1 + (0.5*num1)) , num2, num1 ] , 0 , PI/2 , 3)

            if level[i][j]==6:
                pygame.draw.arc(screen , color ,  [(j*num2 + (num2*0.5))  , (i*num1 + (0.5*num1)) , num2, num1 ] , PI/2, PI  , 3)

            if level[i][j]==7:
                pygame.draw.arc(screen , color ,  [(j*num2 + (num2*0.5))  , (i*num1 - (0.3*num1)) , num2, num1 ] , PI, 3*PI/2  , 3)

            if level[i][j]==8:
                pygame.draw.arc(screen , color ,  [(j*num2 - (num2*0.3)) - 4  , (i*num1 - (0.4*num1)) , num2, num1 ] , 3*PI/2, 2*PI  , 3)


            if level[i][j]==9:
                pygame.draw.line(screen ,  'red' , (j * num2 , i*num1 + (0.5*num1)), (j * num2 + num2 , i*num1+(0.5*num1) ), 3)

            


def draw_player():
    #0-right , 1-left , 2-up, 3-down
    if direction == 0:
        screen.blit(player_images[counter//5],(player_x,player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter//5],True,False),(player_x,player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter//5],90),(player_x,player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter//5],270),(player_x,player_y))

def check_position(centerx,centery):
    global fps,downtime,stoptime
    #print(time.time()-downtime)
    if fps==40:
        if (time.time() - downtime  >= 5):fps=60      #slow down for 5 seconds
    elif fps==0:
        if (time.time() - stoptime  >= 3):fps=60      #slow down for 5 seconds
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 33
    num2 = (WIDTH // 30)
    #print(num1,num2)
    num3 = 10
    # check collisions based on center x and center y of player +/- fudge number
    #print(num1,num2,"//")
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3 :
                turns[1] = True
                ch=level[centery // num1][(centerx - num3) // num2]
                if ch == -1:
                    downtime=time.time()
                    fps=40
               # elif ch == -2:
                    ########think of what can be done
                    
                    

                
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
                ch = level[centery // num1][(centerx - num3) // num2]
                if ch == -1:
                    downtime=time.time()
                    fps=40
                elif ch == -2:
                    stoptime=time.time()
                    fps=0

        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
                ch = level[centery // num1][(centerx - num3) // num2]
                if ch == -1:
                    downtime=time.time()
                    fps=40
                elif ch == -2:
                    stoptime=time.time()
                    fps=0
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True
                ch=level[centery // num1][(centerx - num3) // num2]
                if ch == -1:
                    downtime=time.time()
                    fps=40
                elif ch == -2:
                    stoptime=time.time()
                    fps=0

        if direction == 2 or direction == 3:
            if 6 <= centerx % num2 <= 15:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
                    
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
            if 6<= centery % num1 <= 15:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0

        if direction == 0 or direction == 1:
            if 6 <= centerx % num2 <= 15:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
            if 6 <= centery % num1 <= 15:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
                    ch=level[centery // num1][(centerx - num3) // num2]
                    if ch == -1:
                        downtime=time.time()
                        fps=40
                    elif ch == -2:
                        stoptime=time.time()
                        fps=0
    else:
        turns[0] = True
        turns[1] = True

    
    

    return turns

def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y
    
def calculatescore(score):
    num1=(HEIGHT-50)//33
    num2=WIDTH//30
    if 0<player_x<570:
        if level[center_y // num1][center_x//num2]==1:   #center of pacman eats a coin, instead of just entering square
            level[center_y // num1][center_x//num2]=0
            score+=10   #10 points for a coin

        if level[center_y // num1][center_x//num2]==2:   #center of pacman eats a coin, instead of just entering square
            level[center_y // num1][center_x//num2]=0
            score+=50   #50 points for a bigger coin  

        
        if level[center_y // num1][center_x//num2]==-1:   #center of pacman eats a coin, instead of just entering square
            level[center_y // num1][center_x//num2]=0
            score-=20   #-20 points for a bigger red slow down ticket   
    
    
    return score



run = True
while run:
    #print(player_x,player_y)
    print(blinky_xc,blinky_yc)
    if player_y == 570:
        print("game over")
        print(f'SCORE:{score}')
        break
    timer.tick(fps)
    if counter < 19:
        counter+=1
        if counter > 3:
            flicker = False
    else:
        counter=0
        flicker = True


    screen.fill('black')
    #<-----------BOARD-------------->
    draw_board()
    draw_player()
    blinky=Ghost(blinky_xc,blinky_yc,targets[0],ghost_speeds[0],blinky_img,blinky_direction,blinky_box,0)


    draw_misc()        #####for displayyy
    center_x = player_x + 15
    center_y = player_y + 15
    #pygame.draw.circle(screen,'white',(center_x,center_y),2)
    
    turns_allowed = check_position(center_x,center_y)
    player_x,player_y=move_player(player_x,player_y)
    blinky_xc,blinky_yc=blinky.move_blinky()
    #blinky.move_blinky()
    score = calculatescore(score)

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
               # print(0)
            if event.key == pygame.K_LEFT:
                direction_command = 1
                #print(1)
            if event.key == pygame.K_UP:
                direction_command = 2
                #print(2)
            if event.key == pygame.K_DOWN:
                direction_command = 3
                #print(3)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = direction
                #print(direction)
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = direction
                #print(direction)
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = direction
                #print(direction)
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = direction
                #print(direction)
        
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3

    if player_x > 560:
        player_x = -47
    elif player_x < -50:
        player_x = 560
    

    pygame.display.flip()  

pygame.quit()






