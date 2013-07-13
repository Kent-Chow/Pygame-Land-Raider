"""
Author: Kent Chow
Date: June 6, 2012
Description: This is the module for sprites.
"""
import pygame, math, random

class Player(pygame.sprite.Sprite):   
    """This class defines the sprite for the player."""
    def __init__(self, screen):
        """This initializer takes a screen surface as a parameter, initializes
        the image and rect attributes, and x, y direction of the player."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the player.
        self.image = pygame.image.load("./pictures/player/land_raider_base.gif")
        self.image.set_colorkey((255,0,255))    
        self.image = self.image.convert() 
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height() - 75)
        
        # Save the screen and set the speed of player
        self.__screen = screen
        self.__dx = 7
        
    def change_direction(self, right_direction):
        """This method takes one parameter, and moves the player's rect to
        either left or right, based on the inputted value."""
        # Save a copy of old x, y coordinate
        self.__centerx_copy = self.rect.centerx
        # If True, move rect right, else move rect left
        if right_direction:
            self.rect.centerx += self.__dx
        else:
            self.rect.centerx += -self.__dx
        # If rect is offscreen, assign back to old rect
        if self.rect.left < -self.__dx or self.rect.right > self.__screen.get_width() + self.__dx:
            self.rect.centerx = self.__centerx_copy
            
class Terrain(pygame.sprite.Sprite):  
    """This class defines the sprite for the terrain."""
    def __init__(self, screen, image, speed):
        """This initializer takes a screen surface, image name, and value
        of speed as parameters. Initializes the image and rect attributes, 
        and x, y coordinates of the terrain."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the terrain.
        self.image = pygame.image.load(image)
        self.image = self.image.convert() 
        self.rect = self.image.get_rect() 
        self.rect.left = 0
        self.rect.bottom = screen.get_height()
        
        # Save the screen and store the speed of terrain
        self.__dx = speed
        self.__screen = screen
        
    def set_speed(self, amount):
        """This method takes the amount of speed as parameters and stores it
        in a variable."""
        self.__dx = amount
        
        
    def update(self):
        """This method will be called automatically to reposition the
        terrain on the screen."""    
        # If image reaches to its right, move image to start back at left
        if self.rect.right < self.__screen.get_width() + self.__dx:
            self.rect.left = 0
        else:
            self.rect.left -= self.__dx
            
