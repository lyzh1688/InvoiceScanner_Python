__author__ = 'Yuezhi.Liu'

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
        if 'BLOCK_SIZE' in self.thresholdDict.keys() and 'MINUS_PARAM' in self.thresholdDict.keys():
            #self.grayImg = cv.threshold(srcGrayImg,self.thresholdDict['GRAY_THRESH'],255,cv.THRESH_BINARY )[1]
            self.grayImg = cv.adaptiveThreshold(srcGrayImg, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,
                                                self.thresholdDict['BLOCK_SIZE'], self.thresholdDict['MINUS_PARAM'])

            # Some morphology to clean up image
            #kernel = np.ones((5,5), np.uint8)
            #self.grayImg = cv.morphologyEx(filtered, cv.MORPH_OPEN, kernel)
            #self.grayImg = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)

            #cv.imshow('filtered',filtered)
            #kernel = cv.getStructuringElement(cv.MORPH_RECT,(2, 2))
            #self.grayImg= cv.dilate(filtered,kernel)
            #self.grayImg = cv.dilate(erode,kernel)
            cv.imshow('srcGrayImg',self.grayImg)

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

