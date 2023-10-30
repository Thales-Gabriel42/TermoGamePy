from src.termo import game
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    width = 800
    height = 900
    x = round((root.winfo_screenwidth() - width)/2)
    y = round((root.winfo_screenheight() - height)/2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(0, 0)
    t1 = game.Game(root, 800, 900)
    # m = Menu(root, width, height, t1)
    t1.place(x=0, y=0)
    root.mainloop()