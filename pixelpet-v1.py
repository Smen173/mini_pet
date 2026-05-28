import tkinter as tk
import math
import random

COLORS = ["#6af407", "#07f4dc", "#f40707", "#0b07f4", "#f40766", "#ef9d0e", "#6af407"]

class PixelBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PixelBot")
        self.window.geometry("50x50+1400+80")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.config(bg="#F0F0F0")

        self.canvas = tk.Canvas(self.window, width=50, height=50,bg="#F0F0F0", highlightthickness=0)
        self.canvas.pack()

        self.body = self.canvas.create_rectangle(
            0, 0, 50, 50, fill="#601ab1", outline=""
        )

        self.eye_left = self.canvas.create_oval(
            10, 10, 22, 22, fill="black", outline=""
        )

        self.eye_right = self.canvas.create_oval(
            28, 10, 40, 22, fill="black", outline=""
        )

        self.mouth_line = self.canvas.create_line(
            15, 36, 35, 36, fill="black", width=2, smooth=True
        )

        self.mouth_oval = self.canvas.create_oval(
            18, 34, 32, 42, fill="black", outline=""
        )
        self.canvas.itemconfig(self.mouth_oval, state='hidden')

        self.click_animation = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.window.bind("<Button-1>", self.on_click)
        self.window.bind("<Escape>", lambda e: self.window.destroy())
        self.canvas.bind("<ButtonPress-3>", self.on_drag_start)
        self.canvas.bind("<B3-Motion>", self.on_drag)
        self.window.bind("<Alt_L>", self.toggle_mouth)
        self.window.focus_force()    
        self.update_gaze()

    def update_gaze(self):
        wx = self.window.winfo_rootx()
        wy = self.window.winfo_rooty()
        mx = self.window.winfo_pointerx()
        my = self.window.winfo_pointery()

        local_x = mx - wx
        local_y = my - wy

        center_x, center_y = 25, 25
        dx = local_x - center_x
        dy = local_y - center_y
        distance = math.hypot(dx, dy)
        if distance > 0:
            shift_x = 5 * dx / distance
            shift_y = 5 * dy / distance
        else:
            shift_x = shift_y = 0

        self.canvas.coords(
            self.eye_left,
            10 + shift_x, 10 + shift_y,
            22 + shift_x, 22 + shift_y
        )

        self.canvas.coords(
            self.eye_right,
            28 + shift_x, 10 + shift_y,
            40 + shift_x, 22 + shift_y
        )

        self.window.after(50, self.update_gaze)

    def on_click(self, event=None):
        random_color = random.choice(COLORS)
        self.canvas.itemconfig(self.body, fill=random_color)
        self.canvas.itemconfig(self.mouth_line, state="normal")
        self.canvas.itemconfig(self.mouth_oval, state="hidden")
        print("Клик!")
        if self.click_animation:
            self.window.after_cancel(self.click_animation)
        self.click_animation = self.window.after(
            700, lambda: self.canvas.itemconfig(self.body, fill="#601ab1")
        )

    def on_drag_start(self, event):
        self.drag_offset_x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        self.drag_offset_y = self.window.winfo_pointery() - self.window.winfo_rooty()

    def on_drag(self, event):
        self.canvas.itemconfig(self.mouth_oval, state="normal")
        self.canvas.itemconfig(self.mouth_line, state="hidden")
        x = self.window.winfo_pointerx() - self.drag_offset_x
        y = self.window.winfo_pointery() - self.drag_offset_y
        self.window.geometry(f"+{x}+{y}")

    def toggle_mouth(self, event=None):
        if self.canvas.itemcget(self.mouth_oval, 'state') == 'normal':
            self.unsmile()
        else:
            self.smile()

    def smile(self, event=None):
        self.canvas.itemconfig(self.mouth_line, state='hidden')
        self.canvas.itemconfig(self.mouth_oval, state='normal')

    def unsmile(self, event=None):
        self.canvas.itemconfig(self.mouth_oval, state='hidden')
        self.canvas.itemconfig(self.mouth_line, state='normal')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    bot = PixelBot()
    bot.run()