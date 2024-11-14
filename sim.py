import os
import json
import random
import pygame

#def check_hs(new_score : int):
#    with open('high_score.json','r+') as log:
#        score = json.load(log)
#        if score_val < new_score:
#            score['s'] = new_score
#        json.update(score,log)
#        return 0

#check_hs(50)

pygame.init()

WID = 852
HGT = 480

BLACK = (0,0,0)
WHITE = (255,255,255)

IsRunning = True

#display[window]
screen = pygame.display.set_mode((WID,HGT))

#Background
bg = pygame.image.load("bg.jpg")

#images
bus = pygame.image.load('bus.png')
bus = pygame.transform.scale(bus, (50, 90))

rio_image = pygame.image.load('rio.png')
rio_image = pygame.transform.scale(rio_image,(70,90))   #SCALING THE PICTURE [RIO]

font = pygame.font.Font(None, 36)
score_txt = font.render("Score: 0", True, WHITE)

#player

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bus
        self.rect = self.image.get_rect()
        self.rect.center = (WID // 2, HGT - 80)
        self.speed = 1

    def update(self,dx):
        #self.rect.x += float(dx * self.speed)
        self.rect.x += float(dx)

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WID:
            self.rect.right = WID


class FallingObject(pygame.sprite.Sprite):
    def __init__(self,x,speed = 0.51):
        super().__init__()
        self.image = rio_image
        self.speed = speed  #rios pseed
        self.rect = self.image.get_rect()
        self.rect.center = (x,0)  #position of rio

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HGT:
            self.kill()

player = Player()

falling_objects = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

score = 0
current_row = 0
skp_row = 0



#main game loop

while IsRunning:

    screen.blit(bg,(0,0))



    #actual kovement
    dx = 0
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        dx -= 0.7
    if keys[pygame.K_RIGHT]:
        dx += 0.7

    player.update(dx)

    #all_sprites.update() -->wtf

    for sprite in all_sprites:
        if isinstance(sprite,FallingObject):
            sprite.update()

    collid  = pygame.sprite.spritecollide(player,falling_objects,True)
    for thing in collid:
        score += 5

    screen.blit(player.image, player.rect)

    if random.random() < 0.005: #chances
        if skp_row < 1:
            x_position = random.randint(0, WID - 30)
            falling_object = FallingObject(x_position)
            falling_objects.add(falling_object)
            all_sprites.add(falling_object)
            skp_row += 1
        else:
            skp_row -= 1   

    falling_objects.draw(screen) #prints rio

    score_display = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_display, (10, 10))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            IsRunning = False
            break
        


pygame.quit()