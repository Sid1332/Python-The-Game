import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.directionX = 0
        self.directionY = 25
        self.points = 0
        # self.rect.move_ip(self.directionX, self.directionY)
        # self.segments = []
        # self.addSegment()

    # class Segment:
    #     def __init__(self):
    #         self.surf = pygame.Surface((25, 25))
    #         self.surf.fill((255, 255, 255))
    #         self.rect = self.surf.get_rect()
    #         self.directionX = 0
    #         self.directionY = 25
    # def addSegment(self):
    #     surf = pygame.Surface((25, 25))
    #     surf.fill((255, 255, 255))
    #     rect = surf.get_rect()
    #     directionX = 0
    #     directionY = 25
    #     self.segments.append({surf: surf, rect: rect, directionX: directionX, directionY: directionY})

    def update(self, pressed_keys):
        
        if pressed_keys[K_UP]:
            # if self.directionY != 25:
                self.directionX = 0
                self.directionY = -25
        if pressed_keys[K_DOWN]:
            # if self.directionY != -25:
                self.directionX = 0
                self.directionY = 25
        if pressed_keys[K_LEFT]:
            # if self.directionX != 25:
                self.directionX = -25
                self.directionY = 0
        if pressed_keys[K_RIGHT]:
            # if self.directionX != -25:
                self.directionX = 25
                self.directionY = 0
        self.rect.move_ip(self.directionX, self.directionY)
        # if pressed_keys[K_UP]:
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0, 5)
        # if pressed_keys[K_LEFT]:
        #     self.rect.move_ip(-5, 0)
        # if pressed_keys[K_RIGHT]:
        #     self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            
    def addPoints(self):
        self.points += 1
        

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((100, 100, 100))
        self.rect = self.surf.get_rect()
        self.position = (int(random.randint(0, SCREEN_HEIGHT/25)*25), int(random.randint(0, SCREEN_WIDTH/25)*25))
        # if self.position[0] <= 0 or self.position[0] >= SCREEN_HEIGHT:
        #     self.position[0] = 25
        # if self.position[1] < 0 or self.position[1] > SCREEN_WIDTH:
        #     self.position[1] = 25
    
    def update(self, player, pressed_keys):
        if self.position == player.rect.topleft:
            self.position = (int(random.randint(0, SCREEN_HEIGHT/25)*25), int(random.randint(0, SCREEN_WIDTH/25)*25))
            player.addPoints()
            # if self.position[0] <= 0 or self.position[0] >= SCREEN_HEIGHT:
            #     self.position[0] = 25
            # if self.position[1] < 0 or self.position[1] > SCREEN_WIDTH:
            #     self.position[1] = 25
        if pressed_keys[K_SPACE]:
            self.position = (int(random.randint(0, SCREEN_HEIGHT/25)*25), int(random.randint(0, SCREEN_WIDTH/25)*25))
            


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
clock = pygame.time.Clock()

player = Player()
food = Food()

while running:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    pressed_keys = pygame.key.get_pressed()

    
    
    player.update(pressed_keys)

    food.update(player, pressed_keys)

    screen.fill((0, 0, 0))
    
    screen.blit(food.surf, food.position)

    screen.blit(player.surf, player.rect)


    pygame.display.flip()
print(player.points)