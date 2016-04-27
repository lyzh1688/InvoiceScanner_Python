__author__ = 'Yuezhi.Liu'
import sys
sys.path.append("..")
import RunLenMark
import ExternalRect as rc
import cv2 as cv
from scan.algorithm.util import utils as ut

#RELATIVE_POS = ut.enum('A,B,C,D')

class RunLenSet():
    def __init__(self,runLenSet,threshold):
        #self.allRunLenMark = runLenSet
        self.runLenSet = runLenSet
        self.MaxStrokNum = threshold['MaxStrokNum']
        self.MaxDistance = threshold['MaxRLDistance']
        self.MinRLDistance = threshold['MinRLDistance']

        self.HJoinMax = threshold['HJoinMax']
        self.VJoinMax = threshold['VJoinMax']
        self.MinHeight = threshold['MinHeight']
        self.H_Offset = threshold['H_Offset']
        self.V_Offset = threshold['V_Offset']
        self.externalRectDict = {}

    def reflagRunLengthMark(self):
        #print self.runLenSet
        for i in range(len(self.runLenSet)):
            rowList = self.runLenSet[i]['RLRowList']
            for j in range(len(rowList)):
                rightStrok,endPix = self.__calcRightBlackRL(i,j)
                leftStrok,startPix = self.__calcLeftBlackRL(i,j)
                curLeft = rowList[j].start
                curRight = rowList[j].end
                flag = self.__calcRunLengthMarkType(curLeft,curRight,rightStrok,leftStrok,endPix,startPix,rowList[j].flag)
                self.runLenSet[i]['RLRowList'][j].flag = flag


    def join(self):
        self.__horizontalJoin()
        group = self.__verticalJoin()
        groupIdList = self.__getGroupIdList()
        return groupIdList

    def __getGroupIdList(self):
        groupIdList = []
        for i in range(len(self.runLenSet)):
            for item in self.runLenSet[i]['RLRowList']:
                if item.group not in groupIdList:
                    groupIdList.append(item.group)
        return groupIdList

    def calcExternalRects(self):
        self.reflagRunLengthMark()
        groupIdList = self.join()
        self.externalRectDict = rc.ExternalRect.calcExternalRect(self.runLenSet,groupIdList)
        return self.filterExternalRect(self.externalRectDict)
        #return self.externalRectDict

    def filterExternalRect(self,externalRectDict):
        externalRects = rc.ExternalRect.sort(externalRectDict)

        for item_a in externalRects:
            if item_a.isKeep == False:
                continue
            for item_b in externalRects:
                if item_b.isKeep == False:
                    continue

                if item_a.canMerge(item_b,self.H_Offset,self.V_Offset) == True:
                    item_a.merge(item_b)

        for extRect in externalRects:
            if (extRect.bottom - extRect.top) < self.MinHeight or (extRect.right - extRect.left) < (extRect.bottom - extRect.top):
                extRect.isKeep = False

        #return externalRects
        '''
        for item_a in externalRects:
            if item_a.isKeep == False:
                continue
            for item_b in externalRects:
                if item_b.isKeep == False:
                    continue

                if item_a.isOverlap(item_b) == True:
                    item_a.merge(item_b)
                else:
                    if item_a.isNear(item_b,self.VJoinMax) == True:
                        item_a.merge(item_b)
        '''
                #if item_a.isOverlap(item_b) == True:
                #   item_a.merge(item_b)
                #if item_a.isNear(item_b,self.VJoinMax) == True:
                #   item_a.merge(item_b)
        return  filter(lambda item:item.isKeep == True,externalRects)


        #print externalRects
        #for exrect in externalRects:
        #    print 'top : %d,left : %d'%(exrect.top,exrect.left)

    def __verticalJoin(self):
        group = 0
        for i in range(len(self.runLenSet)):
            for j in range(len(self.runLenSet[i]['RLRowList'])):
                if(self.runLenSet[i]['RLRowList'][j].isSet == False):
                    group += 1
                    self.__deepSearch(i,j,group)
        return group

    def __deepSearch(self,currentI,currentJ,group):
        current = self.runLenSet[currentI]['RLRowList'][currentJ]
        current.group = group
        if currentI >= len(self.runLenSet) - 1:
            return
        else:

            for k in range(self.VJoinMax):
                i = currentI + k + 1
                if i >= len(self.runLenSet) - 1:
                    return
                for j in range(len(self.runLenSet[i]['RLRowList'])):
                    next = self.runLenSet[i]['RLRowList'][j]
                    if True == self.__isConnect(current,next):
                        if next.isSet == False:
                            next.isSet = True
                            next.group = current.group
                            self.__deepSearch(i,j,next.group)
                        else:
                            self.__reSetGroup(current.group,next.group)
                    else:
                        if next.isSet == False:
                            break

    def __reSetGroup(self,oldGroup,newGroup):
        for row in self.runLenSet:
            for item in row['RLRowList']:
                if item.group == oldGroup:
                    item.group = newGroup



    def __isConnect(self,current,next):
        if(isinstance(current,RunLenMark.RunLenMark) == True and isinstance(next,RunLenMark.RunLenMark)):
            if((current.start <= next.end) and (current.end >= next.start)):
                return True
            else:
                return False

    def __horizontalJoin(self):
        for i in range(len(self.runLenSet)):
            rowList = self.runLenSet[i]['RLRowList']
            cur = 0
            for j in range(len(rowList) - 1):
                if abs(rowList[cur].end - rowList[j + 1].start) <= self.HJoinMax:
                    rowList[cur].end = rowList[j + 1].end
                    rowList[j + 1].isSet = True
                else:
                    cur = j
            self.runLenSet[i]['RLRowList'] = filter(lambda item:item.isSet != True,self.runLenSet[i]['RLRowList'])
        '''
        srcTestImg = cv.imread('C:/Project/invoiceScan/pic/A/1.1500007-r.png')
        for i in range(len(self.runLenSet)):
            rowList = self.runLenSet[i]['RLRowList']
            for j in range(len(rowList)):
                if j % 5 == 0:
                    cv.line(srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(0,255,0),1)
                elif j % 5 == 1:
                    cv.line(srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(0,0,255),1)
                elif j % 5 == 2:
                    cv.line(srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(255,0,255),1)
                elif j % 5 == 3:
                    cv.line(srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(255,255,0),1)
                elif j % 5 == 4:
                    cv.line(srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(255,0,0),1)

        cv.imshow('horizontalJoin',srcTestImg)
        '''


    def __calcRunLengthMarkType(self,curLeft,curRight,rightStrok,leftStrok,endPix,startPix,currentType):
        if currentType == 0:
            #return 0
            midPix = (curRight - curLeft) / 2
            if ((endPix - startPix) < self.MaxDistance) \
                    or (( midPix - endPix) < self.MaxDistance and ( midPix - endPix) > self.MinRLDistance) \
                    or (( startPix - midPix) < self.MaxDistance and ( startPix - midPix) > self.MinRLDistance):
                return 0
            else:
                return 255

        else:
            if ((endPix - startPix) < self.MaxDistance) :
                    #and (rightStrok == self.MaxStrokNum and leftStrok == self.MaxStrokNum):
                return 0
            else:
                return 255

    def __calcRightBlackRL(self,i,j):
        strokNum = 0
        RLRowList = self.runLenSet[i]['RLRowList']
        current = j + 1
        while (current < len(RLRowList) and (strokNum < self.MaxStrokNum)):
            if(RLRowList[current].flag == 0):
                strokNum += 1
            current += 1
        return strokNum,RLRowList[current - 1].end

    def __calcLeftBlackRL(self,i,j):
        strokNum = 0
        RLRowList = self.runLenSet[i]['RLRowList']
        current = j - 1
        while (current > 0 and (strokNum < self.MaxStrokNum)):
            if(RLRowList[current].flag == 0):
                strokNum += 1
            current -= 1
        return strokNum,RLRowList[current + 1].start

