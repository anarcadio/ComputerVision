import cv2
def load (name):
    capture =  cv2.VideoCapture(name)
    ret = True
    while (ret):
        ret, frame = capture.read()
        if (ret):
            cv2.imshow("Example2",frame)
            c = cv2.waitKey(33)
            if (c==27):
                ret = False
if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()
    load(name)
