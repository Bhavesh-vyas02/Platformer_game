import pygame
from pygame.locals import *  # noqa - this is a hack to make pylint ignore the unused import
import pickle
from os import path

pygame.init()  # Initialize pygame

clock = pygame.time.Clock()
fps = 60

# Set up the display 
screen_width = 980 # width of screen for screen resolution display
screen_height = 700 # Screen height for screen resolution display

screen = pygame.display.set_mode((screen_width, screen_height))  # Screen to display with screen resolution display
pygame.display.set_caption('platformer')  # Display title for platformer

# define game variables
tile_size = 35
game_over = 0
main_menu = True
level = 1

# load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# def draw_grid():
#     for line in range(0,30):
#         pygame.draw.line(screen, (255, 255, 255),(0, line*tile_size), (screen_width, line*tile_size))
#         pygame.draw.line(screen, (255, 255, 255),(line*tile_size, 0), (line*tile_size, screen_height))


class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw(self):
        
        action = False
        
    #get mouse position
        pos = pygame.mouse.get_pos()
        
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1  and self.clicked == False:
                action = True
                self.clicked = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        # draw button
        screen.blit(self.image, self.rect)
        
        return action

class player():
    def __init__(self, x ,y):
        self.reset(x ,y)
        
    def update(self,game_over):
        dx=0
        dy=0
        walk_cooldown = 5
        
        if game_over == 0:
            # get key presses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter +=1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter +=1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            
            # handaling animation
            
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            
            
            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
                
            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx=0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0: 
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0      
                        self.in_air =False 
            #check for collision with enemise 
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over =-1 
            
            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over =-1 

            # update plyare coordinates
            self.rect.x += dx
            self.rect.y += dy
        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5
        # draw player onto screen
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        return game_over
    
    def reset(self ,x ,y): 
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right=pygame.image.load(f'img/guy{num}.png')
            img_right = pygame.transform.scale(img_right,(30,60))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)   
            self.images_left.append(img_left)   
            self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class world():
    def __init__(self, data):
        self.tile_list=[]
        dirt_img = pygame.image.load('img/dirt.png')
        grass_img = pygame.image.load('img/grass.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile==1:
                    img=pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile==2:
                    img=pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size -50, row_count * tile_size)
                    blob_group.add(blob)
                    
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                    if tile == 8:
                        exit = Exit(col_count * tile_size, row_count * tile_size)
                        exit_group.add(exit)
                col_count += 1
            row_count +=1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255,255,255), tile[1] ,2)

# Adding enimies
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter >= 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2)) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)) ) 
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



player = player(70, screen_height - 95)
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# load in level data and create world
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = world(world_data)

# create button
restart_button =  Button(screen_width // 2 - 50, screen_height // 2 - 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2 , start_img)
exit_button = Button(screen_width // 2  + 150, screen_height // 2 , exit_img)

run = True # run is a boolean variable that is used to control the main game loop
while run:
    
    clock.tick(fps)
    
    screen.blit(bg_img, (0, 0)) # blit background
    screen.blit(sun_img, (100, 100)) # blit sun 
    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()
    
        if game_over == 0:
            blob_group.update()
    
        blob_group.draw(screen)
        lava_group.draw(screen)
    
        game_over=player.update(game_over)
    
    # if player died
    if game_over == -1:
        if restart_button.draw():
            player.reset(70, screen_height - 95)
            game_over = 0
            
    
    # draw_grid()
    
    for event in pygame.event.get(): # event is a pygame. graphics.
        if event.type == pygame.QUIT:    # quit event is a pygame. graphics.
            run = False # run is a boolean variable that is used to control the main game loop
    pygame.display.update() # update the display window

pygame.quit()