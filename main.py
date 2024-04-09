import pygame
import pytmx
import random
import sys
pygame.init()
pygame.display.set_caption("Kaleido")

clock = pygame.time.Clock()

MAP_SCALE = 5
SCREEN_WIDTH = 320 * MAP_SCALE
SCREEN_HEIGHT = 176 * MAP_SCALE
TILE_WIDTH = 12
TILE_HEIGHT = 12
X_VELOCITY = 0
Y_DEATH_ZONE = 3000
RUNNING_SPEED = 10
X_ZONE_FOR_CAMERA = 350
Y_ZONE_FOR_CAMERA = 200
GRAVITY_PULL = 2
PLAYER_LAND_DEPENDENCY = 26
WHITE = (255, 255, 255)
BLUEISHBACKGR = (153, 159, 207)

colideEnemieBool = False
# musicBool = True
mainBool = True
lastVelocity = 1
EnemyVelocity = 1
dash = 0
dashDelay = 0
jumpHeight = 25
playerScale = 1.7
enemyScale = 2.1
playerGravity = 0
landedTimer = 0

font = pygame.font.Font("assets/font/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 24)
font2 = pygame.font.Font("assets/font/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 100)
font3 = pygame.font.Font("assets/font/Pixelify_Sans/PixelifySans-VariableFont_wght.ttf", 45)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
tmx_map = pytmx.load_pygame("assets/terein/savana.tmx")
jumpSound = pygame.mixer.Sound("assets/sounds/soundEffects/jump.wav")
hitSound = pygame.mixer.Sound("assets/sounds/soundEffects/hit.wav")
hurtSound = pygame.mixer.Sound("assets/sounds/soundEffects/hurt.wav")
gameName = font2.render("Kaleido", True, WHITE)
instruction1 = font3.render("press space to play", True, WHITE)
# pygame.mixer.music.load("assets/sounds/soundEffects/music.wav")
# pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1)

jumpSound.set_volume(0.3)
hitSound.set_volume(0.3)
hurtSound.set_volume(0.3)


def mainMenu():
    while True:
        for event2 in pygame.event.get():
            global mainBool
            if event2.type == pygame.QUIT:
                sys.exit()
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_SPACE and mainBool == True:
                    transitionAnim()
                    mainBool = False
                    return
        screen.blit(gameName, (SCREEN_WIDTH/2- gameName.get_width()/2, SCREEN_HEIGHT/2- gameName.get_height()/2))
        screen.blit(instruction1, (SCREEN_WIDTH/2- instruction1.get_width()/2, SCREEN_HEIGHT/2- instruction1.get_height()/2+ gameName.get_height()))
        pygame.display.flip()
        clock.tick(60)
        
def transitionAnim():
    canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for x in range(0, 255, 15):
        canvas.set_alpha(x)
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(40)

    # https://stackoverflow.com/questions/58540537/how-to-fade-the-screen-out-and-back-in-using-pygame
    # same problem as i have



def playerDeath():
    global enemiesList
    player_rect.y = playerSpawnPos[0]
    player_rect.x = playerSpawnPos[1]
    
    enemiesList = [
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1000, screen.get_height() / 2)), [1000, 533], 1, [1000, 1230]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1100, screen.get_height() / 2)), [1100, 533], 1, [1100, 1230]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1440, screen.get_height() / 2)), [1440, 593], 1, [1440, 1615]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2150, screen.get_height() / 2)), [2160, 653], 1, [2160, 2330]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2220, screen.get_height() / 2)), [2220, 653], 1, [2220, 2330]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2500, screen.get_height() / 2)), [2500, 653], 1, [2500, 2600]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2700, screen.get_height() / 2)), [2700, 653], 1, [2700, 2800]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2900, screen.get_height() / 2)), [2900, 653], 1, [3000, 3100]],
    ]
    

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

playerSpawnPos = [-50, 450]
idleList = [
    prepareIMG("playerIDLE1", playerScale, "playerIDLE"),
    prepareIMG("playerIDLE2", playerScale, "playerIDLE")
    ]

runningList = [
    prepareIMG("playerRunn1", playerScale, "playerRUN"),
    prepareIMG("playerRunn2", playerScale, "playerRUN"),
    prepareIMG("playerRunn3", playerScale, "playerRUN"),
    prepareIMG("playerRunn4", playerScale, "playerRUN"),
    prepareIMG("playerRunn5", playerScale, "playerRUN"),
    prepareIMG("playerRunn6", playerScale, "playerRUN"),
    prepareIMG("playerRunn7", playerScale, "playerRUN")
]

