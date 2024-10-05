import cv2

def draw_boundary(img, classifier, scaleFactor, minNeigh, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    feautres = classifier.detectMultiScale



#object video 0 is default webcam
video_capture = cv2.VideoCapture(0)
#infinit loop
while True:
    _, img = video_capture.read()
    cv2.imshow("AWesome", img)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
#q stops executiong
        break
video_capture.release()
cv2.destroyAllWindows()
