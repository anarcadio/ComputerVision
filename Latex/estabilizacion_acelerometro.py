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
            date_str = aux[2]
            aux_date = date_str.split(":")
            #date = [int(aux_date[0]), int(aux_date[1]), float(aux_date[2])]
            #get the time in seconds
            date = ((int(aux_date[0])*60 + int(aux_date[1]))*60 + float(aux_date[2])) - t0
            fline = [float(aux[0]), float(aux[1]), date]
            #esto es un poco cutre habria que cambiarlo
            if date != old_date:
                array.append( fline )
                old_date = date
    acc_file.close()
    return array

def calculate_movement(filename):
    array = get_array(filename)
    t0 = 0.0
    x0 = 0.0
    vx0 = 0.0
    y0 = 0.0
    vy0 = 0.0
    dx = [(0.0,0.0)]
    dy = [(0.0,0.0)]
    for line in array:
        ax = line[0]
        ay = line[1]
        t1 = line[2]
        vx1 = vx0 + ax*(t1-t0)
        vy1 = vy0 + ay*(t1-t0)
        x1 = x0 + (vx0 + vx1)*(t1-t0)/2
        y1 = y0 + (vy0 + vy1)*(t1-t0)/2
        dx.append((t1, x1))
        dy.append((t1, y1))
        x0 = x1
        y0 = y1
        t0 = t1
    return dx, dy


if __name__ == '__main__':

    import sys
    try: 
        name = sys.argv[1]
        accname = sys.argv[2]
    except: 
        print("Error, introduce nombre del archivo de entrada")
        sys.exit()
    cap = cv2.VideoCapture(name)
    x, y = calculate_movement(accname)
    print x,y
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))
    print fps
    fps = 30
    t = 0.0

    # Create some random colors
    color = np.random.randint(0,255,(10000,3))
    
    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)


    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    cv2.imshow('original',old_frame)
    cv2.imshow('stabilized',old_frame)

    while(1):
        ret,frame = cap.read()
        cv2.imshow('original',frame)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        h, w = old_frame.shape[:2]

        #calculamos la traslacion
        t = t + 1.0/fps
        dx = np.interp(t,[d[0] for d in x], [d[1] for d in x])
        dy = np.interp(t,[d[0] for d in y], [d[1] for d in y])       

        dx = dx*(138000.0)
        dy = dy*(138000.0)

        M = np.array([[1, 0, dx],[0, 1, dy]])


        overlay = cv2.warpAffine(frame, M, (w,h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
 
    
        old_frame = overlay.copy()

    
        cv2.imshow('stabilized',overlay)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

        # Now update the previous frame and previous points

        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    cv2.destroyAllWindows()
    cap.release()
