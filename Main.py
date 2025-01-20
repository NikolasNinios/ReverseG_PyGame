import pygame
#from Ball import Ball
pygame.init()
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,255)

screenwidth=800
screenheight=600
centerx=screenwidth/2
centery=screenheight/2

size=(screenwidth,screenheight)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("MyGame")

clock=pygame.time.Clock()
done = False
counter=0

#--------------------------------
#ball1=Ball(BLUE,20,20)
#ball1.rect.center=(centerx,centery)
all_sprites = pygame.sprite.Group()
#all_sprites.add(ball1)
#--------------------------------
#static background
background=pygame.Surface(screen.get_size())
background.fill(WHITE)
pygame.draw.line(background,BLACK,(0,0),(screenwidth,0),10)
pygame.draw.line(background,BLACK,(0,0),(0,screenheight),10)
pygame.draw.line(background,BLACK,(screenwidth,0),(screenwidth,screenheight),10)
pygame.draw.line(background,BLACK,(0,screenheight),(screenwidth,screenheight),10)

rect_x=centerx
rect_y=centery
rect_change_x=2
rect_change_y=2

myrectanglewidth=30
myrectangleheight=30

while not done:
    #INPUT
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            done=True
        elif event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_x:
                rect_change_x=rect_change_x * 2
            elif event.key == pygame.K_y:
                rect_change_y=rect_change_y * 2   
            elif event.key == pygame.K_c:
                rect_change_x=rect_change_x / 2
            elif event.key == pygame.K_u:
                rect_change_y=rect_change_y / 2  
            elif event.key == pygame.K_r:
                rect_x=centerx
                rect_y=centery
                rect_change_x=2
                rect_change_y=2

    # CONTROL/GAME LOGIC
    #if rect_x < screenwidth:
     #   rect_x=rect_x+rect_change_x
    #else:
     #   rect_x =770

    #if rect_y < screenheight:
     #   rect_y=rect_y+rect_change_y
    #else:
     #   rect_y =570

    #ball1.rect.x = ball1.rect.x+ ball1.velocity[0]
    #ball1.rect.y = ball1.rect.y+ ball1.velocity[1]
    rect_x=rect_x+rect_change_x
    rect_y=rect_y+rect_change_y

    if rect_x >screenwidth -myrectanglewidth or rect_x < 0:
        rect_change_x=rect_change_x *-1
        

    if rect_y >screenheight -myrectangleheight or rect_y < 0:
        rect_change_y=rect_change_y *-1

   # if ball1.rect.left <=0 or ball1.rect.right > screenwidth:
    #    ball1.velocity[0] =ball1.velocity[0] * -1
    #if ball1.rect.top <=0 or ball1.rect.bottom > screenheight:
    #    ball1.velocity[1] =ball1.velocity[1] * -1

        

    # DRAWING
    #background
    #screen.fill(WHITE)
    screen.blit(background,(0,0))

    counter=counter+1


    
    #variables
   

    #myrect=pygame.Rect(screenwidth-30,centery-30,30,30)
    myrect=pygame.Rect(rect_x-myrectanglewidth/2,rect_y-myrectangleheight/2,myrectanglewidth,myrectangleheight)
   

    startpos=(770,270)
    endpos=(400,300)
    #elements
    #pygame.draw.circle(screen,RED,(400,300),30)
    #pygame.draw.circle(screen,GREEN,(400,30),30)
    pygame.draw.rect(screen,BLACK,myrect)
    #pygame.draw.line(screen,BLUE,startpos,endpos)
    #pygame.draw.ellipse(screen,(100,100,0),myrect,10)

    myfont=pygame.font.Font(None,30)
    text=myfont.render("Updates: " + str(counter),1,(200,200,0))

    screen.blit(text,(5,5)) 

    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30) #30 fps

#pygame.quit()