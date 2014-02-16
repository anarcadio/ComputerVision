#!/usr/bin/env python

import numpy as np
import cv2
import cv

if __name__ == '__main__':

    import sys
    try: 
        name = sys.argv[1]
        nout = sys.argv[2]
    except: 
        print("Error, introduce nombre de los ficheros de entrada y salida")
        sys.exit()
    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))  
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    ret = True
    frames = []
    while(ret):
        ret,frame = cap.read()
	if ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            h, w = old_frame.shape[:2]
            old_gray = np.float32(old_gray)
            frame_gray = np.float32(frame_gray)
            dx, dy = cv2.phaseCorrelate(old_gray, frame_gray)
            M = np.array([[1, 0, dx],[0, 1, dy]])
            old_frame = cv2.warpAffine(frame, M, (w,h), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            frames.append(old_frame)
            old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)


    writer = cv2.VideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    for frm in frames:
        writer.write(frm)
    cap.release()
