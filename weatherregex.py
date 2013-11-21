# -*- coding: utf-8 -*-
import re
from ledwandutil import *

HTMLCODES = [
    ["&ouml;", "ö"],
    ["&auml;", "ä"],
    ["&uuml;","ü"],
    ["&deg;", "°"]
    ]


class WeatherObj:
    def __init__(self, mintemp, maxtemp, vormittag, nachmittag, abend):
        self.Min = mintemp
        self.Max = maxtemp
        self.Vormittag = vormittag
        self.Nachmittag = nachmittag
        self.Abend = abend

    def __repr__(self):
        res = "%5s %5s %-12s %-12s %-12s"%(self.Min, self.Max, self.Vormittag, self.Nachmittag, self.Abend)
        return res


class WeatherRequest(LedwandProvider):
    def __init__(self, url="http://m.wetteronline.de/cgi-bin/city",  plz=14109):
        LedwandProvider.__init__(self)
        self.Url = url
        self.Plz = str(plz)
        self.List = list()
        self.tPlz = self.Plz

    def getHtml(self):
        return HttpRequest(self.Url, {"L":"dep"+self.Plz})

    def getData(self):
        self.Ledwand.clear()
        self.List = list()
        count = 0
        orgPlz = self.tPlz
        self.List.append("Wettervorhersage  für Postleitzahlenbereich:" + orgPlz)
        self.List.append("%-5s %-5s %-12s %-12s %-12s"%("Min", "Max", "Vormittag", "Nachmittag", "Abend"))
        while count < 4:
            self.Plz = orgPlz + "0" + `count`
            data = subHtmlcode(re.sub(r"[\t\r\n]","",self.getHtml()), HTMLCODES)
            m = re.findall(r"<div class=\"city\">.*?</table>", data)
            for match in m:
                #print match
                m1 = re.search(r"<td class=\"mintemp\".*?>(?P<mintemp>.*?)</td>.*?<td class=\"maxtemp\".*?>(?P<maxtemp>.*?)</td>.*?<img.*?alt=\"(?P<vormittag>.*?)\".*?></td>.*?<img.*?alt=\"(?P<nachmittag>.*?)\".*?></td>.*?<img.*?alt=\"(?P<abend>.*?)\".*?></td>",match)
                #print m1.group("mintemp"), m1.group("maxtemp"),  m1.group("vormittag"), m1.group("nachmittag"), m1.group("abend")
                obj = WeatherObj(m1.group("mintemp"), m1.group("maxtemp"),  m1.group("vormittag"), m1.group("nachmittag"), m1.group("abend"))
                self.List.append(obj)
            count += 1
        return self.List


if __name__ == "__main__":
    weather = WeatherRequest()
    weather.Ledwand.clear()

    weather.displayData()
