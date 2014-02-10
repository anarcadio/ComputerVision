import cv2
import cv2.cv as cv
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
    import sys
    try: 
        name = sys.argv[1]
        nout = sys.argv[2]
    except: 
        print("Error, introduce los nombre de los ficheros de entrada y salida")
        sys.exit()

    frames = []
    cap = cv2.VideoCapture(name)
    fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    fps = 16
    size = (int(cap.get( cv.CV_CAP_PROP_FRAME_WIDTH)),int(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT)))
    nframes = int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT))
    count = 1 
    ret = True

    while(ret):
        ret,frame = cap.read()
        if ret:
            out = process_image(frame)
            out = cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
            frames.append(out)
            porcentaje = 100*count/nframes
            print porcentaje, "% completed......................."
            count += 1
    writer = cv2.VideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    for frm in frames:
        writer.write(frm)
    cap.release()

