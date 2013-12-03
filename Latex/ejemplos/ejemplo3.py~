import cv2.cv as cv
global g_slider_position
def onTrackbarSlide(pos):
    cv.SetCaptureProperty(g_capture,cv.CV_CAP_PROP_POS_FRAMES,pos)
def load (name):
    g_slider_position=0
    cv.NamedWindow("Example3",cv.CV_WINDOW_AUTOSIZE)
    global g_capture
    g_capture = cv.CreateFileCapture(name)
    frames =int( cv.GetCaptureProperty(g_capture,cv.CV_CAP_PROP_FRAME_COUNT))
    if (frames != 0):
        cv.CreateTrackbar("Position","Example3",g_slider_position,frames,onTrackbarSlide)   
    while (True):
        frame = cv.QueryFrame(g_capture)
        if (not frame): break
        cv.ShowImage("Example3",frame)
        g_slider_position =int(cv.GetCaptureProperty(g_capture,cv.CV_CAP_PROP_POS_FRAMES))
        
        cv.SetTrackbarPos("Position","Example3",g_slider_position)
        c = cv.WaitKey(33)
        if (c==27): break
    cv.DestroyWindow("Example3")
def main():
    name = raw_input("Nombre de archivo:")
    load(name)
main()
