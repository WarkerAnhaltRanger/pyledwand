from ledwandutil import Ledwand
import Image

class ImageLedwand(Ledwand):
    def __init__(self):
        Ledwand.__init__(self)
    
    def drawImage(self, path):   
        img = Image.open(path) 
        xs, ys = img.size
        xfactor, yfactor = (self.Linelen*self.ModuleWidth)/float(xs), (self.Lines*self.ModuleHeight)/float(ys)
        factor = 1.0
        if xfactor < yfactor:
            factor = xfactor
        else:
            factor = yfactor
        print "factor", factor
        img = img.resize((int(factor*xs), int(factor*ys))).convert("1")
        xs, ys = img.size
        x, y = 0, 0
        for pix in img.getdata():
            if x >= xs:
                y, x = y+1, 0
            if pix > 0:
                self.setpixel(x,y,True)
            x=x+1
        self.drawbuffer()


def main():
    print "started main"
    ledwand = ImageLedwand()
    ledwand.clear()
    #ledwand.setpixel(2,2,True)
    #ledwand.setpixel(2,3,True)
    #ledwand.drawbuffer()
    ledwand.drawImage("Mona.jpg")

if __name__ ==  "__main__":
    main()
