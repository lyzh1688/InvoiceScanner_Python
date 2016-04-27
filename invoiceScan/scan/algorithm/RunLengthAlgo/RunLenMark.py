__author__ = 'Yuezhi.Liu'
class RunLenMark(object):
    def __init__(self,start,end,y,flag,isSet = False):
        self.start = start;
        self.end = end;
        self.y = y;
        self.flag = flag;
        self.isSet = False;
        self.group = 0

class VerticalLine(object):
    def __init__(self,pxStart,pxEnd):
        self.pxStart = pxStart
        self.pxEnd = pxEnd