import cv2

if __name__ == '__main__':

    capture =  cv2.VideoCapture(0)

    while (True):
        ret, frame = capture.read()
        if (not ret): break
        cv2.imshow("Example9",frame)
        c = cv2.waitKey(33)
        if (c==27): break
