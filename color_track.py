import numpy as np
from scipy import ndimage
from math import sqrt
import cv2, serial, time

arduino = serial.Serial('COM7', 9600)
time.sleep(2)
cap = cv2.VideoCapture(0)
margen = 8
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.GaussianBlur(frame, (15,15), 8)
    x_centr , y_centr = frame.shape[1]//2, frame.shape[0]//2
    frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = cv2.cvtColor(frame1, cv2.COLOR_RGB2HSV)

    # definir rango de color a aislar
    lower_hsv = np.array([-15, 130, 100], dtype=np.uint8 )
    upper_hsv = np.array([20, 255, 255], dtype=np.uint8)

    # color mask
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # determinar cantidad de pixeles blancos
    mask_area = np.sum(mask, axis=None)/255.0

    # si hay más de 1500 pixeles blancos
    if mask_area >= 1500:

        # obtener centro
        y, x = ndimage.measurements.center_of_mass(mask)
        dist_x, dist_y = x-x_centr, y-y_centr
        #print('derecha') if dist_x > 0 else print('izquierda')
        #print('abajo') if dist_y > 0 else print('arriba')

        if dist_y > margen:
            arduino.write(b'1')
        elif dist_y < -margen:
            arduino.write(b'0')
        elif dist_x > margen:
            arduino.write(b'4')
        elif dist_x < -margen:
            arduino.write(b'3')

        try:
            width = int( sqrt(mask_area) )
            rx = int( x - width/2.0); ry = int( y - width/2.0)

            cv2.rectangle(frame, (rx, ry), (rx + width, ry + width), (0, 255, 0), 4)

        except ValueError:
            pass
    # Display the resulting frame
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
