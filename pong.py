# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle1_pos = 200
paddle2_pos = 200 
paddle1_vel = 0
paddle2_vel = 0

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0] # pixels per update (1/60 seconds)

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2] # reinitialize ball position to center
    
    # set random horizontal and vertical velocity
    h_vel = random.randrange(120, 240)
    v_vel = random.randrange(60, 180)
    
    # direction upwards and towards right (and left)
    if direction == RIGHT:
        ball_vel = [h_vel, -v_vel]
    if direction == LEFT:
        ball_vel = [-h_vel, -v_vel]       
        
        
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    #spawn_ball(direction)

# Handlers for keydown and keyup
   
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 5   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 5    
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = -5 
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -5  
    
    

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["S"]:
        paddle1_vel = 0   
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0     
    if key == simplegui.KEY_MAP["W"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0  
    
# Handler to draw on canvas
 
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
     # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # collide and reflect on bottom and top of canvas
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] - BALL_RADIUS >= 360:
        ball_vel[1] = - ball_vel[1]
    
    # collide and reflect on left and right gutters of canvas
    if ball_pos[0] - BALL_RADIUS <= 0:
        spawn_ball(LEFT)
    if ball_pos[0] - BALL_RADIUS >= 600:
        spawn_ball(RIGHT)
    
    # update paddle's vertical position, keep paddle on the screen  
    
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
     
    
    # draw paddles 
    canvas.draw_line([0, paddle1_pos - HALF_PAD_HEIGHT],[0, paddle1_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH, paddle2_pos - HALF_PAD_HEIGHT],[WIDTH, paddle2_pos + HALF_PAD_HEIGHT], PAD_WIDTH, "White")

    
    # determine whether paddle and ball collide    
    
    # draw scores
        
 

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
