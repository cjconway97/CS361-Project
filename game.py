import pygame
from sys import exit

pygame.init()

# Creating screen of size width x height pixels
display_width = 800
display_height = 400
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Potato')

clock = pygame.time.Clock()

test_surface = pygame.Surface((100,200))
test_surface.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)  # This ensures our while loop runs only 60 times per second (AKA establish max fps of 60)
