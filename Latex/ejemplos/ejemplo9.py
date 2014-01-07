import cv2
global r
def call(pos):
    global r
    r = pos
    return
def main ():
    global r
    r = 3
    cv2.namedWindow("Blur")
    capture =  cv2.VideoCapture(0)
    cv2.createTrackbar("Radio","Blur",r,30,call)
    while (True):
        ret, frame = capture.read()
        if (not ret): break
        if ( r!=0):
            out = cv2.blur(frame, (r,r))
            cv2.imshow("Blur",out)
        else:
            cv2.imshow("Blur",frame)
        c = cv2.waitKey(33)
        if (c==27): break
    cv2.destroyAllWindows()
main()
