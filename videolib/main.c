#include <stdio.h>
#include <stdint.h>

#define LINES 20
#define LINELEN 56
#define MODWIDTH 8
#define MODHEIGHT 10
#define BIAS 5

#define WIDTH 448
#if defined(__LP64__)
#define SIZE (WIDTH/8)
#else
#define SIZE (WIDTH/4)
#endif
#define STEP (MODHEIGHT*SIZE)

int fast_img_convert(const char* imgbuf, const uint32_t len, char* ledbuf)
{
    if(len != LINES*LINELEN*MODWIDTH*MODHEIGHT)
    {
        printf("size of imagebuf should be %d but is %d\n", LINELEN*LINES*MODWIDTH*MODHEIGHT, len);
        return 1;
    }

    size_t *in =  (size_t*)imgbuf;
    size_t *res = (size_t*)ledbuf;
    size_t t1, s, i;
    for(s = 0; s < LINES*STEP; s+=STEP){
        t1 = (s/STEP)*SIZE;
        for(i = 0; i < SIZE; i++){
#if defined(__LP64__)
            res[i+t1] = (0x8080808080808080 & in[i+s]) |
                        (0x4040404040404040 & in[i+s+SIZE]) |
                        (0x2020202020202020 & in[i+s+2*SIZE]) |
                        (0x1010101010101010 & in[i+s+3*SIZE]) |
                        (0x0808080808080808 & in[i+s+4*SIZE]) |
                        (0x0404040404040404 & in[i+s+5*SIZE]) |
                        (0x0202020202020202 & in[i+s+6*SIZE]) |
                        (0x0101010101010101 & in[i+s+7*SIZE]);
#else
            res[i+t1] = (0x80808080 & in[i+s]) |
                        (0x40404040 & in[i+s+SIZE]) |
                        (0x20202020 & in[i+s+2*SIZE]) |
                        (0x10101010 & in[i+s+3*SIZE]) |
                        (0x08080808 & in[i+s+4*SIZE]) |
                        (0x04040404 & in[i+s+5*SIZE]) |
                        (0x02020202 & in[i+s+6*SIZE]) |
                        (0x01010101 & in[i+s+7*SIZE]);
#endif
        }
    }

    return 0;
}

int Regular_to_Ledbuffer(const char* imagebuf, const uint32_t len, char* ledbuffer)
{
    if(len != LINES*LINELEN*MODWIDTH*MODHEIGHT)
    {
        printf("size of imagebuf should be %d but is %d\n", LINELEN*LINES*MODWIDTH*MODHEIGHT, len);
        return 1;
    }
    uint32_t i = 0, pos = 0;
    for(i = 0; i<LINELEN*MODWIDTH*LINES; i++)
    {
        pos = (i%(LINELEN*MODWIDTH))+(((uint32_t)(i/(MODWIDTH*LINELEN)))*MODWIDTH*LINELEN*MODHEIGHT);
        ledbuffer[i] =  (imagebuf[pos] & 0x80) |
                        ((imagebuf[pos+LINELEN*MODWIDTH]>>1) & 0x40) |
                        ((imagebuf[pos+2*LINELEN*MODWIDTH]>>2) & 0x20) |
                        ((imagebuf[pos+3*LINELEN*MODWIDTH]>>3) & 0x10) |
                        ((imagebuf[pos+4*LINELEN*MODWIDTH]>>4) & 0x8) |
                        ((imagebuf[pos+5*LINELEN*MODWIDTH]>>5) & 0x4) |
                        ((imagebuf[pos+6*LINELEN*MODWIDTH]>>6) & 0x2) |
                        ((imagebuf[pos+7*LINELEN*MODWIDTH]>>7) & 0x1);
        }
    return 0;
}

int compare_Buffs(const char* buf1, const uint32_t buf1_len, const char* buf2, const uint32_t buf2_len, char* diffbuf, const uint32_t diffbuf_len)
{
    if(buf1_len != buf2_len && buf1_len != diffbuf_len)
    {
        printf("size of buffers are not equal buf1: %d buf2: %d diffbuf: %d\n", buf1_len, buf2_len, diffbuf_len);
        return 1;
    }

    size_t i = 0;

    size_t *p_buf1 = (size_t*)buf1;
    size_t *p_buf2 = (size_t*)buf2;
    size_t *p_diffbuf = (size_t*)diffbuf;

    for(i=0; i<(buf1_len/sizeof(size_t)); i++)
        p_diffbuf[i] = p_buf1[i]^p_buf2[i];

    return 0;
}
