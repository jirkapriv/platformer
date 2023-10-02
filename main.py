import pygame
import pytmx

pygame.init()

MAP_SCALE = 4
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 16
TILE_HEIGHT = 16
playerGravity = 0
X_VELOCITY = 0

pygame.display.set_caption("Platformer")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_map = pytmx.load_pygame("terein/map.tmx")
player = pygame.image.load("playya.png")
player = pygame.transform.scale(player, (48, 48))
clock = pygame.time.Clock()
player_rect = player.get_rect(
    topleft=(screen.get_width() / 2, screen.get_height() / 2))
run = True
groundLevel = screen.get_height() - (16 * MAP_SCALE * 3)

left = False
right = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerGravity = -30
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    screen.fill((255, 255, 255))

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                scaled_image = pygame.transform.scale(
                    image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE))

    playerGravity += 2
    player_rect.y += playerGravity

    if right:
        X_VELOCITY = 10
    elif left:
        X_VELOCITY = -10
    else:
        X_VELOCITY = 0

    player_rect.x += X_VELOCITY

    if player_rect.bottom > groundLevel:
        player_rect.bottom = groundLevel
        playerGravity = 0
        
    colideWithPlatform = False
    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "platform":
            for x, y, tile in layer.tiles():
                platform = pygame.Rect(x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE,
                                       TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platform):
                    colideWithPlatform = True
                    if X_VELOCITY > 0:
                        player_rect.right = platform.left
                    if X_VELOCITY < 0:
                        player_rect.left = platform.right
                    if playerGravity > 0:
                        player_rect.bottom = platform.top
                        playerGravity = 0
                    if playerGravity < 0:
                        player_rect.top = platform.bottom


    pygame.draw.rect(screen, (255, 255, 255), player_rect, 5)
    screen.blit(player, player_rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()