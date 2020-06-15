import pygame
import random
from pygame.locals import *

fpsClock = pygame.time.Clock()

TILESIZE = 40
MAPWIDTH  = 20
MAPHEIGHT = 20
INVHEIGHT = 2*TILESIZE
PADDING = TILESIZE/2

BLACK = (0,0,0)
WHITE = (255,255,255)

DIRT  = 0
GRASS = 1
WATER = 2
COAL  = 3
ROCK  = 4
LAVA  = 5
WOOD  = 6
FIRE  = 7
SAND  = 8
STONE = 9
BRICK = 10
CLOUD = 11

resources = [DIRT, GRASS, WATER, COAL, ROCK, LAVA, WOOD, FIRE, SAND, STONE, BRICK]

textures = {
    DIRT  : pygame.image.load('Images/DirtPixel.png'),
    GRASS : pygame.image.load('Images/GrassPixel.png'),
    WATER : pygame.image.load('Images/WaterPixel.png'),
    COAL  : pygame.image.load('Images/CoalPixel.png'),
    ROCK  : pygame.image.load('Images/RockPixel.png'),
    LAVA  : pygame.image.load('Images/LavaPixel.png'),
    WOOD  : pygame.image.load('Images/WoodPixel.png'),
    FIRE  : pygame.image.load('Images/TorchPixel.png'),
    SAND  : pygame.image.load('Images/SandPixel.png'),
    STONE : pygame.image.load('Images/StonePixel.png'),
    BRICK : pygame.image.load('Images/BrickPixel.png'),
    CLOUD : pygame.image.load('Images/CloudPixel.png')
}

inventory = {
    DIRT  : 0,
    GRASS : 0,
    WATER : 0,
    COAL  : 0,
    ROCK  : 0,
    LAVA  : 0,
    WOOD  : 0,
    FIRE  : 0,
    SAND  : 0,
    STONE : 0,
    BRICK : 0
}

craft = {
    WOOD  : { DIRT:  2},
    FIRE  : { WOOD:  2,  COAL: 1},
    SAND  : { DIRT:  1,  ROCK: 1},
    STONE : { ROCK:  2},
    BRICK : { STONE: 1,  SAND: 1}
}

controls = {
    DIRT  : 49,     # event 49 is 1 key
    GRASS : 50,     # event 50 is 2 key
    WATER : 51,     # event 51 is 3 key
    COAL  : 52,     # event 52 is 4 key
    ROCK  : 53,     # event 53 is 5 key
    LAVA  : 54,     # event 54 is 6 key
    WOOD  : 55,     # event 54 is 7 key
    FIRE  : 56,     # event 55 is 8 key
    SAND  : 57,     # event 56 is 9 key
    STONE : 48,     # event 57 is 0 key
    BRICK : 45      # event 49 is - key
}

BASE_RARITY = 0
VERY_COMMON = 30
COMMON      = 45
RARE        = 50
VERY_RARE   = 53
ULTRA_RARE  = 54

pygame.init()
DISPLAY_SURFACE = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE + INVHEIGHT))
pygame.display.set_caption('MINECRAFT - 2 D')

pygame.display.set_icon(pygame.image.load('Images/Player.gif'))

tilemap = [ [GRASS for i in range(MAPWIDTH)] for j in range(MAPHEIGHT)]
for row in range(MAPHEIGHT):
    for column in range(MAPWIDTH):
        random_num = random.randint(BASE_RARITY, ULTRA_RARE)
        this_tile = GRASS
        if random_num < VERY_COMMON:
            if (random_num % 3) == 0:
                this_tile = ROCK
            else:
                this_tile = GRASS
        elif random_num >= VERY_COMMON and random_num < COMMON:
            if (random_num % 2) == 0:
                this_tile = WATER
            else:
                this_tile = DIRT
        elif random_num >= RARE and random_num < VERY_RARE:
            if (random_num % 2) == 0:
                this_tile = COAL
            else:
                this_tile = LAVA
        tilemap[row][column] = this_tile

INVFONT = pygame.font.Font('Fonts/freesansbold.ttf', 18)

PLAYER = pygame.image.load('Images/Player.gif')
player_position = [random.randint(0, MAPWIDTH - 1), random.randint(0, MAPHEIGHT - 1)]

cloud_x_pos = [-200, -500, -1000]
cloud_y_pos = [random.randint(0, MAPHEIGHT*TILESIZE - 1), random.randint(0, MAPHEIGHT*TILESIZE - 1), random.randint(0, MAPHEIGHT*TILESIZE - 1)]


while True:
    DISPLAY_SURFACE.fill(BLACK)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if (event.key == K_RIGHT) and (player_position[0] < MAPWIDTH - 1):
                player_position[0] +=1
            elif (event.key == K_LEFT) and (player_position[0] > 0):
                player_position[0] -=1
            elif (event.key == K_UP) and (player_position[1] > 0):
                player_position[1] -=1
            elif (event.key == K_DOWN) and (player_position[1] < MAPHEIGHT - 1):
                player_position[1] +=1
            elif (event.key == K_SPACE):
                this_tile = tilemap[player_position[1]][player_position[0]]
                inventory[this_tile] +=1
                tilemap[player_position[1]][player_position[0]] = DIRT

            for key in controls:
                if (event.key == controls[key]):
                    if key in craft:
                        canBeMade = True
                        for each in craft[key]:
                            if craft[key][each] > inventory[each]:
                                canBeMade = False
                        if canBeMade == True:
                            for i in craft[key]:
                                inventory[i] -= craft[key][i]
                            inventory[key] += 1
                    else:
                        if inventory[key] > 0:
                            standing_tile = tilemap[player_position[1]][player_position[0]]
                            inventory[standing_tile] += 1
                            inventory[key] -= 1
                            tilemap[player_position[1]][player_position[0]] = key

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAY_SURFACE.blit(textures[tilemap[row][column]], (column*TILESIZE, row*TILESIZE))

    inventory_x_position = PADDING
    inventory_y_position = MAPHEIGHT*TILESIZE + PADDING
    for item in resources:
        DISPLAY_SURFACE.blit(textures[item], (inventory_x_position, inventory_y_position))
        inventory_x_position += PADDING
        numInventoryText = INVFONT.render(str(inventory[item]), True, WHITE, BLACK)
        DISPLAY_SURFACE.blit(numInventoryText, (inventory_x_position, inventory_y_position))
        inventory_x_position += PADDING*2

    DISPLAY_SURFACE.blit(PLAYER, (player_position[0]*TILESIZE, player_position[1]*TILESIZE))

    for each in range(len(cloud_x_pos)):
        DISPLAY_SURFACE.blit(textures[CLOUD], (cloud_x_pos[each], cloud_y_pos[each]))
        cloud_x_pos[each] += 1
        if cloud_x_pos[each] > MAPWIDTH*TILESIZE:
            cloud_x_pos[each] = -random.randint(0, 450)
            cloud_y_pos[each] = random.randint(0, MAPHEIGHT*TILESIZE - 1)

    pygame.display.update()
    fpsClock.tick(24)