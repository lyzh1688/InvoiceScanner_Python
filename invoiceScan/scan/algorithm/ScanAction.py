import settings
import cv2 as cv
import numpy as np
class ScanAction():
    def __init__(self,file,imgType):
        #self.thresholdDict = {}
        self.thresholdDict = self.loadSettins(imgType)
        srcGrayImg = None
        if isinstance(file,str):
            srcGrayImg = cv.imread(file,cv.IMREAD_GRAYSCALE).astype(np.uint8);
        else:
            srcGrayImg = file
        srcGrayImg = cv.resize(srcGrayImg,(self.thresholdDict['COL'],self.thresholdDict['ROW']))
        self.srcImg = srcGrayImg
        if 'GRAY_THRESH' in self.thresholdDict.keys():
            self.grayImg = cv.threshold(srcGrayImg,self.thresholdDict['GRAY_THRESH'],255,cv.THRESH_BINARY )[1]

            #cv.imshow('srcGrayImg',self.grayImg)
            #kernel = cv.getStructuringElement(cv.MORPH_RECT,(2, 2))
            #self.grayImg = cv.erode(self.grayImg,kernel)
            #self.grayImg = cv.dilate(self.grayImg,kernel)
            #cv.imshow('erode',self.grayImg)

        self.srcGrayImg = self.grayImg.tolist()
        #cv.imshow('srcGrayImg',self.grayImg)
        self.imgType = imgType
        self.lineImgList = []
        self.row,self.col = srcGrayImg.shape

    def loadSettins(self,imgType):
        if imgType in settings.RUN_LEN_THRESHOLD.keys():
            threDict = settings.RUN_LEN_THRESHOLD[imgType]
        else:
            threDict = settings.RUN_LEN_THRESHOLD['DEFAULT']
        return threDict

    def doSplitAction(self):
        return {};

