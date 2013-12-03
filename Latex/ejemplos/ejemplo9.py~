import cv2.cv as cv
def main ():
    cv.NamedWindow("Example9",1)
    capture = cv.CreateCameraCapture(0)
    while (True):
        frame = cv.QueryFrame(capture)
        if (not frame): break
        cv.ShowImage("Example9",frame)
        c = cv.WaitKey(33)
        if (c==27): break
    cv.DestroyWindow("Example9")
main()
