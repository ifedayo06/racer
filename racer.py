#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
import pygame
import numpy as np
pygame.init()
#pygame.key.set_repeat(16)

# Carrega la llibreria de C...
def load_func(name, path):
    try:
        lib = np.ctypeslib.load_library(name, path)
    except:
        raise ImportError("Render library not found!")
    c_render = lib.render
    # Tipus arguments d'entrada
    uint32_p = np.ctypeslib.ndpointer(dtype=np.uint32, ndim=2, )
    f32_p2 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=2, )
    f32_p1 = np.ctypeslib.ndpointer(dtype=np.float32, ndim=1, )
    c_render.argtypes = [uint32_p,      # *display
                         uint32_p,      # *ground
                         f32_p1,        # acw[3]
                         f32_p2,        # C[9]
                         ctypes.c_float,# D
                         ctypes.c_float,# over_lamb
                         ctypes.c_int,  # wd
                         ctypes.c_int,  # hd
                         ctypes.c_int,  # wg
                         ctypes.c_int   # hg
                        ]
    c_render.restype = None
    return c_render

c_render = load_func("render", "bin")

class Camera:
    def __init__(self, display, lamb_max):
        self.pos = self.x, self.y, self.z = np.asarray((0, 0, 0), dtype=np.float32)
        # Referència al display actiu com a array de píxels
        self.display = display
        self.pixels = pygame.surfarray.pixels2d(display)
        self.phi = 0
        self.theta = np.pi/8
        self.D = self.display.get_width()/2
        # Crea matriu de rotació
        self.direction = np.zeros(3)
        self.C = np.zeros((3, 3), dtype=np.float32, order="C")
        self.update_rot_matrix()
        self.over_lamb = 1/lamb_max

        # PROPIETATS FÍSIQUES
        self.b = 5e-4
        self.v = np.zeros(3)
        self.ext_force = np.zeros(3)
        self.over_m = 1

    def update_rot_matrix(self, phi=None, theta=None):
        """Actualitza la matriu de rotació del sistema."""
        if phi:
            self.phi = phi
        if theta:
            self.theta = theta
        cphi = np.cos(self.phi)
        ctheta = np.cos(self.theta)
        sphi = np.sin(self.phi)
        stheta = np.sin(self.theta)
        self.direction[:] = (sphi, 0, -cphi)
        self.C[0, :] = cphi, sphi*stheta, -sphi*ctheta
        self.C[1, :] = 0, ctheta, stheta
        self.C[2, :] = sphi, -cphi*stheta, cphi*ctheta

    def draw_floor(self, level_pixels):
        """Dibuixa en self.pixels el terra donat per level_pixels."""
        self.display.lock()
        c_render(self.pixels,
                 level_pixels,
                 self.pos,
                 self.C,
                 self.D,
                 self.over_lamb,
                 *self.pixels.shape, 
                 *level_pixels.shape)
        self.display.unlock()
    
    def update(self, dt):
        """Actualitza la força impresa sobre el cos."""
        self.v[:] += self.over_m*(self.ext_force-self.v*self.b)*dt
        self.pos[:] += self.v*dt

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
        self.camera = Camera(self.display, 10)
        self.camera.pos[1] = 32
        self.camera.update_rot_matrix(np.pi)
        # TODO: must lock surface!
        i = 0
        t0 = self.clock.tick()
        self.display.fill((0, 128, 255))
        while self.running:
            # Escaneja l'entrada del teclat
            events = pygame.event.get()
            self.handle_input(events)
            # Actualitza la pantalla
            dt = self.clock.tick()
            self.camera.update(dt)
            self.draw_screen()
            """
            i += 1
            if i > 1000:
                print(f"FPS = {1e6/(dt-t0)} s^-1")
                i = 0
                t0 = self.clock.tick()
            """

    def handle_input(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.camera.ext_force = 1e-3*self.camera.direction
                elif event.key == pygame.K_LEFT:
                    self.camera.phi -= .1
                    self.camera.update_rot_matrix()
                elif event.key == pygame.K_RIGHT:
                    self.camera.phi += .1
                    self.camera.update_rot_matrix()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.camera.ext_force = 0*self.camera.direction

    def draw_screen(self):
        self.camera.draw_floor(self.level_pixels)
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
    h = 480
    w = int(16/9*480)
    joc = Racer(w, h)
    joc.mainloop()
