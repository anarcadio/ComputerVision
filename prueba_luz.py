import cv2
import numpy as np


def correct_gamma(img, dst, correction):

    temp = img.copy()/255.0
    #temp = cv2.convertScaleAbs(img, alpha=1.0/255, beta=0) 
    temp = np.array(temp, dtype=np.float32)
    temp = cv2.pow(temp, correction)*255.0
    #dst = cv2.convertScaleAbs(temp, alpha=255, beta=0)
    return temp

def doCeq(im,a,t):
    #im =  cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    #hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    #cdf = hist_item.cumsum()

    aint = np.abs(im)
    m = np.power(aint, a)
    m = np.mean(m)
    m = pow(m,1.0/a)

    im = im/m


    m = np.array([[pow(min(t,x),a) for x in y] for y in aint])
    m = np.mean(m)
    m = pow(m,1.0/a)
    im = im/m
    #cdf_m = cdf_m/m

    #cdf = np.ma.filled(cdf_m,0).astype('uint8')
    #out = cdf[im]
    #im= np.array(im, dtype=np.uint8)
    #im = cv2.equalizeHist(im)
    return im

def process_image(img):

    gr =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gr = np.array(gr, dtype=np.uint8)
    gf = correct_gamma(gr, gr, 0.2)
    #gf = gr
    b1 = cv2.GaussianBlur(gf,(0,0), 1)
    b2 = cv2.GaussianBlur(gf,(0,0), 2)
    b2 = cv2.subtract(b1, b2)
    gr = b2
    gr = cv2.convertScaleAbs(b2, alpha=127, beta=127)
    #gr2 = doCeq(gr, 0.1, 10)
    #gr2 = np.array(gr2, dtype=np.uint8)
    #cv2.imshow("Example9-ouewqet",gr2)
    gr = cv2.equalizeHist(gr)
    #gr = np.array(gr, dtype=np.uint8)
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
