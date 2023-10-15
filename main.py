import pygame
import pytmx
import math
import random

pygame.init()

MAP_SCALE = 4
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 16
TILE_HEIGHT = 16
X_VELOCITY = 0
mrakScale = 5
pocetMraku = 20

pygame.display.set_caption("Platformer")
playerGravity = 0
offsetCam = [100, 100]
camera = pygame.Rect(offsetCam[0], 0, SCREEN_WIDTH -
                     offsetCam[1] * 2, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_map = pytmx.load_pygame("terein/map2.tmx")
player = pygame.image.load("playya.png")
player = pygame.transform.scale(player, (48, 48))
mrak1 = pygame.image.load("mrak1.png")
mrak1 = pygame.transform.scale(
    mrak1, (mrak1.get_width() * mrakScale, mrak1.get_height() * mrakScale))
mrak2 = pygame.image.load("mrak2.png")
mrak2 = pygame.transform.scale(
    mrak2, (mrak2.get_width() * mrakScale, mrak2.get_height() * mrakScale))
mrak3 = pygame.image.load("mrak3.png")
mrak3 = pygame.transform.scale(
    mrak3, (mrak3.get_width() * mrakScale, mrak3.get_height() * mrakScale))

mraky = []
for x in range(0, pocetMraku):
    indexObrazku = random.randint(1, 3)
    (posX, posY) = random.randint(-200, screen.get_width()
                                  ), random.randint(0, screen.get_height())
    depth = random.uniform(.4, 1.1)
    mraky.append([(posX, posY), indexObrazku, depth])


clock = pygame.time.Clock()
player_rect = player.get_rect(
    topleft=(screen.get_width() / 2, screen.get_height() / 2))
# groundLevel = screen.get_height() - (16 * MAP_SCALE * 3)
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

    for x in range(0, len(mraky)):

        if mraky[x][1] == 1:
            mrak1jedna = pygame.transform.scale(
                mrak1, (mrak1.get_width() * mraky[x][2], mrak1.get_height() * mraky[x][2]))
            screen.blit(mrak1jedna, mraky[x][0])

        if mraky[x][1] == 2:
            mrak2jedna = pygame.transform.scale(
                mrak2, (mrak2.get_width() * mraky[x][2], mrak2.get_height() * mraky[x][2]))
            screen.blit(mrak2jedna, mraky[x][0])

        if mraky[x][1] == 3:
            mrak3jedna = pygame.transform.scale(
                mrak3, (mrak3.get_width() * mraky[x][2], mrak3.get_height() * mraky[x][2]))
            screen.blit(mrak3jedna, mraky[x][0])

    if player_rect.y > 1000:
        player_rect.y = 0
        player_rect.x = 200

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
                        jumping = False

                    elif X_VELOCITY < 0:
                        player_rect.left = platformX.right
                        jumping = False

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
                        jumping = False
                    elif playerGravity < 0:
                        player_rect.top = platformY.bottom
                        playerGravity = -1

    for x in range(len(mraky)-1, -1, -1):
        mraky[x][0] = list(mraky[x][0])
        mraky[x][0][0] += 1 * mraky[x][2]
        mraky[x][0] = tuple(mraky[x][0])

        if mraky[x][0][0] > screen.get_width() + 200:
            del mraky[x]
            indexObrazku = random.randint(1, 3)
            (posX, posY) = random.randint(0, screen.get_width()) - \
                500, random.randint(0, screen.get_height())
            depth = random.uniform(.4, 1.4)
            mraky.append([(posX, posY), indexObrazku, depth])

    screen.blit(player, (player_rect.x - camera.x, player_rect.y))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
