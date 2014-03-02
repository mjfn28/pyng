import pygame, sys, os, random
from pygame.locals import *

#state manager class.
#this controls which state is currently in use and keeps track of all states
class StateManager:
    current = 0
    stateArray = []

    def Switch(self, newState):
        self.stateArray[self.current].exit()
        self.current=newState
        self.stateArray[self.current].enter()

manager = StateManager()

#test state.
class TestState:
    
    def __init__(self):
        self.whiteColor = pygame.Color(255,255,255)

    def enter(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)

        self.testSurface = pygame.image.load(self.path + '\\test.jpg')
        
    def loop(self):
        i=0
        
    def render(self, screen):
        screen.fill(self.whiteColor)
        screen.blit(self.testSurface, (0,0))

    def event(self, e):
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
                
    def exit(self):
        i=0

ts= TestState()

manager.stateArray.append(ts)

#main game state
class GameState:
    
    
    def __init__(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)
        
        self.whiteColor = pygame.Color(255,255,255)
        self.blackColor = pygame.Color(0,0,0)
        
        
        
        pygame.font.init()
        self.font = pygame.font.Font(self.path + '\\flerp.ttf', 32)

    def enter(self):
        self.bounce=0
        
        self.x1=10
        self.y1=10
        self.w1=25
        self.h1=100
        
        self.x2=765
        self.y2=10
        self.w2=25
        self.h2=100
        
        self.p1moveup=False
        self.p1movedown=False
        self.p2moveup=False
        self.p2movedown=False

        self.xb=self.x1+self.w1+15
        self.yb=int(self.y1+(self.h1/2))

        self.start=False

        self.bs=8

        self.p1score=0
        self.p2score=0
        self.startpos=1

    # move the player, check collisions
    def loop(self):
        #move the players
        if self.p1movedown == True:
            self.y1+=10
        if self.p1moveup == True:
            self.y1-=10
        if self.p2movedown == True:
            self.y2+=10
        if self.p2moveup == True:
            self.y2-=10

        if self.y1 < 0 :
            self.y1=0
        elif self.y1+self.h1 > 600 :
            self.y1=600-self.h1
            
        if self.y2 < 0 :
            self.y2=0
        elif self.y2+self.h2 > 600 :
            self.y2=600-self.h2

        #move the ball
        if self.start == True:
            if self.dir == 0:
                self.xb+=self.bs + int(self.bounce/5)
                self.yb+=self.bs + int(self.bounce/5)
            elif self.dir == 1:
                self.xb+=self.bs + int(self.bounce/5)
                self.yb-=self.bs + int(self.bounce/5)
            elif self.dir == 2:
                self.xb-=self.bs + int(self.bounce/5)
                self.yb-=self.bs + int(self.bounce/5)
            elif self.dir == 3:
                self.xb-=self.bs + int(self.bounce/5)
                self.yb+=self.bs + int(self.bounce/5)

        #ball collision with top & bottom walls
        if self.yb-10 < 0:
            self.yb=10
            if self.dir == 1:
                self.dir=0
            elif self.dir == 2:
                self.dir=3
            self.bounce += 1
        elif self.yb+10 > 600:
            self.yb=590
            if self.dir == 0:
                self.dir=1
            elif self.dir == 3:
                self.dir=2
            self.bounce += 1

        #ball collision with paddles
        '''
        if self.dir == 0:
                bline = ((self.xb,self.yb),(self.xb+self.bs + int(self.bounce/5),self.yb+self.bs + int(self.bounce/5)))
            elif self.dir == 1:
                bline = ((self.xb,self.yb),(self.xb+self.bs + int(self.bounce/5),self.yb-self.bs + int(self.bounce/5)))
            elif self.dir == 2:
                bline = ((self.xb,self.yb),(self.xb-self.bs + int(self.bounce/5),self.yb-self.bs + int(self.bounce/5)))
            elif self.dir == 3:
                bline = ((self.xb,self.yb),(self.xb-self.bs + int(self.bounce/5),self.yb+self.bs + int(self.bounce/5)))
        '''      
        #p1        
        if self.xb-10 < self.x1+self.w1 and self.yb-10 > self.y1 and self.yb+10 < self.y1+self.h1 :
            self.xb = self.x1+self.w1+10
            if self.dir == 2:
                self.dir=1
            elif self.dir == 3:
                self.dir=0
            self.bounce += 1
        #p2
        if self.xb+10 > self.x2 and self.yb-10 > self.y2 and self.yb+10 < self.y2+self.h2 :
            self.xb = self.x2-10
            if self.dir == 1:
                self.dir=2
            elif self.dir == 0:
                self.dir=3
            self.bounce += 1

        #ball hits wall
        #left
        if self.xb-10 < 0:
            self.p2score += 1
            self.start = False
            self.xb=11
            self.startpos=1
            self.bounce = 0
        #right
        if self.xb+10 > 800:
            self.p1score +=1
            self.start = False
            self.xb=789
            self.startpos=2
            self.bounce = 0

        #score
        msg = str(self.p1score) + " | " + str(self.p2score)
        self.scoreSurface = self.font.render(msg, False, self.whiteColor)

        #winning condition
        if self.p1score >=10 :
            manager.Switch(4)
        elif self.p2score >=10:
            manager.Switch(5)
        
    def render(self, screen):
        screen.fill(self.blackColor)

        screen.blit(self.scoreSurface, (400-(self.scoreSurface.get_width()/2),0))
        
        pygame.draw.rect(screen, self.whiteColor, (self.x1, self.y1, self.w1, self.h1))
        pygame.draw.rect(screen, self.whiteColor, (self.x2, self.y2, self.w2, self.h2))

        if self.start == False:
            if self.startpos==1:
                pygame.draw.circle(screen, self.whiteColor, (self.x1+self.w1+15, int(self.y1+(self.h1/2))), 10, 0)
            elif self.startpos==2:
                pygame.draw.circle(screen, self.whiteColor, (self.x2-15, int(self.y2+(self.h2/2))), 10, 0)
        else:
            pygame.draw.circle(screen, self.whiteColor, (self.xb, self.yb), 10, 0)
            
    def event(self, e):
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_w:
                self.p1moveup=True
            elif e.key == K_s:
                self.p1movedown=True
            elif e.key == K_o:
                self.p2moveup=True
            elif e.key == K_k:
                self.p2movedown=True
            elif e.key == K_SPACE:
                if self.start == False:
                    self.start = True
                    if self.startpos==1:
                        self.dir = random.randint(0,3)
                        self.xb=self.x1+self.w1+15
                        self.yb=int(self.y1+(self.h1/2))
                    elif self.startpos==2:
                        self.dir = random.randint(0,3)
                        self.xb=self.x2-15
                        self.yb=int(self.y2+(self.h2/2))
            #elif e.key == K_9:
            #    manager.Switch(0)
        elif e.type == KEYUP:
            if e.key == K_w:
                self.p1moveup=False
            elif e.key == K_s:
                self.p1movedown=False
            elif e.key == K_o:
                self.p2moveup=False
            elif e.key == K_k:
                self.p2movedown=False
        
    def exit(self):
        i=0

    #input line as pair of points
    def linex(line1, line2):
        
        A1 = line1[1][1] - line1[0][1]
        B1 = line1[0][0] - line1[1][0]
        A2 = line2[1][1] - line2[0][1]
        B2 = line2[0][0] - line2[1][0]

        det = A1*B2 - A2*B1

        if det == 0:
            return false
        else:
            return true

