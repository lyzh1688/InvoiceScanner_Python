#coding=utf-8
import sys
sys.path.append("..")
from scan.algorithm import ScanAction as baseAction
import cv2 as cv
import numpy as np
import RunLenMark
import RunLenSet

class RunLenAction(baseAction.ScanAction):
    def __init__(self,fileName,imgType):
        baseAction.ScanAction.__init__(self,fileName,imgType)
        #self.blackRL = []
        #self.whiteRL = []
        self.RLSet = []
        self.externalRectDict = {}
        #self.verticalLine = []
        self.__removeVerticalLine()
        self.__getAllRunLen()

        #self.__reflagRunLen(self.RLSet)
        #self.drawLine()
        #cv.imshow('lineImg',self.srcImg)

    def doSplitAction(self):
        rlSet = RunLenSet.RunLenSet(self.RLSet,self.thresholdDict)
        '''
        rlSet.reflagRunLengthMark()

        for i in range(len(rlSet.runLenSet)):
            rowList = rlSet.runLenSet[i]['RLRowList']
            for j in range(len(rowList)):
                if rowList[j].flag == 0:
                    cv.line(self.srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(0,255,0),1)
                else:
                    cv.line(self.srcTestImg,(rowList[j].start,rowList[j].y),(rowList[j].end,rowList[j].y),(0,0,255),1)

        cv.imshow('runlen',self.srcTestImg)
        '''
        self.externalRects = rlSet.calcExternalRects()
        return self.externalRects

    def __FillWhitePix(self,startPx,endPx,col):
        #cv.line(self.srcImg,startPx,endPx,(0,255,0),1)
        #print startPx,endPx,col
        k = startPx
        while k <= endPx:
            self.srcGrayImg[k][col] = 255
            k += 1

    def __removeVerticalLine(self):
        i = 0
        j = 0
        while (i < self.col):
            j = 0
            pixStart = j
            pixEnd = j
            while (j < self.row - 1):
                if (self.srcGrayImg[j][i] == self.srcGrayImg[j + 1][i]):
                    j += 1
                else:
                    #the last white pix
                    if self.srcGrayImg[j][i] == 255:
                        j += 1
                        pixStart = j
                        pixEnd = j
                    #the last balck pix
                    else:
                        if (j - pixStart) > self.thresholdDict['MaxRLHeight']:
                            pixEnd = j
                            self.__FillWhitePix(pixStart,pixEnd,i)
                            #verticalLineItem = RunLenMark.VerticalLine((i,pixStart),(i,pixEnd))
                            #self.verticalLine.append(verticalLineItem)
                    j += 1
            i += 1

    #setp 1
    #find all RLs and save it in RLSet
    def __getAllRunLen(self):
        print 'rol : %d,col : %d'%(self.row,self.col)
        i = 0
        while (i < self.row):
            j = 0
            pixStart = j
            k = pixStart
            RLRowList = []
            while(k < self.col - 1):
                if self.srcGrayImg[i][k] == self.srcGrayImg[i][k + 1]:
                      k += 1
                else:
                    if (k - pixStart) < self.thresholdDict['MaxRLWidth']:
                        runLenMark = RunLenMark.RunLenMark(pixStart,k,i,self.srcGrayImg[i][k])
                        #加入RL队列
                        RLRowList.append(runLenMark)
                        #for test
                        '''
                    if runLenMark.flag == 0:
                        self.blackRL.append(runLenMark)
                    elif runLenMark.flag == 255:
                        self.whiteRL.append(runLenMark)
                    '''
                    pixStart = k + 1
                    k += 1
            if len(RLRowList) > 0:
                self.RLSet.append({'Row':i,'RLRowList':RLRowList})
            i += 1
        self.drawLine()

    def drawRectangle(self,externalRects):
        for item in externalRects:
            cv.rectangle(self.srcImg,
                         (item.left,item.top),
                         (item.right,item.bottom),
                         (255,255,255),1)


        '''
        emptyImage = np.zeros((self.row,self.col,1), np.uint8)

        for rc in self.externalRects:
            cv.rectangle(emptyImage,
                         (rc.left,rc.top),
                         (rc.right,rc.bottom),
                         (255,255,255),-1)
        contours, hierarchy = cv.findContours(emptyImage,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)[-2:]
        cv.drawContours(emptyImage,contours,-1,(255,255,255),1)
        cv.imshow('empty',emptyImage)
        '''
    def drawLine(self):
        #for item in self.blackRL:
        #    cv.line(self.srcImg,(item.start,item.y),(item.end,item.y),(0,255,0),3)
        #for item in self.verticalLine:
        #    cv.line(self.srcImg,item.pxStart,item.pxEnd,(0,255,0),3)
        for i in range(len(self.RLSet)):
            row = self.RLSet[i]['Row']
            for item in self.RLSet[i]['RLRowList']:
                if item.flag == 0:
                    cv.line(self.srcImg,(item.start,row),(item.end,row),(0,255,0),1)
        #cv.imshow('runlen',self.srcImg)

'''
if __name__ == '__main__':
    #filename = 'C:/Project/invoiceScan/pic/A/1.1500007-r.png'
    #filename = 'C:/Project/invoiceScan/pic/A/1.150000002-r.png'
    #filename = 'C:/Project/invoiceScan/pic/A/00021.png'
    filename = 'C:/Project/invoiceScan/pic/A/00022.png'
    #filename = 'C:/Project/invoiceScan/pic/A/002300027.png'
    #filename = 'C:/Project/invoiceScan/pic/A/002300028.png'
    rlAction = RunLenAction(filename,'ab')
    externalRects = rlAction.doSplitAction()

    rlAction.drawRectangle(externalRects)
    cv.imshow('rect',rlAction.srcImg)
    cv.waitKey(0)
'''