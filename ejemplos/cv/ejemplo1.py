import cv2.cv as cv
def load (name):
    img = cv.LoadImage(name)
    cv.NamedWindow("Example1",10)
    cv.ShowImage("Example1",img)
    cv.WaitKey(0)
#    cv.ReleaseImage(img)
    cv.DestroyWindow("Example1")
def main():
    name = raw_input("Nombre de archivo:")
    load(name)
main()
