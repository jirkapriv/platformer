import pygame
import pytmx

pygame.init()

MAP_SCALE = 4
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 16
TILE_HEIGHT = 16
X_VELOCITY = 0


pygame.display.set_caption("Platformer")
playerGravity = 0
offsetCam = [100, 100]
camera = pygame.Rect(offsetCam[0], 0, SCREEN_WIDTH -
                     offsetCam[1] * 2, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_map = pytmx.load_pygame("terein/map.tmx")
player = pygame.image.load("playya.png")
player = pygame.transform.scale(player, (48, 48))
clock = pygame.time.Clock()
player_rect = player.get_rect(
    topleft=(screen.get_width() / 2, screen.get_height() / 2))
#groundLevel = screen.get_height() - (16 * MAP_SCALE * 3)
run = True
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

    screen.fill((0, 178, 255))

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                scaled_image = pygame.transform.scale(
                    image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH *
                            MAP_SCALE - camera.x, y * TILE_HEIGHT * MAP_SCALE))

    if right:
        X_VELOCITY = 10
    elif left:
        X_VELOCITY = -10
    else:
        X_VELOCITY = 0

    player_rect.x += X_VELOCITY

    if player_rect.x - camera.x < 200:
        camera.x = player_rect.x - 200
    if player_rect.x - camera.x > SCREEN_WIDTH - 400:
        camera.x = player_rect.x - (SCREEN_WIDTH - 400)

    for layerX in tmx_map.visible_layers:
        if isinstance(layerX, pytmx.TiledTileLayer) and layerX.name == "platform":
            for x, y, tile in layerX.tiles():
                platformX = pygame.Rect(x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE,
                                        TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platformX):
                    if X_VELOCITY > 0:
                        player_rect.right = platformX.left
                    elif X_VELOCITY < 0:
                        player_rect.left = platformX.right

    playerGravity += 2
    player_rect.y += playerGravity

    """
    if player_rect.bottom > groundLevel:
        player_rect.bottom = groundLevel
        playerGravity = 0
    """

    for layerY in tmx_map.visible_layers:
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "platform":
            for n, m, tile in layerY.tiles():
                platformY = pygame.Rect(n * TILE_WIDTH * MAP_SCALE, m * TILE_HEIGHT * MAP_SCALE,
                                        TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platformY):
                    if playerGravity > 0:
                        player_rect.bottom = platformY.top
                        playerGravity = 0
                    elif playerGravity < 0:
                        player_rect.top = platformY.bottom
                        playerGravity = -1

    screen.blit(player, (player_rect.x - camera.x, player_rect.y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
