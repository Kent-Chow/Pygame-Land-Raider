"""
Author: Kent Chow
Date: June 6, 2012
Description: This is the main file for the game.

Game Description:  Land Raider is a single player, side scrolling game. 
The player controls a tank called the “Land Raider”, and is equipped with 
armour, and weapons. The tank can be controlled using the arrow keys, and 
the weapons can be controlled using the A, and D keys. The Space Bar can 
be used to fire weapons and the C key can be used to change the missile types. 
As the game begins, the player is set on a journey and must fend off aerial 
attacks from airplanes, and missiles. The goal of the game is to survive 
and reach the end of the level. The time it takes for the player to finish 
the game is determined by a set distance from start to finish. The distance 
slowly drops as they keep playing. They lose if the tank runs out of health. 
It is not necessary to destroy any of the enemies, but points can be scored 
if done. 

Implementations: 
- Added player sprite. Stays on screen, and can be controlled by the user 
using the keyboard
- Moving background images
- Gun sprites that can change angle and follow player
- Shooting functionality, allows changing of angle in bullets
- Multiple enemy sprites with different behaviours
- Includes statskeeper to track statistics
- Explosion and shooting sounds
- Main menu

"""
# I - IMPORT AND INITIALIZE
import pygame, sprites, random
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))

def game():
    """This is the main-line logic for the Land Raider game. It accepts no 
    variables and returns nothing."""
    # ENTITIES
    background = pygame.Surface(screen.get_size()) 
    background.fill((255, 255, 255)) 
    screen.blit(background, (0, 0))
    
    #LOAD MUSIC
    pygame.mixer.music.load("./music/Two Steps From Hell - Invincible.wav")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    
    #LOAD ALL SOUND EFFECTS AND SET VOLUME
    explosion_sound = []
    death_sound = pygame.mixer.Sound("./sound/explosions/death.wav")    
    hit_sound = pygame.mixer.Sound("./sound/explosions/explosion5.wav")
    plasma_sound = pygame.mixer.Sound("./sound/shots/plasma_shot.wav")
    turret_sound = pygame.mixer.Sound("./sound/shots/turret_shot.wav")
    for i in range(5):
        explosion_sound.append(pygame.mixer.Sound("./sound/explosions/explosion"+str(i+1)+".wav"))
        explosion_sound[i].set_volume(0.2)
        
    plasma_sound.set_volume(0.05)
    hit_sound.set_volume(0.1)
    death_sound.set_volume(1.0)
    turret_sound.set_volume(0.05)

             
    #LOAD PLAYER
    player = sprites.Player(screen)
    player_group = pygame.sprite.GroupSingle(player)
    gun = sprites.Gun(screen, "./pictures/player/land_raider_side.gif", \
                      player.rect.centerx + 11, player.rect.centery + 6, 0)
    turret = sprites.Gun(screen, "./pictures/player/turret.gif", \
                         player.rect.centerx - 26, player.rect.centery - 30, 0)
    gun_group = pygame.sprite.Group(gun, turret)
    
    #LOAD TERRAIN
    ground = sprites.Terrain(screen,"./pictures/background/ground_large.jpg",10)
    mountain = sprites.Terrain(screen, "./pictures/background/mountains.jpg", 2)
    
    #LOAD STATSKEEPER
    stats_keeper = sprites.StatsKeeper() 
     
    #LOAD SPRITE GROUPS
    player_bullets = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group() 
    explosions = pygame.sprite.Group() 
    allSprites = pygame.sprite.OrderedUpdates(mountain, ground, player_group, \
                                              enemies, player_bullets, enemy_projectiles, gun_group, explosions, stats_keeper)
    
    #LOAD FONT
    font = pygame.font.Font("./fonts/digital.TTF", 40)
    
    # ASSIGN  
    clock = pygame.time.Clock() 
    keepGoing = True
    
    # Gun variables - used for tracking cooldown and which gun is used
    las_gun = True
    cool_down = pygame.time.get_ticks()
    
    # Statskeeper variables - used for tracking time and game state
    distance_timer = 0
    armour_timer = 0
    turret_timer = 0
    distance_track = 100
    game_over = False
    death = False
    
    #Spawn - used for spawning enemies
    spawn_factor = 0
            
    # LOOP 
    while keepGoing: 
      
        # TIME 
        clock.tick(30)
        
        # EVENT HANDLING
        
        # Get all keys pressed
        pressedkeys = pygame.key.get_pressed()
        
        for event in pygame.event.get(): 
            
            # If quit button pressed, stop music and return to menu
            if event.type == pygame.QUIT: 
                pygame.mixer.music.stop 
                screen.fill((255, 255, 255))
                return
            if event.type == pygame.KEYDOWN:                       
                #Switch weapons
                if event.key == pygame.K_c:
                    if las_gun:
                        las_gun = False
                    else:
                        las_gun = True
                        
        if not death: 
            #Moves player left or right
            if pressedkeys[pygame.K_LEFT]:
                player.change_direction(False)  
            if pressedkeys[pygame.K_RIGHT]:
                player.change_direction(True)
            
            #Changes gun angle
            if pressedkeys[pygame.K_a]:
                if las_gun:
                    if gun.get_angle() > 179:
                        pass
                    else:
                        gun.change_angle(True)
                else:
                    if turret.get_angle() > 179:
                        pass
                    else:
                        turret.change_angle(True)
                        
            if pressedkeys[pygame.K_d]:
                if las_gun:
                    if gun.get_angle() < 1:
                        pass
                    else:
                        gun.change_angle(False) 
                else:
                    if turret.get_angle() < 1:
                        pass
                    else:
                        turret.change_angle(False)
                        
            #If space bar pressed, shoot bullet according to gun and cooldown  
            if pressedkeys[pygame.K_SPACE]:
                if not las_gun and pygame.time.get_ticks() - cool_down > 120 \
                   and stats_keeper.get_turret() > 0:
                    #Add random factor into shots
                    rand_factor = random.randrange(-1,2)
                    rand_factor *= random.random() * 7
                    #Add bullet into bullet group
                    bullet = sprites.Bullet("./pictures/bullet/plasma_bullet.gif",player.rect.centerx-26, \
                                            player.rect.centery-30,turret.get_angle()+rand_factor,15,screen,40,None,None,None,3)
                    player_bullets.add(bullet)   
                    #Adjust cooldown, statskeeper, and play sound
                    cool_down = pygame.time.get_ticks()
                    stats_keeper.set_turret(-1)
                    turret_sound.play()
                elif las_gun and pygame.time.get_ticks() - cool_down > 500:
                    #Add bullet to bullet group
                    bullet = sprites.Bullet("./pictures/bullet/plasma_shot.gif",player.rect.centerx+11, \
                                            player.rect.centery+6,gun.get_angle(),20,screen,90,None,None,None,5)
                    player_bullets.add(bullet) 
                    #Adjust cooldown, and play sound
                    cool_down = pygame.time.get_ticks()
                    plasma_sound.play()
                                                   
            #Adjust the gun location according to player
            gun.adjust_xy(player.rect.centerx + 11, player.rect.centery + 6)
            turret.adjust_xy(player.rect.centerx - 26, player.rect.centery - 30)
                     
        if not game_over:            
            #Spawn enemies
            if len(enemies) < spawn_factor:
                enemy1 = sprites.Enemy_Jet(screen)
                enemy2 = sprites.Enemy_Chopper(screen)
                enemy3 = sprites.Enemy_Hover_Chopper(screen)
                enemy4 = sprites.Enemy_Helicopter(screen)
                enemy5 = sprites.Enemy_Gunner(screen)
                enemies.add(enemy1,enemy2,enemy3,enemy4,enemy5)            
                                     
            #Enemies actions
            for enemy in enemies:
                #Get player x and y
                enemy.store_player_xy(player.rect.centerx, player.rect.centery)
                
                #Enemy shooting
                if enemy.is_shooting():
                    bullet = enemy.get_bullet()
                    enemy_projectiles.add(bullet)
                                                 
                #Enemy collisions     
                for bullet in pygame.sprite.spritecollide(enemy, player_bullets, True):
                    #Adjust enemy health, if below 0, kill sprite and add explosion
                    enemy.take_damage(bullet.get_damage())               
                    if enemy.get_health() < 0:
                        stats_keeper.set_statistics(score = enemy.get_points())   
                        enemy.kill()
                        explosion = sprites.Explosion("death/explosion",16, enemy.rect.centerx,enemy.rect.bottom)
                        explosions.add(explosion)
                        sound = random.randrange(0,5)
                        explosion_sound[sound].play()
            
            #Adjust all projectiles
            for projectile in enemy_projectiles:
                explosion = None
                #If projectile is a missile, pass the coordinates of player.
                if isinstance(projectile, sprites.Missile):
                    projectile.store_player_xy(player.rect.centerx, \
                                               player.rect.centery)
                #If projectile hits player, adjust damage on player and 
                #instantiate explosion for projectile
                if pygame.sprite.spritecollide(projectile, player_group, False):
                    stats_keeper.take_damage(projectile.get_damage())
                    explosion = sprites.Explosion(projectile.get_death()+"/explosion",\
                                                  projectile.get_frames(),projectile.rect.centerx, projectile.rect.centery + 40)
                    hit_sound.play()
                #If projectile is exploding due to hitting ground, instantiate 
                #explosion for projectile
                if projectile.is_exploding():
                    explosion = sprites.Explosion(projectile.get_death()+"/explosion",\
                                                  projectile.get_frames(),projectile.rect.centerx, projectile.rect.centery)
                #If there is explosions, add to explosions group
                if explosion:
                    explosions.add(explosion)
                    projectile.kill()
                    
            #Checks if enemy projectiles hits player's bullets, adjust score
            #and the bullet's health for the player
            for projectile in pygame.sprite.groupcollide(enemy_projectiles, player_bullets, False, False):
                stats_keeper.set_statistics(projectile.get_points())
                for bullet in pygame.sprite.groupcollide(player_bullets, enemy_projectiles, False, True):
                    bullet.set_health()
                                                   
            #ADJUST SPAWN FACTORS
            if stats_keeper.get_distance() < distance_track and not game_over:
                spawn_factor += 1
                distance_track -= 3
                       
        #ADJUST STATSKEEPER
            #Increase the amount of armour
            if (pygame.time.get_ticks() - armour_timer) > 350 and \
               stats_keeper.get_armour() < 100:
                stats_keeper.set_statistics(armour = 1)
                armour_timer = pygame.time.get_ticks()
            #Increase the amount of turret ammo based on cooldown, and 
            #whether turret is still being pressed
            if (pygame.time.get_ticks() - turret_timer) > 250 and \
               stats_keeper.get_turret() < 300 and not pressedkeys[pygame.K_SPACE]:
                stats_keeper.set_turret(1)
                turret_timer = pygame.time.get_ticks()
            elif las_gun and (pygame.time.get_ticks() - turret_timer) > 250 \
                 and stats_keeper.get_turret() < 300:
                stats_keeper.set_turret(1)
                turret_timer = pygame.time.get_ticks()
            #Decrease the amount of distance
            if (pygame.time.get_ticks() - distance_timer) > 2500:
                stats_keeper.set_statistics(distance = -1)
                distance_timer = pygame.time.get_ticks()
                
            #CHECKS IF PLAYER WON
            if stats_keeper.get_distance() < 1:           
                game_over = True
                over_timer = pygame.time.get_ticks()
                message = "YOU WIN!"
            #CHECKS IF PLAYER LOST - empty all sprites if true and play death 
            #animation
            if stats_keeper.get_health() == 0:
                explosion = sprites.Explosion("player/explosion",15,player.rect.centerx,player.rect.bottom)
                explosions.add(explosion)
                player_group.empty()
                gun_group.empty()
                game_over = True 
                over_timer = pygame.time.get_ticks()
                message = "YOU LOSE!"
                death_sound.play()
                death = True
        else:
            #If game is over, set all background to 0 speed, and explode all enemies. Return to menu in 10 seconds
            ground.set_speed(0)
            mountain.set_speed(0)
            enemy_projectiles.empty()
            for enemy in enemies:
                explosion = sprites.Explosion("end/explosion",5,enemy.rect.centerx,enemy.rect.bottom)
                explosions.add(explosion)
                enemy.kill()        
            if pygame.time.get_ticks() - over_timer > 10000:
                pygame.mixer.music.stop 
                screen.fill((255, 255, 255))
                return
                
                                                                                           
        # REFRESH SCREEN
        allSprites = pygame.sprite.OrderedUpdates(mountain, ground, player_group, enemies, player_bullets, \
                                                  enemy_projectiles, gun_group, explosions, stats_keeper)
        allSprites.clear(screen, background) 
        allSprites.update() 
        allSprites.draw(screen) 
        # Display game state on screen if game is over
        if game_over:
            label = font.render(message,1,(0,0,0))
            label2 = font.render("Your Score: "+str(stats_keeper.get_score()),1,(0,0,0))
            screen.blit(label,(50,150))   
            screen.blit(label2,(50,250))   
        pygame.display.flip() 
    
