# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
angle = 0
angle_vel = 0
angle_vel_inc = 0.1
c = 0.01 # friction coefficient
rock_group = set([])
missile_group = set([])
num_collision = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):

        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0]+ self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)

        else: 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

            
    def update(self):
        
        #position update
        self.angle += self.angle_vel
        self.pos[0]= (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1]= (self.pos[1] + self.vel[1]) % HEIGHT

        #velocity update with friction
        self.vel[0] *= (1-c)
        self.vel[1] *= (1-c)
        
        #velocity update with acceleration (thrust effect)
        if self.thrust:
            acceleration = angle_to_vector(self.angle)
            self.vel[0] += acceleration[0]* 0.1
            self.vel[1] += acceleration[1]* 0.1
        
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius 
        
        
    def fire_missile(self):
        global missile_group

        power_shoot = 7.5 # control the velocity of the missile
        acceleration = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * acceleration[0], self.pos[1] + self.radius * acceleration[1]]
        missile_vel = [self.vel[0] + power_shoot*acceleration[0] , self.vel[1]+ power_shoot*acceleration[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle,0, missile_image, missile_info, missile_sound))
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

 
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.age += 1
        if self.age >= self.lifespan:
            return True
        else:
            return False

    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius    
    
    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_radius = other_object.get_radius()
        length = dist(self.pos, other_pos)
        
        if length < self.radius + other_radius:
            return True
        else:
            return False
            
            
# define keyhandlers to control ship movement

def keydown(key):
    global angle_vel
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel += angle_vel_inc
    
    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel -= angle_vel_inc

    elif simplegui.KEY_MAP["up"] == key :
        my_ship.thrust = True
        ship_thrust_sound.play()

    elif simplegui.KEY_MAP["space"] == key:
        my_ship.fire_missile()
     
        
def keyup(key):
    global angle_vel
        
    if simplegui.KEY_MAP["left"] == key:
        my_ship.angle_vel -= angle_vel_inc

    elif simplegui.KEY_MAP["right"] == key:
        my_ship.angle_vel += angle_vel_inc
    
    elif simplegui.KEY_MAP["up"] == key :
        my_ship.thrust = False
        ship_thrust_sound.pause()
    
    
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True            
        timer.start()
        score = 0
        lives = 3
        soundtrack.pause()
    
# define draw handlers           
def draw(canvas):
    global time, lives, score, started
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
   

    # Explosions when collide (optionnal, to do)

    
    
    # draw ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    
    # update ship and sprites
    my_ship.update()
    if group_collide(rock_group,my_ship):
        lives -=1
    group_group_collide(rock_group, missile_group)

         
    # check if game over
    if lives == 0:
        restart()
        
    # draw score and lives
    canvas.draw_text("lives: {}".format(lives),[WIDTH*0.1,HEIGHT*0.1], 24, "Red")
    canvas.draw_text("score: {}".format(score),[WIDTH*0.8,HEIGHT*0.1], 24, "White")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        soundtrack.play()
    
    
    
# helper function to draw set of rocks, missile, ...
def process_sprite_group(group, canvas):
    remove_sprite = set([])
    for sprite in group.copy(): # we put group.copy() to iterate over a constant set
        sprite.draw(canvas)
        if sprite.update() == True:
              remove_sprite.add(sprite)
        group.difference_update(remove_sprite)

# helper functions to modelize collision
def group_collide(group, other_object):
    global explosion_group
    remove_set = set([])
    for sprite in group.copy():
        if sprite.collide(other_object) == True:
            explosion_sound.play()
            remove_set.add(sprite)
        group.difference_update(remove_set)
    if len(remove_set) != 0 :
        return True

def group_group_collide(group1, group2):
    global num_collision, score
    remove_set = set([])
    for sprite in group1.copy():
        if group_collide(group2,sprite) == True:
            num_collision += 1
            score +=1
            explosion_sound.play()
            remove_set.add(sprite)
        group1.difference_update(remove_set)
    return num_collision



# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    # use formule min + (max-min)* random to obtain also negative numbers
    rock_initial_position = [int(random.random()*WIDTH), int(random.random()*HEIGHT)]
    rock_angle_velocity = -0.1 + 0.2*random.randint(0,1)
    rock_initial_velocity = [-2 + 4*random.random(),-2 + 4*random.random()]
    if dist(rock_initial_position, my_ship.get_position()) > 100:    
        
        rock_group.add(Sprite(rock_initial_position, rock_initial_velocity, 0 , rock_angle_velocity, asteroid_image, asteroid_info))
        if len(rock_group.copy()) < 12:
            rock_group.add(Sprite(rock_initial_position, rock_initial_velocity, 0 , rock_angle_velocity, asteroid_image, asteroid_info))

        
def restart():
    global started,rock_group,missile_group
    timer.stop()
    started = False
    rock_group = set([])
    missile_group = set([])

    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0 , 0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
if started:
    timer.start()
frame.start()