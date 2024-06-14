import tkinter as tk

from src.termo.menu import Menu

if __name__ == '__main__':
    root = tk.Tk()
    width = 800
    height = 900
    x = round((root.winfo_screenwidth() - width)/2)
    y = round((root.winfo_screenheight() - height)/2)
    root.title("TermoGamePy")
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.resizable(False, False)
    app = Menu(root, 800, 900)
    app.place(x=0, y=0)
    root.mainloop()
