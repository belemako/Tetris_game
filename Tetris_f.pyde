import random
N_ROWS=19
N_COLS=10
B_WIDTH=20
B_HEIGHT=20

# list of colors to randomly choose from
COLORS=[[255,51,52],[12,150,228],[30,183,66],[246,187,0],[76,0,153],[255,255,255],[0,0,0]]

class Block():
    def __init__(self,r,c):
        self.w=B_WIDTH
        self.h=B_HEIGHT
        self.clr_index=random.randint(0,len(COLORS)-1)
        self.c=c
        self.r=r
 
    def display(self):
        # Randomly choose from list of color to fill the block
        fill(COLORS[self.clr_index][0],COLORS[self.clr_index][1],COLORS[self.clr_index][2])
        rect(self.c*B_HEIGHT, self.r*B_WIDTH,self.w,self.h)
        
    def move(self,row, col): 
        self.r += row
        self.c += col
        
class Game(list):
    def __init__(self):
        self.taken_spaces=[]
        self.current_block=self.get_random_block()
        self.blocks=[]
        self.speed=0
        self.score=0


     # a function for getting random block
    def get_random_block(self):
        self.block = Block(0,random.randint(0,(N_COLS-1)))
        # generate again if it's on already taken space
        while [self.block.r,self.block.c] in self.taken_spaces:
            self.block = Block(0,random.randint(0,(N_COLS-1)))            
        return self.block
    
   # check for the block inside board
    def block_inside(self):
        if self.current_block.r >=0 and self.current_block.r < N_ROWS and self.current_block.c >=0 and self.current_block.c < N_COLS:
            return True
        return False
    
    # to check if a space is pre-occupied or not
    def is_occupied(self):
        # store the row and column attribute of block into taken_space
        if [self.current_block.r,self.current_block.c] in self.taken_spaces:
            return True
        return False
    
    def move_right(self):
        self.current_block.move(0,1)
        # move it back if the block is outside or on occupied space
        if self.block_inside()==False or self.is_occupied():
            self.current_block.move(0,-1)

    
    def move_left(self):
        self.current_block.move(0,-1)
        # move it back if the block is outside or on occupied space
        if self.block_inside()==False or self.is_occupied():
            self.current_block.move(0,1)

    def move_down(self):
        self.current_block.move(1,0)
        # move it back if the block is outside or on occupied space
        if self.block_inside()==False or self.is_occupied():
            self.current_block.move(-1,0)
            self.lock_block()  
            
           


    def clear_same_colors(self):
         for block in self.blocks:
             # at least three block under a block to be cleared
            if block.r < N_ROWS - 3:
                # a list that contain three blocks under the just appended block if they are same color to a block
                same_color_blocks = [b for b in self.blocks if b.c == block.c and b.r in [block.r + 1, block.r + 2, block.r + 3] and b.clr_index == block.clr_index]
                if len(same_color_blocks) == 3:
                    # remove the three blocks
                    for b in same_color_blocks:
                        if [b.r, b.c] in self.taken_spaces:
                            self.taken_spaces.remove([b.r, b.c])
                        self.blocks.remove(b)
                    # remove the fourth block
                    self.taken_spaces.remove([block.r, block.c])
                    self.blocks.remove(block)
                    self.speed = 0
                    self.score += 1
     # Fit the block at bottom or on top of other block  
    def lock_block(self):
        if self.all_occupied()==False:
            self.prev_block=self.current_block
            self.taken_spaces.append([self.prev_block.r,self.prev_block.c]) 
            self.blocks.append(self.current_block)
            self.clear_same_colors()
            # get random block only if there is space that is not taken
            if self.all_occupied()==False:
                self.current_block=self.get_random_block()
                self.speed+=0.25
          
    def all_occupied(self):
        for i in range(N_ROWS):
            for j in range(N_COLS):
                if [i,j] not in self.taken_spaces:
                    return False
            return True
                               
    def game_over(self):
        return self.all_occupied()
    
    # for game over message
    def display_game_over(self):
        background(210)
        textSize(20)
        fill(0)
        text("Score : " + str(game.score), (N_COLS*B_WIDTH/4), (N_ROWS*B_HEIGHT)/2-50)
        text("GAME OVER!", (N_COLS*B_WIDTH/4), (N_ROWS*B_HEIGHT)/2)
    
    # restart for mouse click
    def restart(self):
        for i in range(len(self.blocks)):
            self.blocks.pop()
        for i in range(len(self.taken_spaces)):
            self.taken_spaces.pop()
        self.speed=0
        self.score=0 
        self.current_block=self.get_random_block()  
        
        
    def display(self):
        # move down by default
        self.move_down()
        
        # display both stationary and moving block
        for block in self.blocks:
            block.display()
        self.current_block.display()
   
        
                                    
def setup():
    size(N_COLS*B_WIDTH,N_ROWS*B_HEIGHT)
    background(210)
    stroke(180)
   

def draw(): 
    
    #slow down the game by not calling the display() method every frame
    if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1:
        background(210)
        
    #this calls the display method of the game class
        game.display()
        print(game.taken_spaces)
        # a code for grid of line
        for i in range(N_ROWS):
            line(0,i*B_HEIGHT,N_COLS*B_WIDTH,i*B_HEIGHT)    
        for i in range(N_COLS):
            line(i*B_HEIGHT,0,i*B_HEIGHT,N_ROWS*B_HEIGHT) 
    # for displaying score
        textSize(15)
        fill(10)
        text("Score: "+ str(game.score), N_COLS*B_WIDTH - 80, 15)

    
    if game.game_over():
        game.display_game_over()
   
        
def keyPressed():
        if keyCode == RIGHT:
            game.move_right()           
        if keyCode == LEFT:
            game.move_left()
            
def mouseClicked():
    game.restart()
    
game=Game()
