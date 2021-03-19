import random as r
import pygame as pg
import firework as f
import shapes


pg.init()
clock = pg.time.Clock()
screen_size = (800, 800)
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Fireworks")

fireworks = []


def instantiate(probabilty):
    probabilty /= 100 # p = probability of instantiating each frame
    
    if r.uniform(0, 1) <= probabilty:
        fireworks.append(f.Firework(r.randint(0, 800), 800, shapes.HEART))
    

def game():      
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        
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
    game()