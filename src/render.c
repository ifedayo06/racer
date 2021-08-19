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
        int wd, 
        int hd, 
        int wg, 
        int hg)
{
    /* Pinta el terra en la pantalla */
    const float D = 320;
    // TODO: fes que siguin paràmetres...
    // Intersecció amb el terra
    float theta = M_PI/8;
    float cth = cos(theta);
    float sth = sin(theta);
    float acw_y = 128;
    int ymax = hd/2-D*tan(theta);
    ymax = ymax > hd ? hd : ymax;
    ymax = ymax < 0 ? 0 : ymax;
    #pragma omp parallel for 
    for (int j = ymax; j < hd; j++)
    {
        float yp = hd/2-j;
        float lamb = acw_y/(D*sth-yp*cth);
        for (int i = 0; i < wd; i++)
        {
            float xp = i-wd/2;
            int xw = lamb*xp;
            int zw = lamb*(-yp*sth-D*cth);
            xw = modulo(xw, wg);
            zw = modulo(zw, hg);
            // Pinta...
            display[i+j*wd] = ground[xw+zw*wg];
        };
    };
};
