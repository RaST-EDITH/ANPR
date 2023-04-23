import cv2
import re
import numpy as np
import pytesseract

plateCascade = cv2.CascadeClassifier(r"C:\Users\ASUS\Documents\anpr work\ANPR\haarcascade_plate_number.xml")

def textExtract( img ) :

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    contours, hierarchy = cv2.findContours(sure_bg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
        roi = sure_bg[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi)
    
    return text

def checkPlate( imgRoi, img ) :

    global count
    while True :

        # if cv2.waitKey(1) & 0xFF ==ord('s'):

        cv2.imwrite(r"C:\Users\ASUS\Documents\anpr work\ANPR\result\out"+str(count)+".jpg",imgRoi)

        # image = cv2.imread(r"C:\Users\ASUS\Documents\anpr work\out"+str(count)+".jpg")

        text1 = pytesseract.image_to_string(imgRoi)
        text2 = textExtract( imgRoi )
        print(text1)
        print(text2)
        ntext1 = ""
        ntext2 = ""

        for i in range( 0, len(text1) ) :
            if ( text1[i].isalpha() ) :
                ntext1 = text1[i:i+10]
                break
        print(ntext1)

        for i in range( 0, len(text2) ) :
            if ( text2[i].isalpha() ) :
                ntext2 = text2[i:i+10]
                break
        print(ntext2)

        plate_format1 = re.compile("^([A-Z]{2})(\d{2})[A-Z]{2}(\d{4})$")
        plate_format2 = re.compile("^([A-Z]{2})(\d{1})[A-Z]{3}(\d{4})$")

        if ( plate_format1.match(ntext1) or plate_format2.match(ntext1) ) :
            print( "Valid" )
        
        else :
            print("Invalid")
        
        if ( plate_format1.match(ntext2) or plate_format2.match(ntext2) ) :
            print( "Valid" )
        
        else :
            print("Invalid")

        # digits , character = 0, 0

        # for i in ntext :
        #     if( i.isalpha() ) :
        #         character = character + 1
        #     elif ( i.isdigit() ) :
        #         digits = digits + 1

        # if ( character == 4 and digits == 6):
        #     print('valid')

        # else:
        #     print('not valid')

        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(50)
        count+=1
        return


def findPlate( img ) :

    minArea = 500
    imgRoi = 0
    # img = cv2.imread( file )
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade .detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgRoi)
            cv2.waitKey( 100 )

    cv2.imshow("Result",img)
    cv2.waitKey( 100 )

    if ( type(imgRoi) == type(np.array([1])) ) :
        checkPlate(imgRoi, img)
    
    else :
        print("Not Found")

def frameOut( vid ) :

    cap = cv2.VideoCapture( vid )
    skip = 20
    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        if cap.get(cv2.CAP_PROP_POS_FRAMES) % skip != 0:
            continue

        findPlate( frame )

    cap.release()


if __name__ == "__main__" :

    global count
    count = 0
    file = r'C:\Users\ASUS\Documents\anpr work\ANPR\Images\car.jpg'
    img = cv2.imread( file )
    vid1 = r'C:\Users\ASUS\Documents\anpr work\ANPR\sample_video.mp4'
    vid2 = r'C:\Users\ASUS\Documents\anpr work\sample_video_Trim.mp4'
    frameOut( vid1 )
    # findPlate( img )
