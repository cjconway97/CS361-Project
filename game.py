import pygame
from sys import exit

pygame.init()

# Creating screen of size width x height pixels
display_width = 800
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Potato')
clock = pygame.time.Clock()
font = pygame.font.Font('Fonts/Pixeltype.ttf', 50)

# Establishing game state
is_game_active = -1

# Creating all the skybox + ground surfacesto use
sky_surface = pygame.image.load('Background/Environment/PNG/sky.png').convert()
sea_surface = pygame.image.load('Background/Environment/PNG/sea.png').convert()
ground_surface = pygame.image.load('Background/Environment/PNG/ground1.png').convert_alpha()

# Creating score surfaces
# score_surface = font.render('Score:', False, 'Black')
# score_rect = score_surface.get_rect(center=(400, 50))
end_score_surface = font.render('Score:', False, 'Black')
end_score_rect = end_score_surface.get_rect(center=(400, 50))

# Creating title screen surfaces
# Creating end screen surfaces
start_surface_title = font.render('Potato...', False, 'White')
start_surface_play = font.render('Play!', False, 'White', 'Green')
start_surface_quit = font.render('Quit :(', False, 'White', 'Red')
start_surface_quit2 = font.render('Are You Sure You Want to Quit?', False, 'White', 'Red')
start_surface_quit2_yes = font.render('Yes', False, 'White', 'Green')
start_surface_quit2_no = font.render('No', False, 'White', 'Red')
start_surface_hiscores = font.render('View Hiscores', False, 'White', 'Purple')
start_surface_changelog = font.render('Recent Changes:', False, 'White')
start_rect_title = start_surface_play.get_rect(center=(375, 150))
start_rect_play = start_surface_play.get_rect(center=(400, 200))
start_rect_quit = start_surface_quit.get_rect(center=(400, 250))
start_rect_quit2 = start_surface_quit2.get_rect(center=(400, 275))
start_rect_quit2_yes = start_surface_quit2_yes.get_rect(center=(350, 325))
start_rect_hiscores = start_surface_hiscores.get_rect(center=(400, 300))
start_rect_quit2_no = start_surface_quit2_no.get_rect(center=(450, 325))
start_rect_changelog = start_surface_changelog.get_rect(center=(150, 375))
second_quit = 0

# Creating end screen surfaces
end_surface1 = font.render('Press *Spacebar* to try again!', False, 'Black')
end_surface2 = font.render('Press *Esc Button* to see the title menu!', False, 'Black')
end_surface3 = font.render('Game Over!', False, 'Black')
end_rect1 = end_surface1.get_rect(center=(400, 200))
end_rect2 = end_surface2.get_rect(center=(400, 250))
end_rect3 = end_surface3.get_rect(center=(400, 150))

# Creating Hiscore screen surfaces
hiscore_surface1 = font.render('Nothing Here Yet...', False, 'White')
hiscore_surface2 = font.render('Return to Title', False, 'White', 'Green')
hiscore_rect1 = hiscore_surface1.get_rect(center=(400, 200))
hiscore_rect2 = hiscore_surface2.get_rect(center=(400, 300))

# Creating enemy + hit box
enemy_surface = pygame.image.load('Enemy Assets/Enemies Files/sprites/fox/fox1.png').convert_alpha()
enemy_surface = pygame.transform.scale(enemy_surface, (50, 50))
enemy_rect = enemy_surface.get_rect(midbottom=(800, 315))

class Player:

    def __init__(self):
        self.player_speed = 10
        self.player_gravity = 0
        self.player_surface = pygame.image.load(
            'Player Assets/BlueWizard Animations/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00000.png').convert_alpha()
        self.player_surface = pygame.transform.scale(self.player_surface, (75, 75))
        self.player_rect = self.player_surface.get_rect(midbottom=(50, 335))

    def get_player_speed(self):
        return self.player_speed

    def get_player_surface(self):
        return self.player_surface

    def get_player_rect(self):
        return self.player_rect

    def get_left_position(self):
        return self.player_rect.left

    def get_right_position(self):
        return self.player_rect.right

    def get_bottom_position(self):
        return self.player_rect.bottom

    def move(self, keys):
        self.player_rect.right += (keys[pygame.K_d] - keys[pygame.K_a]) * self.player_speed
        if keys[pygame.K_SPACE] is True and self.player_rect.bottom >= 315:
            self.player_gravity = -20

    def reset(self):
        self.player_rect = self.player_surface.get_rect(midbottom=(50, 335))

    def induce_gravity(self):
        self.player_gravity += 1
        self.player_rect.bottom += self.player_gravity

    def set_left_position(self, pos):
        self.player_rect.left = pos

    def set_right_position(self, pos):
        self.player_rect.right = pos

    def set_bottom_position(self, pos):
        self.player_rect.bottom = pos

