import tkinter as tk
from tkinter import Button
import turtle
import cv2
from PIL import Image, ImageTk
import threading

# Tkinter GUI
class DrawingApp:
    def __init__(self, root):
        self._root = root
        self._root.title("Turtle Drawing and Object Detection")
        self._root.geometry("800x600")

        # Creating a Turtle Screen for drawing
        self.canvas = turtle.ScrolledCanvas(self._root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Creating a Turtle object
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.t = turtle.RawTurtle(self.turtle_screen)

        # Buttons for drawing control
        self.draw_button = Button(self._root, text="Draw Circle", command=self.draw_circle)
        self.draw_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = Button(self._root, text="Clear", command=self.clear_screen)
        self.clear_button.pack(side=tk.LEFT, padx=10)

    # Function to draw a circle using Turtle
    def draw_circle(self):
        self.t.circle(50)

    # Function to remove the canvas
    def clear_screen(self):
        self.t.clear()

# Running the app
if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()



# Function to implement object detection using OpenCV
class ObjectDetectionMixin:
    def load_model(self):
        # Load MobileNet SSD pre-trained model
        self.net = cv2.dnn.readNetFromCaffe('MobileNetSSD_deploy.prototxt', 'MobileNetSSD_deploy.caffemodel')

    def start_detection(self):
        self.cap = cv2.VideoCapture(0)  # Start webcam
        self.running = True

        # Start separate thread to display video feed
        threading.Thread(target=self.video_loop).start()

    def stop_detection(self):
        self.running = False
        if self.cap:
            self.cap.release()

    def video_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Perform object detection
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            self.net.setInput(blob)
            detections = self.net.forward()

            # Draw bounding boxes on detected objects
            frame = self.display_detections(frame, detections)

            # Convert the frame to a format suitable for Tkinter and update label
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

    def display_detections(self, frame, detections):
        # List of object labels
        CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair",
                   "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa",
                   "train", "tvmonitor"]

        (h, w) = frame.shape[:2]
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return frame