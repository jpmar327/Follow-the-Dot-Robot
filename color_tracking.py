# import serial
# from time import sleep

# import cv2
# import numpy as np
# import math

# #Video capture through webcam
# cap=cv2.VideoCapture(0)
# # ser = serial.Serial ("/dev/ttyS0", 4800,timeout=0)    #Open port with baud rate
# ser = serial.Serial ("COM4", 57600,timeout = 0)    #Open port with baud rate

# while(1):

#     centers_blue=[]
#     # centers_red=[]
#     centers_black=[]


#     _, img = cap.read()

#     hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #A histogram based on color saturations is obtained.

#     blue_lower=np.array([80,150,0],np.uint8)
#     blue_upper=np.array([140,255,255],np.uint8)

#     black_lower=np.array([0, 0, 0],np.uint8) # black
#     black_upper=np.array([180, 255, 30],np.uint8)

#     # red_lower=np.array([0,50,20],np.uint8) # red
#     # red_upper=np.array([5,255,255],np.uint8)

#     # red2_lower=np.array([175,50,20],np.uint8) # red
#     # red2_upper=np.array([180,255,255],np.uint8)

#     blue=cv2.inRange(hsv,blue_lower,blue_upper) #A mask is created using blue intervals.

#     # red1=cv2.inRange(hsv,red_lower,red_upper) #A mask is created using red intervals.
#     # red2=cv2.inRange(hsv,red2_lower,red2_upper) #A mask is created using red intervals.
#     # red = red1+red2

#     black=cv2.inRange(hsv,black_lower,black_upper) #A mask is created using red intervals.


#     kernal = np.ones((5 ,5), "uint8") # Make a 5x5 matrix that records the video.

#     blue=cv2.erode(blue,kernal, iterations=1) # Erode to make mask.
#     # red=cv2.erode(red,kernal, iterations=1) # Erode to make mask.
#     black=cv2.erode(black,kernal, iterations=1) # Erode to make mask.


#     res1=cv2.bitwise_and(img, img, mask = blue) # New blue image.
#     # res2=cv2.bitwise_and(img, img, mask = red) # New red image.
#     res3=cv2.bitwise_and(img, img, mask = black) # New red image.


#     (contours_blue,hierarchy_blue)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_blue of the objects seen in the filter
#     # (contours_red,hierarchy_red)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_red of the objects seen in the filter
#     (contours_black,hierarchy_black)=cv2.findContours(black,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_red of the objects seen in the filter


#     cx_blue = 0
#     cy_blue = 0
#     cx_black = 0
#     cy_black = 0
#     # cx_red = 0
#     # cy_red = 0


#     for pic, contour in enumerate(contours_blue):
#         area = cv2.contourArea(contour) #opencv function that gets the contours_blue


#         if(area>300):


#             # x,y,w,h = cv2.boundingRect(contour) #Find coordinates of the contours_blue.
#             # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#             # cv2.putText(img,"Blue Marker",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))


#             M = cv2.moments(contour) #The center of mass of the found markers is obtained.
#             cx_blue = int(M['m10'] /M['m00'])
#             cy_blue = int(M['m01'] /M['m00'])
#             centers_blue.append([cx_blue,cy_blue])
#             #cv2.circle(img, (cx_blue, cy_blue), 7, (255, 255, 255), -1)

#             break


#             #print("blue: (%d, %d)",cx_blue, cy_blue)

#     for pic, contour in enumerate(contours_black):
#         area = cv2.contourArea(contour) #opencv function that gets the contours_blue


#         if(area>300):


#             # x,y,w,h = cv2.boundingRect(contour) #Find coordinates of the contours_blue.
#             # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
#             # cv2.putText(img,"Black Marker",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))


#             M = cv2.moments(contour) #The center of mass of the found markers is obtained.
#             cx_black = int(M['m10'] /M['m00'])
#             cy_black = int(M['m01'] /M['m00'])
#             centers_black.append([cx_black,cy_black])
#             #cv2.circle(img, (cx_black, cy_black), 7, (255, 255, 255), -1)
#             break

#     # D = math.sqrt((cx_red - cx_blue)**2 + (cy_red - cy_blue)**2)
#     #D = np.linalg.norm(cx-cy) #Euclidean distance is applied to find the distance between the centers of mass.
#     #print((cy_red - cy_black))
#     locations = str(cx_blue) + "," + str(cy_blue) + "," + str(cx_black) + "," + str(cy_black) + chr(13)# + "," + str(cx_blue) + "," + str(cy_blue) + chr(13)
#     #locations = [cx_blue, cy_blue, cx_black, cy_black, cx_red, cy_red]
    
#     #cx_blue,cy_blue,cx_black,cy_black,cx_red,cy_red,
#     received_data = ser.read()              #read serial port
#     #print (received_data)                   #print received data
#     sleep(0.03)
#     data_left = ser.inWaiting()             #check for remaining byte
#     received_data += ser.read(data_left)

#     if len(centers_blue)>0 and len(centers_black)>0:
        
#         for i in range(0,len(locations)):
#             ser.write(str.encode(locations[i]))                #transmit data serially
#             print(locations[i])
#             sleep(0.1)
#         # sleep(0.25)

