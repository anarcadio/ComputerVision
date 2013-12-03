import cv2

def doPyrDown(im):
    h, w = im.shape[:2]
    assert (w%2 == 0 and h%2 == 0)
    out= cv2.pyrDown(im)
    return out


if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()

    img = cv2.imread(name)
    out = doPyrDown(img)
    cv2.imshow('Example5-in',img)
    cv2.imshow("Example5-out", out)
    cv2.waitKey(0)
