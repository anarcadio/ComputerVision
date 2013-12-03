import cv2.cv as cv
global r
def call(pos):
    global r
    r = pos
    return
def main ():
    global r
    r = 3
    cv.NamedWindow("Blur",1)
    capture = cv.CreateCameraCapture(0)
    cv.CreateTrackbar("Radio","Blur",r,30,call)
    while (True):
        frame = cv.QueryFrame(capture)
        if (not frame): break
	out= cv.CreateImage(cv.GetSize((frame)),frame.depth,frame.nChannels)
        if ( r!=0):
            cv.Smooth(frame, out, cv.CV_BLUR, r, r)
            cv.ShowImage("Blur",out)
        else:
            cv.ShowImage("Blur",frame)
        c = cv.WaitKey(33)
        if (c==27): break
    cv.DestroyAllWindows()
main()
