import cv2

def doCanny(im, lowThresh, highThresh, aperture):
    if (len(im.shape) != 2): 
        aux =  cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        out = cv2.Canny(aux, lowThresh, highThresh, aperture)
    else:
        out = cv2.Canny(im, lowThresh, highThresh, aperture)
    return out

if __name__ == '__main__':

    capture =  cv2.VideoCapture(0)

    while (True):
        ret, frame = capture.read()
        if (not ret): break
        out = doCanny(frame, 50, 100, 3)
        cv2.imshow("Example9-in",frame)
        cv2.imshow("Example9-out",out)
        c = cv2.waitKey(33)
        if (c==27): break
