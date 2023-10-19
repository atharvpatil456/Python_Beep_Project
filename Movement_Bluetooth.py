import cv2
import serial
import time

# Bluetooth device configuration
bluetooth_port = 'COM5'  # Replace with the COM port of your Bluetooth device
baud_rate = 9600  # Adjust the baud rate as per your device's configuration

cam = cv2.VideoCapture(0)

try:
    # Open the serial port for communication with the Bluetooth device
    ser = serial.Serial(bluetooth_port, baud_rate)

    while cam.isOpened():
        ret, frame1 = cam.read()
        ret, frame2 = cam.read()

        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for c in contours:
            if cv2.contourArea(c) < 5000:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            motion_detected = True

        cv2.imshow('Motion Detection', frame1)

        if motion_detected:
            # Send 'beep' signal to the Bluetooth device
            ser.write(b'beep\n')
            ser.flush()

        if cv2.waitKey(10) == ord('q'):
            break

finally:
    ser.close()  # Close the serial port
    cv2.destroyAllWindows()
