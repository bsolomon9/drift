from constants import *

class EffectsHandler:
    def __init__(self):
        self.drift_lines = []
        self.smoke = []
    
    def update(self, frame, player):
        if frame % FRAMES_BETWEEN_SMOKE_SPAWN == 0:
            for i in range(SMOKE_PER_SPAWN):
                random_x = round(random.randrange(RANDOM_SMOKE_RANGE) * -player.dir_vector.x)
                random_y = round(random.randrange(RANDOM_SMOKE_RANGE) * -player.dir_vector.y)
                self.smoke.append([random.choice(SMOKE_PALETTE), (player.x+(random_x -player.dir_vector.x*10), player.y+(random_y-player.dir_vector.y*10) ), SMOKE_START_SIZE])
            
        if player.gap < MAX_TIRE_TRACK_GAP and player.movement_speed>MIN_TIRE_TRACK_SPEED:
            self.drift_lines.append( ((player.x-player.dir_vector.x*10+player.dir_vector.x*4)-1, (player.y-player.dir_vector.y*10)-2 ) )
            self.drift_lines.append( ((player.x-player.dir_vector.x*10+player.dir_vector.x*-4)-1, (player.y-player.dir_vector.y*10)-2 ) )
        
        if len(self.drift_lines) > MAX_TIRE_TRACKS: 
            self.drift_lines.pop(0)
            self.drift_lines.pop(1)
    

    def draw(self):
        for rectangle in self.drift_lines:
            win.blit(DRIFT_SURF, rectangle)

        for particle in self.smoke:
            pygame.draw.circle(win,particle[0], particle[1], particle[2])
            particle[2] += SMOKE_SIZE_INCREASE
            if particle[2] > SMOKE_MAX_SIZE:
                self.smoke.remove(particle)