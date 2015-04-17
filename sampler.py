import numpy as np
import matplotlib.pyplot as pl

import sys, cv2
import copy
import os

Rect = []
img_type = []
type_ = 1

# mouse callback function
def get_coordinates(event,x,y,flags,param):
    global Rect,img_type,type_
    if event == cv2.EVENT_LBUTTONDOWN:
        Rect.append((x,y))
        img_type.append(type_)

def main():
    global Rect,img_type,type_
    number_of_sample = 0
    directory = '.'
    files = os.listdir(directory)
    images = filter(lambda x: x.endswith('.jpeg'), files)
    for image in images:
        cv2.namedWindow('image')
        cv2.setMouseCallback('image',get_coordinates)
        img = cv2.imread(image,1)
        img_ = copy.deepcopy(img)
        m,n,k = img.shape
        print 'file name: ' + image
        print 'image size: ' + str(m)+' '+str(n)+' '+str(k)
        img = cv2.resize(img,(n/6,m/6))
        img2_ = copy.deepcopy(img)
        print 'size of resize image: '+ str(m/6)+' '+str(n/6)
        Rect = []
        img_type = []
        while(1):
            cv2.imshow('image',img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('r'):
                Rect = []
                img_type = []
                img = copy.deepcopy(img2_)
                continue
            elif k == 27:
                cv2.destroyAllWindows()
                return
            elif k == ord('n'):
                for i in xrange(0,len(Rect)-1,2):
                   x_1 = min(Rect[i][0],Rect[i+1][0]) * 6
                   x_2 = max(Rect[i][0],Rect[i+1][0]) * 6
                   y_1 = min(Rect[i][1],Rect[i+1][1]) * 6
                   y_2 = max(Rect[i][1],Rect[i+1][1]) * 6
                   roi = img_[y_1:y_2,x_1:x_2]
                   cv2.imwrite(str(number_of_sample)+'_'+str(img_type[i])+'.jpg',roi)
                   number_of_sample += 1
                Rect = []
                img_type = []
                break
            elif k == ord('t'):
                if type_ == 1:
                    type_ = 0
                elif type_ == 0:
                    type_ = 1

            for i in xrange(0,len(Rect)-1,2):
                     print len(Rect)
                     print len(img_type)
                     print i
                     x_1 = min(Rect[i][0],Rect[i+1][0])
                     x_2 = max(Rect[i][0],Rect[i+1][0])
                     y_1 = min(Rect[i][1],Rect[i+1][1])
                     y_2 = max(Rect[i][1],Rect[i+1][1])
                     if img_type[i] == 1:
                         cv2.rectangle(img,(x_1,y_1),(x_2,y_2),(0,255,0),1) 
                     elif img_type[i] == 0:
                         cv2.rectangle(img,(x_1,y_1),(x_2,y_2),(255,0,0),1) 

        cv2.destroyAllWindows()
        



if __name__ == "__main__":
    main()
