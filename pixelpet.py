import tkinter as tk
import math
import random

COLORS = ["#6af407", "#07f4dc", "#f40707", "#0b07f4", "#f40766", "#ef9d0e", "#6af407"]

class PixelBot:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PixelBot")
        self.window.geometry("150x150+1400+80")
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)

        self.transparent_color = "#010101"
        self.window.wm_attributes("-transparentcolor", self.transparent_color)
        
        self.canvas = tk.Canvas(
            self.window, width=150, height=150,
            bg=self.transparent_color, highlightthickness=0
        )
        self.canvas.pack()

        self.body = self.canvas.create_rectangle(
            50, 50, 100, 100, fill="#601ab1", outline=""
        )
        # self.mask = self.canvas.create_rectangle(
        #     52, 54, 98, 78,          # от x=52 до 98, y=54 до 78 (шире и выше глаз)
        #     fill="white", outline=""
        # )
        
        self.eye_left = self.canvas.create_oval(
            80, 62, 88, 70, fill="black", outline=""
        )
        self.eye_right = self.canvas.create_oval(
            62, 62, 70, 70, fill="black", outline=""
        )
        self.mouth_line = self.canvas.create_line(
            65, 86, 85, 86, fill="black", width=2, smooth=True         
        )

        self.mouth_oval = self.canvas.create_oval(68, 84, 82, 92, fill="black", outline="")
        self.canvas.itemconfig(self.mouth_oval, state='hidden')

        self.click_animation = None

        self.window.bind("<Button-1>", self.on_click)
        self.window.bind("<Escape>", lambda e: self.window.destroy())
        self.window.bind("<B3-Motion>", self.on_drag,)
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

        center_x, center_y = 75, 75

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
            60 + shift_x, 60 + shift_y,
            72 + shift_x, 72 + shift_y
        )
        self.canvas.coords(
            self.eye_right,
            78 + shift_x, 60 + shift_y,
            90 + shift_x, 72 + shift_y
        )

        self.window.after(50, self.update_gaze)

    def on_click(self, event = None):
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

    def on_drag(self, event):
        x = self.window.winfo_x()
        y = self.window.winfo_y()
        self.canvas.itemconfig(self.mouth_oval, state="normal")
        self.canvas.itemconfig(self.mouth_line, state="hidden")
        self.window.geometry(f"+{event.x_root - 75}+{event.y_root - 75}")

    def toggle_mouth(self, event = None):
        if self.canvas.itemcget(self.mouth_oval, 'state') == 'normal':
            self.unsmile()
        else:
            self.smile()

    def smile(self,event = None):
            self.canvas.itemconfig(self.mouth_line, state='hidden')
            self.canvas.itemconfig(self.mouth_oval, state='normal')

    def unsmile(self, event = None):
            self.canvas.itemconfig(self.mouth_oval, state='hidden')
            self.canvas.itemconfig(self.mouth_line, state='normal')

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    bot = PixelBot()
    bot.run()