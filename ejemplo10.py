import cv2.cv as cv
def load(name, nout):
    capture = 0
    capture = cv.CreateFileCapture(name)
    if (not capture): return -1
    bgr_frame = cv.QueryFrame(capture)
    fps = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS)
    size = (int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)),int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)))
    writer = cv.CreateVideoWriter(nout, cv.CV_FOURCC('M','J','P','G'), fps, size)
    logpolar_frame = cv.CreateImage (size, cv.IPL_DEPTH_8U, 3)
    while (cv.QueryFrame(capture) != None):
        bgr_frame = cv.QueryFrame(capture)
        cv.LogPolar(bgr_frame, logpolar_frame,(bgr_frame.width/2,bgr_frame.height/2),40,cv.CV_INTER_LINEAR+cv.CV_WARP_FILL_OUTLIERS)
        cv.WriteFrame(writer, logpolar_frame)
    return 0

def main():
    name = raw_input("Nombre de archivo de entrada:")
    nout = raw_input("\nNombre archivo salida:")
    load(name, nout)
main()

