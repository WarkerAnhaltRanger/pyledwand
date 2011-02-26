#include <stdio.h>

#define LINES 20
#define LINELEN 56
#define MODWIDTH 8
#define MODHEIGHT 12

int Image_to_Ledbuffer(const char* imagebuf, int len, char* ledbuffer)
{
    if(len != LINES*LINELEN*MODWIDTH*MODWIDTH)
    {
        printf("size of imagebuf hould be %d but is %d\n", LINELEN*LINES*MODWIDTH*MODWIDTH, len);
        return 1;
    }
    int i = 0, pos = 0, step = LINELEN*MODWIDTH*(MODWIDTH-1);
    for(i = 0; i<LINELEN*MODWIDTH*LINES; i++)
    {
        pos = ((int)(i/(LINELEN*MODWIDTH)))*step;
        ledbuffer[i] =  (imagebuf[i+pos] & 0x10000000) |
                        (imagebuf[i+pos+LINELEN*MODWIDTH] & 0x1000000) |
                        (imagebuf[i+pos+2*LINELEN*MODWIDTH] & 0x100000) |
                        (imagebuf[i+pos+3*LINELEN*MODWIDTH] & 0x10000) |
                        (imagebuf[i+pos+4*LINELEN*MODWIDTH] & 0x1000) |
                        (imagebuf[i+pos+5*LINELEN*MODWIDTH] & 0x100) |
                        (imagebuf[i+pos+6*LINELEN*MODWIDTH] & 0x10) |
                        (imagebuf[i+pos+7*LINELEN*MODWIDTH] & 0x1);
    }
    return 0;
}

int Regular_to_Ledbuffer(const char* imagebuf, int len, char* ledbuffer)
{
    if(len != LINES*LINELEN*MODWIDTH*MODWIDTH)
    {
        printf("size of imagebuf hould be %d but is %d\n", LINELEN*LINES*MODWIDTH*MODWIDTH, len);
        return 1;
    }
    int i = 0, pos = 0, step = LINELEN*MODWIDTH*(MODWIDTH-1);
    for(i = 0; i<LINELEN*MODWIDTH*LINES; i++)
    {
        //pos = ((int)(i/(LINELEN*MODWIDTH)))*step;
        pos = ((int)(i/step))*step;
        ledbuffer[i] =  (imagebuf[i+pos] & 0x10000000) |
                        ((imagebuf[i+pos+LINELEN*MODWIDTH]>>1) & 0x1000000) |
                        ((imagebuf[i+pos+2*LINELEN*MODWIDTH]>>2) & 0x100000) |
                        ((imagebuf[i+pos+3*LINELEN*MODWIDTH]>>3) & 0x10000) |
                        ((imagebuf[i+pos+4*LINELEN*MODWIDTH]>>4) & 0x1000) |
                        ((imagebuf[i+pos+5*LINELEN*MODWIDTH]>>5) & 0x100) |
                        ((imagebuf[i+pos+6*LINELEN*MODWIDTH]>>6) & 0x10) |
                        ((imagebuf[i+pos+7*LINELEN*MODWIDTH]>>7) & 0x1);
    }
    return 0;
}

