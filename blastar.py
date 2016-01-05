import pygame
import time
import random

pygame.init()

# Display
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('UFOs')

# Colors
white = (255,255,255)
black = (0,0,0)
gray = (100,100,100)
red = (200,0,0)
light_red = (255,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)
blue = (0,0,255)

# Clock
clock = pygame.time.Clock()
FPS = 25

# UFO
UFOWidth = 40
UFOHeight = 20
turretWidth = 5
UFOshotStart = 20
UFOshotEnd = 50
mainUFOSpeed = 4
mainUFOX = display_width * 0.9
mainUFOY = display_height * 0.9
UFOMove = 0

# Health
newScore = 0
newhealth = 10

# Enemy UFO
enemyUFOSpeed = 7
enemyUFOX = display_width * 0.1
enemyUFOY = display_height * 0.1

# Fonts
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

# Score display
def score(score):
    text = smallfont.render("Score: "+str(score), True, white)
    gameDisplay.blit(text, [5,5])

# Font sizes
def text_objects(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Display buttons
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)

# Display message to screen   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

# UFO
def UFO(x,y):
    x = int(x)
    y = int(y)
  
    pygame.draw.circle(gameDisplay, blue, (x,y), int(UFOHeight/2))
    pygame.draw.ellipse(gameDisplay, blue, (x-UFOHeight, y, UFOWidth, UFOHeight))
    pygame.draw.line(gameDisplay,blue,(x,y),(x,y-20),turretWidth)

# Enemy UFO
def enemy_UFO(x,y):
    x = int(x)
    y = int(y)
  
    pygame.draw.circle(gameDisplay, blue, (x,y), int(UFOHeight/2))
    pygame.draw.ellipse(gameDisplay, blue, (x-UFOHeight, y, UFOWidth, UFOHeight))

# Player Health
def health_bar(player_health):
    if player_health > 7.5:
        player_health_color = green
    elif player_health > 5.0:
        player_health_color = yellow
    else:
        player_health_color = red

    text = smallfont.render("Health: ", True, white)
    gameDisplay.blit(text, [display_width-250,5])
    pygame.draw.rect(gameDisplay, player_health_color, (680, 10, player_health*10, 25))
    
# Enemy UFO Fire    
def enemyUFOFire():
    enemyFired = True
    global mainUFOX
    global mainUFOY
    global enemyUFOX
    global enemyUFOY
    global UFOMove
    global enemyUFOSpeed
    global newScore
    global newhealth

    # UFO's Movement
    mainUFOX += UFOMove
    enemyUFOX += enemyUFOSpeed
    
    # Display black screen
    gameDisplay.fill(black)
    
    # Display UFO's
    UFO(mainUFOX,mainUFOY)
    enemy_UFO(enemyUFOX,enemyUFOY)

    # Draw Laser Beam
    pygame.draw.line(gameDisplay,green,(enemyUFOX,enemyUFOY+20),(enemyUFOX,enemyUFOY+500), turretWidth)

    # Laser Beam HIT (Lost health)
    if mainUFOX+(UFOWidth/2) >= enemyUFOX+(UFOWidth/2) >= mainUFOX-(UFOWidth/2):
        newhealth -= 1
    
    # Update Score and Health   
    score(newScore)
    health_bar(newhealth)
    
    # Update Display                
    pygame.display.update()
    
    # Clock Tick
    clock.tick(FPS)

# UFO Fire
def fire():
    fired = True
    global UFOshotStart
    global UFOshotEnd
    UFOshotStart = 20
    UFOshotEnd = 50
    global mainUFOX
    global mainUFOY
    global enemyUFOX
    global enemyUFOY
    global UFOMove
    global enemyUFOSpeed
    global newScore
    global newhealth

    UFOXfiredMovement = 0

    while fired == True:
        global enemyUFOX
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    UFOMove = -mainUFOSpeed
                elif event.key == pygame.K_RIGHT:
                    UFOMove = mainUFOSpeed
                elif event.key == pygame.K_p:
                    pause()

            elif event.type == pygame.KEYUP:
                if UFOMove == -mainUFOSpeed:
                    if event.key == pygame.K_LEFT:
                        UFOMove = 0
                if UFOMove == mainUFOSpeed:
                    if event.key == pygame.K_RIGHT:
                        UFOMove = 0

        gameDisplay.fill(black)
        mainUFOX += UFOMove
        enemyUFOX += enemyUFOSpeed
        UFO(mainUFOX,mainUFOY)
        UFO(mainUFOX,mainUFOY)
        enemy_UFO(enemyUFOX,enemyUFOY)
        UFOXfiredMovement = UFOXfiredMovement+UFOMove
        pygame.draw.line(gameDisplay,red,(mainUFOX-UFOXfiredMovement,mainUFOY-UFOshotStart),(mainUFOX-UFOXfiredMovement,mainUFOY-UFOshotEnd), turretWidth)
        UFOshotEnd += 20
        UFOshotStart += 20
        
        randomFire = random.randrange(1,15)
        enemyFiring(randomFire)

        if enemyUFOX+(UFOWidth/2) >= mainUFOX-UFOXfiredMovement >= enemyUFOX-(UFOWidth/2) and mainUFOY-UFOshotStart == enemyUFOY:
            newScore += 1
            enemyUFOX = -random.randrange(50,500)
            
        score(newScore)
        health_bar(newhealth)
                    
        pygame.display.update()
        clock.tick(FPS)

        if display_height-UFOshotEnd < 0:
            fired = False

