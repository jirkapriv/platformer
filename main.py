import pygame
import pytmx

pygame.init()
pygame.display.set_caption("Platformer")

clock = pygame.time.Clock()


MAP_SCALE = 5
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 12
TILE_HEIGHT = 12
X_VELOCITY = 0
X_ZONE_FOR_CAMERA = 200
Y_ZONE_FOR_CAMERA = 150
GRAVITY_PULL = 2
RUNNING_SPEED = 10
WHITE = (255, 255, 255)
BLUEISHBACKGR = (153, 159, 207)
offsetCam = [100, 100]
playerScale = 1.7
lastVelocity = 1
landedTimer = 0
dash = 0
playerGravity = 0
left = False
right = False
run = True
jumping = False
camera = pygame.Rect(offsetCam[0], 0, SCREEN_WIDTH - offsetCam[1] * 2, SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("assets/font/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 24)
tmx_map = pytmx.load_pygame("assets/terein/savana.tmx")
clock = pygame.time.Clock()
action = "idle"

def prepareIMG(name, scale, dirAb, colorKey=WHITE):
    img = pygame.image.load(f"assets/images/{dirAb}/{name}.png").convert()
    img.set_colorkey(colorKey)
    imgPrepared = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    return imgPrepared

def anim(ListAnim):
    time = pygame.time.get_ticks()
    animation_duration = 750
    frame_count = len(ListAnim)
    frame_duration = animation_duration / frame_count
    current_frame = (time % animation_duration) // frame_duration
    toBlit = ListAnim[int(current_frame)]
    return toBlit
    # GPT helped here
    
playerIDLE1 = prepareIMG("playerIDLE1", playerScale, "playerIDLE")
idleList = [playerIDLE1, prepareIMG("playerIDLE2", playerScale, "playerIDLE")]
runningList = [
    prepareIMG("playerRunn1", playerScale, "playerRUN"),
    prepareIMG("playerRunn2", playerScale, "playerRUN"),
    prepareIMG("playerRunn3", playerScale, "playerRUN"),
    prepareIMG("playerRunn4", playerScale, "playerRUN"),
    prepareIMG("playerRunn5", playerScale, "playerRUN"),
    prepareIMG("playerRunn6", playerScale, "playerRUN"),
    prepareIMG("playerRunn7", playerScale, "playerRUN")
]

playerFallingDown = prepareIMG("heroFalling", playerScale, "playerFalling")
playerJumpingUp = prepareIMG("jumpHero", playerScale, "playerjumpingUp")
playerDashing = prepareIMG("dash", playerScale, "playerDashed")
playerLanded = prepareIMG("heroLanded2", playerScale, "playerLanded")
player_rect = playerIDLE1.get_rect(topleft=(screen.get_width() / 2 - 100, screen.get_height() / 2-200))


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumping == False:
                action = "jumped"
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
        
    if landedTimer > 0:
        landedTimer -= 1

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, image in layer.tiles():
                image.convert()
                image.set_colorkey(WHITE)
                scaled_image = pygame.transform.scale(
                    image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH *
                            MAP_SCALE - camera.x, y * TILE_HEIGHT * MAP_SCALE - camera.y))

    if right:
        X_VELOCITY = RUNNING_SPEED
        if playerGravity == 0:
            action = "running"
        lastVelocity = 1
    elif left:
        X_VELOCITY = -RUNNING_SPEED
        if playerGravity == 0:
            action = "running2"
        lastVelocity = -1
    else:
        X_VELOCITY = 0
        if jumping == False:
            if lastVelocity == 1 and landedTimer <= 0:
                action = "idle"
            else:
                if landedTimer <= 0:
                    action = "idle2"
    if dash > 0:
        action = "dash"
        if lastVelocity == 1:
            X_VELOCITY += 20
            dash -= 40
        elif lastVelocity == -1:
            X_VELOCITY -= 20
            dash -= 40
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

    playerGravity += GRAVITY_PULL
    player_rect.y += playerGravity
    if playerGravity > 13:
        action = "jumped"
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

    if action == "idle":
        toBlit = anim(idleList)

    if action == "idle2":
        toBlit = anim(idleList)
        toBlit = pygame.transform.flip(toBlit, True, False)

    if action == "running":
        toBlit = anim(runningList)

    if action == "running2":
        toBlit = anim(runningList)
        toBlit = pygame.transform.flip(toBlit, True, False)
        
    if action == "jumped":
        if playerGravity < 0:
            toBlit = playerJumpingUp
            if lastVelocity == -1:
                toBlit = pygame.transform.flip(toBlit, True, False)
        if playerGravity > 13:
            toBlit = playerFallingDown
            if lastVelocity == -1:
                toBlit = pygame.transform.flip(toBlit, True, False)

    screen.blit(toBlit, (player_rect.x - camera.x, player_rect.y - camera.y))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()