class Gun(pygame.sprite.Sprite):
    """This class defines the sprite for the guns."""
    def __init__(self, screen, image, x, y, angle):
        """This initializer takes a screen surface, image name, and value
        of x and y and an angle as parameters. Initializes the image and rect 
        attributes, angle, and x and y coordinates of the gun sprite."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the terrain.
        self.image = pygame.image.load(image)
        self.image = self.image.convert() 
        self.image.set_colorkey((255,0,255))
        self.image = pygame.transform.rotate(self.image, angle)              
        self.rect = self.image.get_rect() 
        
        # Store copy of image, x and y coordinates, and angle of gun
        self.__image_copy = self.image
        self.__x = x
        self.__y = y
        self.__angle = angle
        
    def adjust_xy(self, x, y):
        """This method adjusts the x and y coordinates of the gun by assigning
        them the values inputting through the x and y parameters."""
        self.__x = x
        self.__y = y
        
    def change_angle(self, higher):
        """This method accepts either True or False value as a parameter. If
        True, it increases the angle of the image and transforms it. If False,
        it decreases the angle of the image, and transforms it."""
        # Save the old rect of image
        self.__old_rect = self.image.get_rect()
        # Change the angle of the image
        if higher:
            self.__angle += 1
        else:
            self.__angle -= 1
        # Transform the image based on angle
        self.image = pygame.transform.rotate(self.__image_copy, self.__angle)
        # Set rect back to original
        self.rect = self.__old_rect
        
    def get_angle(self):
        """This method accepts no parameters, and returns the value of angle."""
        return self.__angle
            
    def update(self):
        """This method will be called automatically to reposition the
        gun on the screen."""   
        self.rect.center = (self.__x, self.__y)
        
class Bullet(pygame.sprite.Sprite):
    """This class defines the sprite for the bullets."""
    def __init__(self, image, x, y, angle, speed, screen, damage, points, death, frames, health = 0):
        """This initializer takes a screen surface, image name, values for
        speed, angle, x, y, points, death images, frames, and health as parameters. 
        Initializes the image and rect  attributes, angle, and x and y coordinates 
        of the bullet sprite."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the terrain.
        self.image = pygame.image.load(image)
        self.image.set_colorkey((255,0,255))
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = self.image.convert()         
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y)
        
        # Store x and y location of sprite
        self.__x = x
        self.__y = y
        
        # Store speed of sprite
        self.__speed = speed
        
        # Store information for death of sprite
        self.__points = points
        self.__death = death
        self.__frames = frames
        self.__damage = damage
        self.__health = health
        
        # Store the screen
        self.__screen = screen
       
        # Calculate the direction of x and y bullet is travelling
        self.__dx = math.cos(float(angle) / 180 * math.pi)
        self.__dy = math.sin(float(angle) / 180 * math.pi)
        
        # Track if bullet is exploding
        self.__exploding = False
        
    def is_exploding(self):
        """This method accepts no parameters, and returns whether sprite is 
        exploding."""
        return self.__exploding
    
    def get_damage(self):
        """This method accepts no parameters, and returns the value of damage."""
        return self.__damage
    
    def get_points(self):
        """This method accepts no parameters, and returns the value of sprite's
        points."""
        return self.__points
    
    def get_death(self):
        """This method accepts no parameters, and returns the pathname for 
        sprite's death image."""
        return self.__death
    
    def get_frames(self):
        """This method accepts no parameters, and returns the amount of 
        frames in death animation."""
        return self.__frames
        
    def set_health(self):
        """This method accepts no parameters. It decreases the bullet's health
        by 1 and kills it if it reaches below 0."""
        self.__health -= 1
        if self.__health < 0:
            self.kill()
                    
    def update(self):
        """This method will be called automatically to reposition the
        bullet on the screen.""" 
        # Move rect of bullet
        self.__x += self.__dx * self.__speed
        self.__y -= self.__dy * self.__speed
        self.rect.center = (self.__x, self.__y)
        # If bullet offscreen, kill sprite
        if self.rect.centerx < - 125 or self.rect.centerx > self.__screen.get_width() + 125 or self.rect.centery < 0:
            self.kill()
        # If bullet hits the ground, explode sprite
        elif self.rect.centery > self.__screen.get_height() - 50:
            self.__exploding = True
            
