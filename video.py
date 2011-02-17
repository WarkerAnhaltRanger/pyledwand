import gst
from imaging import ImageLedwand
import gobject
import Image

'''
Todo: Optimierungen:    -zu viele setpixel aufrufe!
                                            -konvertierung ohne Image
'''

class LedwandSink(gst.BaseSink):
    __gsttemplates__=(
        gst.PadTemplate("sink",
                        gst.PAD_SINK,
                        gst.PAD_ALWAYS,
                        gst.Caps("video/x-raw-gray, bbp=8,width=448, height=160")),
        )

    def __init__(self, name):
        self.count = 0
        self.__gobject_init__()
        self.set_name(name)
        self.ledwand = ImageLedwand(timeout=1) #30fps = 0.033s/7Parts~=4ms
        self.Image = Image.new("L", (448, 160))
        self.ledwand.setbrightness(8)
        self.Fps = 5
        
    def do_render(self, buffer):
        '''width = buffer.caps[0]["width"]
            height = buffer.caps[0]["height"]
            colorbits = buffer.size/width/height*8.0
            print "Size", buffer.size, "width", width, "height", height, "colorbits", colorbits'''
        if self.count % 7 == 0:
            self.Image.fromstring(buffer)
            self.ledwand.drawImage(self.Image)
        self.count += 1
        return gst.FLOW_OK

class MyPlayer:
    def __init__(self, filepath):
        self.player = gst.element_factory_make("playbin2")
        self.player.set_property("uri", "file://" + filepath)
        #sink = gst.element_factory_make("aasink")
        sink = LedwandSink("sink")
        self.player.set_property("video_sink", sink)
        bus = self.player.get_bus()
        bus.add_watch(self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
                self.player.set_state(gst.STATE_NULL)
                print "EOS"
                quit()
        elif t == gst.MESSAGE_ERROR:
                self.player.set_state(gst.STATE_NULL)
                err, debug = message.parse_error()
                print "Error: %s" % err, debug
                quit()
        return True

    def play(self):
        print "playing"
        self.player.set_state(gst.STATE_PLAYING)

def main():
    gobject.type_register(LedwandSink)
    filepath = "/home/warker/Desktop/cccb/pyledwand/video.mpeg"
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
