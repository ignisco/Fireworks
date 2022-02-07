import pygame as pg
import random as r
import numpy as np
gravity = 1

colors = {
    "GREEN": (0, 237, 24, 255),
    "RED": (255, 0, 68, 255),
    "BLUE": (0, 34, 255, 255),
    "PURPLE": (212, 0, 227, 255),
    "ORANGE": (255, 111, 0, 255)
        }

_sound_library = {}
def play_explosion_sound():
    sounds = (
    #"sounds\\172870__escortmarius__carbidexplosion.wav",
    "sounds\\186958__readeonly__explosion7.wav",
    "sounds\\402010__eardeer__gunshot-high-1.wav",
    "sounds\\402012__eardeer__gunshot-high-5.wav",
    #"sounds\\587186__derplayer__explosion-00.wav",
    #"sounds\\587196__derplayer__explosion-06.ogg",
    )
    path = sounds[r.randint(0, len(sounds) - 1)]
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        sound = pg.mixer.Sound(path)
        _sound_library[path] = sound
    sound.play()

def play_fuse_sound():
    sounds = (
    "sounds\\140715__j1987__fuse2.wav",
    "sounds\\540829__eminyildirim__fire-fuse-ignite-flame-low.wav")
    path = sounds[r.randint(0, len(sounds) - 1)]
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        sound = pg.mixer.Sound(path)
        _sound_library[path] = sound
    sound.play()

class Particle:
    
    def __init__(self, x, y, vel, color=None, shape=None):
        self.lifespan = 51  # number of frames alive
        self.pos = np.array((x, y), float)
        if vel:
            if (shape):
                self.vel = np.array((shape[0]/self.lifespan * vel, -shape[1]/self.lifespan * vel), float)
            else:
                self.vel = np.array((r.randint(-5, 5) * vel, r.randint(-5, 5) * vel), float)
        self.acc = np.array((0, 0), float)
        if color:   # Color from parent Firework
            self.color = color
        else:
            self.color = r.choice(list(colors.values()))    # Fireworks pick their own color
        self.slowdown = 0.98
        self.size = 7

    def update(self):
        self.vel += self.acc
        self.pos += self.vel
        self.vel = self.vel * self.slowdown
        
        self.lifespan -= 1
        if self.lifespan < 0: 
            self.lifespan = 0
        self.color = (self.color[0], self.color[1], self.color[2], self.lifespan*5)
        
        
                
        
    def show(self, screen):
        s = pg.Surface((self.size, self.size), pg.SRCALPHA)
        s.fill(self.color)
        screen.blit(s, (self.pos[0], self.pos[1]))
        #pg.draw.rect(screen, self.color, pg.Rect(self.pos[0], self.pos[1], self.size, self.size))
        

class Firework(Particle):
    
    def __init__(self, x, y, audio, shape = [], child_vel=100):
        super().__init__(x, y, None)
        self.audio = audio
        # if audio:
        #    play_fuse_sound()
        FSVM = np.sqrt(y/800)
        self.vel = np.array((0, -r.randint(int(28*FSVM), int(38*FSVM))), float)
        self.child_vel = child_vel
        self.acc = np.array((0, gravity), float)
        self.exploded = False
        self.particles =  []
        if len(shape) > 0:
            self.number_of_children = len(shape)
            self.has_shape = True
            self.shape = shape
        else:
            self.number_of_children = 30
            self.has_shape = False

        self.size = 10
    
    def update(self):
        if not self.exploded:
            self.vel += self.acc
            self.pos += self.vel
            
            if self.vel[1] >= 0:
                self.exploded = True
                self.instantiate()
                # Sound effect
                if self.audio:
                    play_explosion_sound()
                
    
    def show(self, screen):
        if not self.exploded:
            super().show(screen)
        
    def instantiate(self):
        for i in range (self.number_of_children):
            if (self.has_shape):
                self.particles.append(Particle(self.pos[0], self.pos[1], self.child_vel, self.color, self.shape[i]))
            else:
                self.particles.append(Particle(self.pos[0], self.pos[1], self.child_vel, self.color))
        
        