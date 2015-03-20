import cv2
import numpy as np

def main():

    #Cascade Classifiers
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

    #Camera Variables
    kCamPort = 0
    kFrameInterval = 30

    #Frame Variables
    kFrameWidth = 320
    kFrameHeight = 240

    #Functional Variables
    debug = False
    useGUI = True

    #Init Variables
    ret = False
    camClosed = True

    #Constants
    windowName = "3D Face Tracker"

    #Objects
    if useGUI:
        cv2.namedWindow(windowName)
    cam = cv2.VideoCapture(kCamPort)

    #Startup Routine
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, kFrameWidth)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, kFrameHeight)

    while camClosed:
        if cam.isOpened():
            ret, img = cam.read()
            camClosed = not ret
        else:
            camClosed = True

    #Tracker Loop
    while ret:
        #Face Detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cx = (x+w) / 2
            cy = (y+h) / 2
            centroid = (cx, cy)
            cv2.rectangle(img, (x, y), (x+w, y+h),
                          (255, 0, 0), 2)
        #Display Image
        cv2.imshow(windowName, img)
        #Read New Image
        ret, img = cam.read()
        #Check for escape key
        if cv2.waitKey(kFrameInterval) == 27:
            break

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
    exit(0)
