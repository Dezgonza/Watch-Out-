import cv2, serial, time
import numpy as np

#arduino = serial.Serial('COM5', 9600)
time.sleep(2)

cam = cv2.VideoCapture(0)
y, x = 480, 640 #307200
margen = 40

while True:
    _, frame = cam.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    verde_bajos = np.array([55,60,60])
    verde_altos = np.array([120, 255, 255])
    rojos_bajos = np.array([-15,61,64])
    rojos_altos = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, verde_bajos, verde_altos)

    #Eliminamos ruido
    kernel = np.ones((4,4),np.uint8)
    mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)

    # determinar cantidad de pixeles blancos
    mask_area = np.sum(mask, axis=None)/255.0

    # si hay más de 1500 pixeles blancos
    if mask_area >= 1500:

        try:
            _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            mayor_contorno = max(contours, key = cv2.contourArea)
            momentos = cv2.moments(mayor_contorno)
            cx = float(momentos['m10']/momentos['m00'])
            cy = float(momentos['m01']/momentos['m00'])
            width = int(np.sqrt(mask_area))
            rx = int(cx - width/2.0); ry = int(cy - width/2.0)
            cv2.rectangle(frame, (rx, ry), (rx + width, ry + width), (0, 255, 0), 4)
            dist_x, dist_y = cx-x//2, cy-y//2
            #if dist_x > margen: arduino.write(b'3') #print('derecha')
            #if dist_x < -margen: arduino.write(b'4') #print('izquierda')
            #if dist_y > margen: arduino.write(b'1') #print('abajo')
            #if dist_y < -margen: arduino.write(b'0') #print('arriba')
            #else: print('bkn')

        except ValueError:
            pass

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
