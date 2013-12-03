import cv2.cv as cv
def load (name):
    img = cv.LoadImage(name)
    cv.NamedWindow("Example4-in",0)
    cv.NamedWindow("Example4-out",0)
    cv.ShowImage("Example4-in",img)
    out= cv.CreateImage(cv.GetSize((img)), cv.IPL_DEPTH_8U,3)
    cv.Smooth(img, out, cv.CV_GAUSSIAN, 3, 3)
    cv.ShowImage("Example4-out", out)
    cv.WaitKey(0)
    cv.DestroyWindow("Example4-in")
    cv.DestroyWindow("Example4-out")
def main():
    name = raw_input("Nombre de archivo:")
    load(name)
main()
