import pygame
from nanobot import NanoBot  # Import the NanoBot class
from bacteria import Bacteria

# Initialize Pygame
pygame.init()

# Screen settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Character Movement")

# Create character instance
FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

# Load font
font = pygame.font.Font(None, 36)  # Default font, size 36

breach_sound = pygame.mixer.Sound("breach.wav")
bacteria_hit_sound = pygame.mixer.Sound("bacteria_fire.wav")
nanobot_hit_sound = pygame.mixer.Sound("nanobot_hit.wav")

#Set text
# Render score and lives text
    # Main game loop - Displaying Player
nanobot_laser_group = pygame.sprite.Group()
nanobot_group = pygame.sprite.Group()
nanobot = NanoBot(nanobot_laser_group)
nanobot_group.add(nanobot)

bacteria_group = pygame.sprite.Group()
bacteria_laser_group=pygame.sprite.Group()

num_rows = 5
num_cols = 11
start_x = 100
start_y = 100
spacing_x = 60  # horizontal spacing between bacteria
spacing_y = 70     # vertical spacing between rows

for row in range(num_rows):
    for col in range(num_cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        bacteria = Bacteria(x, y, 2, bacteria_laser_group,bacteria_group)
        bacteria_group.add(bacteria)
gameover=False
game_win=False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                nanobot.fire()

    screen.fill((0, 0, 0))  # Clear the screen before drawing
    # Render text
    score_text = font.render(f"Score: {nanobot.score}", True, WHITE)
    score_rect = score_text.get_rect(centerx=WINDOW_WIDTH // 2, top=60)
    
    lives_text = font.render(f"Lives: {nanobot.lives}", True, WHITE)
    lives_rect = lives_text.get_rect(topright=(WINDOW_WIDTH - 20, 70))
    
    # Draw on screen
    screen.blit(score_text, score_rect)
    screen.blit(lives_text, lives_rect)
    pygame.draw.line(screen, WHITE, (0, 50), (WINDOW_WIDTH, 50), 4)
    pygame.draw.line(screen, WHITE, (0, WINDOW_HEIGHT - 100), (WINDOW_WIDTH, WINDOW_HEIGHT - 100), 4)
    
    # Render text
    
    # Update and draw the player
    nanobot_group.update(event)
    nanobot_group.draw(screen)

    nanobot_laser_group.update()
    nanobot_laser_group.draw(screen)
    
    bacteria_group.update()
    bacteria_group.draw(screen)

    
    bacteria_laser_group.update()
    bacteria_laser_group.draw(screen)

    # Check for collisions between nanobot lasers and bacteria
  
    
    if pygame.sprite.groupcollide(nanobot_laser_group, bacteria_group, True, True):
        nanobot.score += 100
        bacteria_hit_sound.play()
    if pygame.sprite.spritecollide(nanobot, bacteria_laser_group, True):
       nanobot.lives -= 1
       nanobot_hit_sound.play()
    for bacteria in bacteria_group:
        if bacteria.rect.bottom >= WINDOW_HEIGHT - 100 or nanobot.lives<=1:
            defeat_text = font.render("You Lost! Game Over!", True, WHITE)
            defeat_text_rect = defeat_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            breach_sound.play()
            gameover=True
        
        if nanobot.score==4400:
            game_win=True
            gamewin_text=font.render("CONGRATULATIONS! YOU WON!",True,WHITE)
            gamewin_text_Rect=gamewin_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
                
        
    if gameover:
            screen.fill("black")  # Clear screen
            screen.blit(defeat_text, defeat_text_rect)  # Display "GAME OVER"
            pygame.display.update()  # Update screen

            pygame.time.delay(2000)  # Pause for 2 seconds
     
            running = False  # Exit game loop

    if game_win:
            screen.fill("black")  # Clear screen
            screen.blit(gamewin_text, gamewin_text_Rect)  #  "GAME OVER"
            pygame.display.update()  # Update screen

            pygame.time.delay(2000)  # Pause for 2 seconds

            running = False  # Exit game 

    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
