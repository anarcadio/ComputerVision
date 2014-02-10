#!/usr/bin/env python

import numpy as np
import cv2
import cv2.cv as cv


def get_array(filename):
    acc_file = open( filename, "r" )
    array = []
    first = True
    old_date = 0.0
    for line in acc_file:
        if first:
            aux_date = line.split(":")
            t0 = ((int(aux_date[0])*60 + int(aux_date[1]))*60 + float(aux_date[2])) 
            first = False
        else:
            aux = line.split()
            date_str = aux[1]
            aux_date = date_str.split(":")
            date = ((int(aux_date[0])*60 + int(aux_date[1]))*60 + float(aux_date[2])) - t0
            fline = [float(aux[0]), date]
       
            if date != old_date:
                array.append( fline )
                old_date = date
    acc_file.close()
    return array


def correct_gamma(img, correction):

    temp = img.copy()/255.0
    temp = np.array(temp, dtype=np.float32)
    temp = cv2.pow(temp, 1./correction)*255.0
    return temp

def adjust_levels(im,bot,mid,top):
    lut = np.zeros(256)
    for i in xrange(256):
        if i <= bot:
            lut[i]=0
        elif i >= top:
            lut[i] = 255
        else:
            lut[i]=255*(i-bot)/(top-bot)
    aux = cv2.LUT(im, lut)
    aux = np.array(aux, dtype=np.uint8)
    if mid < 0.1:
        mid = 0.1
    aux = correct_gamma(aux, mid)
    aux = np.array(aux, dtype=np.uint8)
    #aux = cv2.equalizeHist(aux)
    return aux

def autolevels(im, mid=1):
    inf = np.percentile(im,1)
    sup = np.percentile(im,99)
    return adjust_levels(im, inf,mid,sup)

def draw_hist(im, name):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    y = 255 -y
    cv2.imshow(name, y)


if __name__ == '__main__':

    import sys
    try: 
        name = sys.argv[1]
        illuname = sys.argv[2]
    except: 
        print("Error, introduce nombre del archivo de entrada")
        sys.exit()
    cap = cv2.VideoCapture(name)
    array = get_array(illuname)
    fps = 22
    i = 0
    ret = True
    while(1):
        ret,frame = cap.read()
        t = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)/1000
        #t = t*1.197
        if ret:
            i = 0
            while i < len(array)-1:
                if (array[i][1]<=t) and (t<array[i+1][1]):
                    break
                i = i+1
            lux = array[i][0]
            if lux > 400:
                lux = 400
            k = pow((lux/400),1./4)
            x = -2*k+1
            y = pow(10,x)

        
            gr =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            out = autolevels(gr, y)
            cv2.imshow('Sensor-in',gr)
            cv2.imshow("Sensor-out", out)
            #draw_hist(gr, "hist_in")
            #draw_hist(out, "hist_out")
        
            c = cv2.waitKey(33)
            if (c==27): ret =False
