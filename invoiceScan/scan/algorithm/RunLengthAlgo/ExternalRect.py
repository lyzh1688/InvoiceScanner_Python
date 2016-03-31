import cv2 as cv

class ExternalRect(object):

    def __init__(self,left = -1,top = -1,right = -1,bottom = -1):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.isKeep = True

    def __str__(self):
        return 'left :%d,top :%d,right :%d,bottom :%d'%(self.left,self.top,self.right,self.bottom)

    def __cmp__(self, other):
        if self.top == other.top:
            return cmp(self.left,other.left)
        return cmp(self.top,other.top)

    def  merge(self,other):
        if self != other:
            self.top = min(self.top,other.top)
            self.left = min(self.left,other.left)
            self.bottom = max(self.bottom,other.bottom)
            self.right = max(self.right,other.right)
            other.isKeep = False

    def canMerge(self,other,h_offset,v_offset):
        if abs(self.left - other.left) < h_offset or abs(self.right - other.right) < h_offset:
            if (self.right - self.left) / 2 < (other.right - other.left):
                if abs(other.top - self.bottom) < v_offset:
                    return True

        return False

    def isNear(self,other,threshold):
        if self != other:

            if threshold > abs(self.left - other.right) >= 0 \
                    and (self.top < other.top < self.bottom  or self.bottom > other.bottom > self.top):
                return True
            if threshold > abs(other.left - self.right) >= 0 \
                    and (self.top < other.top < self.bottom  or self.bottom > other.bottom > self.top):
                return True

            if threshold > abs(self.top - other.bottom) >= 0 and abs(self.left - other.left) < threshold and abs(self.right - other.right) < threshold:
                    #and (self.right > other.right > self.left or self.left < other.left < self.right):
                return  True
            if threshold >abs(other.top - self.bottom) >= 0 and abs(self.left - other.left) < threshold and abs(self.right - other.right) < threshold:
                    #and (self.right > other.right > self.left or self.left < other.left < self.right):
                return True

            return  False

        return False

    def isOverlap(self,other):
        if max((other.left),0) > self.right:
            return False
        if max((other.top),0)> self.bottom:
            return False
        if (other.right) < max(self.left,0):
            return False
        if (other.bottom) < max(self.top,0):
            return False
        colInt = min(other.right ,self.right) - max(other.left, self.left)
        rowInt = min(other.bottom,self.bottom) - max(other.top,self.top)
        if colInt > 0 and rowInt > 0:
            return True
        else:
            return  False

    @staticmethod
    def sort(externalRectDict):
        externalRects = externalRectDict.values()
        externalRects.sort()
        return externalRects

    @staticmethod
    def calcExternalRect(runLenSet,groupidList):
        externalRectDict = {}
        for group in groupidList:
            externalRect = ExternalRect()
            externalRectDict[group] = externalRect

        srcTestImg = cv.imread('C:/Project/invoiceScan/pic/A/1.1500007-r.png')
        for i in range(len(runLenSet)):
            for item in runLenSet[i]['RLRowList']:
                if item.group % 5 == 0:
                    cv.line(srcTestImg,(item.start,item.y),(item.end,item.y),(0,255,0),1)
                elif item.group % 5 == 1:
                    cv.line(srcTestImg,(item.start,item.y),(item.end,item.y),(0,0,255),1)
                elif item.group % 5 == 2:
                    cv.line(srcTestImg,(item.start,item.y),(item.end,item.y),(255,0,255),1)
                elif item.group % 5 == 3:
                    cv.line(srcTestImg,(item.start,item.y),(item.end,item.y),(255,255,0),1)
                elif item.group % 5 == 4:
                    cv.line(srcTestImg,(item.start,item.y),(item.end,item.y),(255,0,0),1)

        cv.imshow('runlen',srcTestImg)
        for i in range(len(runLenSet)):
            for item in runLenSet[i]['RLRowList']:
                if externalRectDict[item.group].left > item.start or externalRectDict[item.group].left == -1:
                    externalRectDict[item.group].left = item.start
                if externalRectDict[item.group].right < item.end or externalRectDict[item.group].right == -1:
                    externalRectDict[item.group].right = item.end
                if externalRectDict[item.group].top > item.y or externalRectDict[item.group].top == -1:
                    externalRectDict[item.group].top = item.y
                if externalRectDict[item.group].bottom < item.y or externalRectDict[item.group].bottom == -1:
                    externalRectDict[item.group].bottom = item.y

        return externalRectDict

if __name__ == '__main__':
    a = ExternalRect(0,0,6,5)
    b = ExternalRect(6,6,8,8)
    if a.isNear(b,2):
        print True
        a.merge(b)
    print a