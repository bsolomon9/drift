import pygame, os, glob, json, random, math


pygame.init()
path = os.path.dirname(os.path.realpath(__file__))


WIDTH = 800
HEIGHT = 800

win = pygame.display.set_mode((WIDTH,HEIGHT), pygame.HWSURFACE, pygame.DOUBLEBUF)

GREEN = (10,100,50)
SILVER = (192,192,192)
GREY = (100,100,107)

CAR_SPRITE = pygame.image.load(path + "\cars\CAR.png").convert()
CAR_SPRITE.set_colorkey((0,0,0))

RIVAL_SPRITE = pygame.image.load(path + "\cars\RIVAL.png").convert()
RIVAL_SPRITE.set_colorkey((0,0,0))

X_OFFSET, Y_OFFSET = CAR_SPRITE.get_rect().width/2, CAR_SPRITE.get_rect().height/2

TURN = 0.055
TURN_ANGLE_MOMENTUM = 0.0011
ANGLE_MOMENTUM_DECAY = 0.001 

FRICTION = 1.001
FRICTION_GAP_EXPONENT = 0.1
FRICTION_GAP_DIVISOR = 50

SMOKE_PALETTE = [
    (116, 130, 118), 
    (144, 153, 147), 
    (245, 245, 245), 
    (211, 222, 218), 
    (191, 206, 199)]
RANDOM_SMOKE_RANGE = 10
FRAMES_BETWEEN_SMOKE_SPAWN = 5
SMOKE_PER_SPAWN = 5
SMOKE_START_SIZE = 2
SMOKE_SIZE_INCREASE = 0.5
SMOKE_MAX_SIZE = 6

BREAK_FORCE =  0.07
GAS = 0.17

MIN_TIRE_TRACK_SPEED = 2
MAX_TIRE_TRACK_GAP = 0.999
MAX_TIRE_TRACKS = 800

DRIFT_SURF = pygame.Surface((2,4))
pygame.draw.rect(DRIFT_SURF, (20,20,20), [0,0,2,4])


TRACKS = []
for filename in os.listdir(path + "\maps"):
    if filename[0].isdigit():
        image = pygame.image.load(path + "\\maps\\" + filename).convert()
        image.set_colorkey((0,0,0))
        TRACKS.append(image)




def Rotate(image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    return[rotated_image, rotated_image_rect]


def rotate_vector(vector, angle):
    x2 = vector.x * math.cos(angle) - vector.y * math.sin(angle)
    y2 = vector.x * math.sin(angle) + vector.y * math.cos(angle)

    return pygame.Vector2(x2,y2)


def draw_vector(win,x,y,vector, col):
    pygame.draw.line(win,col, [x,y] ,[x+vector.x*10, y+vector.y*10])


def menu(win,clock,finished,time, logger):

    font = pygame.font.SysFont("lucidaconsole", 20)
    if finished:
        message_surf = font.render('You Completed, press enter to retry',True, (25, 10,255))
        message_size = font.size('You Completed, press enter to retry')
        score_message_surf = font.render(f'time: {time}', True, (25,10,255))
        score_message_size = font.size(f'time: {time}')

        if logger.did_win(finished):
            logger.update_permanent_log()
        
            message_surf = font.render('You Win, press enter to retry',True, (255, 215,0))
            message_size = font.size('You Win, press enter to retry')
            score_message_surf = font.render(f'time: {time}', True, (255,215,0))
            score_message_size = font.size(f'time: {time}')

    else:
        message_surf = font.render('You Died, press enter to retry',True, (255, 130,160))
        message_size = font.size('You Died, press enter to retry')
        score_message_surf = font.render(f'time: {time}', True, (255,130,160))
        score_message_size = font.size(f'time: {time}')

    logger.draw_shadows()

    win.blit(message_surf, [WIDTH/2-message_size[0]/2, HEIGHT/2-message_size[1]/2])
    win.blit(score_message_surf, [WIDTH/2-score_message_size[0]/2, HEIGHT/2+score_message_size[1]/2])
    pygame.display.flip()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]: return
