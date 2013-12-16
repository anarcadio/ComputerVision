#!/usr/bin/env python

import numpy as np
import cv2


# Parameters for lucas kanade optical flow
lk_params = dict( winSize  = (30,30),
                  maxLevel = 4,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

def checkedTrace(img0, img1, p0, back_threshold = 1.0):
    p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
    p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
    d = abs(p0-p0r).reshape(-1, 2).max(-1)
    status = d < back_threshold
    return p1, status


if __name__ == '__main__':

    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo de entrada")
        sys.exit()
    cap = cv2.VideoCapture(name)

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 10000,
                       qualityLevel = 0.001,
                       minDistance = 5,
                       blockSize = 3 )

    term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1 )
    # Create some random colors
    color = np.random.randint(0,255,(10000,3))
    
    draw = False

    # Take first frame and find corners in it
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    cv2.cornerSubPix(old_gray, p0, (5, 5), (-1, -1), term)

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)

    cv2.imshow('original',old_frame)
    cv2.imshow('stabilized',old_frame)

    while(True):
        ret,frame = cap.read()
	if not ret:
	    break
        cv2.imshow('original',frame)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # calculate optical flow
        #p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        p2, trace_status = checkedTrace(old_gray, frame_gray, p0)

        p1 = p2[trace_status].copy()
        p0 = p0[trace_status].copy()

        # Select good points
       # good_new = p1[st==1]
        #good_old = p0[st==1]

        h, w = old_frame.shape[:2]

        H, status = cv2.findHomography(p0, p1, cv2.RANSAC, 0)

        overlay = cv2.warpPerspective(frame, H, (w, h),  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
 
    
        # draw the tracks
        old_frame = overlay.copy()
        if draw:
            for i,(new,old) in enumerate(zip(p1,p0)):
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
        cv2.cornerSubPix(old_gray, p0, (5, 5), (-1, -1), term)

    cv2.destroyAllWindows()
    cap.release()
