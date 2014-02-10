import cv2
import numpy as np


def correct_gamma(img, dst, correction):

    temp = img.copy()/255.0
    temp = np.array(temp, dtype=np.float32)
    temp = cv2.pow(temp, correction)*255.0
    return temp

def doCeq(im,a,t):
    aint = np.abs(im)
    m = np.power(aint, a)
    m = np.mean(m)
    m = np.power(m,1.0/a)

    im = im/m
    aint = np.abs(im)

    #m = np.array([[pow(min(t,x),a) for x in y] for y in aint])
    m = np.minimum(aint, t)
    m = np.power(m, a)

    m = np.mean(m)
    m = np.power(m,1.0/a)
    im = im/m

    im = t*np.tanh(im/t)
    im = cv2.convertScaleAbs(im, alpha=127, beta=0)
    return im

def process_image(img):

    gr =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gr = np.array(gr, dtype=np.uint8)
    gf = correct_gamma(gr, gr, 0.2)
    b1 = cv2.GaussianBlur(gf,(0,0), 1,1)
    b2 = cv2.GaussianBlur(gf,(0,0), 2,2)
    b2 = cv2.subtract(b1, b2)
    gr = cv2.convertScaleAbs(b2, alpha=127, beta=127)
    gr = doCeq(gr, 0.1, 10)
    #gr = cv2.normalize(gr,alpha = 0,beta = 255,norm_type = cv2.NORM_MINMAX)
    return gr


if __name__ == '__main__':

    capture =  cv2.VideoCapture(0)

    while (True):
        ret, frame = capture.read()
        if (not ret): break
        out = process_image(frame)
        gr =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Example9-in",gr)
        cv2.imshow("Example9-out",out)
        c = cv2.waitKey(33)
        if (c==27): break