if __name__ == '__main__':
    i1 = RunLenMark.RunLenMark(0,3,0,0)
    i2 = RunLenMark.RunLenMark(5,7,0,0)
    i3 = RunLenMark.RunLenMark(12,16,0,0)
    i4 = RunLenMark.RunLenMark(2,6,1,0)
    i5 = RunLenMark.RunLenMark(10,13,1,0)
    i6 = RunLenMark.RunLenMark(14,17,1,0)
    i7 = RunLenMark.RunLenMark(5,8,2,0)
    i8 = RunLenMark.RunLenMark(9,11,2,0)
    i9 = RunLenMark.RunLenMark(1,6,3,0)
    i10 = RunLenMark.RunLenMark(7,10,3,0)
    i11 = RunLenMark.RunLenMark(4,8,4,0)
    i12 = RunLenMark.RunLenMark(18,20,0,0)
    i13 = RunLenMark.RunLenMark(19,22,1,0)

    rlList1 = []
    rlList = []
    rlList1.append(i1)
    rlList1.append(i2)
    rlList1.append(i3)
    rlList1.append(i12)
    rlrow1 = {'Row':0,'RLRowList':rlList1}

    rlList2 = []
    rlList2.append(i4)
    rlList2.append(i5)
    rlList2.append(i6)
    rlList2.append(i13)
    rlrow2 = {'Row':1,'RLRowList':rlList2}

    rlList3 = []
    rlList3.append(i7)
    rlList3.append(i8)
    rlrow3 = {'Row':2,'RLRowList':rlList3}

    rlList4 = []
    rlList4.append(i9)
    rlList4.append(i10)
    rlrow4 = {'Row':3,'RLRowList':rlList4}

    rlList5 = []
    rlList5.append(i11)
    rlrow5 = {'Row':4,'RLRowList':rlList5}

    rlList.append(rlrow1)
    rlList.append(rlrow2)
    rlList.append(rlrow3)
    rlList.append(rlrow4)
    rlList.append(rlrow5)

    rl = RunLenSet(rlList,3,200,10)

    rl.calcExternalRects()

    for key in rl.externalRectDict.keys():
        print 'top:%d,left:%d,bottom:%d,right:%d'%\
            (rl.externalRectDict[key].top,rl.externalRectDict[key].left,rl.externalRectDict[key].bottom,rl.externalRectDict[key].right)