def menu():
    """This function is the mainline logic for the game's menu. It accepts no variables
    and returns nothing."""
    # DISPLAY
    pygame.display.set_caption("Land Raider")
    
    # ENTITIES
    background = pygame.Surface(screen.get_size()) 
    background.fill((255, 255, 255)) 
    screen.blit(background, (0, 0)) 
    
    #LOAD MUSIC
    pygame.mixer.music.load("./music/Two Steps From Hell - Moving Mountains.wav")
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)
    
    # Load menu and instruction picture
    menu = pygame.image.load("./pictures/menus/game_menu.gif").convert()
    instructions = pygame.image.load("./pictures/menus/instructions_menu.gif").convert()
    
    # Load font and messages
    font = pygame.font.Font("./fonts/biondi.ttf", 30)
    label1 = font.render("play", 1, (255, 255, 255))
    label2 = font.render("exit", 1, (255, 255, 255))
    label3 = font.render("continue", 1, (255, 255, 255))
    
    label1_hover = font.render("play", 1, (0, 255, 0))
    label2_hover = font.render("exit", 1, (0, 255, 0))
    label3_hover = font.render("continue", 1, (0, 255, 0))
           
    # ASSIGN  
    clock = pygame.time.Clock() 
    keepGoing = True
    
    # Keep track of screens
    menu_screen = True
    instructions_screen = False
    game_playing = False
            
    # LOOP 
    while keepGoing: 
      
        # TIME 
        clock.tick(30)
        
        # Get mouse position
        x, y = pygame.mouse.get_pos()
       
        for event in pygame.event.get(): 
            #If player presses quit button, exit the game
            if event.type == pygame.QUIT: 
                keepGoing = False
            #Check if mouse button is pressed and whether it is within buttons
            if pygame.mouse.get_pressed()[0]:
                if menu_screen:
                    if x > 280 and x < 545 and y < 465 and y > 400:
                        #Loads instruction screen
                        menu_screen = False
                        instructions_screen = True
                        screen.fill((255, 255, 255)) 
                    elif x > 280 and x < 545 and y < 555 and y > 490:
                        #Exits the game
                        keepGoing = False
                elif instructions_screen:
                    if x > 280 and x < 545 and y < 555 and y > 490:
                        #Loads sets screen, and loads the game
                        instructions_screen = False
                        menu_screen = True
                        game_playing = True
                        pygame.mixer.music.stop 
                        screen.fill((255, 255, 255))
                        game()
                                                 
        if menu_screen:
            #Blit the menu screen
            screen.blit(menu, (0, 0))
            #Check if mouse is hovering over buttons
            if x > 280 and x < 545 and y < 465 and y > 400:
                screen.blit(label1_hover, (375, 430))
            else:
                screen.blit(label1, (375, 430))                
            if x > 280 and x < 545 and y < 555 and y > 490:
                screen.blit(label2_hover, (380, 517))
            else:
                screen.blit(label2, (380, 517))              
        elif instructions_screen:
            #Blit the instructions screen
            screen.blit(instructions, (0, 0))
            #Check if mouse is hovering over buttons
            if x > 280 and x < 545 and y < 555 and y > 490:
                screen.blit(label3_hover, (338, 516))
            else:
                screen.blit(label3, (338, 516))
         
        #Resets the music after game
        if game_playing:
            pygame.mixer.music.load("./music/Two Steps From Hell - Moving Mountains.wav")
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play(-1)
            game_playing = False
                                         
        # REFRESH SCREEN    
        pygame.display.flip() 
          
    # Close the game window 
    pygame.quit()      
          
# Call the main function 
menu()