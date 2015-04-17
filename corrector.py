import argparse
import numpy as np
import matplotlib.pyplot as pl

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.utils.multiclass import unique_labels
from sklearn import cross_validation
from sklearn.decomposition import PCA
from sklearn import metrics

import sys, cv2
import os


def main():
    directory = '.'
    treshold_val = 10 
    kernel = np.ones((30,30),np.uint8)
    kernel_ = np.ones((50,50),np.uint8)
    files = os.listdir(directory)
    images = filter(lambda x: x.endswith('.jpeg'), files)
    clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
    for image in images:
        img = cv2.imread(image,0)
        img = clahe.apply(img)
        img = clahe.apply(img)
        #pl.hist(img.ravel(),256,[0,256]); pl.show()
        
        #img = cv2.GaussianBlur(img,(11,11),0)
        img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        img = cv2.erode(img,kernel_,iterations=1)
        #img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
        img = cv2.GaussianBlur(img,(31,31),4)
        #img = cv2.dilate(img,kernel,iterations=2)
        #img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
        img = clahe.apply(img)
        cv2.imwrite('new_'+image,img)

if __name__ == "__main__":
    main()
