import pygame
import math as m

pygame.init()

#colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (34, 139, 34)
blue = (64, 224, 208)
red = (255, 0, 0)

#pictures
arrowImg = pygame.image.load('arrow.png')
background = pygame.image.load('background.jpg')
background2 = pygame.image.load('background2.jpg')


#Screen size
screenWidth=1200
screenHeight=1000
screen = pygame.display.set_mode((screenWidth, screenHeight))

#solar objects
earthAngle=0.0174

mercuryDistance = 70
mercuryRadius = 3
sunRadius = mercuryRadius*10

sunColor = (211, 32, 0)
mercuryColor = (211,211,211)
venusColor = (255,228,181)
earthColor = (0,255,255)
marsColor = (255,99,71)
jupiterColor = (205,92,92)
saturnColor = (245,245,220)
uranusColor = (135,206,250)
neptuneColor = (30,144,255)

#other constants
cameraX = 1
cameraY = 1
xChange = 0
yChange = 0
velocity = 1.0
showOrbits = False
demo = 0.2

selected_option = 0.30
running = True
programState = "menu" #first state, there is also "simulation" and "about"

#text writting
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_display(game_display, text, x, y, font_size, color, centered_x=False, centered_y=False):
    font = pygame.font.Font(None,font_size)
    TextSurf, TextRect = text_objects(text, font, color)
    if centered_x and centered_y:
        TextRect.center = ((screenWidth/2),(screenHeight/2))
    elif centered_x:
        TextRect.center = ((screenWidth/2),y)
    elif centered_y:
        TextRect.center = (x,(screenHeight/2))
    else:
        TextRect.center = (x,y)
    game_display.blit(TextSurf, TextRect)
def draw_image(x, y, image):
    screen.blit(image, (x, y))


class Planet:

    def __init__(self,color, distance, radius, angle):
        self.color = color
        self.distance = distance
        self.radius = radius
        self.angle = angle

    def draw_orbit(self):
        pygame.draw.circle(screen, self.color, (screenWidth / 2 * cameraX, screenHeight / 2 * cameraY), self.distance, 1)

    def draw_planet(self):
        pygame.draw.circle(screen, self.color, (int(m.cos(self.angle) * self.distance) + (screenWidth / 2) * cameraX,
                                                 int(m.sin(self.angle) * self.distance) + (screenHeight / 2) * cameraY), self.radius)

    def draw_about_planet(self, x, y, size):
        pygame.draw.circle(screen, self.color, (x, y), size)

class Button:

    def __init__(self, posX, posY, way):
        self.posX = posX
        self.posY = posY
        self.buttonWidth = 100
        self.buttonHeight = 50
        self.way = way

    def draw_button(self):
        if self.way == "up":
            pygame.draw.rect(screen, white, pygame.Rect(self.posX, self.posY, self.buttonWidth, self.buttonHeight))
            pygame.draw.polygon(screen, green, [(self.posX + self.buttonWidth * 0.2, self.posY + self.buttonHeight * 0.8),
                                                (self.posX + self.buttonWidth * 0.5, self.posY + self.buttonHeight * 0.2),
                                                (self.posX + self.buttonWidth * 0.8, self.posY + self.buttonHeight * 0.8)])
        if self.way == "down":
            pygame.draw.rect(screen, white, pygame.Rect(self.posX, self.posY, self.buttonWidth, self.buttonHeight))
            pygame.draw.polygon(screen, green, [(self.posX + self.buttonWidth * 0.2, self.posY + self.buttonHeight * 0.2),
                                                (self.posX + self.buttonWidth * 0.5, self.posY + self.buttonHeight * 0.8),
                                                (self.posX + self.buttonWidth * 0.8, self.posY + self.buttonHeight * 0.2)])
        if self.way == "stop":
            pygame.draw.rect(screen, white, pygame.Rect(self.posX, self.posY, self.buttonWidth, self.buttonHeight))
            message_display(screen, "STOP", self.posX + self.buttonWidth * 0.5, self.posY + self.buttonHeight * 0.5, 40, red)

buttonUp = Button(1050,50, "up")
buttonDown = Button(1050,140, "down")
buttonStop = Button(1050,200, "stop")

