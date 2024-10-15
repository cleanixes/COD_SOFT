import cv2
from PIL import Image, ImageTk
import tkinter as tk

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    coords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]
    return coords

def detect(img, faceCascade, eyesCascade, noseCascade, mouthCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0), "white": (255, 255, 255)}
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['blue'], "Face")
    
    if len(coords) == 4:
        roi_img = img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]
        coords = draw_boundary(roi_img, eyesCascade, 1.1, 14, color['red'], "Eyes")
        coords = draw_boundary(roi_img, noseCascade, 1.1, 5, color['green'], "Nose")
        coords = draw_boundary(roi_img, mouthCascade, 1.1, 20, color['white'], "Mouth")
    
    return img

# Provide the correct path to the haarcascade XML files
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eyesCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
noseCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_mcs_nose.xml")
mouthCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_mcs_mouth.xml")

# Create a Tkinter window
window = tk.Tk()
window.title("Face Features Recognition")

# Create a label to display the video feed
label = tk.Label(window)
label.pack()

# Object video 0 is default webcam
video_capture = cv2.VideoCapture(0)

def update_frame():
    _, frame = video_capture.read()
    frame = detect(frame, faceCascade, eyesCascade, noseCascade, mouthCascade)
    
    # Convert the frame to RGB (OpenCV uses BGR)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to a PhotoImage
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    
    # Update the label with the new image
    label.imgtk = imgtk
    label.configure(image=imgtk)
    
    # Schedule the next frame update
    label.after(10, update_frame)

# Start updating frames
update_frame()

# Start the Tkinter event loop
window.mainloop()

# Release the video capture when the window is closed
video_capture.release()