class Missile(pygame.sprite.Sprite):
    """This class defines the sprite for the missiles."""
    def __init__(self, screen, image, angle, speed, x, y, px, py, damage, points, death, frames):
        """This initializer takes a screen surface, image name, values for
        speed, angle, x, y, points, death images, frames, and health as parameters. 
        Initializes the image and rect  attributes, angle, and x and y coordinates 
        of the missile sprite."""
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the terrain.
        self.image = pygame.image.load(image)
        self.image.set_colorkey((255,0,255))
        self.__image_copy = self.image     
        # Change the angle of the image
        self.change_angle(angle)
        self.image = self.image.convert()                
        self.rect.center = (x, y)
             
        # Define the missile's location, speed, and direction
        self.__x = x
        self.__y = y
        self.__speed = speed      
        self.__dx = math.cos(float(angle) / 180 * math.pi)
        self.__dy = math.sin(float(angle) / 180 * math.pi)
        
        # Set missile life
        self.__init_time = pygame.time.get_ticks()
        self.__exploding = False
        
        # Set death and damage
        self.__points = points
        self.__death = death
        self.__frames = frames
        self.__damage = damage
        
        # Save the screen
        self.__screen = screen
        
    def is_exploding(self):
        """This method accepts no parameters, and returns whether sprite is 
        exploding."""
        return self.__exploding
    
    def get_damage(self):
        """This method accepts no parameters, and returns the value of damage."""
        return self.__damage
    
    def get_points(self):
        """This method accepts no parameters, and returns the value of sprite's
        points."""
        return self.__points
    
    def get_death(self):
        """This method accepts no parameters, and returns the pathname for 
        sprite's death image."""
        return self.__death
    
    def get_frames(self):
        """This method accepts no parameters, and returns the amount of 
        frames in death animation."""
        return self.__frames
              
    def change_angle(self, angle):
        """This method accepts an angle as a parameter. It transforms the 
        sprite's image according to angle."""
        self.__old_rect = self.image.get_rect()
        self.image = pygame.transform.rotate(self.__image_copy, angle)
        self.rect = self.__old_rect
               
    def store_player_xy(self, x, y):
        """This method accepts the player's x and y coordinates as parameters
        and stores them."""
        self.__player_x = x
        self.__player_y = y
        
    def find_direction(self, px, py, x, y):
        """This method accepts the player's coordinates and missile's
        coordinates as parameters. It calculates the angle the missile must 
        travel to reach player."""
        # Find distance between player and missile
        # Calculate angle using cos, uses distance from the ground and
        # distance from player.
        self.__distance = math.sqrt((float(x) - px)**2 + (float(py) - y)**2)
        self.__angle = math.acos((py - y)/self.__distance) * 180 / math.pi 
        if px < x:
            self.__angle = -90 - self.__angle
        elif px > x:
            self.__angle = -90 + self.__angle
        else: self.__angle = -90
        # Sets the new path for missile
        self.__dx = math.cos(float(self.__angle) / 180 * math.pi)
        self.__dy = math.sin(float(self.__angle) / 180 * math.pi)
                                                                            
    def update(self):
        """This method will be called automatically to reposition the
        missile on the screen.""" 
        # Times when missile should die off
        if pygame.time.get_ticks() - self.__init_time > 2800:
            self.__dx = 0
            self.__dy = -1
        # If missile has time, find angle between player, and move rect
        else:  
            self.find_direction(self.__player_x, self.__player_y, self.__x, self.__y)    
            self.change_angle(self.__angle)    
        self.__x += self.__dx * self.__speed
        self.__y -= self.__dy * self.__speed  
        self.rect.center = (self.__x, self.__y)
        # If missile offscreen, kill sprite
        if self.rect.centerx < - 125 or self.rect.centerx > self.__screen.get_width() + 125:
            self.kill()
        elif self.rect.centery > self.__screen.get_height() - 50:
            self.__exploding = True     
            
                       
class Enemy(pygame.sprite.Sprite):
    """This class defines the sprite for all the enemies."""
    def __init__(self, screen, img, spd, hp, ammo, cooldown, bulletimg, bulletspd, \
                 bulletangle, points, bulletdmg, bulletpoints, bulletdeath, bulletframes):
        """This initializer takes a screen surface, image name, values for
        speed, angle, x, y, points, death images, frames, health, and 
        values of its bullets as parameters. Initializes the image and rect 
        attributes, x and y coordinates, direction, shooting states, and ammo 
        for the enemy sprite."""       
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Define the image attributes for the enemy.
        self.image = pygame.image.load(img)
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()         
        self.rect = self.image.get_rect()
       
        # Save the screen
        self.screen = screen
        
        # Set random altitude and direction
        self.direction = random.randrange(-1, 2)
        while self.direction == 0:
            self.direction = random.randrange(-1, 2)
             
        if self.direction < 0:
            self.x = self.screen.get_width() + 100
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.x = -100           
        self.y = random.randrange(92, 226)
        
        # Set speed, health, ammo, cooldown and points
        self.speed = spd
        self.health = hp
        self.ammo = ammo
        self.init_time = 0
        self.cooldown = cooldown
        self.points = points
        
        # Set gun and bullet information, track if sprite is shooting
        self.shooting = False
        self.bullet_image = bulletimg
        self.bullet_speed = bulletspd
        self.bullet_angle = bulletangle
        self.bullet_death = bulletdeath
        self.bullet_frames = bulletframes
        self.bullet_points = bulletpoints
        self.bullet_damage = bulletdmg
        
    def store_player_xy(self, x, y):
        """This method accepts players coordinates a parameters and stores 
        them."""
        self.player_x = x
        self.player_y = y
        
    def is_shooting(self):
        """This method accepts no parameters, and returns whether sprite is 
        shooting."""
        return self.shooting
    
    def get_bullet(self):
        """This method accepts no parameters, and returns the bullet 
        information for sprite."""
        self.ammo -= 1
        self.shooting = False
        return Bullet(self.bullet_image, self.rect.centerx, self.rect.centery, self.bullet_angle, \
                      self.bullet_speed, self.screen, self.bullet_damage, self.bullet_points, self.bullet_death, self.bullet_frames)     
    
    def get_points(self):
        """This method accepts no parameters, and returns the points from
        sprite."""
        return self.points
    
    def take_damage(self, amount):
        """This method accepts the amount of damage as parameters, and 
        subtracts it off the health of sprite."""
        self.health -= amount
        
    def get_health(self):
        """This method accepts no parameters, and returns value of health
        for sprite."""
        return self.health
                
