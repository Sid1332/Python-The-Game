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
    QUIT,
    MOUSEBUTTONDOWN,
    K_p,
    K_w,
    K_a,
    K_s,
    K_d,
    K_m
)

class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super(Player, self).__init__()
        self.surf = pygame.Surface((25, 25))
        self.surf.fill(color)
        self.rect = self.surf.get_rect()
        self.directionX = 0
        self.directionY = 25
        self.points = 0
        self.segments = [PlayerSegment(self, 0)]
        self.stopped = False
        self.walldeathdelay = 2
        self.queuedDirections = []
        
        
    def update(self, pressed_keys, pressable):
        moved = False
        while not moved:
            if len(self.queuedDirections) > 0:
                if self.directionX == -self.queuedDirections[0][0] and self.directionY == -self.queuedDirections[0][1]:
                    pass
                elif not (self.directionX == self.queuedDirections[0][0] and self.directionY == self.queuedDirections[0][1]):
                    self.directionX = self.queuedDirections[0][0]
                    self.directionY = self.queuedDirections[0][1]
                    moved = True
                self.queuedDirections.pop(0)
            else:
                break
        
        if pressed_keys[pressable[0]]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionY != 25 and not (self.directionX == 0 and self.directionY == -25):
                self.directionX = 0
                self.directionY = -25
                moved = True
        if pressed_keys[pressable[2]]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionY != -25 and not (self.directionX == 0 and self.directionY == 25):
                self.directionX = 0
                self.directionY = 25
                moved = True
        if pressed_keys[pressable[1]]:
            if moved:
                self.queuedDirections.append([0, -25])
            elif self.directionX != 25 and not (self.directionX == -25 and self.directionY == 0):
                self.directionX = -25
                self.directionY = 0
                moved = True
        if pressed_keys[pressable[3]]:
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

    
    def multiplayerUpdate(self, pressed_keys, pressable, other_player):
        for segment in other_player.segments:
            if self.rect.topleft == segment.position:
                return False
        return self.update(pressed_keys, pressable)



        
class PlayerSegment(pygame.sprite.Sprite):
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
        if pressed_keys[K_SPACE]:
            self.position = (int(random.randint(0, (SCREEN_WIDTH - 25)/25)*25), int(random.randint(0, (SCREEN_HEIGHT - 25)/25)*25))
            print(self.position)
            




def singleloop():
    player = Player((255, 255, 255))
    food = Food()
    playagain = False
    running = True
    while running:
        clock.tick(10)
        
        
        pressed_keys = pygame.key.get_pressed()
        
        running = player.update(pressed_keys, [K_UP, K_LEFT, K_DOWN, K_RIGHT])

        food.update(player, pressed_keys)
  
        screen.fill((0, 0, 0))

        for segment in reversed(player.segments):
            segment.update(player)
            screen.blit(segment.surf, segment.position)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                elif event.key == K_p:
                    pauseloop()
            if event.type == QUIT:
                quit()
        
        screen.blit(food.surf, food.position)
        screen.blit(player.surf, player.rect)
        pygame.display.flip()

    return [[player]]

def multiplayerloop():
    player1 = Player((255, 255, 255))
    player2 = Player((0, 255, 0))
    player2.rect.topleft = (0, 25)
    player2.segments[0].position = (0, 25)
    food = Food()
    onerunning = True
    tworunning = True
    while onerunning and tworunning:
        clock.tick(10)      
        
        pressed_keys = pygame.key.get_pressed()
        
        onerunning = player1.multiplayerUpdate(pressed_keys, [K_UP, K_LEFT, K_DOWN, K_RIGHT], player2) 
        tworunning = player2.multiplayerUpdate(pressed_keys, [K_w, K_a, K_s, K_d], player1)

        food.update(player1, pressed_keys)
        food.update(player2, pressed_keys)
        
        screen.fill((0, 0, 0))

        for segment in reversed(player1.segments):
            segment.update(player1)
            screen.blit(segment.surf, segment.position)

        for segment in reversed(player2.segments):
            segment.update(player2)
            screen.blit(segment.surf, segment.position)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                elif event.key == K_p:
                    pauseloop()
            if event.type == QUIT:
                quit()
        
        screen.blit(food.surf, food.position)

        screen.blit(player1.surf, player1.rect)
        screen.blit(player2.surf, player2.rect)

        pygame.display.flip()
    
    return [[player1, player2], [onerunning, tworunning]]
  
