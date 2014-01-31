#!/usr/bin/env python

import numpy as np
import cv2
import cv

feature_params = dict( maxCorners = 10000,
                       qualityLevel = 0.001,
                       minDistance = 5,
                       blockSize = 3 )

term = ( cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.001 )
lk_params = dict( winSize  = (50,50),
                  maxLevel = 4,
                  criteria=term
)

def checkedTrace(img0, img1, p0, back_threshold = 1.0):
    p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
    p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
    d = abs(p0-p0r).reshape(-1, 2).max(-1)
    status = d < back_threshold
    return p1, status

if __name__ == '__main__':
    frames = []
    import sys
    try: 
        name = sys.argv[1]
        nout = sys.argv[2]
    except: 
        print("Error, introduce los nombre de los ficheros de entrada y salida")
        sys.exit()

    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))
    nframes = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
    ret, old_frame = cap.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
    cv2.cornerSubPix(old_gray, p0, (5, 5), (-1, -1), term)
    frames.append(old_frame)
    count = 1 

    while(True):
        porcentaje = 100*count/nframes
        print porcentaje, "% completed......................."
        ret,frame = cap.read()

        if not ret:
            break

        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p2, trace_status = checkedTrace(old_gray, frame_gray, p0)

        p1 = p2[trace_status].copy()
        p0 = p0[trace_status].copy()

        h, w = old_frame.shape[:2]

	try:
        	H, status = cv2.findHomography(p0, p1, cv2.RANSAC)
	except:
		pass

        old_frame = cv2.warpPerspective(frame, H, (w, h),  flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
        frames.append(old_frame)
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
        cv2.cornerSubPix(old_gray, p0, (5, 5), (-1, -1), term)
        count += 1
    writer = cv2.VideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    for frm in frames:
        writer.write(frm)
    cv2.destroyAllWindows()
    cap.release()
