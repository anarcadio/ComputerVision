import cv2.cv as cv

def doCanny(im, lowThresh, highThresh, aperture):
    if (im.nChannels != 1): return 0
    out = cv.CreateImage(cv.GetSize(im), IPL_DEPTH_8U, 1)
    cvCanny(im, out, lowThresh, highThresh, aperture)
    return out
def doPyrDown(im):
    assert (im.width%2 == 0 and im.height%2 == 0)
    out = cv.CreateImage((im.width/2,im.height/2),im.depth,im.nChannels)
    cv.PyrDown(im,out)
    return out

def main():
    name = raw_input("Nombre de archivo:")
    img = cv.LoadImage(name)
    img1 = doPyrDown(img)
    img2 = doPyrDown(img1)
    out = doCanny(img2, 10, 100, 3)
    cv.NamedWindow("Example6-in",1)
    cv.NamedWindow("Example6-out",1)
    cv.ShowImage("Example6-in",img)
    cv.ShowImage("Example6-out",out)
    cv.WaitKey(0)
    cv.DestroyWindow("Example5-in")
    cv.DestroyWindow("Example5-out")
main()
