#include <stdint.h>
void render(uint32_t* display, uint32_t* ground, int wd, int hd, int wg, int hg)
{
    /* Pinta el terra en la pantalla */
    for (int j = 0; j < hd; j++)
    {
        for (int i = 0; i < wd; i++)
        {
            display[i+wd*j] = ground[i+wg*j];
        };
    };
};
