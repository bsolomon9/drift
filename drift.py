from constants import * 

from player import MovementHandler
from graphics import  EffectsHandler
from log import Logger

clock = pygame.time.Clock()
pygame.font.init()


def main():

    start_ticks=pygame.time.get_ticks()
    frame = 0

    current_track = 0
    
    player = MovementHandler()
    effects = EffectsHandler()
    logger = Logger()

    while True:
        clock.tick(60)
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit() 

        keys = pygame.key.get_pressed()

        player.update(keys)
        if player.x > WIDTH: 
            return True, (pygame.time.get_ticks()-start_ticks)/1000, logger

        logger.update(player)            

        win.fill(GREEN)
        win.blit(TRACKS[current_track],(0,0))

        player.update_death()
        if player.dead:
            return False, (pygame.time.get_ticks()-start_ticks)/1000, logger

        logger.draw_rival(frame)
        player.draw()

        effects.update(frame, player)
        effects.draw()

        pygame.display.flip()


while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit() 

    won, time, logger = main()
    menu(win,clock,won,time, logger)