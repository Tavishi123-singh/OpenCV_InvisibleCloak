import cv2
import numpy as np

def empty(a):
    pass

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
cap.set(10,160)

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV",640,300)
cv2.createTrackbar("Hue Min","HSV",101,179,empty)
cv2.createTrackbar("Hue Max","HSV",155,179,empty)
cv2.createTrackbar("Sat Min","HSV",99,255,empty)
cv2.createTrackbar("Sat Max","HSV",255,255,empty)
cv2.createTrackbar("Val Min","HSV",0,255,empty)
cv2.createTrackbar("Val Max","HSV",255,255,empty)

while True:
    cv2.waitKey(1000)
    ret,init_frame = cap.read()
    if(ret):
        break

while True:
    _, frame =cap.read()
    imgHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","HSV")
    h_max = cv2.getTrackbarPos("Hue Max", "HSV")
    s_min = cv2.getTrackbarPos("Sat Min", "HSV")
    s_max = cv2.getTrackbarPos("Sat Max", "HSV")
    v_min = cv2.getTrackbarPos("Val Min", "HSV")
    v_max = cv2.getTrackbarPos("Val Max", "HSV")
    #print(h_min)
    kernel = np.ones((5,5),np.uint8)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    mask = cv2.medianBlur(mask,3)
    mask_inv = 255-mask
    mask= cv2.erode(mask,kernel,iterations=3)
    mask = cv2.dilate(mask,kernel,iterations=5)

    b = frame[:,:,0]
    g = frame[:,:,1]
    r = frame[:,:,2]
    b = cv2.bitwise_and(mask_inv,b)
    g = cv2.bitwise_and(mask_inv,g)
    r = cv2.bitwise_and(mask_inv,r)
    frame_inv = cv2.merge((b,g,r))

    b = init_frame[:,:,0]
    g = init_frame[:,:,1]
    r = init_frame[:,:,2]
    b = cv2.bitwise_and(b,mask)
    g = cv2.bitwise_and(g,mask)
    r = cv2.bitwise_and(r,mask)
    sheet_area = cv2.merge((b,g,r))

    final = cv2.bitwise_or(frame_inv,sheet_area)

    cv2.imshow("Invisible",final)
    #cv2.imshow("Original",frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()