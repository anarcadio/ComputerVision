import cv2.cv as cv
def load (name):
    cv.NamedWindow("Example2",1)
    capture = cv.CreateFileCapture(name)
    while (True):
        frame = cv.QueryFrame(capture)
        if (not frame): break
        cv.ShowImage("Example2",frame)
        c = cv.WaitKey(33)
        if (c==27): break
    cv.DestroyWindow("Example2")
def main():
    name = raw_input("Nombre de archivo:")
    load(name)
main()
