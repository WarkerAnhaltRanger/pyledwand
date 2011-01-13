# -*- coding: utf-8 -*-
from socket import *
from array import array
import math
import urllib

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

def HttpRequest(url, params=dict()):
    if(params != dict()):
        f = urllib.urlopen("%s?%s" % (url, urllib.urlencode(params)))
        print "requesting: %s?%s" % (url, urllib.urlencode(params))
    else:
        f = urllib.urlopen(url)
    return f.read()

class Ledwand:

    def __init__(self, host="172.23.42.120", port=2342, linelen=56, lines=20):
        self.UdpSocket = socket(AF_INET, SOCK_DGRAM)
        self.UdpAddress = (host, port)
        self.Linelen = linelen
        self.Lines = lines
        self.clearBuf()

    def processline(self, line):
        line = array('c', str(line))
        tempbuf = array('c', " "*self.Linelen)
        if len(line) < self.Linelen:
            tempbuf[0:len(line)] = line
        else:
            tempbuf = line[0:self.Linelen]
        return tempbuf

    def sendline(self, linenum, line):
        self.setlineraw(0, linenum, self.processline(line).tostring())

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
        self.request(3, 0, 0, self.Linelen, self.Lines, self.DisplayBuf.tostring().decode("utf8").encode("cp437"))
    
    def clearBuf(self):
        self.DisplayBuf = array('c', " "*self.Linelen*self.Lines)
        

class LedwandProvider:

    def __init__(self, ledwand = Ledwand()):
        self.Ledwand = ledwand

    def getData(self):
        pass

    def displayData(self):
        data = self.getData()
        linecount = 0
        for obj in data:
            print "data:", obj
            self.Ledwand.sendline(linecount, obj)
            linecount += 1
