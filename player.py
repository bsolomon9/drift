from constants import *

class MovementHandler:
    def __init__(self):
        self.angle = 2*math.pi
        self.x = 150
        self.y = 150

        self.angle_momentum = 0

        self.dir_vector = pygame.math.Vector2(math.cos(self.angle),math.sin(self.angle))
        self.movement_vector = self.dir_vector
        self.dead = False

    def update(self, keys):
        self.movement_speed = self.movement_vector.magnitude()
        if self.movement_speed > 0:
            #how close the movement vector is to being perpendicular to the direction vector
            self.gap = abs((self.movement_vector.normalize() - self.dir_vector).magnitude() - 1.5)

        if keys:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: 
                self.turn(-1)

            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: 
               self.turn(1)

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                self.movement_vector += self.dir_vector * GAS

            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                if self.movement_speed  > 0:
                    self.movement_vector.scale_to_length(self.movement_speed - BREAK_FORCE)
                    if self.movement_speed < 0:
                        self.movement_vector = pygame.Vector2(0,0)


        self.dir_vector = pygame.math.Vector2(math.cos(self.angle),math.sin(self.angle))
        self.update_angle_momentum()

        self.movement_speed = self.movement_vector.magnitude()
        self.apply_friction()
        self.update_location()
    
    def draw(self):
        win.blit(self.draw_info[0], self.draw_info[1])

        #draw_vector(win,self.x,self.y,self.movement_vector,(0,0,255))


    def apply_friction(self):
        friction = FRICTION + (self.gap**FRICTION_GAP_EXPONENT) / FRICTION_GAP_DIVISOR

        if self.movement_speed > 0.1:
            self.movement_vector.scale_to_length(self.movement_speed/friction)
        else:
            self.movement_vector = pygame.Vector2(0,0)


    def update_death(self):
        self.draw_info = Rotate(CAR_SPRITE, (self.x, self.y), (X_OFFSET, Y_OFFSET), -math.degrees(self.angle))
        self.dead = (not self.is_alive())


    def update_location(self):
        self.x += self.movement_vector.x
        self.y += self.movement_vector.y

        #if self.x > WIDTH:  x = 0; track = 1; return True
        #elif self.x < 0: x = WIDTH; track = -1
    
        #if self.y > HEIGHT: self.y = 0 
        #elif self.y < 0: self.y = HEIGHT 
    

    def turn(self, sign):
        self.angle += (sign*TURN)
        self.movement_vector = rotate_vector(self.movement_vector,sign*TURN/1.5)
        self.angle_momentum += (sign * (TURN_ANGLE_MOMENTUM * self.movement_speed/2))

    

    def update_angle_momentum(self):
        if self.angle_momentum > 1: self.angle_momentum = 1
        if self.angle_momentum < -1: self.angle_momentum = -1
    
        self.angle += self.angle_momentum

        if self.angle_momentum > 0: self.angle_momentum -= ANGLE_MOMENTUM_DECAY
        if self.angle_momentum < 0: self.angle_momentum += ANGLE_MOMENTUM_DECAY


    
    
    def is_alive(self):
        center = self.draw_info[1].center
    
        if center[0] < WIDTH and center[0] > 0 and center[1] < HEIGHT and center[1] > 0:
            return win.get_at(center) == GREY
        else:
            return True