class Enemy:

    def __init__(self):
        self.speed = 1
        self.gravity = 0
        self.surface = None
        self.rect = None

    def create_enemy(self, surface):
        self.surface = surface
        self.rect = surface.get_rect(midbottom=(800, 315))

    def get_speed(self):
        return self.speed

    def get_surface(self):
        return self.surface

    def get_rect(self):
        return self.rect

    def get_left_position(self):
        return self.rect.left

    def get_right_position(self):
        return self.rect.right

    def get_bottom_position(self):
        return self.rect.bottom

    def think(self):
        # TO BE IMPLEMENTED, THIS WILL BE THE ENEMY AI
        return None

    def move(self):
        # think()
        self.rect.left -= 1

    def induce_gravity(self):
        self.gravity += 1
        self.rect.bottom += self.gravity

    def set_left_position(self, pos):
        self.rect.left = pos

    def set_right_position(self, pos):
        self.rect.right = pos

    def set_bottom_position(self, pos):
        self.rect.bottom = pos

def display_score():
    current_time = int((pygame.time.get_ticks()/1000)-start_time)
    score_surface = font.render(str(current_time), False, 'Black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)

start_time = 0
player = Player()
enemies = []
is_game_active = -1
while True:
    # Establish movement + quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Handling inputs at game over screen
        elif is_game_active == 0:
            player.reset()
            # enemy.rest()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                enemies = []
                start_time = pygame.time.get_ticks()/1000
                is_game_active = 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                enemies = []
                is_game_active = -1

        # Handling inputs at hiscore screen
        elif is_game_active == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hiscore_rect2.collidepoint(event.pos):
                    is_game_active = -1

        # Handling clicks at title screen
        elif is_game_active == -1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect_play.collidepoint(event.pos):
                    second_quit = 0
                    enemies = []
                    start_time = pygame.time.get_ticks()/1000
                    is_game_active = 1
                if start_rect_quit.collidepoint(event.pos):
                    second_quit = 1
                if start_rect_quit2_yes.collidepoint(event.pos):
                    pygame.quit()
                    exit()
                if start_rect_quit2_no.collidepoint(event.pos):
                    second_quit = 0
                if start_rect_hiscores.collidepoint(event.pos):
                    is_game_active = 2

    # Build skybox
    skybox_x = 0
    while skybox_x < display_width + 112:
        screen.blit(sky_surface, (skybox_x, 0))
        screen.blit(sea_surface, (skybox_x, 304))
        skybox_x += 112

    if is_game_active == 1:
        # Build ground
        ground_x = -50
        while ground_x < display_width + 50:
            screen.blit(ground_surface, (ground_x, 300))
            ground_x += 75

        # Create text surfaces (if needed)
        display_score()

        # Handle player movement + creation
        keys = pygame.key.get_pressed()
        player.move(keys)
        player.induce_gravity()

        if player.get_left_position() > 750:
            player.set_right_position(50)
        if player.get_bottom_position() >= 315:
            player.set_bottom_position(315)
        screen.blit(player.get_player_surface(), player.get_player_rect())

        # Move enemies
        count = 0
        for enemy in enemies:
            enemy.move()
            screen.blit(enemy.get_surface(), enemy.get_rect())
            #Handling collisions with player (if any)
            if player.get_player_rect().colliderect(enemy.get_rect()):
                end_score_surface2 = font.render(str(int((pygame.time.get_ticks()/1000)-start_time)), False, 'Black')
                end_score_rect2 = end_score_surface2.get_rect(midleft=(460, 50))
                is_game_active = 0
                break
            if enemy.get_right_position() < 0:
                enemies.pop(count)
            count += 1


        # Spawn additional enemies
        if len(enemies) == 0:
            new_enemy = Enemy()
            new_enemy.create_enemy(enemy_surface)
            enemies.append(new_enemy)

    # Game Over Screen
    elif is_game_active == 0:
        screen.fill('Red')
        screen.blit(end_surface1, end_rect1)
        screen.blit(end_surface2, end_rect2)
        screen.blit(end_surface3, end_rect3)
        screen.blit(end_score_surface,end_score_rect)
        screen.blit(end_score_surface2,end_score_rect2)

    # Hiscore Screen
    elif is_game_active == 2:
        screen.fill('Black')
        screen.blit(hiscore_surface1, hiscore_rect1)
        screen.blit(hiscore_surface2, hiscore_rect2)

    # Title Screen
    else:
        screen.fill('Black')
        screen.blit(start_surface_title, start_rect_title)
        screen.blit(start_surface_play, start_rect_play)
        screen.blit(start_surface_quit, start_rect_quit)
        screen.blit(start_surface_hiscores, start_rect_hiscores)
        screen.blit(start_surface_changelog, start_rect_changelog)
        if second_quit == 1:
            screen.blit(start_surface_quit2, start_rect_quit2)
            screen.blit(start_surface_quit2_yes, start_rect_quit2_yes)
            screen.blit(start_surface_quit2_no, start_rect_quit2_no)

    # Update display to show all surfaces, lock FPS to 60
    pygame.display.update()
    clock.tick(60)  # This ensures our while loop runs only 60 times per second (AKA establish max fps of 60)
