import cv2
import numpy as np

def correct_gamma(img, correction):

    temp = img.copy()/255.0
    temp = np.array(temp, dtype=np.float32)
    temp = cv2.pow(temp, 1./correction)*255.0
    return temp

def adjust_levels(im,bot,mid,top):
    lut = np.zeros(256)
    for i in xrange(256):
        if i <= bot:
            lut[i]=0
        elif i >= top:
            lut[i] = 255
        else:
            lut[i]=255*(i-bot)/(top-bot)
    aux = cv2.LUT(im, lut)
    aux = np.array(aux, dtype=np.uint8)
    aux = correct_gamma(aux, mid)
    aux = np.array(aux, dtype=np.uint8)
    return aux

def autolevels(im, mid=1):
    inf = np.percentile(im,1)
    sup = np.percentile(im,99)
    return adjust_levels(im, inf,mid,sup)

def draw_hist(im, name):
    h = np.zeros((300,256,3))
    if len(im.shape)!=2:
        im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    hist_item = cv2.calcHist([im],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0),(x,y),(255,255,255))
    y = np.flipud(h)
    y = 255 -y
    cv2.imshow(name, y)

if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()

    img = cv2.imread(name)
    gr =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #out = adjust_levels(gr, 68,0.5, 228)
    #out = cv2.equalizeHist(gr)
    #out = cv2.normalize(gr,alpha = 0,beta = 255,norm_type = cv2.NORM_MINMAX)
    out = autolevels(gr)
    cv2.imshow('Example6-in',gr)
    cv2.imshow("Example6-out", out)
    draw_hist(gr, "hist_in")
    draw_hist(out, "hist_out")
    cv2.waitKey(0)