clock = pygame.time.Clock()
#main loop
while running:
    msElapsed = clock.tick(60)
    screen.fill(black)

    mercury = Planet(mercuryColor, mercuryDistance, mercuryRadius, earthAngle / 0.24)
    venus = Planet(venusColor, mercuryDistance*1.5667, mercuryRadius*2.4, earthAngle / 0.615)
    earth = Planet(earthColor, mercuryDistance*2.143, mercuryRadius*2.52, earthAngle)
    mars = Planet(marsColor, mercuryDistance*3.57, mercuryRadius*1.36, earthAngle / 1.88)
    jupiter = Planet(jupiterColor,mercuryDistance*10.743,mercuryRadius*28, earthAngle/11.86)
    saturn = Planet(saturnColor,mercuryDistance*21.143, mercuryRadius*23.3, earthAngle/29.46)
    uranus = Planet(uranusColor,mercuryDistance*42.143,mercuryRadius*10.5, earthAngle/84)
    neptune = Planet(neptuneColor,mercuryDistance*63.857,mercuryRadius*9.5,earthAngle/165)

    #events after using keyboard/mouse
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if programState == 'simulation' or programState == 'about':
                    programState = 'menu'
            # ----------------Menu Events-------------
            elif programState == 'menu':
                if event.key == pygame.K_DOWN:
                    if selected_option < 0.45:
                        selected_option += 0.10
                    else:
                        selected_option = 0.30
                elif event.key == pygame.K_UP:
                    if selected_option > 0.35:
                        selected_option -= 0.10
                    else:
                        selected_option = 0.50
                elif event.key == pygame.K_RETURN:
                    if selected_option < 0.35:
                        programState = 'simulation'
                    elif selected_option == 0.40:
                        programState = 'about'
                    elif selected_option == 0.50:
                        running = False
            elif programState == 'simulation':
                if event.key == pygame.K_RIGHT:
                    xChange=-0.01
                if event.key == pygame.K_LEFT:
                    xChange=0.01
                if event.key == pygame.K_DOWN:
                    yChange=-0.01
                if event.key == pygame.K_UP:
                    yChange=0.01
                if event.key == pygame.K_SPACE:
                    if showOrbits == False:
                        showOrbits = True
                    else:
                        showOrbits = False
        if event.type == pygame.KEYUP:
            if programState == 'simulation':
                if event.key == pygame.K_LEFT:
                    xChange=0
                if event.key == pygame.K_RIGHT:
                    xChange=0
                if event.key == pygame.K_UP:
                    yChange=0
                if event.key == pygame.K_DOWN:
                    yChange=0
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > 1050 and pos[0]<1150 and pos[1]>50 and pos[1]<100:
                velocity+=0.5
            if pos[0] > 1050 and pos[0]<1150 and pos[1]>140 and pos[1]<190:
                if velocity>0:
                    velocity -= 0.5
                else:
                    pass
            if pos[0] > 1050 and pos[0]<1150 and pos[1]>200 and pos[1]<250:
                velocity = 0

    #3 states of programme
    if programState == "menu":
        draw_image(0,0,background)
        draw_image(screenWidth/4 + 120, screenHeight/8 + screenHeight*selected_option - 85, arrowImg)
        if pygame.font:
            # menu title
            message_display(screen, "Solar system simulation", 0, 75 + round(screenHeight * 0.15), 130, red, True)
            # menu items
            message_display(screen, "Play", 0, 75 + round(screenHeight * 0.30), 80, white, True)
            message_display(screen, "About", 0, 75 + round(screenHeight * 0.40), 80, white, True)
            message_display(screen, "Quit", 0, 75 + round(screenHeight * 0.50), 80, white, True)

        #animation on main page
        pygame.draw.circle(screen, earthColor,(int(m.cos(demo) * 250) + 900, int(m.sin(demo) * 100) + 800), 10)
        pygame.draw.circle(screen, sunColor, (900, 800), 30, 50)
        demo +=0.05

    if programState == 'simulation':

        draw_image(0+xChange,0+yChange,background2)
        pygame.draw.circle(screen, sunColor, (screenWidth/2*cameraX, screenHeight/2*cameraY), sunRadius, 150)#sun
        #putanje

        mercury.draw_planet()
        venus.draw_planet()
        earth.draw_planet()
        mars.draw_planet()
        jupiter.draw_planet()
        saturn.draw_planet()
        uranus.draw_planet()
        neptune.draw_planet()

        if showOrbits==True:
            mercury.draw_orbit()
            venus.draw_orbit()
            earth.draw_orbit()
            mars.draw_orbit()
            jupiter.draw_orbit()
            saturn.draw_orbit()
            uranus.draw_orbit()
            neptune.draw_orbit()

        buttonUp.draw_button()
        buttonDown.draw_button()
        message_display(screen, str(velocity), 1100, 120, 50, white)
        buttonStop.draw_button()


        pygame.display.flip()
        earthAngle += 0.0174 * velocity
        cameraX +=xChange
        cameraY +=yChange

    if programState == 'about':
        mercury.draw_about_planet(200,100,20)
        venus.draw_about_planet(200,200,35)
        earth.draw_about_planet(200,300,35)
        mars.draw_about_planet(200,400,24)
        jupiter.draw_about_planet(200,600,120)
        saturn.draw_about_planet(800,150,90)
        pygame.draw.circle(screen, saturnColor, (800, 150), 110, 5)
        uranus.draw_about_planet(800,350,60)
        neptune.draw_about_planet(800,500,50)

        message_display(screen, " - Mercury", 350, 100, 40, white)
        message_display(screen, " - Venus", 350, 200, 40, white)
        message_display(screen, " - Earth", 350, 300, 40, white)
        message_display(screen, " - Mars", 350, 400, 40, white)
        message_display(screen, " - Jupiter", 450, 600, 40, white)
        message_display(screen, " - Saturn", 1000, 150, 40, white)
        message_display(screen, " - Uranus", 950, 350, 40, white)
        message_display(screen, " - Neptune", 950, 500, 40, white)

        message_display(screen, " If you want to see orbits", 0, 800, 30, white, True)
        message_display(screen, "of the planets, just press SPACE", 0, 830, 30, white, True)
        message_display(screen, " when start simulation.", 0, 860, 30, white, True)

        message_display(screen, " Press ESC to return to menu.", 0, 920, 30, white, True)

    pygame.display.update()
pygame.quit()
quit