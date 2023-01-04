import pygame
import neat
import os
#import time
import random
pygame.font.init()
WIN_WEIDTH=600
WIN_HEIGHT=800
Bird_image=[pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\\image\\bird1.jpeg"))),pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\\image\\bird2.jpeg"))),pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\image\\bird3.jpeg")))]
Pipe_image=pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\\image\\pipe.jpeg")))
Ground_image=pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\\image\\ground.jpeg")))
Background_image=pygame.transform.scale2x(pygame.image.load(os.path.join("C:\\Users\\Sankhadip Chowdhury\\OneDrive\\Desktop\\pythone\\Flappy bird game(NEAT)\\image\\background.jpeg")))
START_FONT=pygame.font.SysFont("comicsans",50)
class Bird:
    IMG=Bird_image
    max_rotation=25
    rot_velocity=20
    animation_time=5
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tilt=0
        self.tick_count=0
        self.vel=0
        self.height=self.y
        self.img_count=0
        self.img=self.IMG[0]
    def jump(self):
        self.vel=-10.5
        self.height=self.y
        self.tick_count=0
    def move(self):
        self.tick_count+=1
        d=self.vel*self.tick_count+1.5*self.tick_count**2
        if d>=16:
            d=16
        if d<0:
            d-=2
        self.y=self.y+d
        if d<0 or self.y<self.height+50:
            if self.tilt<self.max_rotation:
                self.tilt=self.max_rotation
        else:
            if self.tilt>-90:
                self.tilt-=self.rot_velocity
    def draw(self,win):
        self.img_count+=1
        if self.img_count<=self.animation_time:
            self.img=self.IMG[0]
        elif self.img_count<=self.animation_time*2:
            self.img=self.IMG[1]
        elif self.img_count<=self.animation_time*3:
            self.img=self.IMG[2]
        elif self.img_count<=self.animation_time*4:
            self.img=self.IMG[1]
        elif self.img_count<=self.animation_time*4 +1:
            self.img=self.IMG[0]
            self.img_count=0
        if self.tilt<=-80:
            self.img=self.IMG[1]
            self.img_count=self.animation_time*2
        # rotated_img=pygame.transform.rotate(self.img,self.tilt)
        # new_rect=rotated_img.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)
        # win.blit(rotated_img,new_rect.topleft)
        blitRotateCenter(win,self.img,(self.x,self.y),self.tilt)
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
class Pipe:
    GAP=200
    vEL=5
    def __init__(self,x):
        self.x=x
        self.height=0
        self.top=0
        self.bottom=0
        self.PIPE_TOP=pygame.transform.flip(Pipe_image,False,True)
        self.PIPE_BOTTOM=Pipe_image
        self.passed=False
        self.set_height()
    def set_height(self):
        self.height=random.randrange(50,450)
        self.top=self.height-self.PIPE_TOP.get_height()
        self.bottom=self.height+self.GAP
    def move(self):
        self.x-=self.vEL
    def collide(self,bird):
        bird_mask=bird.get_mask()
        top_mask=pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask=pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset=(self.x-bird.x,self.top-round(bird.y))
        bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))
        b_point=bird_mask.overlap(bottom_mask,bottom_offset)
        t_point=bird_mask.overlap(top_mask,top_offset)
        if b_point or t_point:
            return True
        return False
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top))
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
        
class Base:
    VEL=5
    WIDTH=Ground_image.get_width()
    IMG=Ground_image
    def __init__(self,y): 
        self.y=y
        self.x1=0
        self.x2=self.WIDTH
    def move(self):
        self.x1-=self.VEL
        self.x2-=self.VEL
        if self.x1+self.WIDTH<0:
            self.x1=self.x2+self.WIDTH
        if self.x2+self.WIDTH<0:
            self.x2=self.x1+self.WIDTH
    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))
def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)
def draw_window(win,birds,base,pipes,score):
    win.blit(Background_image,(0,0))
    for pipe in pipes:
        pipe.draw(win)
    text=START_FONT.render("Score : "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WEIDTH-15-text.get_width(),10))
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
def main(genomes, config):
    nets=[]
    ge=[]
    birds=[]
    for _,g in genomes:
        g.fitness=0
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(g)
    base=Base(700)
    pipes=[Pipe(700)]
    win=pygame.display.set_mode((WIN_WEIDTH,WIN_HEIGHT))
    run=True
    score=0
    clock=pygame.time.Clock()
    while run and len(birds)>0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                quit()
        pipe_ind=0
        if len(birds)>0:
            if len(pipes)>1 and birds[0].x>pipes[0].x+pipes[0].PIPE_TOP.get_width():
                pipe_ind=1
        else:
            run=False
            break
        for x,bird in enumerate(birds):
            ge[x].fitness+=0.1
            bird.move()
            output=nets[x].activate((bird.y,abs(bird.y-pipes[pipe_ind].height),abs(bird.y-pipes[pipe_ind].bottom)))
            if output[0]>0.6:
                bird.jump() 
        base.move()
        add_pipe=False
        rem=[]
        for pipe in pipes:
            pipe.move()
            for bird in birds:
                if pipe.collide(bird):
                    ge[birds.index(bird)].fitness-=1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                   
            if pipe.x+pipe.PIPE_TOP.get_width()<0:
                rem.append(pipe)
            if not pipe.passed and pipe.x<bird.x:
                    pipe.passed=True
                    add_pipe=True
        if add_pipe:
            score+=1
            for g in ge:
                g.fitness+=5
            pipes.append(Pipe(WIN_WEIDTH))
        for r in rem:
            pipes.remove(r)
        for bird in birds:
            if bird.y+bird.img.get_height()-10>=700 or bird.y<-50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))
                
        draw_window(win,birds,base,pipes,score)
    
def run(config_file):
    config=neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_file)
    p=neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats=neat.StatisticsReporter()
    p.add_reporter(stats)
    winner=p.run(main,20)

if __name__ == '__main__':
    locals_dir=os.path.dirname(__file__)
    config_path=os.path.join(locals_dir,'config.txt')
    run(config_path) 