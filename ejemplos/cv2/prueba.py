import cv2
def load ():
    capture =  cv2.VideoCapture(0)
    while (True):
        ret, frame = capture.read()
        if (not ret): break
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print "ndim", frame.ndim
        print "shape", frame.shape
        print "dtype", frame.dtype
        print "size", frame.size
        cv2.imshow("prueba",frame)
        c = cv2.waitKey(33)
        if (c==27): break


if __name__ == '__main__':
    load()
