#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import pygame
import numpy as np
pygame.init()

# Carrega la llibreria de C...
def load_func(name, path):
    try:
        lib = np.ctypeslib.load_library(name, path)
    except:
        raise ImportError("Render library not found!")
    c_render = lib.render
    # Tipus arguments d'entrada
    uint32_p = np.ctypeslib.ndpointer(dtype=np.uint32, ndim=2, )
    c_render.argtypes = [uint32_p, uint32_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    c_render.restype = None
    return c_render

c_render = load_func("render", "bin")

class Camera:
    def __init__(self):
        self.pos = self.x, self.y, self.z = 0, 0, 0

class Racer:
    def __init__(self, w, h):
        self.size = self.w, self.h = w, h
        self.display = pygame.display.set_mode(self.size)
        self.display_pixels = pygame.surfarray.pixels2d(self.display)
        self.clock = pygame.time.Clock()

    def mainloop(self):
        self.running = True
        self.level = pygame.image.load("maps/test.png").convert()
        self.level_pixels = pygame.surfarray.pixels2d(self.level)
        print(self.level_pixels)
        self.camera = Camera()
        self.camera.y = 128
        # TODO: must lock surface!
        i = 0
        t0 = self.clock.tick()
        while self.running:
            # Escaneja l'entrada del teclat
            events = pygame.event.get()
            self.handle_input(events)
            # Actualitza la pantalla
            self.draw_screen()
            i += 1
            if i > 1000:
                t1 = self.clock.tick()
                print(f"FPS = {1e6/(t1-t0)} s^-1")
                i = 0
                t0 = self.clock.tick()

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.camera.z -= 20
                elif event.key == pygame.K_s:
                    self.camera.z += 20
                elif event.key == pygame.K_d:
                    self.camera.x += 20
                elif event.key == pygame.K_a:
                    self.camera.x -= 20

    def draw_screen(self):
        self.display.lock()
        c_render(self.display_pixels,
                 self.level_pixels,
                 self.w, self.h, *self.level_pixels.shape)
        self.display.unlock()
        pygame.display.flip()

    def py_draw_screen(self):
        """ PROTOTIP DE FUNCIO """
        # Linia de l'horitzo
        D = self.w//2
        theta = np.pi/8
        y_hor = int(max(0, min(self.h/2-D*np.tan(theta), self.h)))
        cth = np.cos(theta)
        sth = np.sin(theta)
        ny, nx = self.level_pixels.shape
        for j in range(y_hor, self.h):
            yp = self.h//2-j
            lamb = self.camera.y/(D*sth-yp*cth)
            for i in range(self.w):
                xp = i-self.w//2
                # Calculo la posicio
                xw = lamb*xp+self.camera.x
                zw = lamb*(-yp*sth-D*cth)+self.camera.z
                # Pinto la posicio de la textura
                xw = int(xw) % nx
                zw = int(zw) % ny
                self.display_pixels[i, j] = self.level_pixels[xw, zw]
        pygame.display.flip()

if __name__ == "__main__":
    w, h = 640, 480
    joc = Racer(w, h)
    joc.mainloop()
