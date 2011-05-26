from ledwandutil import *
import vbbregex
import weatherregex
import termios, sys, os, time
from threading import Thread

TERMIOS = termios

class UpdateThread(Thread):
    def __init__(self, provider, time = 30):
        self.provider = provider
        self.time = time
        Thread.__init__(self)
        self.Killed = False

    def run(self):
        while self.Killed == False:
            self.provider.displayData()
            time.sleep(self.time)

class ScreenCube(LedwandProvider):

    def __init__(self):
        LedwandProvider.__init__(self)
        self.position = 0
        self.current = None
        self.screens = list()
        self.data = list()
        

    def set_current(self):
        self.current = self.screens[self.position]
        self.Ledwand.clear()
        self.displayData()

    def rotate_left(self):
        print "rotate left"
        if self.position > 0:
            self.position -= 1
            self.set_current()

    def rotate_right(self):
        print "rotate right"
        if self.position < len(self.screens)-1:
            self.position += 1
            self.set_current()
    
    def getData(self):
        if self.current != None:
            return self.current.getData()
        return None

    def append(self, provider):
        if isinstance(provider, LedwandProvider):
            self.screens.append(provider)
            if len(self.screens) == 1:
                self.position = 0
                self.set_current()
        else:
            print "provided object is not instance of LedWandProvider"


def getkey():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
        new[6][TERMIOS.VMIN] = 1
        new[6][TERMIOS.VTIME] = 0
        termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
        c = None
        try:
                c = os.read(fd, 1)
        finally:
                termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
        return c

def main():
    cube = ScreenCube()
    cube.append(vbbregex.VbbRequest())
    cube.append(weatherregex.WeatherRequest())
    t = UpdateThread(cube)
    t.start()
    while 1:
        c = getkey()
        if c == "a":
            cube.rotate_left()
        elif c == "d":
            cube.rotate_right()
        elif c == "c":
            t.Killed = True
            exit()
        else:
            print ord(c)
            
    
if __name__ == "__main__":
    main()