gs= GameState()

manager.stateArray.append(gs)

#main menu
class MenuState:

    #initialization
    def __init__(self):
        self.whiteColor = pygame.Color(255,255,255)
        self.blackColor = pygame.Color(0,0,0)

    #load images, fonts and set text
    def enter(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)

        self.titleSurface = pygame.image.load(self.path + '\\title.png')

        pygame.font.init()
        self.fontBig = pygame.font.Font(self.path + '\\flerp.ttf', 32)
        self.fontSmall = pygame.font.Font(self.path + '\\flerp.ttf', 12)

        msg = "v0.1"
        self.versionSurface = self.fontSmall.render(msg, False, self.whiteColor)
        newstr = "NEW GAME"
        self.newSurface = self.fontBig.render(newstr, False, self.whiteColor)
        quitstr = "QUIT"
        self.quitSurface = self.fontBig.render(quitstr, False, self.whiteColor)
        pointerstr= ">"
        self.pointerSurface = self.fontBig.render(pointerstr, False, self.whiteColor)
        
        self.menuIndex=0

    #do nothing
    def loop(self):
        i=0

    #draw to screen
    def render(self, screen):
        screen.fill(self.blackColor)
        screen.blit(self.titleSurface, ((800/2)-(self.titleSurface.get_width()/2),0))
        screen.blit(self.versionSurface, (800-self.versionSurface.get_width(),600-self.versionSurface.get_height()))

        screen.blit(self.newSurface, ((800/2)-(self.newSurface.get_width()/2),300))
        screen.blit(self.quitSurface, ((800/2)-(self.quitSurface.get_width()/2),500))

        if self.menuIndex == 0:
            screen.blit(self.pointerSurface, ((800/2)-(self.newSurface.get_width()/2)-self.pointerSurface.get_width(),300))
        elif self.menuIndex == 1:
            screen.blit(self.pointerSurface, ((800/2)-(self.quitSurface.get_width()/2)-self.pointerSurface.get_width(),500))

    #handle events        
    def event(self, e):
        #X out
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        #keydown
        elif e.type == KEYDOWN:
            #enter
            if e.key == K_RETURN:
                if self.menuIndex == 0: #new game
                    manager.Switch(3)
                elif self.menuIndex == 1: #quit
                    pygame.event.post(pygame.event.Event(QUIT))
            #key down to scroll in menu
            if e.key == K_DOWN:
                self.menuIndex += 1
                if self.menuIndex > 1:
                    self.menuIndex = 0
            #key up to scroll in menu
            if e.key == K_UP:
                self.menuIndex -= 1
                if self.menuIndex < 0:
                    self.menuIndex = 1

    def exit(self):
        i=0

