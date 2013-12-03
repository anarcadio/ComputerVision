import cv2.cv as cv
def doPyrDown(im):
    assert (im.width%2 == 0 and im.height%2 == 0)
    out = cv.CreateImage((im.width/2,im.height/2),im.depth,im.nChannels)
    cv.PyrDown(im,out)
    return out
def main():
    name = raw_input("Nombre de archivo:")
    img = cv.LoadImage(name)
    out = doPyrDown(img)
    cv.NamedWindow("Example5-in",1)
    cv.NamedWindow("Example5-out",1)
    cv.ShowImage("Example5-in",img)
    cv.ShowImage("Example5-out",out)
    cv.WaitKey(0)
    cv.DestroyWindow("Example5-in")
    cv.DestroyWindow("Example5-out")
main()
