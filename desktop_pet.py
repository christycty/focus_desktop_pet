import tkinter as tk
from tkinter import Label, Button
import time
import os
import platform
from PIL import Image, ImageTk, ImageSequence

class DesktopPet:
    def __init__(self):
        # Create a root window
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)

        # Load and preprocess animated GIF
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gif_path = os.path.join(script_dir, "coding_snoopy.gif")
        
        gif = Image.open(gif_path)
        self.frames = []
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            resized_frame = frame.resize((100, 100), Image.NEAREST)
            self.frames.append(ImageTk.PhotoImage(resized_frame))

        # Animation variables
        self.current_frame = 0
        self.frame_count = len(self.frames)

        # Create pet label with the first frame
        self.pet_label = Label(self.root, image=self.frames[0], borderwidth=0, highlightthickness=0)
        self.pet_label.pack()

        # Platform-specific transparency
        if platform.system() == "Windows":
            self.root.config(bg="#FF00FF")
            self.pet_label.config(bg="#FF00FF")
            self.root.wm_attributes("-transparentcolor", "#FF00FF")
        elif platform.system() == "Darwin":  # macOS
            self.root.attributes("-transparent", True)
            self.root.config(bg="systemTransparent")
            self.pet_label.config(bg="systemTransparent")

        # Initial position on desktop
        self.root.geometry(f"+{100}+{self.root.winfo_screenheight()-200}")

        # Timer stats
        self.focus_time_left = 25 * 60  # Default 25 minutes
        self.initial_focus_time = self.focus_time_left
        self.is_focusing = False
        self.is_playing = False

        # Timer frame for - [label] + and play/stop
        self.timer_frame = tk.Frame(self.root, bg="black")
        self.timer_frame.pack()

        # Timer adjustment widgets
        self.minus_button = Button(self.timer_frame, text="-", command=self.decrease_time, bg="black", fg="white")
        self.minus_button.pack(side=tk.LEFT)
        
        self.time_label = Label(self.timer_frame, text=self.format_time(self.initial_focus_time), 
                               font=("Arial", 12), bg="black", fg="white")
        self.time_label.pack(side=tk.LEFT)
        
        self.plus_button = Button(self.timer_frame, text="+", command=self.increase_time, bg="black", fg="white")
        self.plus_button.pack(side=tk.LEFT)

        # Play/Stop button
        self.play_stop_button = Button(self.timer_frame, text="▶", command=self.toggle_play_stop, 
                                      bg="black", fg="white")
        self.play_stop_button.pack(side=tk.LEFT)  # Added padding for spacing
        
        self.reset_button = Button(self.timer_frame, text="⟳", command=self.reset_timer, 
                          bg="black", fg="white")

        # Bind mouse events for dragging
        self.pet_label.bind("<Button-1>", self.start_drag)
        self.pet_label.bind("<B1-Motion>", self.drag)

        # Context menu for options
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Start Focus", command=self.start_focus)
        self.menu.add_command(label="Reset Timer", command=self.reset_timer)
        self.menu.add_command(label="Toggle Float", command=self.toggle_float)
        self.menu.add_command(label="Exit", command=self.root.quit)
        self.pet_label.bind("<Button-3>", self.show_menu)

        # Start updates and animation
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

    def decrease_time(self):
        if self.initial_focus_time >= 300:  # Minimum 5 minutes
            self.initial_focus_time -= 300
            self.focus_time_left = self.initial_focus_time
            self.time_label.config(text=self.format_time(self.initial_focus_time))

    def increase_time(self):
        self.initial_focus_time += 300
        self.focus_time_left = self.initial_focus_time
        self.time_label.config(text=self.format_time(self.initial_focus_time))

    def toggle_play_stop(self):
        if not self.is_focusing:  # Before session starts
            self.start_focus()
        else:  # During session
            self.is_playing = not self.is_playing
            self.play_stop_button.config(text="▶" if not self.is_playing else "⏸")

    def start_focus(self):
        if not self.is_focusing:
            self.is_focusing = True
            self.is_playing = True
            self.minus_button.pack_forget()
            self.plus_button.pack_forget()
            self.time_label.config(text=self.format_time(self.focus_time_left))
            self.play_stop_button.config(text="⏸")            
            self.reset_button.pack(side=tk.LEFT)
            
    def reset_timer(self):
        self.is_focusing = False
        self.is_playing = False
        self.focus_time_left = self.initial_focus_time
        
        self.reset_button.pack_forget()
        self.play_stop_button.pack_forget()
        self.play_stop_button.config(text="▶")
        
        self.time_label.config(text=self.format_time(self.initial_focus_time))
    
        self.minus_button.pack(side=tk.LEFT)
        self.play_stop_button.pack(side=tk.LEFT)    
        self.plus_button.pack(side=tk.LEFT)
        
    def update_pet(self):
        if self.is_focusing and self.is_playing:
            self.focus_time_left -= 1
            self.time_label.config(text=self.format_time(self.focus_time_left))
            if self.focus_time_left <= 0:
                self.is_focusing = False
                self.is_playing = False
                self.time_label.config(text="Focus Done!")
                self.play_stop_button.config(text="▶")
                self.minus_button.pack(side=tk.LEFT)
                self.plus_button.pack(side=tk.LEFT)
                self.focus_time_left = self.initial_focus_time
                self.time_label.config(text=self.format_time(self.initial_focus_time))
        self.root.after(1000, self.update_pet)

    def animate(self):
        if self.is_playing:
            self.pet_label.config(image=self.frames[self.current_frame])
            self.current_frame = (self.current_frame + 1) % self.frame_count
        self.root.after(300, self.animate)

if __name__ == "__main__":
    DesktopPet()