def pauseloop():
    running = True
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('Comic Sans MS', 30)
    secondfont = pygame.font.SysFont('Comic Sans MS', 15)
    text = font.render("Paused.", False, (255, 255, 255))
    textrect = text.get_rect()
    textrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 25)
    secondtext = secondfont.render("Click anywhere to resume.", False, (255, 255, 255))
    secondtextrect = secondtext.get_rect()
    secondtextrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2))
    screen.blit(text, textrect)
    screen.blit(secondtext, secondtextrect)
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            if event.type == QUIT:
                quit()
            if event.type == MOUSEBUTTONDOWN:
                running = False

def gameloop(singleplayer):
    if singleplayer:
        return singleloop()
    else:
        return multiplayerloop()
    
def gameoverloop(singleplayer, highscore, players):
    font = pygame.font.SysFont('Comic Sans MS', 30)
    quitplayagain = font.render("Esc to quit; click anywhere to play again", False, (255, 255, 255))
    quitplayagainract = quitplayagain.get_rect()
    running = True
    screen.fill((0, 0, 0))
    if singleplayer:
        if players[0][0].points > highscore:
            f = open("qwerty.uiop", "w")
            f.write(str(players[0][0].points))
            f.close()
            highscoretext = font.render("New Highscore!", False, (255, 255, 255))
            highscore = players[0][0].points
        else:
            highscoretext = font.render("Highscore: " + str(highscore), False, (255, 255, 255))
        
        highscoretextrect = highscoretext.get_rect()
        highscoretextrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2))
        score_text = font.render("Score: " + str(players[0][0].points), False, (255, 255, 255))
        score_textRect = score_text.get_rect()
        score_textRect.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) - 50))
        quitplayagainract.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) + 50))
        gameover = font.render("Game Over!", False, (255, 255, 255))
        gameoverRect = gameover.get_rect()
        gameoverRect.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) - 100))
        brak = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    brak = True
            screen.blit(score_text, score_textRect)
            screen.blit(gameover, gameoverRect)
            screen.blit(quitplayagain, quitplayagainract)
            screen.blit(highscoretext, highscoretextrect)
            pygame.display.flip()
            if brak:
                break
    else:
        if players[1][0] and players[1][1]:
            winnertext = font.render("It is a tie!", False, (255, 255, 255))
        elif players[1][0]:
            winnertext = font.render("Player 1 wins!", False, (255, 255, 255))
        else:
            winnertext = font.render("Player 2 wins!", False, (255, 255, 255))

        winnertextrect = winnertext.get_rect()
        winnertextrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 25)
        quitplayagainract.center = (((SCREEN_WIDTH//2), (SCREEN_HEIGHT//2) + 25))
        screen.blit(winnertext, winnertextrect)
        screen.blit(quitplayagain, quitplayagainract)
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                if event.type == QUIT:
                    quit()
                if event.type == MOUSEBUTTONDOWN:
                    running = False

def titleloop():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    secondfont = pygame.font.SysFont('Comic Sans MS', 15)
    thirdfont = pygame.font.SysFont('Comic Sans MS', 10)
    text = secondfont.render("For Singleplayer mode: Arrow Keys to move - P to pause - Press S to start", False, (255, 255, 255))
    textrect = text.get_rect()
    textrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 25)
    secondtext = secondfont.render("For Multiplayer mode: Arrow Keys to move Player 1 - WASD to move Player 2 - P to pause - Press M to start", False, (255, 255, 255))
    secondtextrect = secondtext.get_rect()
    secondtextrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 45)
    title = font.render("Python (The Game)", False, (255, 255, 255))
    titlerect = title.get_rect()
    titlerect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    credittext = thirdfont.render("Made by Siddhartha Guggilam", False, (255, 255, 255))
    credittextrect = credittext.get_rect()
    credittextrect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 59)
    screen.blit(title, titlerect)
    screen.blit(text, textrect)
    screen.blit(secondtext, secondtextrect)
    screen.blit(credittext, credittextrect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
                if event.key == K_m:
                    return False
                if event.key == K_s:
                    return True
            if event.type == QUIT:
                quit()
            
def credits():
    font = pygame.font.SysFont('Comic Sans MS', 30)
    secondfont = pygame.font.SysFont('Comic Sans MS', 15)

pygame.init()
pygame.display.set_caption("Python (the game)")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True
clock = pygame.time.Clock()

f = open("qwerty.uiop", "r")
highscore = int(f.read(10))
f.close()

singleplayer = titleloop()

running = True
while running:
    players = gameloop(singleplayer)
    
    gameoverloop(singleplayer, highscore, players)
