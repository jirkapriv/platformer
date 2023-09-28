import pygame
import pytmx

pygame.init()

MAP_SCALE = 4
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 16
TILE_HEIGHT = 16
GRAVITY = 10
SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Platformer")
tmx_map = pytmx.load_pygame("terein/map.tmx")
player = pygame.image.load("playya.png")
player = pygame.transform.scale(player, (48, 48))
clock = pygame.time.Clock()
playerPos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_rect = pygame.Rect(playerPos.x, playerPos.y, 64, 64)
colideWithGround = False
run = True
isJumping = False
jump_count = 10

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill((255, 255, 255))

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                scaled_image = pygame.transform.scale(image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE))

    if not colideWithGround:
        playerPos.y += GRAVITY

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "ground":
            for x, y, tile in layer.tiles():
                tile_rect = pygame.Rect(x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE, TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(tile_rect):
                    colideWithGround = True
                    #playerPos.y = tile_rect.top - player_rect.height

    #if playerPos.x >= 192 * MAP_SCALE and playerPos.x <= 256 * MAP_SCALE and player_rect.top <= 6 * 16 * MAP_SCALE:
    #    playerPos.y = 6 * 16 * MAP_SCALE
        
    
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerPos.x -= SPEED
    if keys[pygame.K_d]:
        playerPos.x += SPEED
    if keys[pygame.K_SPACE] and isJumping == False:
        isJumping = True

        
    if isJumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            playerPos.y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            isJumping = False
            jump_count = 10
    
    player_rect = pygame.Rect(playerPos.x, playerPos.y, 64, 64)
    screen.blit(player, (playerPos.x, playerPos.y))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()