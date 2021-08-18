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

    def draw_screen(self):
        self.display.lock()
        c_render(self.display_pixels,
                 self.level_pixels,
                 self.w, self.h, *self.level_pixels.shape)
        self.display.unlock()
        pygame.display.flip()

if __name__ == "__main__":
    w, h = 640, 480
    joc = Racer(w, h)
    joc.mainloop()
