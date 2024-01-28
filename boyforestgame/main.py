import pygame 
import random

WIDTH, HEIGHT = 900, 620
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption("the boy and thy fox")


#title screen
titlescreen_image = pygame.image.load("assets/darkforest.jpeg")
titlescreen = pygame.transform.scale(titlescreen_image, (900, 500))

#image for start button
startbutton_width = 100
startbutton_height = 50
startbutton_image = pygame.image.load("assets/start.png")
startbutton_image = pygame.transform.scale(startbutton_image, (startbutton_width, startbutton_height))




#image for standing boy in the beginning 
#standing boy = 80 x 100 pixels
standingboy_image = pygame.image.load("assets/standingboy.png")

#standing boy flipped 
standingboy_flipped = pygame.transform.flip(standingboy_image, True, False)

#fox image 180 x 135
fox_width = 90
fow_height = 67

fox_image1 = pygame.image.load("assets/fox1.png")
fox_image1 = pygame.transform.scale(fox_image1, (fox_width, fow_height))

fox_image2 = pygame.image.load("assets/fox2.png")
fox_image2 = pygame.transform.scale(fox_image2, (fox_width, fow_height))

fox_image3 = pygame.image.load("assets/fox3.png")
fox_image3 = pygame.transform.scale(fox_image3, (fox_width, fow_height))

fox_image4 = pygame.image.load("assets/fox4.png")
fox_image4 = pygame.transform.scale(fox_image4, (fox_width, fow_height))

fox_image5 = pygame.image.load("assets/fox5.png")
fox_image5 = pygame.transform.scale(fox_image5, (fox_width, fow_height))

#walking boy images 
# 80 x 100 pixels 
walkingboy_image1 = pygame.image.load("assets/walkingboy1.png")
walkingboy_image2 = pygame.image.load("assets/walkingboy2.png")

walking_animation = [0, walkingboy_image1, standingboy_image, walkingboy_image2, standingboy_image]
#game state class to store all the game state properties
class GameState:
    def __init__(self):
        self.startbutton_display = True
        self.intro_display = False
        self.flip_boy = True
        self.walk = False
        self.still = True

def boy_walk(walking_animation, player_hitbox):
    walking_animation[0] = (walking_animation[0] + 1) % 40
    if walking_animation[0] < 10:
        WIN.blit(walking_animation[1], (player_hitbox.x, player_hitbox.y)) #replace y by rectangle y
    elif walking_animation[0] < 20: 
        WIN.blit(walking_animation[2], (player_hitbox.x, player_hitbox.y))
    elif walking_animation[0] < 30:
        WIN.blit(walking_animation[3], (player_hitbox.x, player_hitbox.y))
    else :
        WIN.blit(walking_animation[4], (player_hitbox.x, player_hitbox.y))

def draw_window(startbutton, gamestate, fox_intro, player_hitbox, ground_scroll):
    WIN.blit(titlescreen, (0,0))
    ground_img = pygame.image.load('assets/dirt.jpeg')
    WIN.blit(ground_img, (ground_scroll, 700))
    if (gamestate.startbutton_display):
        WIN.blit(startbutton_image, (startbutton.x, startbutton.y))
    if (gamestate.intro_display):
        if gamestate.flip_boy:
            WIN.blit(standingboy_flipped, (270, 400))
        elif gamestate.still:
            WIN.blit(standingboy_image, (270,400))
        if (fox_intro.x % 25 < 5):
            WIN.blit(fox_image1, (fox_intro.x, fox_intro.y))
        elif (fox_intro.x % 25 < 10):
            WIN.blit(fox_image2, (fox_intro.x, fox_intro.y))
        elif (fox_intro.x % 25 < 15):
            WIN.blit(fox_image3, (fox_intro.x, fox_intro.y))
        elif (fox_intro.x % 25 < 20):
            WIN.blit(fox_image4, (fox_intro.x, fox_intro.y))
        else :
            WIN.blit(fox_image5, (fox_intro.x, fox_intro.y))
    if (gamestate.walk):
        gamestate.still = False
        boy_walk(walking_animation, player_hitbox)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True

    #game state
    gamestate = GameState()

    #rectangle for startbutton
    startbutton = pygame.Rect(400, 225, 100, 50)

    #rectangle for player
    player_hitbox = pygame.Rect(270, 400, 80, 100)

    # jump variables
    isJump = False
    jumpCount = 10
    original_y = player_hitbox.y

    #rectangle for fox animation
    fox_intro = pygame.Rect(375, 433, 1, 1)

    # stump/obstable variables
    ground_scroll = 0
    scroll_speed = 4 #4 pixels every iteration
    stump_frequency = 2500
    last_stump = pygame.time.get_ticks() - stump_frequency 
    ground_img = pygame.image.load('assets/dirt.jpeg')

    #obstacle class
    class Stump(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('assets/stump.png')
            self.image = pygame.transform.scale(self.image, (200,200))
            self.rect = self.image.get_rect() #gets image and puts rect boundary
            self.rect.topleft = [x, y]

        def update(self):
            self.rect.x -= scroll_speed
            if self.rect.right < 0: #if the stump is off the screen kill it to save memory
                self.kill()
    stump_group = pygame.sprite.Group()
        
    
    #plays music 
    pygame.mixer.init()
    pygame.mixer.music.load("assets/dearly_beloved.mp3")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            #checks if user closed window
            if event.type == pygame.QUIT:
                run = False


            #checks if user clicked the start button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startbutton.collidepoint(event.pos):
                    gamestate.startbutton_display = False
                    gamestate.intro_display = True
        
        
        # draw and scroll the ground
        stump_group.draw(WIN)
        stump_group.update()
        WIN.blit(ground_img, (ground_scroll, 700))
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 50:
            ground_scroll = 0

        # generate new stumps
        time_now = pygame.time.get_ticks() #gets current time 
        if time_now - last_stump > stump_frequency: #enough time has passed --> now we can create new stumps
            stump_width = random.randint(500,900) #random integer within this range
            small_stump = Stump(WIDTH + stump_width,560) #instance of stump class
            stump_group.add(small_stump) #add to the stump group
            last_stump = time_now #update when last stump was
        
        
        # player's jumping mechanism
        keys = pygame.key.get_pressed()
        if not(isJump):
            if keys[pygame.K_SPACE]:
                isJump = True
        else:
            if jumpCount >= -10:
                player_hitbox.y -= (jumpCount * abs(jumpCount)) * 0.5
                jumpCount -= 1
            else:
                jumpCount = 10
                isJump = False   
                player_hitbox.y = original_y


        #when we want to display intro, move the fox and make it go away
        if gamestate.intro_display and fox_intro.x <= 900:
            fox_intro.x += 1
        
        #when the fox is out the screen 
        #make the boy start to walk
        if fox_intro.x == 900:
            gamestate.flip_boy = False
            gamestate.walk = True


        draw_window(startbutton, gamestate, fox_intro, player_hitbox, ground_scroll)

    pygame.quit()

if __name__ == "__main__":
    main()