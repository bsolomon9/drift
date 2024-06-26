from constants import *

class Logger:
    def __init__(self):
        self.player_log = []
        with open("best.json", "r") as file:
            self.best = json.load(file)
        self.best_time = len(self.best)

    def update(self, player):
        self.player_log.append( [player.x, player.y, player.angle] )

    def draw_shadows(self):
        for index, location in enumerate(self.best):
            if index % 3 == 0:
                info = Rotate(RIVAL_SPRITE, (location[0], location[1]), (X_OFFSET, Y_OFFSET), -math.degrees(location[2]))
                win.blit(info[0], info[1])

        for index, location in enumerate(self.player_log):
            if index % 3 == 0:
                info = Rotate(CAR_SPRITE, (location[0], location[1]), (X_OFFSET, Y_OFFSET), -math.degrees(location[2]))
                win.blit(info[0], info[1])
    
    def draw_rival(self, frame):
        if self.best != [] and (self.best_time > frame):
            info = Rotate(RIVAL_SPRITE, (self.best[frame][0], self.best[frame][1]), (X_OFFSET, Y_OFFSET), -math.degrees(self.best[frame][2]))
            win.blit(info[0], info[1])
    
    def did_win(self, finished):
       return (len(self.player_log) < len(self.best) or len(self.best) == 0) and finished
    
    def update_permanent_log(self):
        with open("best.json", "w") as file:
            json.dump(self.player_log, file)