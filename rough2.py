'''''
BLINKY : Minimax algorithm
INKY :simulated annealing 
'''

from board import boards
import math
import pygame
import time
pygame.init()
import csv

import random
#<------------------INITIALISATION START------------------------>
st1=time.time()        ######game start
en=0                   ###end time
WIDTH=600
HEIGHT=650

screen=pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps=80 #max speed
font = pygame.font.Font('freesansbold.ttf',20)
level = boards
color = 'darkgreen'
PI = math.pi
player_images=[]
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'./player/{i}.png'),(25,25)))
ghost_speeds = [0.5,0.1,0.1,0.2]
#<-------------BLINKY GHOST (RED)------------------------------------------>
blinky_img = pygame.transform.scale(pygame.image.load(f'./ghost/red.png'),(25,25))
blinky_box = False
player_x = 35
player_y = 28
blinky_xc= 22#530
blinky_yc= 22#31
blinky_direction=0

inky_img = pygame.transform.scale(pygame.image.load(f'./ghost/blue.png'),(25,25))
inky_box = False
inky_xc= 9#530
inky_yc= 26#31
inky_direction=0
TEMPERATURE = 100  # Initial temperature
COOLING_RATE = 0.5  # Cooling rate to reduce temperature each iteration


death_by_blinky=0
death_by_inky=0



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
        time.sleep(0.01)
        if self.x_pos<=32 and self.y_pos<=29:
            screen.blit(self.img, (self.y_pos*20, self.x_pos*15))

    def check_collisions(self):
        
        # Initialize turns for Right, Left, Up, Down
        self.turns = [False, False, False, False]

        if 0 < blinky_xc < 29:
            # Check available directions based on adjacent tiles
            if level[blinky_xc][blinky_yc ] == 9:
                self.turns[2] = True  # Up
            if level[blinky_xc][blinky_yc ] < 3 or (level[blinky_xc][blinky_yc] == 9 and self.in_box):
                self.turns[3] = True  # Down
            if level[blinky_xc ][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                self.turns[1] = True  # Left
            if level[blinky_xc ][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                self.turns[0] = True  # Right

            # Check additional constraints based on current direction
            if self.direction == 2 or self.direction == 3:
                if 6 <= blinky_yc % 30 <= 15:
                    if level[blinky_xc][blinky_yc ] < 3 or (level[blinky_xc][blinky_yc ] == 9 and self.in_box):
                        self.turns[3] = True
                    if level[blinky_xc][blinky_yc ] < 3 or (level[blinky_xc][blinky_yc ] == 9 and self.in_box):
                        self.turns[2] = True
                if 6 <= blinky_xc % 32 <= 15:
                    if level[blinky_xc - 1][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                        self.turns[1] = True
                    if level[blinky_xc + 1][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 6 <= blinky_yc % 30 <= 15:
                    if level[blinky_xc][blinky_yc ] < 3 or (level[blinky_xc][blinky_yc + 1] == 9 and self.in_box):
                        self.turns[3] = True
                    if level[blinky_xc][blinky_yc ] < 3 or (level[blinky_xc][blinky_yc - 1] == 9 and self.in_box):
                        self.turns[2] = True
                if 6 <= blinky_xc % 32 <= 15:
                    if level[blinky_xc - 1][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                        self.turns[1] = True
                    if level[blinky_xc + 1][blinky_yc] < 3 or (level[blinky_xc ][blinky_yc] == 9 and self.in_box):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True

        # Check if ghost is within the box
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False

        return self.turns, self.in_box



    def createAdjacencyDict(self):
        adjacent_dict = {}
        rows = len(level)
        cols = len(level[0])
        
        for x in range(rows):
            for y in range(cols):
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
    
    def manhattan_distance(self,a,b):
        return (abs(a[0]-b[1]) + abs(a[1]-b[0]))
    
    def minimax(self, position, depth, is_blinky_turn, pacman_pos):
        # Base case: if depth is 0 or the target is reached
        if depth == 0 or position == pacman_pos:
            return self.manhattan_distance(position, pacman_pos)
        
        adjacency_dict = self.createAdjacencyDict()
        adjacent_positions = adjacency_dict.get(position, [])

        if is_blinky_turn:
            # Blinky's turn: minimize distance to Pacman
            min_eval = float('inf')
            for move in adjacent_positions:
                eval = self.minimax(move, depth - 1, False, pacman_pos)
                min_eval = min(min_eval, eval)
            return min_eval
        else:
            # Pacman's turn: maximize distance from Blinky
            max_eval = float('-inf')
            for move in adjacent_positions:
                eval = self.minimax(move, depth - 1, True, pacman_pos)
                max_eval = max(max_eval, eval)
            return max_eval

    def move_blinky(self, depth=3):
        # Current position of Blinky in grid coordinates
        ghost_pos = (self.x_pos, self.y_pos)  # Assuming these are Blinky's grid coordinates
        pacman_pos = (player_y // 15, player_x // 20)  # Pacman's grid coordinates
        
        # Get adjacent positions of Blinky
        adjacency_dict = self.createAdjacencyDict()
        adjacent_positions = adjacency_dict.get(ghost_pos, [])
        
        best_move = ghost_pos
        min_distance = float('inf')

        # Minimax applied for each of Blinky's possible moves
        for move in adjacent_positions:
            eval = self.minimax(move, depth - 1, False, pacman_pos)
            if eval < min_distance:
                min_distance = eval
                best_move = move

        # Update Blinky's position
        self.x_pos += (best_move[0] - ghost_pos[0]) * 0.5
        self.y_pos += (best_move[1] - ghost_pos[1]) * 0.5
        #print(f"Updated Blinky's position to: {best_move}")

        # Redraw Blinky at its new position
        self.draw()

        return best_move[0], best_move[1]
    
    def euclidean(self, pos1, pos2):
        """Calculate Euclidean distance between two positions."""
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

    def move_inky(self):
        """Simulated Annealing for Inky's movement."""
        global TEMPERATURE  # Use global temperature for simulated annealing

        current_pos = (self.x_pos, self.y_pos)
        pacman_pos = (player_y // 15, player_x // 20)  # Convert to grid position

        best_move = current_pos
        best_distance = self.euclidean(current_pos, pacman_pos)

        while TEMPERATURE > 1:
            # Get possible moves from adjacency dictionary
            adjacency_dict=self.createAdjacencyDict()
            adjacent_positions = adjacency_dict.get(current_pos, [])
            if not adjacent_positions:
                break

            # Select a random move from adjacent positions
            next_move = random.choice(adjacent_positions)
            next_distance = self.manhattan_distance(next_move, pacman_pos)

            # Calculate acceptance probability
            if next_distance < best_distance:
                # If next move is better, accept it
                best_move, best_distance = next_move, next_distance
            else:
                # Calculate acceptance probability for worse move
                delta = next_distance - best_distance
                acceptance_probability = math.exp(-delta / TEMPERATURE)
                if random.random() < acceptance_probability:
                    best_move, best_distance = next_move, next_distance

            # Update current position and reduce temperature
            current_pos = best_move
            TEMPERATURE *= COOLING_RATE  # Cool down

        # Move Inky towards Pacman at a slower speed
        TEMPERATURE = 100  # Reset temperature for next call
        self.x_pos += (best_move[0] - self.x_pos) * 0.2
        self.y_pos += (best_move[1] - self.y_pos) * 0.2

        # Redraw Inky at new position
        self.draw()

        return best_move
        
        
        



def draw_misc():
    score_text = font.render(f'Score : {score}',True,'white')
    screen.blit(score_text,(10,600))
    if (time.time()-st1<=25):
        time_text = font.render(str(int(25-(time.time()-st1)))+' Seconds until inky arrives' ,True,'lightblue')
        screen.blit(time_text,(150,600))
    if death_by_blinky or death_by_inky:
        death_text = font.render('GAME OVER!' ,True,'red')
        screen.blit(death_text,(150,600))

    


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


def writeintofile():
    game=random.randint(00000000, 99999999)
    filename = 'game_stats_2.csv'
    #columns = ['game_id', 'time_start', 'time_end', 'score', 'blinky_kill', 'inky_kill', 'playtime']
    data=[]
    data.append(game)
   # data.append(round(st1, 2))
    #data.append(round(en, 2))
    data.append(score)
    data.append(death_by_blinky)
    data.append(death_by_inky)
    data.append(round(en-st1, 2))
    # Create and write to the CSV file
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)  # Write the header
    print("Game:", game)
    print("Start Time (rounded):", round(st1, 2))
    print("End Time (rounded):", round(en, 2))
    print("Score:", score)
    print("Deaths by Blinky:", death_by_blinky)
    print("Deaths by Inky:", death_by_inky)
    print("Total Duration (rounded):", round(en - st1, 2))




run = True
while run:
    
    #print(st1)
    #print(time.time()-st1)
    if player_y == 570:
        print("game over")
        print(f'SCORE:{score}')
        en=time.time()
        break
    if (abs((player_y//15)-blinky_xc)==1 and abs((player_x//20)-blinky_yc)==1):
        print("Blinky killed you!\nGAME OVER")
        print(f'SCORE:{score}')
        death_by_blinky=1
        en=time.time()
        break
    if (time.time()-st1>=25 and abs((player_y//15)-inky_xc)==1 and abs((player_x//20)-inky_yc)==1):
        print("Inky killed you!game over")
        print(f'SCORE:{score}')
        death_by_inky=1
        en=time.time()
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
    if (time.time()-st1>=25):
        inky=Ghost(inky_xc,inky_yc,targets[0],ghost_speeds[0],inky_img,inky_direction,inky_box,0)
        inky_xc,inky_yc=inky.move_inky()
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

writeintofile()
pygame.quit()