class Enemy_Jet(Enemy):
    """This class defines the sprite for the enemy jets."""
    def __init__(self, screen):
        """This initializer takes a screen surface as parameters. Initializes
        the Enemy class."""
        Enemy.__init__(self, screen,"./pictures/enemies/enemy_jet.gif",10,10,1,\
                       0,"./pictures/bullet/bomb.gif",5,-90, 200, 30, 20,"drop",23)
                        
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen.""" 
        #MOVE SPRITE
        self.x += (self.direction * self.speed)
        self.rect.center = (self.x, self.y)
        
        #CHECK SHOOTING
        if self.rect.centerx > self.player_x - 25 and self.rect.centerx < \
           self.player_x + 25 and self.ammo > 0:
            #Adjust shooting based on cooldown
            if (pygame.time.get_ticks() - self.init_time) > self.cooldown:
                self.shooting = True
                self.init_time = pygame.time.get_ticks()
         
        #CHECK IF SPRITE OFFSCREEN
        if self.rect.centerx > self.screen.get_width() + 100 or self.rect.centerx < -100:
            self.kill()
            
class Enemy_Chopper(Enemy):
    """This class defines the sprite for the enemy choppers."""
    def __init__(self, screen):
        """This initializer takes a screen surface as parameters. Initializes
        the Enemy class. Sets angle based on direction of sprite."""
        Enemy.__init__(self, screen,"./pictures/enemies/enemy_chopper.gif",\
                       6,50,5,40,"./pictures/bullet/bullet.gif",7,0, 100, 1,5,"bullet",5)
        
        # Adjust the angle of bullets based on direction
        if self.direction == 1:
            self.bullet_angle = -45
        else:
            self.bullet_angle = 225
       
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen.""" 
        #MOVE SPRITE
        self.x += (self.direction * self.speed)
        self.rect.center = (self.x, self.y)
        
        #CHECK SHOOTING
        if self.rect.centerx > self.player_x - 300 and self.rect.centerx < \
           self.player_x + 300 and self.ammo > 0:
            #Adjust shooting based on cooldown
            if (pygame.time.get_ticks() - self.init_time) > self.cooldown:
                self.shooting = True
                self.init_time = pygame.time.get_ticks()
         
        #CHECK IF SPRITE OFFSCREEN
        if self.rect.centerx > self.screen.get_width() + 100 or self.rect.centerx < -100:
            self.kill()
            
