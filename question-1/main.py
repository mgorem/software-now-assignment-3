import tkinter as tk
from tkinter import Button
import turtle

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