ms = MenuState()

manager.stateArray.append(ms)

#state showing controls. Waits for player to hit enter to start.
class ControlState:
    
    def __init__(self):
        self.whiteColor = pygame.Color(255,255,255)

    def enter(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)

        self.ctrlSurface = pygame.image.load(self.path + '\\ctrl.png')
        
    def loop(self):
        i=0
        
    def render(self, screen):
        screen.fill(self.whiteColor)
        screen.blit(self.ctrlSurface, (0,0))

    def event(self, e):
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_RETURN:
                manager.Switch(1)
                
    def exit(self):
        i=0

cs = ControlState()

manager.stateArray.append(cs)

#if P1 wins enter this state
class P1WinState:

    def __init__(self):
        self.whiteColor = pygame.Color(255,255,255)
        self.blueColor = pygame.Color(0,0,255)

    def enter(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)

        self.titleSurface = pygame.image.load(self.path + '\\title.png')

        pygame.font.init()
        self.fontBig = pygame.font.Font(self.path + '\\flerp.ttf', 32)
        
        
        msg1 = "P1"
        self.msg1Surface = self.fontBig.render(msg1, False, self.blueColor)
        msg2 = "WINS"
        self.msg2Surface = self.fontBig.render(msg2, False, self.whiteColor)
        msg3 = "PRESS ESC TO QUIT"
        self.msg3Surface = self.fontBig.render(msg3, False, self.whiteColor)
        msg4 = "PRESS ENTER FOR MENU"
        self.msg4Surface = self.fontBig.render(msg4, False, self.whiteColor)

    def loop(self):
        i=0

    def render(self, screen):
        screen.blit(self.msg1Surface, ((800/2)-(self.msg1Surface.get_width()/2),200))
        screen.blit(self.msg2Surface, ((800/2)-(self.msg2Surface.get_width()/2),200+self.msg2Surface.get_height()))
        screen.blit(self.msg3Surface, ((800/2)-(self.msg3Surface.get_width()/2),200+self.msg2Surface.get_height()+self.msg3Surface.get_height()+self.msg2Surface.get_height()))
        screen.blit(self.msg4Surface, ((800/2)-(self.msg4Surface.get_width()/2),200+self.msg2Surface.get_height()+self.msg3Surface.get_height()+self.msg4Surface.get_height()+self.msg2Surface.get_height()))
        
    def event(self, e):
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_RETURN:
                manager.Switch(2)
            elif e.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    def exit(self):
        i=0

p1ws = P1WinState()

manager.stateArray.append(p1ws)

#if p2 wins enter this state
class P2WinState:

    def __init__(self):
        self.whiteColor = pygame.Color(255,255,255)
        self.redColor = pygame.Color(255,0,0)

    def enter(self):
        self.full_path = os.path.realpath(__file__)
        self.path, self.file = os.path.split(self.full_path)

        self.titleSurface = pygame.image.load(self.path + '\\title.png')

        pygame.font.init()
        self.fontBig = pygame.font.Font(self.path + '\\flerp.ttf', 32)
        
        
        msg1 = "P2"
        self.msg1Surface = self.fontBig.render(msg1, False, self.redColor)
        msg2 = "WINS"
        self.msg2Surface = self.fontBig.render(msg2, False, self.whiteColor)
        msg3 = "PRESS ESC TO QUIT"
        self.msg3Surface = self.fontBig.render(msg3, False, self.whiteColor)
        msg4 = "PRESS ENTER FOR MENU"
        self.msg4Surface = self.fontBig.render(msg4, False, self.whiteColor)

    def loop(self):
        i=0

    def render(self, screen):
        screen.blit(self.msg1Surface, ((800/2)-(self.msg1Surface.get_width()/2),200))
        screen.blit(self.msg2Surface, ((800/2)-(self.msg2Surface.get_width()/2),200+self.msg2Surface.get_height()))
        screen.blit(self.msg3Surface, ((800/2)-(self.msg3Surface.get_width()/2),200+self.msg2Surface.get_height()+self.msg3Surface.get_height()+self.msg2Surface.get_height()))
        screen.blit(self.msg4Surface, ((800/2)-(self.msg4Surface.get_width()/2),200+self.msg2Surface.get_height()+self.msg3Surface.get_height()+self.msg4Surface.get_height()+self.msg2Surface.get_height()))
        
    def event(self, e):
        if e.type == QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == KEYDOWN:
            if e.key == K_RETURN:
                manager.Switch(2)
            elif e.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    def exit(self):
        i=0

p2ws = P2WinState()

manager.stateArray.append(p2ws)
