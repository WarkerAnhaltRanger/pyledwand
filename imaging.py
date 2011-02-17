from ledwandutil import Ledwand
import Image

class ImageLedwand(Ledwand):
    def __init__(self, timeout=1):
        Ledwand.__init__(self, timeout=timeout)

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

    def drawImage2(self, img): #broken
        img = img.convert("1")
        data = img.getdata()
        pixline = self.Linelen*self.ModuleWidth
        for i in range(self.Lines*pixline):
            self.DisplayBuf[i] = data[i] & 0x10000000 | data[i+pixline] & 0x1000000 | data[i+2*pixline] & 0x100000 | data[i+3*pixline] & 0x10000 | data[i+4*pixline]  & 0x1000 | data[i+5*pixline]  & 0x100 | data[i+6*pixline] & 0x10 | data[i+7*pixline] & 0x1
            self.drawbuffer()

    def drawImage3(self, buffer): #broken
        data = bytearray(buffer.data)
        pixline = self.Linelen*self.ModuleWidth
        '''for i in range(self.Lines*pixline):
            self.DisplayBuf[i] =  data[i] & 0x10000000 | (data[i+pixline]>>1) & 0x1000000 | (data[i+2*pixline]>>2) & 0x100000 | (data[i+3*pixline]>>3) & 0x10000 | (data[i+4*pixline]>>4) & 0x1000 | (data[i+5*pixline]>>5) & 0x100 | (data[i+6*pixline]>>6) & 0x10 | (data[i+7*pixline]>>7) & 0x1'''
        self.DisplayBuf = (data[i] & 0x10000000 | (data[i+pixline]>>1) & 0x1000000 | (data[i+2*pixline]>>2) & 0x100000 | (data[i+3*pixline]>>3) & 0x10000 | (data[i+4*pixline]>>4) & 0x1000 | (data[i+5*pixline]>>5) & 0x100 | (data[i+6*pixline]>>6) & 0x10 | (data[i+7*pixline]>>7) & 0x1 for i in range(self.Lines*pixline))
        self.drawbuffer()
        
def main():
    print "started main"
    ledwand = ImageLedwand()
    ledwand.clear()
    ledwand.drawResizedImageFile("Mona.jpg")

if __name__ ==  "__main__":
    main()