# Controls screen
def game_controls():
    gcont = True

    while gcont:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Controls",blue,-100,size="large")
        message_to_screen("Fire: Spacebar",blue,-30)
        message_to_screen("Move UFO: Left and Right arrows",blue,10)
        message_to_screen("Pause: P",blue,50)


        button("play", 150,450,100,50, green, light_green, action="play")
        button("quit", 550,450,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

# Buttons
def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                game_intro()
            
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,width,height))

    text_to_button(text,black,x,y,width,height)

# Pause Screen
def pause():
    paused = True
    message_to_screen("Paused",blue,-100,size="large")
    message_to_screen("Press P to continue playing or Q to quit",blue,25)
    pygame.display.update()
    
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()

        clock.tick(FPS)      

# Game Intro Screen
def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        intro = False
                    elif event.key == pygame.K_q:                        
                        pygame.quit()
                        quit()

        gameDisplay.fill(black)
        message_to_screen("BLASTAR",blue,-100,size="large")
        message_to_screen("Destroy the fleet of enemy spaceships",blue,-30)

        button("play", 150,450,100,50, green, light_green, action="play")
        button("controls", 350,450,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,450,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

# Game Over Screen
def game_over():
    game_over = True

    while game_over:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.fill(black)
        message_to_screen("Game Over",green,-100,size="large")
        message_to_screen("You died.",black,-30)

        button("play Again", 150,450,150,50, green, light_green, action="play")
        button("controls", 350,450,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,500,450,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(15)

# You Win Screen
def you_win():
    win = True
    global newhealth
    global newScore
    newhealth = 10
    newScore = 0

    # Display Win Screen
    while win:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        # Dispaly Black Screen
        gameDisplay.fill(black)
        
        # Display Message To Screen
        message_to_screen("You won!",blue,-100,size="large")
        message_to_screen("Congratulations!",blue,-30)

        # Display Buttons
        button("play Again", 150,450,150,50, green, light_green, action="play")
        button("controls", 350,450,100,50, yellow, light_yellow, action="controls")
        button("quit", 550,450,100,50, red, light_red, action ="quit")

        pygame.display.update()
        clock.tick(FPS)

# Random Enemy Firing
def enemyFiring(random):
    if random == 1:
        enemyUFOFire()

# Main Game Loop
def gameLoop():
    gameExit = False
    gameOver = False
    global FPS
    global enemyUFOSpeed
    global UFOMove
    global newScore
    global mainUFOX
    global mainUFOY
    global enemyUFOX
    global enemyUFOY
    global newhealth
  
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press P to play again or Q to exit",blue,50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    
                    # Paue/Quit Controls
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            gameExit = True
                            gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            # UFO Movement Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    UFOMove = -mainUFOSpeed
                elif event.key == pygame.K_RIGHT:
                    UFOMove = mainUFOSpeed
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_SPACE:
                    fire()

            elif event.type == pygame.KEYUP:
                if UFOMove == -mainUFOSpeed:
                    if event.key == pygame.K_LEFT:
                        UFOMove = 0
                if UFOMove == mainUFOSpeed:
                    if event.key == pygame.K_RIGHT:
                        UFOMove = 0
        
        # Update UFO movements
        mainUFOX += UFOMove
        enemyUFOX += enemyUFOSpeed

        # Respawn Enemy UFO's
        if enemyUFOX > display_width:
            enemyUFOX = -random.randrange(50,500)

        # Enemy firing
        randomFire = random.randrange(1,15)
        enemyFiring(randomFire)
    
        # Re-Display UFO's
        gameDisplay.fill(black)
        UFO(mainUFOX,mainUFOY)
        enemy_UFO(enemyUFOX, enemyUFOY)
        
        # Update Health
        health_bar(newhealth)

        # Update Score 
        score(newScore)
        if newScore >= 10:
            you_win()
        if newhealth <= 0:
            gameOver = True
        
        # Update Display
        pygame.display.update()
        
        # Clock ticks
        clock.tick(FPS)

    pygame.quit()
    quit()
    
game_intro()
gameLoop()
