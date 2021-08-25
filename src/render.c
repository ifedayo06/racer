#include <stdint.h>
#include <math.h>
#include <stdio.h>
#include <omp.h>

unsigned modulo(int x, unsigned y)
{
    int mod = x % (int)y;
    mod = mod < 0 ? mod+y : mod;
    return mod;
};

int min(int x, int y)
{
    return x > y ? y : x;
};

int max(int x, int y)
{
    return x > y ? x : y;
};

void render(
        uint32_t* display, 
        uint32_t* ground, 
        float acw[3],
        float C[9],
        float D,
        float over_lamb,     // Factor d'escala màxim, regula la visió
        int wd, 
        int hd, 
        int wg, 
        int hg)
{
    /* Pinta el terra en la pantalla */
    // Línia de l'horitzó
    int ymax = hd/2-(D*C[5]-acw[1]*over_lamb)/C[4];
    ymax = ymax > hd ? hd : ymax;
    ymax = ymax < 0 ? 0 : ymax;

    /* Calculo en paral·lel cada línia de la pantalla, ja que es pot
     * realitzar d'una forma absolutament paral·lela */
    #pragma omp parallel for 
    for (int j = ymax; j < hd; j++)
    {
        float yp = hd/2-j;  // Coordenada de la pantalla en SR càmera
        float lamb = acw[1]/(D*C[5]-yp*C[4]);   // Factor d'escala
        for (int i = 0; i < wd; i++)
        {
            float xp = i-wd/2; // Coordenada de la pantalla en SR càmera
            // Transformacions cap a les coordenades del món.
            int xw = lamb*(xp*C[0]+yp*C[1]-D*C[2])+acw[0];
            int zw = lamb*(xp*C[6]+yp*C[7]-D*C[8])+acw[2];
            // TODO: Canvia la funció modulo per una altra, depenent del cas.
            xw = modulo(xw, wg);
            zw = modulo(zw, hg);
            // Pinta finalment...
            display[i+j*wd] = ground[xw+zw*wg];
        };
    };
};