#     # cv2.imshow("Color Tracking",img)
#     # if cv2.waitKey(1) & 0xFF == ord('q'):
#     #     cap.release()
#     #     cv2.destroyAllWindows()
#     #     break


import serial
from time import sleep

import cv2
import numpy as np
import math

#Video capture through webcam
cap=cv2.VideoCapture(0)
# ser = serial.Serial ("/dev/ttyS0", 4800,timeout=0)    #Open port with baud rate
ser = serial.Serial ("COM4", 57600,timeout=0)    #Open port with baud rate

while(1):

    centers_blue=[]
    # centers_red=[]
    centers_black=[]


    _, img = cap.read()

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #A histogram based on color saturations is obtained.

    blue_lower=np.array([80,150,0],np.uint8)
    blue_upper=np.array([140,255,255],np.uint8)

    black_lower=np.array([0, 0, 0],np.uint8) # black
    black_upper=np.array([180, 255, 30],np.uint8)

    # red_lower=np.array([0,50,20],np.uint8) # red
    # red_upper=np.array([5,255,255],np.uint8)

    # red2_lower=np.array([175,50,20],np.uint8) # red
    # red2_upper=np.array([180,255,255],np.uint8)

    blue=cv2.inRange(hsv,blue_lower,blue_upper) #A mask is created using blue intervals.

    # red1=cv2.inRange(hsv,red_lower,red_upper) #A mask is created using red intervals.
    # red2=cv2.inRange(hsv,red2_lower,red2_upper) #A mask is created using red intervals.
    # red = red1+red2

    black=cv2.inRange(hsv,black_lower,black_upper) #A mask is created using red intervals.


    kernal = np.ones((5 ,5), "uint8") # Make a 5x5 matrix that records the video.

    blue=cv2.erode(blue,kernal, iterations=1) # Erode to make mask.
    # red=cv2.erode(red,kernal, iterations=1) # Erode to make mask.
    black=cv2.erode(black,kernal, iterations=1) # Erode to make mask.


    res1=cv2.bitwise_and(img, img, mask = blue) # New blue image.
    # res2=cv2.bitwise_and(img, img, mask = red) # New red image.
    res3=cv2.bitwise_and(img, img, mask = black) # New red image.


    (contours_blue,hierarchy_blue)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_blue of the objects seen in the filter
    # (contours_red,hierarchy_red)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_red of the objects seen in the filter
    (contours_black,hierarchy_black)=cv2.findContours(black,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Find the contours_red of the objects seen in the filter


    cx_blue = 0
    cy_blue = 0
    cx_black = 0
    cy_black = 0
    # cx_red = 0
    # cy_red = 0


    for pic, contour in enumerate(contours_blue):
        area = cv2.contourArea(contour) #opencv function that gets the contours_blue


        if(area>300):


            # x,y,w,h = cv2.boundingRect(contour) #Find coordinates of the contours_blue.
            # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # cv2.putText(img,"Blue Marker",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))


            M = cv2.moments(contour) #The center of mass of the found markers is obtained.
            cx_blue = int(M['m10'] /M['m00'])
            cy_blue = int(M['m01'] /M['m00'])
            centers_blue.append([cx_blue,cy_blue])
            #cv2.circle(img, (cx_blue, cy_blue), 7, (255, 255, 255), -1)

            break


            #print("blue: (%d, %d)",cx_blue, cy_blue)

    for pic, contour in enumerate(contours_black):
        area = cv2.contourArea(contour) #opencv function that gets the contours_blue


        if(area>300):


            # x,y,w,h = cv2.boundingRect(contour) #Find coordinates of the contours_blue.
            # img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # cv2.putText(img,"Black Marker",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))


            M = cv2.moments(contour) #The center of mass of the found markers is obtained.
            cx_black = int(M['m10'] /M['m00'])
            cy_black = int(M['m01'] /M['m00'])
            centers_black.append([cx_black,cy_black])
            #cv2.circle(img, (cx_black, cy_black), 7, (255, 255, 255), -1)
            break

    # D = math.sqrt((cx_red - cx_blue)**2 + (cy_red - cy_blue)**2)
    #D = np.linalg.norm(cx-cy) #Euclidean distance is applied to find the distance between the centers of mass.
    #print((cy_red - cy_black))
    locations = str(cx_blue) + "," + str(cy_blue) + "," + str(cx_black) + "," + str(cy_black) + chr(13)# + "," + str(cx_blue) + "," + str(cy_blue) + chr(13)
    #locations = [cx_blue, cy_blue, cx_black, cy_black, cx_red, cy_red]
    
    #cx_blue,cy_blue,cx_black,cy_black,cx_red,cy_red,
    received_data = ser.read()              #read serial port
    #print (received_data)                   #print received data
    sleep(0.03)
    data_left = ser.inWaiting()             #check for remaining byte
    received_data += ser.read(data_left)

    if len(centers_blue)>0 and len(centers_black)>0:
        
        for i in range(0,len(locations)):
            ser.write(str.encode(locations[i]))                #transmit data serially
            #print(locations[i])
            sleep(0.1)
    #     #sleep(0.25)

    # cv2.imshow("Color Tracking",img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     break

