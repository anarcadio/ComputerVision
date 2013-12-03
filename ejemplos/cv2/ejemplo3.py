import cv2
global g_slider_position

def nothing(*arg):
    pass

def onTrackbarSlide(pos):
    g_capture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,pos)

def load (name):
    g_slider_position=0
    global g_capture
    g_capture =  cv2.VideoCapture(name)
    frames = int(g_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    if (frames != 0):
        cv2.namedWindow("Example3")
        cv2.createTrackbar("Position","Example3",g_slider_position,frames,onTrackbarSlide)   
    while (True):
        ret, frame = g_capture.read()
        if (not ret): break
        cv2.imshow("Example3",frame)
        g_slider_position = int(g_capture.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))
        
        cv2.setTrackbarPos("Position","Example3",g_slider_position)
        c = cv2.waitKey(33)
        if (c==27): break


if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()
    load(name)
