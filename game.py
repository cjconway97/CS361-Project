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
is_game_active = 1

# Creating all the skybox + ground surfacesto use
sky_surface = pygame.image.load('Background/Environment/PNG/sky.png').convert()
sea_surface = pygame.image.load('Background/Environment/PNG/sea.png').convert()
ground_surface = pygame.image.load('Background/Environment/PNG/ground1.png').convert_alpha()

# Creating score surfaces
score_surface = font.render('Score:', False, 'Black')
score_rect = score_surface.get_rect(center=(400, 50))

# Creating title screen surfaces
score_surface = font.render('Score:', False, 'Black')
score_rect = score_surface.get_rect(center=(400, 50))

# Creating end screen surfaces
end_surface1 = font.render('Press *Spacebar* to try again!', False, 'Black')
end_surface2 = font.render('Press *Esc Button* to see the title menu!', False, 'Black')
end_surface3 = font.render('Game Over!', False, 'Black')
end_rect1 = end_surface1.get_rect(center=(400, 200))
end_rect2 = end_surface2.get_rect(center=(400, 250))
end_rect3 = end_surface3.get_rect(center=(400, 150))


# Creating Player + hit box
player_surface = pygame.image.load('Player Assets/BlueWizard Animations/BlueWizard/2BlueWizardIdle/Chara - BlueIdle00000.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (100, 100))
player_rect = player_surface.get_rect(midbottom=(50, 335))
player_gravity = 0
player_right = 0
player_left = 0

# Creating enemy + hit box
enemy_surface = pygame.image.load('Enemy Assets/Enemies Files/sprites/fox/fox1.png').convert_alpha()
enemy_surface = pygame.transform.scale(enemy_surface, (100, 100))
enemy_rect = enemy_surface.get_rect(midbottom=(300, 315))

while True:
    # Establish movement + quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if is_game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 315:
                    player_gravity = -20
                if event.key == pygame.K_d:
                    player_right = 10
                if event.key == pygame.K_a:
                    player_left = -10

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                enemy_rect = enemy_surface.get_rect(midbottom=(300, 315))
                player_rect = player_surface.get_rect(midbottom=(50, 315))
                is_game_active = 1

        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos):
                player_gravity = -20
    # Build skybox
    skybox_x = 0
    while skybox_x < display_width + 112:
        screen.blit(sky_surface, (skybox_x, 0))
        screen.blit(sea_surface, (skybox_x, 304))
        skybox_x += 112
    if is_game_active:
        # Build ground
        ground_x = -50
        while ground_x < display_width + 50:
            screen.blit(ground_surface, (ground_x, 300))
            ground_x += 75

        # Create text surfaces (if needed)
        pygame.draw.rect(screen, 'White', score_rect)
        pygame.draw.rect(screen, 'White', score_rect, 15)
        screen.blit(score_surface, score_rect)

        # Create player
        player_gravity += 1
        player_rect.bottom += player_gravity
        if player_right > 0:
            player_right -= 1
        if player_left < 0:
            player_left += 1
        player_rect.right += player_right
        player_rect.left += player_left

        if player_rect.left > 750:
            player_rect.right = 50
        if player_rect.bottom >= 315:
            player_rect.bottom = 315
        screen.blit(player_surface, player_rect)

        # Create enemy
        enemy_rect.left -= 1
        screen.blit(enemy_surface, enemy_rect)
        if enemy_rect.left > 750:
            enemy_rect.right = 50

        # Handle player-enemy collisions
        if player_rect.colliderect(enemy_rect):
            is_game_active = 0

    else:
        screen.fill('Red')
        screen.blit(end_surface1, end_rect1)
        screen.blit(end_surface2, end_rect2)
        screen.blit(end_surface3, end_rect3)

    # Mouse controls
    mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed())

    # Update display to show all surfaces, lock FPS to 60
    pygame.display.update()
    clock.tick(60)  # This ensures our while loop runs only 60 times per second (AKA establish max fps of 60)
