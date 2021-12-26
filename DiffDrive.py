import numpy as np
import pygame as pg
import pygame.display
from math import cos, sin
from math import pi
import math

deg2radian = lambda deg: (pi/180)*deg
radian2deg = lambda rad: (180/pi)*rad
m2p = lambda spd: 3779.52*spd # Meters to pixels

BLACK = (0,0,0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)


class env:
    def __init__(self):

        self.height = 1000
        self.width = 1000

        pygame.display.set_caption("Diff drive tester")
        self.map=pygame.display.set_mode((self.height,self.width))

class Robot:
    def __init__(self, startpos, width, wheel_width):
        self.width = width # distance between 'wheels'
        self.wheel_width = wheel_width # radius of 'wheels'
        self.x = startpos[0]
        self.y = startpos[1]

        self.offset = 0 # Used sometimes to make robot drive correct facing
        self.theta = self.offset

        self.v_l = 0.02
        self.v_r = 0.02

    def increase_speed(self, wheel, amount):
        if wheel == "right":
            self.v_r += amount
        elif wheel == 'left':
            self.v_l += amount
        else:
            pass

    def update_pos(self):
        x_change = (self.width/2) * (self.v_r + self.v_l)*cos(deg2radian(self.theta+self.offset))
        y_change = (self.width/2)*(self.v_r + self.v_l)*sin(deg2radian(self.theta+self.offset))
        deg_change = (self.wheel_width/self.width)*(self.v_r - self.v_l)

        deg_change = radian2deg(deg_change)

        self.x += x_change
        self.y += y_change
        self.theta += deg_change

        if abs(self.theta) >= 360:
            self.theta = 0

class RotSquare(pygame.Surface):
    """
    Rotatable square drawn using pygame draw.polygon
    """
    
    def __init__(self, pos, angle, height, width, parent):
        self.pos = pos # [x,y] pos of front middle of the shape
        self.angle = angle
        self.height = height
        self.width = width

        self.cornerVector = math.sqrt((self.width/2)**2 + (self.height/2)**2)

        self.corners = self.set_angle(0)

        self.parent = parent # Surface object is drawn on

    def update(self, arrow=True):
        self.corners = self.set_angle(self.angle)
        pg.draw.polygon(self.parent, (0,255,255), self.corners)
        if arrow:
            pg.draw.line(self.parent, (0,255,255),
                         (self.pos[0],self.pos[1]),
                         (self.pos[0] + 100*cos(deg2radian(self.angle)),self.pos[1] + 100*sin(deg2radian(self.angle))))

    def set_angle(self, angle):
        """
        :param angle: New angle to get corners of
        :return: list og lists containing 4 corners of surface in order: [upper_right, upper_left, lower_right, lower_left]
        """

        self.angle = angle
        rotradian = deg2radian(self.angle)

        right_vec = [self.cornerVector*cos(deg2radian(self.angle+45)),self.cornerVector*sin(deg2radian(self.angle+45))]
        left_vec = [self.cornerVector*cos(deg2radian(self.angle+45+90)), self.cornerVector*sin(deg2radian(self.angle+45+90))]

        corners = [[0,0],[0,0],[0,0],[0,0]]

        corners[0][0] = self.pos[0] + right_vec[0]
        corners[0][1] = self.pos[1] + right_vec[1]

        corners[1][0] = self.pos[0] + left_vec[0]
        corners[1][1] = self.pos[1] + left_vec[1]

        corners[2][0] = self.pos[0] - left_vec[0]
        corners[2][1] = self.pos[1] - left_vec[1]

        corners[3][0] = self.pos[0] - right_vec[0]
        corners[3][1] = self.pos[1] - right_vec[1]

        new_corners = [tuple(i) for i in corners] # Remove or change this, only done cuz tuple is immutable
        self.corners = new_corners
        return new_corners


class environment:
    def __init__(self,level_dims=(500,500), num_bots=1):
        self.level_dims = level_dims
        self.num_bots = num_bots

        self.spd_increase = 0.0005 # How fast bot can change positions

        self.rendering = False

    def init_render(self):
        """
        Creates objects to render unto screen
        Should be called once per program start, when rendering first time
        :return:
        """

        pygame.init()
        pygame.display.set_caption("DD-PYTO")
        self.map=pygame.display.set_mode(self.level_dims)
        self.rendering = True

        self.bot_surface = RotSquare(pos=[self.bot.x, self.bot.y], angle=self.bot.theta,
                                     height=2*self.bot.wheel_width, width=self.bot.width,
                                     parent=self.map)

        clock = pg.time.Clock()

    def render(self):
        """
        Render changes to screen, should be called after step function
        :return:
        """
        if not self.rendering:
            self.init_render()

        clock.tick(60)

        pygame.display.update()
        self.map.fill(BLACK)

        # Render surface
        self.bot_surface.set_angle(bot.theta)
        self.bot_surface.pos[0] = bot.x
        self.bot_surface.pos[1] = bot.y
        self.bot_surface.update()

        # Show stats: velocity, angle
        theta = font.render(str('Theta  %.2f' % bot.theta), True, BLACK, WHITE)
        spd = font.render(f"v_r: {str('%.3f' % bot.v_r)}, v_l: {str('%.3f' % bot.v_l)}", True, BLACK, WHITE)
        textRect = theta.get_rect()
        textRect2 = spd.get_rect()
        environ.map.blit(theta, (0,0), textRect)
        environ.map.blit(spd, (0,40), textRect2)

    def reset(self):

        self.bot = Robot([self.level_dims[0]/2, self.level_dims[1]/2], widht=50, wheel_width=100/2)
        #test_surface = RotSquare(pos=[bot.x, bot.y], angle=bot.theta,
        #                         height=2 * bot.wheel_width, width=bot.width,
        #                         parent=environ.map)

    def step(self, action):
        bot.increase_speed(action, self.spd_increase)
        bot.update_pos()

        # Add check to see if bot is outside borders


pygame.init()

start_pos = (500, 500)

running = True

environ = env()

bot = Robot([500, 500], width=50, wheel_width=100/2)

test_surface = RotSquare(pos=[bot.x, bot.y], angle=bot.theta,
                            height=2*bot.wheel_width, width=bot.width,
                            parent=environ.map)

clock = pg.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 32)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            pass

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        bot.v_r += 0.0005
    if keys[pygame.K_s]:
        bot.v_r -= 0.0005
    if keys[pygame.K_e]:
        bot.v_l += 0.0005
    if keys[pygame.K_d]:
        bot.v_l -= 0.0005

    pygame.display.update()
    environ.map.fill(BLACK)

    # Actual bot stuff
    bot.update_pos()

    # Just rendering stuff
    test_surface.set_angle(bot.theta)
    test_surface.pos[0] = bot.x
    test_surface.pos[1] = bot.y

    test_surface.update()
    theta = font.render(str('Theta  %.2f' % bot.theta), True, BLACK, WHITE)
    spd = font.render(f"v_r: {str('%.3f' % bot.v_r)}, v_l: {str('%.3f' % bot.v_l)}", True, BLACK, WHITE)
    textRect = theta.get_rect()
    textRect2 = spd.get_rect()
    environ.map.blit(theta, (0,0), textRect)
    environ.map.blit(spd, (0,40), textRect2)