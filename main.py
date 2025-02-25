import tkinter as tk
from tkinter import Label
import time
import os
from PIL import Image, ImageTk, ImageSequence

class DesktopPet:
    def __init__(self):
        self.focus_time = 25 * 60  # 25 minutes in seconds (Pomodoro default)
        
        # Create a root window
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)  # Start as topmost (floating)
        self.root.overrideredirect(True)  # Remove window borders

        # Load and resize pet image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, "coding_snoopy.gif")
        
        # Open GIF and extract frames
        gif = Image.open(gif_path)
        self.frames = []
        for frame in ImageSequence.Iterator(gif):
            # Convert to RGBA, remove white edges, resize to 100x100
            frame = frame.convert("RGBA")
            datas = frame.getdata()
            new_data = []
            frame.putdata(new_data)
            resized_frame = frame.resize((100, 100), Image.NEAREST)
            self.frames.append(ImageTk.PhotoImage(resized_frame))

        self.current_frame = 0
        self.frame_count = len(self.frames)
        
        # Create pet label with the image, use magenta as background
        self.pet_label = Label(self.root, image=self.frames[0])  # Magenta
        self.pet_label.pack()

        # Make magenta transparent instead of white
        self.root.config(bg="#000100")  # Match the label background
        self.pet_label.config(bg="#000100")
        self.root.wm_attributes("-transparentcolor", "#000100")  # Magenta transparency

        # Initial position on desktop
        self.root.geometry(f"+{100}+{self.root.winfo_screenheight()-200}")  # Near bottom-left

        # Pet stats
        self.focus_time_left = self.focus_time  # 25 minutes in seconds (Pomodoro default)

        # Timer label (positioned below pet)
        self.timer_label = Label(self.root, text=self.format_time(self.focus_time_left), 
                                font=("Arial", 12), fg="white", bg="black")
        self.timer_label.pack()

        # Bind mouse events for dragging
        self.pet_label.bind("<Button-1>", self.start_drag)
        self.pet_label.bind("<B1-Motion>", self.drag)

        # Context menu for options
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Start Focus", command=self.start_focus)
        self.menu.add_command(label="Toggle Float", command=self.toggle_float)
        self.menu.add_command(label="Exit", command=self.root.quit)
        self.pet_label.bind("<Button-3>", self.show_menu)

        # Start updates
        self.is_focusing = False
        self.update_pet()
        self.animate()
        self.root.mainloop()

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        new_x = self.root.winfo_x() + deltax
        new_y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{new_x}+{new_y}")

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def toggle_float(self):
        current = self.root.attributes("-topmost")
        self.root.attributes("-topmost", not current)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def reset_focus(self):
        self.focus_time_left = self.focus_time
        self.timer_label.config(text=self.format_time(self.focus_time_left))
    
    def start_focus(self):
        self.reset_focus()
        self.is_focusing = True

    def update_pet(self):
        if self.is_focusing:
            self.focus_time_left -= 1
            self.timer_label.config(text=self.format_time(self.focus_time_left))
            if self.focus_time_left <= 0:
                self.is_focusing = False
                self.timer_label.config(text="Focus Done!")

        self.root.after(1000, self.update_pet)

    def animate(self):
        # Update the label with the next frame
        self.pet_label.config(image=self.frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % self.frame_count
        # Schedule the next frame (adjust 100 for animation speed, in milliseconds)
        self.root.after(300, self.animate)
        
# Run the pet
if __name__ == "__main__":
    DesktopPet()