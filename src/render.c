#include <stdint.h>
#include <math.h>

void render(uint32_t* display, uint32_t* ground, int wd, int hd, int wg, int hg)
{
    /* Pinta el terra en la pantalla */
    const float dy = 1./hd;
    const float ratio = wd/hd;
    const float f = 1.;
    const float D = 2.0;
    const float h_c = -1.0;
    float yc = -0.5;
    // TODO: fes que siguin paràmetres...
    // Intersecció amb el terra
    float theta = -0.707;
    float tanth = tan(theta);
    int ymax = f*tan(theta);
    ymax = ymax > hd ? hd : ymax;
    for (int j = 0; j < ymax; j++)
    {
        float xc = -0.5*ratio;
        // Calcula la profunditat i la posicio y de la texture
        float z = (h_c-1)/(yc/f+tanth);
        float y = z*tanth+h_c;
        float x_b = z*tanth;
        int k = y*hd;
        for (int i = 0; i < wd; i++)
        {
            //display[i+wd*j] = ground[i+wg*j];
            float x = x_b + xc;
            // Les coordenades del pla són xz
            int l = x*hd;
            display[i+j*wd] = ground[l+k*wg];
            xc += dy;
        };
        y += dy;
    };
};
