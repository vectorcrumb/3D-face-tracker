import cv2
import numpy as np
import serial

def main():

    #Cascade Classifiers
    face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_alt.xml")
    kScaleFactor = 1.2
    kMinNeighbors = 4

    #Code parameters
    kCamPort = 0
    kFrameInterval = 30
    kResolution = 0

    #Frame parameters
    kFrameWidth = 320
    kFrameHeight = 240

    #Frame variables
    kFrameWidthBorder = (kFrameWidth / 10) * 2
    kFrameHeightBorder = (kFrameHeight / 10) * 2

    #Reference constants
    kCenterX = kFrameWidth / 2
    kCenterY = kFrameHeight / 2
    kCenterPoint = [kCenterX, kCenterY]

    #Points and deltas
    centroid = kCenterPoint
    avg_centroid = kCenterPoint
    delta_x = 0
    delta_y = 0

    #Proportional control constants
    kPx = 0.5
    kPy = 0.5
    #Frame border control for Z axis
    kZ = 0.5

    #Center point coorndinates
    x_prod = 0
    y_prod = 0

    #Data packet
    mov_x = 0
    mov_y = 0
    mov_z = 0

    # "Preprocessor" variables
    debug = False
    debug_mov = False
    debug_mov_img = False
    useGUI = False

    #Initialization variables to startup cam
    ret = False
    camClosed = True

    #Window Name
    windowName = "3D Face Tracker"

    #Serial connection
    arduino_port = '/dev/ttyACM0'
    arduino_bitrate = 9600
    arduino = None
    connected = False

    #Start cam and windows if the GUI is enabled
    cam = cv2.VideoCapture(kCamPort)
    if useGUI:
        cv2.namedWindow(windowName)
        cv2.moveWindow(windowName, 100, 100)

    #Set resolutions:
    #    1: Standard definition
    #    2: Low definition
    # else: Set to variables (kFrameWidth, kFrameHeight)
    if kResolution is 1:
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
    elif kResolution is 2:
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
        kFrameWidthBorder = 320 / 10
        kFrameHeightBorder = 240 / 10
        kCenterPoint = (320 / 2, 240 / 2)
    else:
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, kFrameWidth)
        cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, kFrameHeight)

    #While loop to open cam. While the cam is closed, attempt to take a picture until cam.read() returns true. If so, exit loop
    while camClosed:
        if cam.isOpened():
            ret, img = cam.read()
            camClosed = not ret
        else:
            camClosed = True

    try:
        arduino = serial.Serial(arduino_port, arduino_bitrate)
        connected = True
    except serial.serialutil.SerialException as err:
        print(err)
        connected = False
        pass

    #CamShift Loop
    while ret:
        #Connect to arduino if not already connected 
        if not connected:
            try:
                arduino = serial.Serial(arduino_port, arduino_bitrate)
                connected = True
            except serial.serialutil.SerialException as err:
                print(err)
                connected = False
                pass

        #Color conversion to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Detect faces with Haar Cascade Classifier
        faces = face_cascade.detectMultiScale(gray, kScaleFactor, kMinNeighbors)

        #Count the number of faces
        tmp_faces = len(faces)

        #Iterate tuple (x, y, w, h) within faces list to calculate centroids and draw them if the GUI is enabled
        for (x, y, w, h) in faces:
            #Centroid calculation
            cx = x + (w / 2)
            cy = y + (h / 2)
            centroid = [cx, cy]
            #Detect if face is outside the acceptable 80% range
            if (cx < kFrameWidthBorder or cx > (kFrameWidth - kFrameWidthBorder)) or (cy < kFrameHeightBorder or cy > (kFrameHeight - kFrameHeightBorder)):
                mov_z = -1
            #Detect if face is within a 40% interior range
                """
                elif (cx > (kZ * kFrameWidthBorder) or cx < (kFrameWidth - (kZ * kFrameWidthBorder))) or (cy > (kZ * kFrameHeightBorder) or cy < (kFrameHeight - (kZ * kFrameHeightBorder))):
                    mov_z = 1
                """
            elif (cx > (kCenterX - (kZ * kFrameWidthBorder)) or cx < (kCenterX + (kZ * kFrameWidthBorder))) or (cy > (kCenterY - (kZ * kFrameHeightBorder)) or cy < (kCenterY + (kZ * kFrameHeightBorder))):
                mov_z = 1
            #Else, do not shift Z axis
            else:
                mov_z = 0

            #Print centroid coordinates if debug is enabled
            if debug:
                print(centroid)
            #Draw rectangle around face (white) with center point (red)
            if(useGUI):
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 1) #white rectangle, face bounding box
                cv2.circle(img, tuple(centroid), 6, (0, 0, 255), -1) #red point, center of face

        #Print number of faces and faces matrix if debug is enabled
        if debug:
            print("# of faces: " + str(tmp_faces))
            print(faces)

        #Verify Z axis movement
        if tmp_faces is (0 or 1):
            mov_z = 0
        else:
            mov_z = mov_z

        #Check if there are faces to avoid division by zero
        if tmp_faces is not 0:
            #Loop over faces, adding x and y coordinates to average point
            for i in range(tmp_faces):
                x_prod += (faces[i][0] + (faces[i][2] / 2))
                y_prod += (faces[i][1] + (faces[i][3] / 2))
            #Divide sum of all coordinates by number of faces (average)
            x_prod /= tmp_faces
            y_prod /= tmp_faces
        #If no faces were detected, use center point instead
        else:
            x_prod = kCenterX
            y_prod = kCenterY

        #Calculate deltas and movement of camera
        delta_x = kCenterX - x_prod
        delta_y = -(kCenterY - y_prod)
        mov_x = kPx * delta_x
        mov_y = kPy * delta_y

        #Print movement data
        if debug_mov:
            print("Mov X: " + str(mov_x))
            print("Mov Y: " + str(mov_y))
            print("Mov Z: " + str(mov_z))

        #If GUI is enabled, draw a blue point to indicate average center and a green circle to indicate middle of frame
        if useGUI:
            cv2.circle(img, (x_prod, y_prod), 4, (255, 0, 0), -1) #blue point, average of face centroids
            cv2.circle(img, tuple(kCenterPoint), 2, (0, 255, 0), -1) #green point, center of frame
            if debug_mov_img:
                cv2.putText(img, "X Movement: %d" % mov_x, (10, 200), cv2.FONT_HERSHEY_TRIPLEX, 0.35, (100, 20, 150), 1)
                cv2.putText(img, "Y Movement: %d" % mov_y, (10, 215), cv2.FONT_HERSHEY_TRIPLEX, 0.35, (100, 20, 150), 1)
                cv2.putText(img, "Z Movement: %d" % mov_z, (10, 230), cv2.FONT_HERSHEY_TRIPLEX, 0.35, (100, 20, 150), 1)

        #If connected, send data
        if connected:
            arduino.write(str(mov_x))
            arduino.write(str(mov_y))
            arduino.write(str(mov_z))

        #Reset average point and deltas to avoid large numbers
        x_prod = 0
        y_prod = 0
        delta_x = 0
        delta_y = 0
        mov_z = 0

        #Display Image
        if useGUI:
            cv2.imshow(windowName, img)
        #Read New Image
        ret, img = cam.read()
        #Check for escape key
        if cv2.waitKey(kFrameInterval) == 27:
            break

#Execute code
if __name__ == "__main__":
    #Run code
    main()
    #Destroy all OpenCV related windows and exit program with exit code 0
    cv2.destroyAllWindows()
    exit(0)
