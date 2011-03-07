from ledwandutil import Ledwand
import Image
from ctypes import *

class ImageLedwand(Ledwand):
    def __init__(self, timeout=1):
        Ledwand.__init__(self,timeout=timeout)
        self.videolib = CDLL('./videolib/bin/Release/libvideolib.so')
        self.ImageBuf = create_string_buffer(self.Lines*self.Linelen*self.ModuleWidth)
        self.ImageCmp = create_string_buffer(self.Lines*self.Linelen*self.ModuleWidth)
        self.setbrightness(4)

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

    def drawImage4(self, data):
        self.ImageBuf2 = self.ImageBuf
        if self.videolib.Regular_to_Ledbuffer(data, len(data), self.ImageBuf) != 0:
            print "ERROR"
        if self.videolib.compare_Buffs(self.ImageBuf, len(self.ImageBuf), self.ImageBuf2, len(self.ImageBuf2), self.ImageCmp, len(self.ImageCmp) != 0):
            print "compare buffer ERROR"
        self.DisplayBuf = self.ImageBuf
        self.drawbuffer()

    def drawDiffImage(self, diffbuf, newbuf):
        data = list()
        record, tmp = False, 0
        for i in range(len(diffbuf)):
            if diffbuf[i] != 0:
                if record == False:
                    tmp, record = i, True 
            else:
                if record == True:
                    data.append((tmp,i))
                    record = False
        # data hat nun das format list(tuple(changedstartpos, changedendpos))
        
                
def main():
    print "started main"
    ledwand = ImageLedwand()
    ledwand.clear()
    ledwand.drawResizedImageFile("Mona.jpg")

if __name__ ==  "__main__":
    main()
