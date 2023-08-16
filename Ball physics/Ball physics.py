import pygame,random,copy,colorsys

pygame.init()

screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN)
pygame.display.set_caption('Ball physics')
clock = pygame.time.Clock()

mid = (1920/2.5,1080/2.5)

pygame.mouse.set_visible(False)

#Functions
def checkExit():
    key = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            pygame.quit()
            exit()

def addRandomColors():
    ballColors.append(list(colorsys.hsv_to_rgb(random.random(),1,1)))
    ballColors[-1][0] *= 255
    ballColors[-1][1] *= 255
    ballColors[-1][2] *= 255

def addRainbow(r):
    ballColors.append(list(colorsys.hsv_to_rgb(r/50,1,1)))
    ballColors[-1][0] *= 255
    ballColors[-1][1] *= 255
    ballColors[-1][2] *= 255

def dampMouse():
    smoothMouse[0] += (mouse[0]-smoothMouse[0])/10
    smoothMouse[1] += (mouse[1]-smoothMouse[1])/10

def drawBalls():
    for i in range(len(balls)):
        pygame.draw.circle(screen,ballColors[i],(balls[i]),ballRadius[i]/2)
        if visualize:
            getDist(balls[i],(balls[i][0]+ballsVel[i][0],balls[i][1]+ballsVel[i][1]))
            pygame.draw.line(screen,(0,255,255),(balls[i]),(balls[i][0]+ballsVel[i][0],balls[i][1]+ballsVel[i][1]),int(round(dist/5+1)))

