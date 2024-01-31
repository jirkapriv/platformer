import pygame
import pytmx


pygame.init()

MAP_SCALE = 4
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 16
TILE_HEIGHT = 16
X_VELOCITY = 0
X_ZONE_FOR_CAMERA = 200
Y_ZONE_FOR_CAMERA = 150

pygame.display.set_caption("Platformer")
playerGravity = 0
offsetCam = [100, 100]
camera = pygame.Rect(offsetCam[0], 0, SCREEN_WIDTH -
                     offsetCam[1] * 2, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_map = pytmx.load_pygame("terein/mapaBOG01.tmx")
player = pygame.image.load("playya.png").convert()
player.set_colorkey((255,255,255))
player = pygame.transform.scale(player, (48, 48))


clock = pygame.time.Clock()
player_rect = player.get_rect(
    topleft=(screen.get_width() / 2, screen.get_height() / 2))

left = False
right = False
run = True
jumping = False

while run:
       
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumping == False:
                playerGravity = -25
                jumping = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

     
    screen.fill((153, 159, 207))

    if player_rect.y > 1000:
        player_rect.y = 0
        player_rect.x = 200
        
 

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                scaled_image = pygame.transform.scale(
                    image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH *
                            MAP_SCALE - camera.x, y * TILE_HEIGHT * MAP_SCALE - camera.y))

    if right:
        X_VELOCITY = 10
    elif left:
        X_VELOCITY = -10
    else:
        X_VELOCITY = 0

    player_rect.x += X_VELOCITY


    if player_rect.x - camera.x < X_ZONE_FOR_CAMERA:
        camera.x = player_rect.x - X_ZONE_FOR_CAMERA
    if player_rect.x - camera.x > SCREEN_WIDTH - X_ZONE_FOR_CAMERA * 2:
        camera.x = player_rect.x - (SCREEN_WIDTH - X_ZONE_FOR_CAMERA * 2)
    if player_rect.y - camera.y < Y_ZONE_FOR_CAMERA:
        camera.y = player_rect.y - Y_ZONE_FOR_CAMERA
    if player_rect.y - camera.y > SCREEN_HEIGHT - Y_ZONE_FOR_CAMERA * 2:
        camera.y = player_rect.y - (SCREEN_HEIGHT - Y_ZONE_FOR_CAMERA * 2)
        
        
    for layerX in tmx_map.visible_layers:
        if isinstance(layerX, pytmx.TiledTileLayer) and layerX.name == "Vrstva1":
            for x, y, tile in layerX.tiles():
                platformX = pygame.Rect(x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE,
                                        TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platformX):
                    if X_VELOCITY > 0:
                        player_rect.right = platformX.left
                        jumping = False

                    elif X_VELOCITY < 0:
                        player_rect.left = platformX.right
                        jumping = False

    playerGravity += 2
    player_rect.y += playerGravity

    for layerY in tmx_map.visible_layers:
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "Vrstva1":
            for n, m, tile in layerY.tiles():
                platformY = pygame.Rect(n * TILE_WIDTH * MAP_SCALE, m * TILE_HEIGHT * MAP_SCALE,
                                        TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platformY):
                    if playerGravity > 0:
                        player_rect.bottom = platformY.top
                        playerGravity = 0
                        jumping = False
                    elif playerGravity < 0:
                        player_rect.top = platformY.bottom
                        playerGravity = -1

    
    screen.blit(player, (player_rect.x - camera.x, player_rect.y- camera.y))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()