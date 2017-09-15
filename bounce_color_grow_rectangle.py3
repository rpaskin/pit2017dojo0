"""
 Bounces a rectangle around the screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/-GmKoaX2iMs

 Growing bouncing random colors rectangles
 Modified by Pietro Pepe
"""
 
import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

colors = [BLACK,WHITE,GREEN,RED]
 
pygame.init()
 
# Set the height and width of the screen
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Bouncing Rectangle")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# List of rectangles
lst = []
 
# Speed of rectangle
rect_speed_x = 10
rect_speed_y = 16

# How much the rectangle should grow on collision (percentage)
factor = 1.6

# Index of current color
curr = 1

# Limit of insertion
limit = 15

# Number of necessary collisions to spawn a new rectangle
step_size = 2
# Counter of number of collisions
step_count = 0

# Check if it is possible to insert a new rectangle, or if it's beyond limit
def checkInsert():
    if len(lst)>limit:
        if lst[1]["hasDone"] == True:
            lst.pop(0)
        else:
            return False
    return True

#Adds a rectangle with specified position, size, direction, and color
def addRect(x,y,w,h,dx,dy,color = WHITE):
    lst.append({ 'x' : x, 'y' : y, 'w' : w, 'h' : h, 'dx' : dx, 'dy' : dy, 'color' : color, 'hasDone' : False})

# Adds a rectangle with ordered color
def addSequenceColorRect(x,y,w,h):
    if checkInsert():
        global curr
        addRect(x,y,w,h,1,1,colors[curr])
        #lst.append({ 'x' : x, 'y' : y, 'w' : w, 'h' : h, 'dx' : 1, 'dy' : 1, 'hasDone' : False, 'color' : colors[curr] })
        curr = (curr+1)%len(colors)

# Adds a pseudo-random color rectangle
def addRandomColorRect(x,y,w,h):
    if checkInsert():
        global curr
        addRect(x,y,w,h,1,1,[random.randint(0,255),random.randint(0,255),random.randint(0,255)])
        #lst.append({ 'x' : x, 'y' : y, 'w' : w, 'h' : h, 'dx' : 1, 'dy' : 1, 'hasDone' : False, 'color' : colors[curr] })
        curr = (curr+1)%len(colors)
        #addRect(random.randint(0,size[0]),random.randint(0,size[1]),w,h,i)

# Adds rect to the side, to the bottom, and to the right bottom corner
def addQuad(x,y,w,h,dx,dy):
    addRect(x+w,y,w,h,dx,dy)
    addRect(x,y+h,w,h,dx,dy)
    addRect(x+w,y+h,w,h,dx,dy)

# Called when a collision happens
def didCollide(x,y,w,h):
    global step_count
    step_count = step_count+1
    if step_count >= step_size:
        step_count = 0
        addRandomColorRect(x,y,w,h)

addSequenceColorRect(0,0,2,2)

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Drawing
    # Set the screen background
    screen.fill(BLACK)
 
    # Getting each existing rectangle
    for r in lst:
        #Extracting position and size
        rx = r['x']
        ry = r['y']
        rw = r['w']
        rh = r['h']
        rx = rx+r['dx']*rect_speed_x
        ry = ry+r['dy']*rect_speed_y
        # Check if it is too big to move
        if rw > size[0] and rh>size[1]:
            rx = 0
            ry = 0
            r['hasDone'] = True #indicate has finished movement
        else:
            if rx+rw > size[0]:
                #Making size bigger
                rw *= factor; rh *= factor
                #Fixing position
                rx = size[0]-rw
                #Changing direction
                r['dx'] = -1
                #Collision callback
                didCollide(40,0,2,2)
            elif rx<0:
                rw *= factor; rh *= factor
                rx = 0
                r['dx'] = 1
                didCollide(40,0,2,2)
            if ry+rh > size[1]:
                rw *= factor; rh *= factor
                ry = size[1]-rh
                r['dy'] = -1
                didCollide(40,0,2,2)
            elif ry<0:
                rw *= factor; rh *= factor
                ry = 0
                r['dy'] = 1
                didCollide(0,0,2,2)
        #Updating position and size
        r['x'] = rx
        r['y'] = ry
        r['w'] = rw
        r['h'] = rh
        #Drawing rectangle
        pygame.draw.rect(screen, r['color'], [rx, ry, rw, rh])
 
    # --- Wrap-up
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Close everything down
pygame.quit()
