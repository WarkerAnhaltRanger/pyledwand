# -*- coding: utf-8 -*-
import re
import time
from ledwandutil import *

'''
----------------------------------------------------------------------------
"THE BEER-WARE LICENSE" (Revision 42):
Warker wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return

Follow me on twitter @warker
----------------------------------------------------------------------------

VBB requester for LED-Screen at CCCB
'''


HTMLCODES = [
        ["&#246;", "ö"],
        ["&#252;", "ü"],
        ["&#228;", "ä"],
        ["&#214;", "Ö"],
        ["&#220;", "Ü"],
        ["&#196;", "Ä"],
        ["&#223;", "ß"]
    ]

def subHtmlcode(s, code=HTMLCODES):
    for c in code:
        s = s.replace(c[0], c[1].decode("utf8").encode("iso-8859-1"))
    return s

class VbbFahrt:
    def __init__(self, name, time, timeis, dest, platform, diff = 0):
        self.Name, self.Time, self.Timeis, self.Dest, self.Platform, self.Diff = name, time, timeis, dest, platform, diff 

    def __repr__(self):
        self.Dest = self.Dest.replace("(Berlin)", "")
        if len(self.Timeis) <= 0:
            self.Timeis = "        "
        if len(self.Platform) > 3: #some vbb request are just wrong
            self.Platform = " "
        if len(self.Platform) > 0:
            res = "%2s %4s %8s %s" %(self.Platform, self.Name, `self.Diff`+"min", self.Dest)
            #res = "%2s %4s %-30s %s%8s" %(self.Platform, self.Name, self.Dest, "+", `self.Diff`+"min")
        else:
            res = "   %4s %8s %s" %(self.Name, `self.Diff`+"min", self.Dest)
            #res = "   %4s %-30s %8s" %(self.Name,  self.Dest, "+", `self.Diff`+"min")
        return res.replace("&nbsp;", "");

class VbbRequest(LedwandProvider):
    def __init__(self, url = "http://www.vbb-fahrinfo.de/hafas/stboard.exe/dn?", stop="S+U Friedrichstr. Bhf (Berlin)", howmany=20, futuretime=8):
        LedwandProvider.__init__(self)
        self.Url = url 
        self.Stop = stop
        self.Howmany = howmany
        self.List = list()
        self.Ftime = futuretime

    def getHtml(self):
        t = time.localtime()
        m, h = t.tm_min + self.Ftime, 0
        while m > 60:
            m = m / 60
            h += 1
        h = (h + t.tm_hour)%24
        return HttpRequest(self.Url, {"boardOverview":"yes", "maxJourneys":self.Howmany, "boardType":"dep", "input":self.Stop, "start":"Start", "time":"%s:%s"%(h,m), "start":"Erstellen"})        

    def getData(self):
        self.clear()
        self.List.append("Haltestelle %s %s" %(self.Stop.replace("(Berlin)", ""), time.strftime("%H:%M")))
        self.List.append("%2s %4s %8s %s" %("Gl", "Typ", "Ankunft", "Richtung"))
        data = subHtmlcode(re.sub(r"[\t\r\n]","", self.getHtml().replace("&nbsp;",""))).decode("iso-8859-1").encode("utf8")
        m = re.findall(r"<tr class=\"depboard-\w+\".*?>.*?</tr>", data)
        for match in m:
            m1 = re.search(r"<td class=\"time\">(?P<time>.*?)</td>(<td class=\"prognosis(.*?/><img.*?/>|.*?\"><img.*?/>|.*?\">)(ca.)?(?P<timeis>.*?)</td>)?<td class=\"product\">.*?/> *(?P<name>[A-Z0-9]*)</a></td><td class=\"timetable\"><strong>(?P<to>.*?)</strong>.*?</td>(<td class=\"platform\">(?P<platform>.+?)( *<br.*?)?</td>)?", match)
            if m1 != None:
                obj = VbbFahrt(m1.group("name"), m1.group("time"), m1.group("timeis"), m1.group("to"), m1.group("platform"))
                if obj.Timeis is None: # Sometimes there is no predicted time, so we repair
                    obj.Timeis = ""
                if obj.Platform is None:
                    obj.Platform = ""
                if obj.Timeis != "&nbsp;" and len(obj.Timeis) > 0: #debug
                    obj.Diff = self.timediffinmin(obj.Timeis) # debug
                else:
                    obj.Diff = self.timediffinmin(obj.Time)

                ''' Filter for arrivals > 0min'''
                if obj.Diff > 0:
                    self.List.append(obj)
            else:
                print "MISSED:", match
        return self.List

    def clear(self):
        self.Ledwand.clear()
        self.List = list()

    def timediffinmin(self, timestr):
        t = time.localtime()
        if ":" in timestr:
            d = time.strptime(timestr, "%H:%M")
            diff = (d.tm_hour - t.tm_hour)*60 + (d.tm_min - t.tm_min)
            return diff
        return -1

if __name__ == "__main__":
    vbb = VbbRequest(futuretime=5)
    vbb.Ledwand.setbrightness(6)
    vbb.Ledwand.clear()
    while(1):
        vbb.clear()
        vbb.displayData()
        time.sleep(30)