enemiesList = [
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1000, screen.get_height() / 2)), [1000, 533], 1, [1000, 1230]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1100, screen.get_height() / 2)), [1100, 533], 1, [1100, 1230]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(1440, screen.get_height() / 2)), [1440, 593], 1, [1440, 1615]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2150, screen.get_height() / 2)), [2160, 653], 1, [2160, 2330]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2220, screen.get_height() / 2)), [2220, 653], 1, [2220, 2330]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2500, screen.get_height() / 2)), [2500, 653], 1, [2500, 2600]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2700, screen.get_height() / 2)), [2700, 653], 1, [2700, 2800]],
        [prepareIMG("enemyMashroom1", enemyScale, "enemy1"), "Fow", prepareIMG("enemyMashroom1", enemyScale, "enemy1").get_rect(topleft=(2900, screen.get_height() / 2)), [2900, 653], 1, [3000, 3100]],
     ]

enemyRunMashroom1 = [
    prepareIMG("enemyMashroom1", enemyScale, "enemy1"),
    prepareIMG("enemyMashroom2", enemyScale, "enemy1")
]
playerLanded = prepareIMG("heroLanded2", playerScale, "playerLanded")
playerDashing = prepareIMG("dash", playerScale, "playerDashed")
enemy1placeHold = prepareIMG("enemyMashroom1", enemyScale, "enemy1")
playerJumpingUp = prepareIMG("jumpHero", playerScale, "playerjumpingUp")
playerFallingDown = prepareIMG("heroFalling", playerScale, "playerFalling")
backgroundSvana1 = prepareIMG("pozadiSavana1", MAP_SCALE, "backgroundSavana")
backgroundSvana2 = prepareIMG("pozadiSavana2", MAP_SCALE, "backgroundSavana")
backgroundSvana3 = prepareIMG("pozadiSavana3", MAP_SCALE, "backgroundSavana")
backgroundSvana4 = prepareIMG("pozadiSavana4", MAP_SCALE, "backgroundSavana")

# playMusic = prepareIMG("musicPlay", 4, "UI_SoundButtons")
# muteMusic = prepareIMG("musicStop", 4, "UI_SoundButtons")
# musicRect = playMusic.get_rect(topleft=(SCREEN_WIDTH-100, 10))

offsetCam = [100, 300]
particlesList = []

camera = pygame.Rect(offsetCam[0], 0, SCREEN_WIDTH - offsetCam[1] * 2, SCREEN_HEIGHT)

player_rect = idleList[0].get_rect(topleft=(screen.get_width() / 2 - 100, screen.get_height() / 2-200))
enemy_rect = enemy1placeHold.get_rect(topleft=(1000, screen.get_height() / 2))

action = "idle"
left = False
right = False
run = True
jumping = False

