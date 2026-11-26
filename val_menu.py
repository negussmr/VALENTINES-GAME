import pygame, time
from pathlib import Path

# Initializing
pygame.init()
WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MAIN MENU")
TEXT_FONT = pygame.font.SysFont(None, 32)
fps = pygame.time.Clock()

# Colors
WHITE = (255,255,255)   
RED = (255,0,0)
BLUE = (0,0,255)
PURPLE = (128,0,128)
BLACK = (0,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
GRAY = (128,128,128)

#Classes
class Player:  
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.skins = []
        self.current_skin_index = 0 
    
    def draw(self):
        if self.skins:
            # Load and display current skin
            skin_path = f"valentine_game/VALENTINES-GAME/players/{self.skins[self.current_skin_index]}.png"
            sprite = pygame.image.load(skin_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (50, 50))
            screen.blit(sprite, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
    
    def draw_static(self, x, y):
        temp_rect = pygame.Rect(x, y, 50, 50)
        if self.skins:
            skin_path = f"valentine_game/VALENTINES-GAME/players/{self.skins[self.current_skin_index]}.png"
            sprite = pygame.image.load(skin_path).convert_alpha()
            sprite = pygame.transform.scale(sprite, (50, 50))
            screen.blit(sprite, temp_rect)
        else:
            pygame.draw.rect(screen, self.color, temp_rect)
    def draw_nametag(self):
        name = "Runner" if self.color == BLUE else "Pusher"
        text = TEXT_FONT.render(name, True, (BLUE if name == "Runner" else RED))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        screen.blit(text, text_rect)


class Button:
    def __init__(self, x, y, width, height, text, player=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.player = player
    
    def draw(self):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        if self.player and self.player.skins:
            display_text = f"{self.text}: {self.player.skins[self.player.current_skin_index]}"
        else:
            display_text = self.text
        
        text_surf = TEXT_FONT.render(display_text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def next_skin(self, player):
        if player.skins:
            player.current_skin_index = (player.current_skin_index + 1) % len(player.skins)
    
    def previous_skin(self, player):
        if player.skins:
            player.current_skin_index = (player.current_skin_index - 1) % len(player.skins)

#Class Objects
runner = Player(200, 300, BLUE)
pusher = Player(550, 300, RED)

runner_button = Button(100, 400, 300, 50, "Runner", player=runner)
pusher_button = Button(450, 400, 300, 50, "Pusher", player=pusher)

# State Variables
runnerReady = False
pusherReady = False


# Loading Skins to Player Class
skin_folder = Path("valentine_game/VALENTINES-GAME/players/")
runner.skins = [f.stem for f in skin_folder.glob("*.png")]
pusher.skins = [f.stem for f in skin_folder.glob("*.png")]

running = True
while running:
    screen.fill(WHITE)
    
    runner.draw()
    pusher.draw()
    
    runner_button.draw()
    pusher_button.draw()
    
    #Text Ready
    if runnerReady:
        ready_text = TEXT_FONT.render("Runner Ready!", True, GREEN)
        screen.blit(ready_text, (runner_button.rect.x, runner_button.rect.y - 30))
    else:
        not_ready_text = TEXT_FONT.render("Runner Not Ready!", True, RED)
        screen.blit(not_ready_text, (runner_button.rect.x, runner_button.rect.y - 30))
    if pusherReady:
        ready_text = TEXT_FONT.render("Pusher Ready!", True, GREEN)
        screen.blit(ready_text, (pusher_button.rect.x, pusher_button.rect.y - 30))
    else:
        not_ready_text = TEXT_FONT.render("Pusher Not Ready!", True, RED)
        screen.blit(not_ready_text, (pusher_button.rect.x, pusher_button.rect.y - 30))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_s:
                runner_button.next_skin(runner)
            elif event.key == pygame.K_w:
                runner_button.previous_skin(runner)
            elif event.key == pygame.K_d:
                runnerReady = True
            elif event.key == pygame.K_a:
                runnerReady = False
            elif event.key == pygame.K_DOWN:
                pusher_button.next_skin(pusher)
            elif event.key == pygame.K_UP:
                pusher_button.previous_skin(pusher)
            elif event.key == pygame.K_RIGHT:
                pusherReady = True
            elif event.key == pygame.K_LEFT:
                pusherReady = False
                
    pygame.display.flip()
    fps.tick(60)
    
pygame.quit()