class Enemy_Hover_Chopper(Enemy):
    """This class defines the sprite for the enemy hovering choppers."""
    def __init__(self, screen):        
        """This initializer takes a screen surface as parameters. Initializes
        the Enemy class."""
        Enemy.__init__(self, screen,"./pictures/enemies/enemy_hover_chopper.gif",\
                       7,100,15,40,"./pictures/bullet/bullet.gif",7,0, 250,2,5,"bullet",5)
        
        # Adjust the angle of bullets based on direction
        if self.direction == -1:
            self.bullet_angle = 360
        else:
            self.bullet_angle = 180       
    
    def get_bullet(self):
        """This method accepts no parameters and returns the bullet 
        information from sprite.""" 
        self.ammo -= 1
        self.bullet_angle += 10 * self.direction
        if self.ammo < 0:
            self.shooting = False
        return Bullet(self.bullet_image, self.rect.centerx, self.rect.centery, self.bullet_angle, \
                      self.bullet_speed, self.screen, self.bullet_damage, self.bullet_points, self.bullet_death, self.bullet_frames)     
           
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen.""" 
        #MOVE SPRITE
        if self.shooting == True:
            self.rect.center = (self.x, self.y)
        else:
            self.x += (self.direction * self.speed)
            self.rect.center = (self.x, self.y)
        
        #CHECK SHOOTING
        if self.rect.centerx < self.player_x + 10 and self.rect.centerx > self.player_x - 10 and self.ammo > 0:
            self.shooting = True
         
        #CHECK IF SPRITE OFFSCREEN
        if self.rect.centerx > self.screen.get_width() + 100 or self.rect.centerx < -100:                     
            self.kill() 
            
class Enemy_Helicopter(Enemy):
    """This class defines the sprite for the enemy helicopters."""
    def __init__(self, screen):  
        """This initializer takes a screen surface as parameters. Initializes
        the Enemy class."""
        Enemy.__init__(self, screen,"./pictures/enemies/enemy_helicopter.gif",\
                       5,80,2,500,"./pictures/bullet/homing_missile.gif",5,-90, 300,20,10,"bomb",21)
                 
    def get_bullet(self):
        """This method accepts no parameters and returns the bullet 
        information from sprite.""" 
        self.ammo -= 1
        self.shooting = False
        if self.ammo % 2 == 0:
            self.__adjust = 15
        else:
            self.__adjust = -15
        return Missile(self.screen, self.bullet_image, self.bullet_angle, \
                       self.bullet_speed, self.rect.centerx + self.__adjust, \
                       self.rect.centery, self.player_x, self.player_y,\
                       self.bullet_damage, self.bullet_points, self.bullet_death, self.bullet_frames) 
        
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen.""" 
        #MOVE SPRITE
        # Pause sprite if shooting, else continue moving
        if self.shooting == True or pygame.time.get_ticks() - self.init_time < 1000:
            self.rect.center = (self.x, self.y)
        else:
            self.x += (self.direction * self.speed)
            self.rect.center = (self.x, self.y)
        
        #CHECK SHOOTING
        if self.rect.centerx < self.player_x + 10 and self.rect.centerx > self.player_x - 10 and self.ammo > 0:
            if (pygame.time.get_ticks() - self.init_time) > self.cooldown:
                self.shooting = True
                self.init_time = pygame.time.get_ticks()
                
        #CHECK IF SPRITE OFFSCREEN
        if self.rect.centerx > self.screen.get_width() + 100 or self.rect.centerx < -100:                     
            self.kill() 
            
class Enemy_Gunner(Enemy):
    """This class defines the sprite for the enemy gunners."""
    def __init__(self, screen):       
        """This initializer takes a screen surface as parameters. Initializes
        the Enemy class."""
        Enemy.__init__(self, screen,"./pictures/enemies/enemy_gunner.gif",\
                       6,100,5,100,"./pictures/bullet/bullet.gif",10,0, 600,1,5,"bullet",5)
                
    def find_direction(self, px, py, x, y):
        """This method accepts the player's coordinates and missile's
        coordinates as parameters. It calculates the angle the missile must 
        travel to reach player."""
        # Find distance between player and sprite
        # Calculate angle using cos, uses distance from the ground and
        # distance from player.
        # Add random factor to shots
        self.__rand_factor = random.randrange(-1,2)
        self.__rand_factor *= random.random() * 5
        self.__distance = math.sqrt((float(x) - px)**2 + (float(py) - y)**2)
        self.bullet_angle = (math.acos((py - y)/self.__distance) * 180 / math.pi) + self.__rand_factor
        if px < x:
            self.bullet_angle = -90 - self.bullet_angle
        elif px > x:
            self.bullet_angle = -90 + self.bullet_angle
        else: self.bullet_angle = -90
                 
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen.""" 
        #MOVE SPRITE
        # Find direction of player
        self.find_direction(self.player_x, self.player_y, self.x, self.y)
        # Pause sprite if shooting, else continue moving
        if self.shooting == True or pygame.time.get_ticks() - self.init_time < 1000:           
            self.rect.center = (self.x, self.y)
        else:
            self.x += (self.direction * self.speed)
            self.rect.center = (self.x, self.y)
        
        #CHECK SHOOTING
        if self.rect.centerx > 50 and self.rect.centerx < self.screen.get_width() - 50 and self.ammo > 0:
            if (pygame.time.get_ticks() - self.init_time) > self.cooldown:
                self.shooting = True
                self.init_time = pygame.time.get_ticks()
                
        #CHECK IF SPRITE OFFSCREEN
        if self.rect.centerx > self.screen.get_width() + 100 or self.rect.centerx < -100:                     
            self.kill()   
         
class Explosion(pygame.sprite.Sprite):
    """This class defines the sprite for explosions."""
    def __init__(self, image, number, x, y):
        """This initializer takes a image name, number of frames
        and x and y locations as parameters. Initializes the rect and image
        attributes and store the number of frames for explosion."""       
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Load first frame and set attributes for rect
        self.image = pygame.image.load("./pictures/explosion/"+image+"1.gif").convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        
        #Store number of images and pathname
        self.__image = "./pictures/explosion/"+image
        self.__frame = 1
        self.__number = number

            
    def update(self):
        """This method will be called automatically to reposition the
        sprite on the screen and change explosion's image.""" 
        self.__frame += 1
        if self.__frame < self.__number:
            self.image = pygame.image.load(self.__image + str(self.__frame)+".gif")
            self.image = self.image.convert()
        else:
            self.kill()
            
