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
        print("Error, introduce los nombres de los ficheros de entrada y salida")
        sys.exit()
    cap = cv2.VideoCapture(name)

    #fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    #esto da error
    fps=15
    print cap.get(3)
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))
    print size
    writer = cv2.VideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    print fps, size	

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 10000,
                       qualityLevel = 0.001,
                       minDistance = 50,
                       blockSize = 30 )

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (30,30),
                  maxLevel = 4,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Create some random colors
    color = np.random.randint(0,255,(10000,3))
    
    draw = False

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    cv2.imshow('original',old_frame)
    cv2.imshow('stabilized',old_frame)

    while(1):
        ret,frame = cap.read()
        cv2.imshow('original',frame)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # calculate optical flow
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        h, w = old_frame.shape[:2]

        H, status = cv2.findHomography(p0, p1, cv2.RANSAC, 0)

        overlay = cv2.warpPerspective(frame, H, (w, h),  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
 
    
        # draw the tracks
        old_frame = overlay.copy()
        if draw:
            for i,(new,old) in enumerate(zip(good_new,good_old)):
                a,b = new.ravel()
                c,d = old.ravel()
                cv2.circle(overlay,(a,b),5,color[i].tolist(),-1)

    
        cv2.imshow('stabilized',overlay)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        if k == ord('d'):
            draw = not draw

        # Now update the previous frame and previous points

        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    cv2.destroyAllWindows()
    cap.release()
