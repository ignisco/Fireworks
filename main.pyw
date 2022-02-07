import random as r
import pygame as pg
import firework as f
import shapes

screen_size = (800, 800)
current_screen_size = screen_size
FSVM = 1.0
audio = False

def toggle_audio():
    global audio
    audio = not audio

    # Orker ikke å fikse det :////

def toggle_fullscreen():
    global fullscreen, current_screen_size, FSVM
    fullscreen = not fullscreen
    
    if (fullscreen):
        screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(screen_size)
    
    current_screen_size = (pg.display.Info().current_w, pg.display.Info().current_h)


def instantiate(probabilty):
    global audio

    probabilty /= 100 # p = probability of instantiating each frame
    if r.uniform(0, 1) <= probabilty:
        fireworks.append(f.Firework(r.randint(0, current_screen_size[0]), current_screen_size[1], audio, shapes.HEART))
    

def game():      
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
            
            if event.type == pg.KEYDOWN:
                
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    return
                
                elif event.key == pg.K_f:
                    toggle_fullscreen()
                
                elif event.key == pg.K_m:
                    toggle_audio()

                

        
        instantiate(10)
        screen.fill((0, 0, 0))
        for firework in fireworks:
            firework.update()
            firework.show(screen)
            
            if firework.exploded:
                remove = True
                for particle in firework.particles:
                    particle.update()
                    particle.show(screen)
                    if particle.color[3] > 0:   #If one particle still exists, dont remove
                        remove = False
                
                if remove:
                    fireworks.remove(firework)
            
            
        clock.tick(60)
        pg.display.flip()
    


if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode(screen_size)
    pg.display.set_caption("Lots of Love")
    # programIcon = pg.image.load('heart.png')
    # pg.display.set_icon(programIcon)
    fireworks = []
    fullscreen = False
    game()