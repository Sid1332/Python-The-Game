import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN
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
        self.segments = [PlayerSegment(self, 0)]
        self.stopped = False
        self.walldeathdelay = 2
        self.queuedDirections = []
        
        
    def update(self, pressed_keys):
        moved = False
        if len(self.queuedDirections) > 0:
            if self.directionX == -self.queuedDirections[0][0] and self.directionY == -self.queuedDirections[0][1]:
                pass
            elif not (self.directionX == self.queuedDirections[0][0] and self.directionY == self.queuedDirections[0][1]):
                self.directionX = self.queuedDirections[0][0]
                self.directionY = self.queuedDirections[0][1]
                moved = True
            self.queuedDirections.pop(0)
        
        if pressed_keys[K_UP]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionY != 25 and not (self.directionX == 0 and self.directionY == -25):
                self.directionX = 0
                self.directionY = -25
                moved = True
        if pressed_keys[K_DOWN]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionY != -25 and not (self.directionX == 0 and self.directionY == 25):
                self.directionX = 0
                self.directionY = 25
                moved = True
        if pressed_keys[K_LEFT]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionX != 25 and not (self.directionX == -25 and self.directionY == 0):
                self.directionX = -25
                self.directionY = 0
                moved = True
        if pressed_keys[K_RIGHT]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionX != -25 and not (self.directionX == 25 and self.directionY == 0):
                self.directionX = 25
                self.directionY = 0
                moved = True
        
        self.rect.move_ip(self.directionX, self.directionY)

        self.stopped = False
        if self.rect.left < 0:
            self.rect.left = 0
            self.stopped = True
            self.walldeathdelay -= 1
        if self.rect.top < 0:
            self.rect.top = 0
            self.stopped = True
            self.walldeathdelay -= 1
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.stopped = True
            self.walldeathdelay -= 1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.stopped = True
            self.walldeathdelay -= 1

        if not self.stopped:
            self.walldeathdelay = 2

        if self.walldeathdelay == 0:
            return False
        
        for segment in self.segments[1 : len(self.segments) - 1]:
            if self.rect.topleft == segment.position:
                return False
        return True
            
            
    def addPoints(self):
        self.points += 1
        self.segments.append(PlayerSegment(self, len(self.segments)))
        
class PlayerSegment(pygame.sprite.Sprite) :
    def __init__(self, player, index):
        super(PlayerSegment, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((200, 200, 200))
        self.rect = self.surf.get_rect()
        self.directionX = player.directionX
        self.directionY = player.directionY
        self.index = index
        self.position = (list(player.rect.topleft)[0] - player.directionX, list(player.rect.topleft)[1])
    
    def update(self, player):
        if not player.stopped: 
            if self.index == 0:
                self.directionX = list(player.rect.topleft)[0] - list(self.position)[0]
                self.directionY = list(player.rect.topleft)[1] - list(self.position)[1] 
            else:
                self.directionX = list(player.segments[self.index - 1].position)[0] - list(self.position)[0]
                self.directionY = list(player.segments[self.index - 1].position)[1] - list(self.position)[1]
            self.position = (list(self.position)[0] + self.directionX, list(self.position)[1] + self.directionY)

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((100, 100, 100))
        self.rect = self.surf.get_rect()
        self.position = (int(random.randint(0, (SCREEN_WIDTH - 25)/25)*25), int(random.randint(0, (SCREEN_HEIGHT - 25)/25)*25))
    
    def update(self, player, pressed_keys):
        if self.position == player.rect.topleft:
            self.position = (int(random.randint(0, (SCREEN_WIDTH - 25)/25)*25), int(random.randint(0, (SCREEN_HEIGHT - 25)/25)*25))
            player.addPoints()
            


pygame.init()
pygame.display.set_caption("Python (the game)")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
clock = pygame.time.Clock()


playagain = True

while running and playagain:
    player = Player()
    food = Food()
    playagain = False
    while running:
        clock.tick(5*2)
        
        
        pressed_keys = pygame.key.get_pressed()

        
        
        running = player.update(pressed_keys)

        food.update(player, pressed_keys)

        
        screen.fill((0, 0, 0))


        for segment in reversed(player.segments):
            segment.update(player)
            screen.blit(segment.surf, segment.position)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            if event.type == QUIT:
                quit()
        
        screen.blit(food.surf, food.position)

        screen.blit(player.surf, player.rect)

        pygame.display.flip()
        

    running = True
    font = pygame.font.SysFont('Comic Sans MS', 30)
    score_text = font.render(str(player.points), False, (255, 255, 255))
    score_textRect = score_text.get_rect()
    score_textRect.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) - 50))
    gameover = font.render("Game Over!", False, (255, 255, 255))
    gameoverRect = gameover.get_rect()
    gameoverRect.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) - 100))
    quitplayagain = font.render("Esc to quit; click anywhere to play again", False, (255, 255, 255))
    quitplayagainract = quitplayagain.get_rect()
    quitplayagainract.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2)))
    brak = False
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                playagain = True
                brak = True
        screen.fill((0, 0, 0))
        screen.blit(score_text, score_textRect)
        screen.blit(gameover, gameoverRect)
        screen.blit(quitplayagain, quitplayagainract)
        pygame.display.flip()
        if brak:
            break


    
