from ledwandutil import Ledwand
import Image
from ctypes import *

class ImageLedwand(Ledwand):
    def __init__(self, timeout=1):
        Ledwand.__init__(self,timeout=timeout)
        self.videolib = CDLL('./videolib/bin/Release/libvideolib.so')
        self.ImageBuf = create_string_buffer(self.Lines*self.Linelen*self.ModuleWidth)

    def drawImageFile(self, path):
        self.drawImage(Image.open(path))

    def drawResizedImageFile(self, path):
        img = self.resizeImage(Image.open(path))
        self.drawImage(img)

    def resizeImage(self, img):
        xs, ys = img.size
        xfactor, yfactor = (self.Linelen*self.ModuleWidth)/float(xs), (self.Lines*self.ModuleHeight)/float(ys)
        factor = 1.0
        if xfactor < yfactor:
            factor = xfactor
        else:
            factor = yfactor
        print "factor", factor
        return img.resize((int(factor*xs), int(factor*ys)))
    
    def drawImage(self, img):   
        img = img.convert("1")
        xs, ys = img.size
        x, y = 0, 0
        for pix in img.getdata():
            if x >= xs:
                y, x = y+1, 0
            if pix > 0:
                self.setpixel(x,y,True)
            else:
                self.setpixel(x,y,False)
            x=x+1
        self.drawbuffer()

    def drawImage4(self, buffer):
        data = buffer.data
        #print "datalen", len(data)
        if self.videolib.Regular_to_Ledbuffer(data, len(data), self.ImageBuf) != 0:
            print "ERROR"
        self.DisplayBuf = self.ImageBuf.raw
        self.drawbuffer()    
        
def main():
    print "started main"
    ledwand = ImageLedwand()
    ledwand.clear()
    ledwand.drawResizedImageFile("Mona.jpg")

if __name__ ==  "__main__":
    main()
