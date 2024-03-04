import pygame
import pickle
from os import path

pygame.init()

clock = pygame.time.Clock()
fps = 60

#create display window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('UPE Project - Danny George')

#game variables
tile_size = 50
game_over = 0
main_menu = True
keyCollected = False

#load images
sun_img = pygame.image.load('sun.png')
sky_img = pygame.image.load('sky.jpg')
restartbutton_img = pygame.image.load('restartbutton.png')
startbutton_img = pygame.image.load('startbutton.png')
hardbutton_img = pygame.image.load('hardbutton.png')
exitbutton_img = pygame.image.load('exitbutton.png')
title_img = pygame.image.load('gametitle.png')
success_img = pygame.image.load('success.png')

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)

        return action

class Player():
    def __init__(self, x, y):
        self.reset(x, y)
    
    def update(self, game_over):
        dx = 0
        dy = 0

        if game_over == 0:
            #get keypresses
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) and self.jumped == False and self.groundContact == True:
                self.vel_y = -15
                self.jumped = True
                self.groundContact = False
            if (key[pygame.K_SPACE] or key[pygame.K_UP]) == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
            if key[pygame.K_RIGHT]:
                dx += 5

            #add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            #check for collision
            for tile in world.tile_list:

                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0


                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.groundContact = True
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom

            #check for enemy collision
            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
            #check for exit collision
            if pygame.sprite.spritecollide(self, exit_group, False) and keyCollected:
                game_over = 1

            #update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.rect.y += 5


        #draws player onto screen
        screen.blit(self.image, self.rect)

        return game_over
    
    def reset(self, x, y):
        img = pygame.image.load('player.png')
        self.image = pygame.transform.scale(img, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.groundContact = False
        keyCollected = False

class World():
    def __init__(self, data):
        self.tile_list = []
        
        #load images
        dirt_img = pygame.image.load('dirt.jpg')
        grass_img = pygame.image.load('grass.jpg')
        wood_img = pygame.image.load('wood.png')


        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(wood_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    enemy = Enemy(col_count * tile_size, row_count * tile_size)
                    enemy_group.add(enemy)
                if tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size)
                    exit_group.add(exit)
                if tile == 6:
                    key = Key(col_count * tile_size, row_count * tile_size)
                    key_group.add(key)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('bathtub.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('soap.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    

player = Player(100, SCREEN_HEIGHT - 210)
enemy_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()



world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 0, 0, 0],
    [2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2]
    ]

world = World(world_data)

#create buttons
restart_button = Button(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 130, restartbutton_img)
exit_button = Button(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2, exitbutton_img)
quit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, exitbutton_img)
start_button = Button(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2, startbutton_img)

#game loop
run = True
while run:

    clock.tick(fps)

    screen.blit(sky_img, (0, 0))

    if main_menu == True:
        screen.blit(title_img, (10, 50))
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        world.draw()
        screen.blit(sun_img, (100, 100))

        if game_over == 0:
            enemy_group.update()
            #check if bomb collected
            if pygame.sprite.spritecollide(player, key_group, True):
                keyCollected = True
        enemy_group.draw(screen)
        exit_group.draw(screen)
        key_group.draw(screen)

        game_over = player.update(game_over)

        #if player has died
        if game_over == -1:
            if restart_button.draw():
                player.reset(100, SCREEN_HEIGHT - 210)
                game_over = 0
        #if player has succeeded
        if game_over == 1:
            screen.blit(success_img, (50, 50))
            if quit_button.draw():
                run = False
                

    #event handler
    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