mainMenu()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumping == False:
                if action != "dash":
                    action = "jumped"
                playerGravity = -jumpHeight
                jumping = True
                jumpCheck = False
                pygame.mixer.Sound.play(jumpSound)
            if event.key == pygame.K_LSHIFT and dashDelay <= 0:
                dash = 300
                dashDelay = 100
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False
                
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if musicRect.collidepoint(event.pos):
        #         if musicBool:
        #             musicBool = False
        #         else:
        #             musicBool = True

        

    screen.fill(BLUEISHBACKGR)

    screen.blit(backgroundSvana1, (-320 * MAP_SCALE + -camera.x / 10, 0))
    screen.blit(backgroundSvana1, (0 + -camera.x / 10, 0))
    screen.blit(backgroundSvana1, (320 * MAP_SCALE + -camera.x / 10, 0))

    screen.blit(backgroundSvana2, (-320 * MAP_SCALE + -camera.x / 6, 0))
    screen.blit(backgroundSvana2, (0 + -camera.x / 6, 0))
    screen.blit(backgroundSvana2, (320 * MAP_SCALE + -camera.x / 6, 0))

    screen.blit(backgroundSvana3, (-320 * MAP_SCALE + -camera.x / 3, 0))
    screen.blit(backgroundSvana3, (0 + -camera.x / 3, 0))
    screen.blit(backgroundSvana3, (320 * MAP_SCALE + -camera.x / 3, 0))
    screen.blit(backgroundSvana3, (640 * MAP_SCALE + -camera.x / 3, 0))

    screen.blit(backgroundSvana4, (-320 * MAP_SCALE + -camera.x / 1.7, 0))
    screen.blit(backgroundSvana4, (0 + -camera.x / 1.7, 0))
    screen.blit(backgroundSvana4, (320 * MAP_SCALE + -camera.x / 1.7, 0))
    screen.blit(backgroundSvana4, (640 * MAP_SCALE + -camera.x / 1.7, 0))
    screen.blit(backgroundSvana4, (960 * MAP_SCALE + -camera.x / 1.7, 0))

    TimeToDashAgain = font.render(str(100 - max(dashDelay, 0)), True, WHITE)

    if landedTimer > 0:
        landedTimer -= 1

    dashDelay -= 1
    if player_rect.y > Y_DEATH_ZONE:
        pygame.mixer.Sound.play(hurtSound)
        # pygame.mixer.music.rewind()
        transitionAnim()
        playerDeath()

    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name != "popredi":
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


    for layerX in tmx_map.visible_layers:
        if isinstance(layerX, pytmx.TiledTileLayer) and layerX.name == "kolizeS":
            for x, y, tile in layerX.tiles():
                platformX = pygame.Rect(x * TILE_WIDTH * MAP_SCALE, y * TILE_HEIGHT * MAP_SCALE, TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
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
        if action != "dash":
            action = "jumped"

    for layerY in tmx_map.visible_layers:
        if isinstance(layerY, pytmx.TiledTileLayer) and layerY.name == "kolizeS":
            for n, m, tile in layerY.tiles():
                platformY = pygame.Rect(n * TILE_WIDTH * MAP_SCALE, m * TILE_HEIGHT * MAP_SCALE, TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE)
                if player_rect.colliderect(platformY):
                    if playerGravity > 0:
                        if playerGravity > PLAYER_LAND_DEPENDENCY:
                            action = "landed"
                            landedTimer = 20
                            # pokud dojde ke kolizi se zemi a gravitace hrace je vysoka hrac dopadl z vetsi vysky ( gravitace hrace se zvetsuje casem )
                        player_rect.bottom = platformY.top
                        playerGravity = 0
                        jumping = False
                        

                    elif playerGravity < 0:
                        player_rect.top = platformY.bottom
                        playerGravity = -1

    for x in enemiesList:
        x[2].x += x[4]
        x[2].y = x[3][1]
        if x[2].x >= x[5][1]:
            x[4] = -1
            x[1] = "Back"
        if x[2].x <= x[5][0]:
            x[4] = 1
            x[1] = "Fow"

    colideEnemieBool = False
    for x in enemiesList:
        if x[2].colliderect(player_rect):
            if action == "dash" or dash > 0:
                for p in range(20):
                    particlesList.append([[x[2].centerx, x[2].centery], [random.randint(0, 20) / 10 - 1, random.randint(0, 20) / 10 - 1], random.randint(4, 7)])
                    # https://www.youtube.com/watch?v=F69-t33e8tk&t=554s
                pygame.mixer.Sound.play(hitSound)
                enemiesList.remove(x)
                break
            colideEnemieBool = True
            break

        if x[4] > 0:
            x[1] = "Fow"
        else:
            x[1] = "Back"

    if colideEnemieBool:
        pygame.mixer.Sound.play(hurtSound)
        # pygame.mixer.music.rewind()
        transitionAnim()
        playerDeath()

    for particle in reversed(particlesList):
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1

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
    if action == "dash":
        toBlit = playerDashing
        if lastVelocity == -1:
            toBlit = pygame.transform.flip(toBlit, True, False)

    if action == "landed":
        toBlit = playerLanded
        if lastVelocity == -1:
            toBlit = pygame.transform.flip(toBlit, True, False)

    enemyToBlit = anim(enemyRunMashroom1)

    for x in enemiesList:
        if x[1] == "Back":
            enemyToBlit = anim(enemyRunMashroom1)
            enemyToBlit = pygame.transform.flip(enemyToBlit, True, False)

        if x[1] == "Fow":
            enemyToBlit = anim(enemyRunMashroom1)

        screen.blit(enemyToBlit, (x[2].x - camera.x, x[2].y - camera.y))

    screen.blit(toBlit, (player_rect.x - camera.x, player_rect.y - camera.y))


    for layer in tmx_map.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "popredi":
            for x, y, image in layer.tiles():
                image.convert()
                image.set_colorkey(WHITE)
                scaled_image = pygame.transform.scale(
                    image, (TILE_WIDTH * MAP_SCALE, TILE_HEIGHT * MAP_SCALE))
                screen.blit(scaled_image, (x * TILE_WIDTH *
                            MAP_SCALE - camera.x, y * TILE_HEIGHT * MAP_SCALE - camera.y))
    


    for particle in particlesList:
        pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0] - camera.x), int(particle[0][1] - camera.y)], int(particle[2]))

    screen.blit(TimeToDashAgain, (0, 0))
    

    if player_rect.x - camera.x < X_ZONE_FOR_CAMERA:
        camera.x = player_rect.x - X_ZONE_FOR_CAMERA
    if player_rect.x - camera.x > SCREEN_WIDTH - X_ZONE_FOR_CAMERA * 2:
        camera.x = player_rect.x - (SCREEN_WIDTH - X_ZONE_FOR_CAMERA * 2)
    if player_rect.y - camera.y < Y_ZONE_FOR_CAMERA:
        camera.y = player_rect.y - Y_ZONE_FOR_CAMERA
    if player_rect.y - camera.y > SCREEN_HEIGHT - Y_ZONE_FOR_CAMERA * 2:
        camera.y = player_rect.y - (SCREEN_HEIGHT - Y_ZONE_FOR_CAMERA * 2)
    
    # if musicBool:
    #     screen.blit(playMusic, (SCREEN_WIDTH-100, 10))
    #     pygame.mixer.music.unpause()   
    # else:
    #     screen.blit(muteMusic, (SCREEN_WIDTH-100, 10))
    #     pygame.mixer.music.pause()
        
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
