import cv2
def load (name):

    img = cv2.imread(name)
    cv2.imshow('Example4-in',img)

    out = cv2.GaussianBlur(img,(9,9), 0)
    cv2.imshow("Example4-out", out)
    cv2.waitKey(0)

if __name__ == '__main__':
    import sys
    try: name = sys.argv[1]
    except: 
        print("Error, introduce nombre del archivo")
        sys.exit()
    load(name)
