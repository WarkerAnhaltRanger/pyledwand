#!/usr/bin/python
import gst
from imaging import ImageLedwand
import ImageFilter
import gobject
import Image
from threading import Thread
import sys
import os
import time

loop = None

class LedwandSink(gst.BaseSink):
    __gsttemplates__=(
        gst.PadTemplate("sink",
                        gst.PAD_SINK,
                        gst.PAD_ALWAYS,
			gst.Caps("video/x-raw-gray, width=448, height=240")),
        )

    def __init__(self, name):
        self.__gobject_init__()
        self.set_name(name)
        self.ledwand = ImageLedwand(timeout=1) #30fps = 0.033s/7Parts~=4ms
        self.Image = Image.new("L", (448, 240))
        self.ledwand.setbrightness(4)
        self.ledwand.clear()
        self.FrameCount = 0.0
	self.FramesDrawn = 0.0
	self.TargetFPS = 25.0
	self.nextFrame = 0.0
	self.frameDelta = 1.0/self.TargetFPS

    def do_render(self, buf):
        ''' HIER MUSS FRAMEDROPPING HIN'''
	#if self.nextFrame == 0.0:
	#    self.nextFrame = time.time()
	#t = time.time()
	#self.FrameCount += 1.0
	#if (t-0.1 <= self.nextFrame):
	#    self.FramesDrawn += 1.0
	#    print "current framerate: %.2ffps\r" % ((self.FramesDrawn/self.FrameCount)*self.TargetFPS),
        self.Image.fromstring(buf)
        img = self.Image.filter(ImageFilter.EDGE_ENHANCE).convert("1")
        self.ledwand.drawImage2(self.flat(img))
	    #self.Framecount += self.Framedrop
	#self.nextFrame += self.frameDelta
	#self.Image.fromstring(buf)
	#img = self.Image.filter(ImageFilter.EDGE_ENHANCE).convert("1")
	#self.ledwand.drawImage4(self.flat(img))
        return gst.FLOW_OK

    def flat(self, img):
        return str(bytearray(list(img.getdata())))

class MyPlayer:
    def __init__(self, filepath):
        self.player = gst.element_factory_make("playbin2")
        self.player.set_property("uri", "file://" +filepath)
        self.player.set_property("flags",  0x01)
        #sink = gst.element_factory_make("aasink")
        #sink = gst.element_factory_make("xvimagesink")
        sink = LedwandSink("sink")
        #zero = gst.element_factory_make("fakesink")
        #self.player.set_property("audio_sink", zero)
        self.player.set_property("video_sink", sink)
        bus = self.player.get_bus()
        bus.add_watch(self.on_message)

    def on_message(self, bus, message):
        global loop
        t = message.type
        if t == gst.MESSAGE_EOS:
                self.player.set_state(gst.STATE_NULL)
                print "EOS"
                loop.quit()
        elif t == gst.MESSAGE_ERROR:
                self.player.set_state(gst.STATE_NULL)
                err, debug = message.parse_error()
                print "Error: %s" % err, debug
                loop.quit()
        return True

    def play(self):
        print "playing"
        self.player.set_state(gst.STATE_PLAYING)

def main():
    global loop
    gobject.type_register(LedwandSink)

    args = sys.argv
    if len(args) < 2:
        print "Keine quelle angegeben"
        quit()

    inp = args[1]
    if inp.startswith("http"):
	filepath = inp
    else:
        filepath = os.path.abspath(inp)
    
    print "started main"
    mp = MyPlayer(filepath)
    mp.play()
    loop = gobject.MainLoop()
    try:
        loop.run()
    except:
        pass
    print "closing"

if __name__ == "__main__":
    main()
