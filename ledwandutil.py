# -*- coding: utf-8 -*-
from socket import *
#from array import array
import math
import urllib
import Image

'''
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
Warker, Ron, Denis wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy us a beer in return

Follow me on twitter @warker
----------------------------------------------------------------------------

Utility module for LED-Screen at CCCB
'''

def subHtmlcode(s, code):
    for c in code:
        s = s.replace(c[0], c[1])
    return s

def HttpRequest(url, params=dict()):
    if(params != dict()):
        f = urllib.urlopen("%s?%s" % (url, urllib.urlencode(params)))
        print "requesting: %s?%s" % (url, urllib.urlencode(params))
    else:
        f = urllib.urlopen(url)
    return f.read()

class Ledwand:

    def __init__(self, host="172.23.42.120", port=2342, linelen=56, lines=20, module_width=8, module_height=12):
        self.UdpSocket = socket(AF_INET, SOCK_DGRAM)
        self.UdpAddress = (host, port)
        self.Linelen = linelen
        self.Lines = lines
        self.ModuleWidth = module_width
        self.ModuleHeight = module_height
        self.DisplayBuf = bytearray(linelen*lines*self.ModuleWidth)

    def processline(self, line):
        if len(line) < self.Linelen:
            return bytearray(line)
        else:
            return bytearray(line[0:self.Linelen])

    def sendline(self, linenum, line):
        self.setlineraw(0, linenum, self.processline(str(line)))

    def setpixel(self, x, y, state):
        if x < (self.ModuleWidth*self.Linelen) and y < (self.ModuleHeight*self.Lines) and (y%self.ModuleHeight) <= 7:
            if state == True:
                self.DisplayBuf[(y / self.ModuleHeight) * self.Linelen * self.ModuleWidth + x] |= (1 << (7-(y % self.ModuleHeight)))
            else:
                self.DisplayBuf[(y / self.ModuleHeight) * self.Linelen * self.ModuleWidth + x] &= ~(1 << (7-(y % self.ModuleHeight)))

    def drawbuffer(self):
        partsize = (self.Lines * self.Linelen * self.ModuleWidth) / 7
        for i in range(7):
            self.request(16, i*partsize, partsize, 0, 0, self.DisplayBuf[i*partsize:i*partsize+partsize])
        self.refresh()
        
    def convert(self, x):
        x1 = math.floor(x / 256)
        x2 = math.fmod(x, 256)
        return chr(int(x2)) + chr(int(x1))

    def request(self, cmd, xpos, ypos, xs, ys, text):
        cmd = self.convert(cmd)
        xpos = self.convert(xpos)
        ypos = self.convert(ypos)
        xs = self.convert(xs)
        ys = self.convert(ys)
        self.UdpSocket.settimeout(1)
        self.UdpSocket.sendto(cmd + xpos + ypos + xs + ys + text, self.UdpAddress)
        try:
            self.UdpSocket.recv(4096)
        except timeout:
            print "Warning: last transmission timed out"

    def setline(self, x, y, data):
        self.request(4, x, y, 1, 1, data)

    def setlineraw(self, x, y, data):
        data = data.decode("utf8").encode("cp437")
        #print "sending:", 3, x, y, len(data), 20, data.decode("cp437").encode("utf8")
        self.request(3, x, y, len(data), 1, data) # send raw

    def clear(self):
        self.request(2, 0, 0, 0, 0, '') # clear

    def softreset(self):
        self.request(8, 0, 0, 0, 0, '')

    def hardreset(self):
        self.request(11, 0, 0, 0, 0, '')

    def redraw(self):
        self.request(8, 0, 0, 0, 0, ' ') # redraw

    def setbrightness(self, val):
        self.request(7, 0, 0, 0, 0, chr(val)) # brightness

    def closeSocket(self):
        self.UdpSocket.close()

    def changeLineInBuf(self, linenum, line):
        self.DisplayBuf[linenum*self.Linelen:(linenum+1)*self.Linelen] = self.processline(line)

    def sendfilledBuf(self):
        self.request(3, 0, 0, self.Linelen, self.Lines, self.DisplayBuf.decode("utf8").encode("cp437"))
    
    def clearBuf(self):
        self.DisplayBuf = bytearray(self.Linelen*self.Lines)

    def refresh(self):
        self.request(17, 0, 0, 0, 0, '')
        
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

class LedwandProvider:

    def __init__(self, ledwand = Ledwand()):
        self.Ledwand = ledwand

    def getData(self):
        pass

    def displayData(self):
        data = self.getData()
        self.Ledwand.setbrightness(2)
        linecount = 0
        for obj in data:
            print "data:", obj
            self.Ledwand.sendline(linecount, obj)
            linecount += 1


def main():
    print "started main"
    ledwand = Ledwand()
    ledwand.clear()
    #ledwand.setpixel(2,2,True)
    #ledwand.setpixel(2,3,True)
    #ledwand.drawbuffer()
    ledwand.drawImage("Mona.jpg")
    #ledwand.drawImage("test.jpg")

if __name__ ==  "__main__":
    main()
