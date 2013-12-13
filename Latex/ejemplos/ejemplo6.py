import cv2
import numpy as np

def doCanny(im, lowThresh, highThresh, aperture):
    if (len(im.shape) != 2): 
        aux =  cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        out = cv2.Canny(aux, lowThresh, highThresh, aperture)
    else:
        out = cv2.Canny(im, lowThresh, highThresh, aperture)
    return out

if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()

    img = cv2.imread(name)
    out = doCanny(img, 10, 100, 3)
    cv2.imshow('Example6-in',img)
    cv2.imshow("Example6-out", out)
    cv2.waitKey(0)
