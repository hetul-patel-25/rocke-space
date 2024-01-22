from typing import Any
import pygame
import random
from pygame.sprite import Group
pygame.init()
screen=pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()
running="True"

player_pos=pygame.Vector2(screen.get_width())
from pygame.locals import(
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_0
)
score=0
running = True
width=screen.get_width()
height=screen.get_height()
bg_image=pygame.image.load('spaceRocket/space.jpg')
bg_image=pygame.transform.scale(bg_image,(width,height))

#bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet,self).__init__()
        self.surf=pygame.Surface((10,20))
        self.surf.fill("black")
        self.rect=self.surf.get_rect()
        self.rect.top=579
    def update(self):
        self.rect.move_ip(0,-12)

#enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.surf=pygame.Surface((20,10))
        self.surf=pygame.image.load("spaceRocket/enemy.jpeg").convert()
        self.surf=pygame.transform.scale(self.surf,(40,40))
        self.rect=self.surf.get_rect()
        self.rect.top=-5
        self.rect.right=random.randint(0,width)
        self.speed=random.randint(1,10)
    
    def update(self):
        self.rect.move_ip(0,self.speed)
        if self.rect.top>height:
            self.kill()

#player
class Player(Bullet,pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player,self).__init__()
        self.surf=pygame.Surface((75,75))
        self.surf=pygame.image.load("spaceRocket/ship.jpg").convert()
        self.surf=pygame.transform.scale(self.surf,(60,60))
        self.surf.set_colorkey((255,255,255),RLEACCEL)
        self.rect=self.surf.get_rect()
        self.rect.top=570
    #for update
    def update(self,pressed_key):
        bullet=Bullet()
        # if pressed_key[K_UP]:
        #     self.rect.move_ip(0,-5) 
        # if pressed_key[K_DOWN]:
        #     self.rect.move_ip(0,5)
        if pressed_key[K_RIGHT]:
            self.rect.move_ip(8,0)
             
        if pressed_key[K_LEFT]:
            self.rect.move_ip(-8,0)


       #keep user in screen
        if self.rect.left<0:
            self.rect.left=0
        if self.rect.right>width:
            self.rect.right=width
        if self.rect.top<0:
            self.rect.top=0
        if self.rect.bottom>height:
            self.rect.bottom=height



#boundry    
class Boundry(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Boundry,self).__init__()
        self.surf=pygame.Surface((width,10))
        self.surf.fill("red")
        self.rect=self.surf.get_rect()
        self.rect.top=620


player=Player()
boundry=Boundry()
ADDENEMY=pygame.USEREVENT+1
ADDBULLET=pygame.USEREVENT+2
pygame.time.set_timer(ADDENEMY,2700)
pygame.time.set_timer(ADDBULLET,500)
enemies=pygame.sprite.Group()
bullets=pygame.sprite.Group()
space=pygame.sprite.Group()
all_sprite=pygame.sprite.Group()
all_sprite.add(player)
all_sprite.add(boundry)
my_font=pygame.font.Font(pygame.font.get_default_font(),36)
text=my_font.render("Score :- ",True,"white")

while running:
    text_point=my_font.render(str(score),True,"white")
    
    srf=pygame.Surface((50,50))
    srf.fill("green")
    rect=srf.get_rect()
    for event in pygame.event.get():
        w=0
        if event.type==KEYDOWN:
            if event.key==K_ESCAPE:
                running=False
        elif event.type==ADDENEMY:
            new_enemy=Enemy()
            enemies.add(new_enemy)
            all_sprite.add(new_enemy)
        # elif event.type==ADDSPACE:
        #     new_space=Space()
        #     space.add(new_space)
        #     all_sprite.add(new_space)
            
        elif event.type==ADDBULLET:
            
            new_bullet=Bullet()
            new_bullet.rect.right=player.rect.right
            new_bullet.rect.left=player.rect.left+20
            new_bullet.update()
            bullets.add(new_bullet)
            all_sprite.add(new_bullet)

        elif event.type==pygame.QUIT:
            running=False
    
    pressed_key=pygame.key.get_pressed()
    player.update(pressed_key)
    enemies.update()
    bullets.update()
    screen.blit(bg_image,(0,0))
    screen.blit(text,(width-200,0))
    
    pygame.display.update()
    for entity in all_sprite:
        screen.blit(entity.surf,entity.rect)
    if pygame.sprite.spritecollideany(player,enemies):
        player.kill()
        running=False
    for enemy in list(enemies):
        for bullet in list(bullets):
            if pygame.sprite.collide_rect(bullet,enemy):
                score=score+10
                
                print(score)
                enemy.kill()
                bullet.kill()
    for enemy in list(enemies):
        if pygame.sprite.collide_rect(enemy,boundry):
            enemy.kill()
    for bullet in list(bullets):
        if bullet.rect.height<0:
            bullet.kill()
    
    screen.blit(text_point,(width-50,0))
    pygame.display.flip()
    clock.tick(60)

    

pygame.quit()
