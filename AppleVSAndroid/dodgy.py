import pygame as p
import random
import sys

black=((0,0,0))
fps=60
max_mac_time=fps*8
max_mac=10
mac_move_time=fps*0.15

p.init()
Res=(1280,768)
screen=p.display.set_mode(Res)
clock = p.time.Clock()

distance_y=64
distance_x=64
mac_dist=64
no_mac=0
timer=0
move_timer=0

bg_image = p.image.load("wall.jpg").convert()
hero=p.image.load("hero.png").convert_alpha()
mac=p.image.load("mac.png").convert_alpha()


bg_image=p.transform.scale(bg_image,Res)
hero=p.transform.scale(hero,(64,64))
mac=p.transform.scale(mac,(64,64))


heropos=[Res[0]/2,Res[1]-64]
macs=[]

def create_mac(hp):
    global no_mac,macs,screen
    tx = random.randint(1, 19)
    ty = random.randint(1, 11)
    tx = tx * 64
    ty = ty * 64
    no_mac+=1
    macpos=[tx,ty]
    if macpos in macs:
        return
    if macpos==hp:
        return
    screen.blit(mac,macpos)
    macs.append(macpos)


def update_macs():
    global macs,screen
    for i in macs:
        screen.blit(mac,i)

def remove_macs():
    global macs,no_mac
    macs.pop(0)
    no_mac-=1

def check_hero_death(hp):
    if hp in macs:
        return 1
    else:
        return 0

def move_macs():
    global macs
    for i in range(len(macs)):
        pos=macs[i]
        k=random.randint(1,4)
        if k==1:
            pos[1]=pos[1]-mac_dist
        if k==2:
            pos[0]+=mac_dist
        if k==3:
            pos[1]+=mac_dist
        if k==4:
            pos[0]-=mac_dist
        if pos in macs:
            continue
        macs[i]=pos
    return



while 1:

    screen.blit(bg_image, [0, 0])

    if no_mac<max_mac:
        create_mac(heropos)

    if timer>=max_mac_time:
        remove_macs()
        timer=0

    if move_timer>=mac_move_time:
        move_macs()
        move_timer=0
    update_macs()

    h=heropos
    for events in p.event.get():
        if events.type==p.QUIT:
            sys.exit()
        if events.type==p.KEYDOWN and events.key==p.K_w:
            heropos[1]=heropos[1]-distance_y
        if events.type == p.KEYDOWN and events.key == p.K_a:
            heropos[0] = heropos[0] - distance_x
        if events.type == p.KEYDOWN and events.key == p.K_s:
            heropos[1] = heropos[1] + distance_y
        if events.type==p.KEYDOWN and events.key==p.K_d:
            heropos[0]=heropos[0]+ distance_x
    if heropos[0]<=-64:
        heropos=h
        heropos[0]+=64
    if heropos[1]<=-64:
        heropos=h
        heropos[1]+=64
    if heropos[0]>=Res[0]:
        heropos=h
        heropos[0]-=64
    if heropos[1]>=Res[1]:
        heropos=h
        heropos[1]-=64


    if check_hero_death(heropos):
        sys.exit()
    screen.blit(hero,heropos)


    timer+=1
    move_timer+=1
    p.display.flip()
    clock.tick(fps)