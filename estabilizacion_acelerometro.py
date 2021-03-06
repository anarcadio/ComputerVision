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
            date_str = aux[3]
            aux_date = date_str.split(":")
            #get the time in seconds
            date = ((int(aux_date[0])*60 + int(aux_date[1]))*60 + float(aux_date[2])) - t0
            fline = [float(aux[0]), float(aux[1]),float(aux[2]), date]
       
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
    z0 = 0.0
    vz0 = 0.0
    dx = [(0.0,0.0)]
    dy = [(0.0,0.0)]
    dz = [(0.0,0.0)]
    for line in array:
        ax = line[0]
        ay = line[1]
        az = line[2]
        t1 = line[3]
        vx1 = vx0 + ax*(t1-t0)
        vy1 = vy0 + ay*(t1-t0)
        vz1 = vz0 + az*(t1-t0)
        x1 = x0 + (vx0 + vx1)*(t1-t0)/2
        y1 = y0 + (vy0 + vy1)*(t1-t0)/2
        z1 = z0 + (vz0 + vz1)*(t1-t0)/2
        dx.append((t1, x1))
        dy.append((t1, y1))
        dz.append((t1, z1))
        x0 = x1
        y0 = y1
        z0 = z1
        t0 = t1
    return dx, dy, dz

def recalculate_pos(x, z, d, f):
    s = np.sign(x)
    h = np.sqrt(x*x+z*z)
    m = h*d/(d-z)
    return s*(m/d)*(d+f)

if __name__ == '__main__':

    import sys
    try: 
        name = sys.argv[1]
        accname = sys.argv[2]
    except: 
        print("Error, introduce nombre del archivo de entrada")
        sys.exit()
    frames = []
    nout = "out-" + name
    cap = cv2.VideoCapture(name)
    x, y, z = calculate_movement(accname)


    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    fps=16
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))
    t = 0.0
    f = 0.004
    dist = 1.4

    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

    frames.append(old_frame)

    while(ret):
        ret,frame = cap.read()
        if ret:
            cv2.imshow('original',frame)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            t = cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)/1000
            h, w = old_frame.shape[:2]

            #calculamos la traslacion
            dx = np.interp(t,[d[0] for d in x], [d[1] for d in x])
            dy = np.interp(t,[d[0] for d in y], [d[1] for d in y])
            dz = np.interp(t,[d[0] for d in z], [d[1] for d in z])

            dx = recalculate_pos(dx, dz, dist, f)
            dy = recalculate_pos(dy, dz, dist, f)

            dx = dx*149321.0
            dy = dy*149321.0
            M = np.array([[1, 0, dx],[0, 1, dy]])

            old_frame = cv2.warpAffine(frame, M, (w,h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

            frames.append(old_frame)

    writer = cv2.VideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    for frm in frames:
        writer.write(frm)
    cv2.destroyAllWindows()
    cap.release()
