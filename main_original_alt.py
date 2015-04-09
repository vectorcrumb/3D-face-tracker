import numpy as np
import cv2

def main():

    #Cascade Classifiers
    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
    new_face = False
    faces = []

    #Camera Variables
    kCamPort = 1
    kFrameInterval = 30

    #Frame Variables
    kFrameWidth = 640
    kFrameHeight = 480
    centroid = [kFrameWidth / 2, kFrameHeight / 2]
    center_point = centroid
    avg_point = centroid

    #Functional Variables
    debug = False
    useGUI = True

    #Init Variables
    ret = False
    camClosed = True

    #Constants
    windowName = "Window"

    if useGUI:
        cv2.namedWindow(windowName)
        cv2.moveWindow(windowName, 100, 100)

    cam = cv2.VideoCapture(kCamPort)

    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, kFrameWidth)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, kFrameHeight)

    while camClosed:
        if cam.isOpened():
            ret, img = cam.read()
            camClosed = not ret
        else:
            camClosed = True

    while(ret):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        new_face = (len(faces) != 0)
        print("New?" + str(new_face))

        if(new_face is True):
            avg_point = center_point

        i = 0

        for (x, y, w, h) in faces:
            cx = x + (w / 2)
            cy = y + (h / 2)
            centroid = [cx, cy]
            avg_point[0] = avg_point[0] + centroid[0]
            avg_point[1] = avg_point[1] + centroid[1]
            #faces.append(centroid)
            cv2.circle(img, tuple(centroid), 4, (0, 0, 255), -1)


        #Display Image and figures
        if useGUI:
            cv2.imshow(windowName, img)

        #Debugging
        if debug:
            print(new_face + "hey")

        #Refresh list of faces
        #del faces[:]
        #del avg_point[:]
        #Read New Image
        ret, img = cam.read()
        #Check for escape key
        if cv2.waitKey(kFrameInterval) == 27:
            break



if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()
    exit(0)