class StatsKeeper(pygame.sprite.Sprite): 
    """This class defines the sprite for keeping statistics."""
    def __init__(self): 
        """This initializer takes no parameters. Initializes the amount of 
        score, distance, health, armour, and ammo for the player. Also
        intializes font, and tracks state of the game."""
        # Call the parent __init__() method 
        pygame.sprite.Sprite.__init__(self) 
  
        # Load our custom font and background
        self.__font = pygame.font.Font("./fonts/digital.TTF", 20)
                
        # Set starting game statistics
        self.__score = 0
        self.__distance = 100
        self.__health = 100
        self.__armour = 100
        self.__turret = 300
        self.__win = False
        self.__lose = False
                       
    def set_statistics(self, score = 0, distance = 0, armour = 0):
        """This method accepts either score, distance or armour
        as parameters and adjust each values accordingly.""" 
        self.__score += score
        self.__distance += distance
        self.__armour += armour
        
    def take_damage(self, amount):
        """This method accepts value of damage as parameters
        and adjust value accordingly.""" 
        self.__armour -= amount
        if self.__armour < 0:
            amount = 0 - self.__armour
            self.__armour = 0
            self.__health -= amount
            if self.__health < 1:
                self.__health = 0
            
    def get_armour(self):
        """This method accepts no parameters and returns the value of
        armour."""
        return self.__armour
    
    def get_distance(self):
        """This method accepts no parameters and returns the value of
        distance."""
        return self.__distance
    
    def get_health(self):
        """This method accepts no parameters and returns the value of
        health."""
        return self.__health
    
    def get_score(self):
        """This method accepts no parameters and returns the value of
        score."""
        return self.__score
    
    def get_turret(self):
        """This method accepts no parameters and returns the value of
        turret."""
        return self.__turret
    
    def set_turret(self, amount):
        """This method accepts an amount as a parameter. It decreases
        the value of turret ammo."""
        self.__turret += amount
                                                       
    def update(self): 
        """This method will be called automatically to display  
        the current statistics at top of window."""       
        #Create new statskeeper image
        self.image = pygame.image.load("./pictures/background/HUD.gif")
        self.image.set_colorkey((255,0,255))
        self.image = self.image.convert() 
        self.rect = self.image.get_rect() 
        self.rect.left = 0
        self.rect.top = 0 
        
        #Blit the messages
        message = self.__font.render("Score: %i" % (self.__score),1,(0,255,0))
        message2 = self.__font.render("Distance: " + str(self.__distance) + "KM",1,(0,255,0))
        message3 = self.__font.render("Health: " + str(self.__health) + "%",1,(0,255,0))
        message4 = self.__font.render("Armour: " + str(self.__armour) + "%",1,(0,255,0))
        message5 = self.__font.render("Turret: " + str(self.__turret),1,(0,255,0))
        self.image.blit(message,(20,10))
        self.image.blit(message2,(200,10))
        self.image.blit(message3, (360,10))
        self.image.blit(message4, (500,10))   
        self.image.blit(message5, (630,10))  