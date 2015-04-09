import cv2
import numpy as np

def main():

    #Cascade Classifiers
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

    #Camera Variables
    kCamPort = 0
    kFrameInterval = 30
    kResolution = 1

    #Frame Variables
    kFrameWidth = 640
    kFrameHeight = 480
    kFrameWidthBorder = kFrameWidth / 10
    kFrameHeightBorder = kFrameHeight / 10
    kCenterPoint = [kFrameWidth / 2, kFrameHeight / 2]
    centroid = kCenterPoint
    avg_centroid = (0, 0)

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
        cv2.moveWindow(windowName, 100, 100)
    cam = cv2.VideoCapture(kCamPort)

    #Startup Routine
    if(kResolution is 1):
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    elif(kResolution is 2):
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        kFrameWidthBorder = 320 / 10
        kFrameHeightBorder = 240 / 10
        kCenterPoint = (320 / 2, 240 / 2)
    else:
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
            cx = x + (w / 2)
            cy = y + (h / 2)
            centroid = [cx, cy]
            print(centroid)
            print(faces)
            avg_centroid[0] = avg_centroid[0] + centroid[0]
            avg_centroid[1] = avg_centroid[1] + centroid[1]
            if(useGUI):
                cv2.rectangle(img, (x, y), (x+w, y+h),
                              (255, 0, 0), 2)
                cv2.circle(img, centroid, 4, (0, 0, 255), -1)

        for i in range(len(avg_centroid)):
            if len(faces) > 0:
                avg_centroid[i] = avg_centroid[i] / len(faces)

        if(useGUI):
            cv2.circle(img, tuple(kCenterPoint), 4, (0, 255, 0), -1)

        print(centroid)

        delta_x = (centroid[0] - kFrameWidthBorder) - ((kFrameWidth - kFrameWidthBorder) - centroid[0])
        print(delta_x)

        #Print coordinates
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