def getDist(p1,p2):
    global dist
    dist = (((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))**0.5

#Variables
colorType = 2
type = 1
sceneType = 2

ballAmount = 20
chainBallSize = 40

ballRadius = []
randomRadius = [50,70]

ballColors = []
balls = []
oldBalls = []
ballsVel = []

if type == 1:
    for i in range(ballAmount):
        balls.append([random.randint(200,600),random.randint(200,600)])
elif type == 2 or type == 3:
    for i in range(ballAmount):
        balls.append([(-i/1.25*chainBallSize)+(ballAmount*chainBallSize/1.25)+(mid[0]-(ballAmount/2)*chainBallSize*0.8),mid[1]])

for i in range(ballAmount):
    ballsVel.append([0,0])
    oldBalls = copy.deepcopy(balls)
    if type == 2 or type == 3:
        ballRadius.append(chainBallSize)
    else:
        ballRadius.append(random.randint(randomRadius[0],randomRadius[1]))

if type == 2 or type == 3:
    for i in range(ballAmount):
        ballColors.append([255,255,255])
else:
    for i in range(ballAmount):
        if colorType == 1:
            addRandomColors()
        elif colorType == 2:
            addRainbow(i)

collideIter = 20

moveAmount = 1/collideIter

lineIter = 2

record = False
frame = 0

smoothMouse = [400,400]
damping = True
mouseSize = 40
mouseResistance = False

clicked = 0

visualize = False

checkThreshold = randomRadius[0]

breakChain = False

fps = 0
font = pygame.font.SysFont("verdana",20)

while True:
    checkExit()
    
    key = pygame.key.get_pressed()
    click = pygame.mouse.get_pressed()
    mouse = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
    pygame.mouse.set_pos(mouse)
    if damping:
        dampMouse()
    else:
        smoothMouse = mouse
    
    frame += 1

    #draw
    if sceneType == 1:
        screen.fill((20,20,20))    
    elif sceneType == 2:
        screen.fill((50,50,50))
        pygame.draw.circle(screen,(20,20,20),mid,400)

    #show FPS
    text = font.render("FPS: {}".format(round(clock.get_fps(),2)),True,(255,255,255))
    screen.blit(text,(10,10))
    
    #draw lines
    if type == 2 or type == 3:
        for i in range(ballAmount-1):
            pygame.draw.line(screen,(0,0,255),(balls[i]),(balls[i+1]))
    
    #draw mouse
    pygame.draw.circle(screen,(100,0,0),smoothMouse,mouseSize)
    if damping == 1:
        pygame.draw.circle(screen,(100,100,0),mouse,10)
    #draw balls
    for i in range(len(balls)):
        drawBalls()
    
    #set vel
    for i in range(len(balls)):
        ballsVel[i][0] = balls[i][0] - oldBalls[i][0]
        ballsVel[i][1] = balls[i][1] - oldBalls[i][1]
    oldBalls = copy.deepcopy(balls)

    #motion
    for i in range(len(balls)):
        balls[i][0] += ballsVel[i][0]
        balls[i][1] += ballsVel[i][1]
        balls[i][1] += 1
    
    for k in range(collideIter):
        for v,i in enumerate(balls):
            ballRd2 = ballRadius[v]/2
            
            #delete balls
            if click[2]:
                getDist(i,smoothMouse)
                required_dist = ballRadius[v]/2 + mouseSize
                if ((type == 1 or type == 4) and dist < required_dist) or (type == 2 and v > ballAmount-1 and dist < required_dist) or (dist < required_dist and type == 3 and v > ballAmount-1):
                    del balls[v]
                    del oldBalls[v]
                    del ballsVel[v]
                    del ballColors[v]
                    del ballRadius[v]
                    continue
            
            for v2,j in enumerate(balls):
                
                if v != v2:
                    #set two points
                    if type == 2:
                        balls[0] = smoothMouse
                    if type == 3:
                        balls[ballAmount-1] = [mid[0]-(ballAmount/2)*chainBallSize*0.8,mid[1]]
                        balls[0] = [mid[0]+(ballAmount/2)*chainBallSize*0.8,mid[1]]
                    
                    dx = j[0]-i[0]
                    dy = j[1]-i[1]
                    
                    #check if near ball
                    if (type == 2 or type == 3) and v < ballAmount:
                        if breakChain:
                            if abs(dx) < checkThreshold and abs(dy) < checkThreshold:
                                getDist((0,0),(dx,dy))
                            else:
                                continue
                        else:
                            getDist((0,0),(dx,dy))
                    else:
                        if abs(dx) < checkThreshold and abs(dy) < checkThreshold:
                            getDist((0,0),(dx,dy))
                        else:
                            continue
                    
                    #move balls apart
                    required_dist = ballRadius[v]/2 + ballRadius[v2]/2
                    if dist < required_dist:
                        if dist == 0:
                            break
                        overlap = required_dist-dist
                        move = [dx*(overlap/dist)*moveAmount,dy*(overlap/dist)*moveAmount]
                        i[0] -= move[0]
                        i[1] -= move[1]
                        j[0] += move[0]
                        j[1] += move[1]
                    #draw line
                    if visualize:
                        if dist < required_dist+5:
                                pygame.draw.line(screen,(200,0,100),(i),(j))
                    for m in range(lineIter):
                        #move points together
                        if type == 2 or type == 3:
                            if v2 == v-1 and v > 0 and v2 < ballAmount-1:
                                dx = balls[v-1][0]-i[0]
                                dy = balls[v-1][1]-i[1]
                                getDist((0,0),(dx,dy))
                                if dist > ballRadius[v]:
                                    overlap = ballRadius[v]-dist
                                    move = [dx*(overlap/dist)*moveAmount,dy*(overlap/dist)*moveAmount]
                                    i[0] -= move[0]
                                    i[1] -= move[1]
                                    j[0] += move[0]
                                    j[1] += move[1]
                        if type == 3:
                            if v == ballAmount-2 and v2 == ballAmount-1:
                                dx = balls[v2][0]-i[0]
                                dy = balls[v2][1]-i[1]
                                getDist((0,0),(dx,dy))
                                if dist > ballRadius[v]:
                                    overlap = ballRadius[v]-dist
                                    move = [dx*(overlap/dist)*moveAmount,dy*(overlap/dist)*moveAmount]
                                    i[0] -= move[0]
                                    i[1] -= move[1]
                                    j[0] += move[0]
                                    j[1] += move[1]
            #middle click
            if click[1]:
                if type != 2:
                    dx = smoothMouse[0]-i[0]
                    dy = smoothMouse[1]-i[1]
                    getDist((0,0),(dx,dy))
                    if dist == 0:
                        continue
                    required_dist = ballRadius[v]/2 + mouseSize
                    if dist < required_dist:
                        if visualize:
                            pygame.draw.line(screen,(200,0,100),(i),smoothMouse)
                        overlap = required_dist-dist
                        move = [dx*(overlap/dist)*moveAmount,dy*(overlap/dist)*moveAmount]
                        i[0] -= move[0]
                        i[1] -= move[1]
                        if mouseResistance:
                            mouse[0] += move[0]/500
                            mouse[1] += move[1]/500
                            pygame.mouse.set_pos(mouse)
            
            #constrain balls by screen
            if type != 3:
                i[0] = max(min(i[0],mid[0]*2-ballRd2),ballRd2)
                i[1] = max(min(i[1],mid[1]*2-ballRd2),ballRd2)
            elif i[1] > mid[1]*2 and v > ballAmount:
                del balls[v]
                del oldBalls[v]
                del ballsVel[v]
                del ballColors[v]
                del ballRadius[v]
            
            #constrain balls by circle
            if sceneType == 2:
                dx = mid[0]-i[0]
                dy = mid[1]-i[1]
                getDist(balls[v],mid)
                if dist > 400-ballRadius[v]/2:
                    overlap = 400-ballRadius[v]/2-dist
                    move = [dx*(overlap/dist)*moveAmount,dy*(overlap/dist)*moveAmount]
                    i[0] -= move[0]
                    i[1] -= move[1]
    
    #make new ball
    if click[0]:
        if clicked == 0:
            clicked = 1
            balls.append([smoothMouse[0]+random.randint(-1,1),smoothMouse[1]+random.randint(-1,1)])
            oldBalls.append([smoothMouse[0],smoothMouse[1]])
            ballsVel.append([0,0])
            ballRadius.append(random.randint(randomRadius[0],randomRadius[1]))
            if colorType == 1:
                addRandomColors()
            elif colorType == 2:
                addRainbow(frame)
    else:
        clicked = 0

    #make multiple balls
    if key[pygame.K_SPACE]:
        balls.append([smoothMouse[0]+random.randint(-1,1),smoothMouse[1]+random.randint(-1,1)])
        oldBalls.append([smoothMouse[0],smoothMouse[1]])
        ballsVel.append([0,0])
        ballRadius.append(random.randint(randomRadius[0],randomRadius[1]))
        if colorType == 1:
            addRandomColors()
        elif colorType == 2:
            addRainbow(frame)
    
    if not (click[0] or click[2] or key[pygame.K_SPACE]):
        smoothMouse = [mouse[0],mouse[1]]
    
    #clear all
    if key[pygame.K_e]:
        balls, ballsVel, ballColors, oldBalls, ballRadius = [],[],[],[],[]
    #Save png image
    if record:
        pygame.display.set_caption('{}'.format(frame))
        rect = pygame.Rect(0, 0, mid[0]*2, mid[1]*2)
        ss = screen.subsurface(rect)
        pygame.image.save(ss, r"Frames\{}.png".format(frame))
    pygame.display.update()
    clock.tick(60)