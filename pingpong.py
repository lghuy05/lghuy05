import pygame
class Paddle():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,15,80)
        pass

    def draw(self,screen):
        pygame.draw.rect(screen, (255,255,255), self.rect)

    def move(self,speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.move_ip(0,-speed)
        elif keys[pygame.K_DOWN]:
            self.rect.move_ip(0,speed)
        pass

    def check_bounds(self,screen_height):
        if self.rect.top < 0:   
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    
    def ai_move(self,ball,speed):
        if ball.rect.bottom > self.rect.bottom:
            self.rect.move_ip(0,speed)
        if ball.rect.top < self.rect.top:
            self.rect.move_ip(0,-speed)


class Ball():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 1
        self.rect = pygame.Rect(self.x,self.y,15,15)


    def draw(self,screen):
        pygame.draw.rect(screen,(255,255,255),self.rect)

    def move(self,speed,game):
        self.rect.move_ip(self.dx*speed,self.dy*speed)
        if self.rect.left <0:
            game.score[1]+=1
            game.reset()
        if self.rect.right > game.screen.get_width():
            game.score[0]+= 1
            game.reset()
        
    def bounce(self, axis):
        if axis == 'x':
            self.dx *= -1
        if axis == 'y':
            self.dy *= -1

class Pingpong():
    def __init__(self, x=800, y=600):
        pygame.init();
        self.font = pygame.font.Font(None,36)
        self.screen = pygame.display.set_mode((x, y))
        self.paddle1 = Paddle(0,y/2)
        self.paddle2 = Paddle(x-15,y/2)
        self.speed = 5
        self.score = [0,0]
        self.ball = Ball(x/2,y/2)
        self.clock = pygame.time.Clock()
        pass

    def runGame(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.fill((0,0,0))
            self.paddle1.check_bounds(self.screen.get_height())
            self.paddle1.move(self.speed)
            self.paddle1.draw(self.screen)
            self.paddle2.draw(self.screen) 
            self.paddle2.ai_move(self.ball,10) 
            self.paddle1.move(5)
            self.ball.draw(self.screen)
            if self.ball.rect.colliderect(self.paddle1.rect) or self.ball.rect.colliderect(self.paddle2.rect):
                self.ball.bounce('x')
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= self.screen.get_height():
                self.ball.bounce('y')
            score_text = self.font.render(f"lghuy: {self.score[0]} Bot:{self.score[1]}", True, (255,255,255))
            self.screen.blit(score_text, (self.screen.get_width() / 2 - score_text.get_width() / 2,10))
            self.ball.move(10,self)
            self.clock.tick(60)
            pygame.display.flip()


    def reset(self):
        x,y = self.screen.get_size()
        self.paddle1 = Paddle(0,y/2)
        self.paddle2 = Paddle(x-15,y/2)
        self.ball = Ball(x/2,y/2)


myGame = Pingpong()
myGame.runGame()    
            