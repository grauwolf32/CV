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
    files = os.listdir(directory)
    images = filter(lambda x: x.endswith('.jpeg'), files)
    for image in images:
        img = cv2.imread(image,1)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        min_val = []
        max_val = []
        m,n = gray.shape
        for index in xrange(0,m):
            tmp_min = 255
            tmp_max = 0
            for jndex in xrange(0,n):
                if tmp_min > gray[index][jndex] and gray[index][jndex] > treshold_val:
                    tmp_min = gray[index][jndex]
                if tmp_max < gray[index][jndex]:
                    tmp_max = gray[index][jndex]
            min_val.append(tmp_min)
            max_val.append(tmp_max)

        robust_min_value = min(min_val)
        robust_max_value = max(max_val)
        print 'robust min val: '
        print robust_min_value
        print 'robust max val: '
        print robust_max_value

        alpha = float(255) / (robust_min_value - robust_max_value + 1)
        beta  = 255 - int(alpha*robust_max_value)
        for index in xrange(0,m):
            for jndex in xrange(0,n):
                if gray[index][jndex] > 0 :
                    gray[index][jndex] = int(gray[index][jndex]*alpha) + beta
        cv2.imwrite('new_'+image,gray)

if __name__ == "__main__":
    main()
