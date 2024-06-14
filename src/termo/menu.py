import tkinter as tk
from .game import Game


class Menu(tk.Frame):
    def __init__(self, parent, _width, _height):
        tk.Frame.__init__(self, parent, width=_width, height=_height)
        self.parent = parent
        self._width = _width
        self._height = _height
        self.place_widgets()

    def place_widgets(self):
        tk.Button(self, text="Play", command=self.screen_change).place(x=0, y=0)
        modeOptions = tk.Frame(self, borderwidth=1, width=100, height=140, relief="solid")
        modeOptions.place(x=50, y=30)
        self.modeVar = tk.IntVar()
        fourLetters = tk.Radiobutton(modeOptions, text="4 Letters", variable=self.modeVar, value=4)
        fiveLetters = tk.Radiobutton(modeOptions, text="5 Letters", variable=self.modeVar, value=5)
        sixLetters = tk.Radiobutton(modeOptions, text="6 Letters", variable=self.modeVar, value=6)
        fourLetters.place(x=10, y=40, anchor='sw')
        fiveLetters.place(x=10, y=80, anchor='sw')
        sixLetters.place(x=10, y=120, anchor='sw')
        fourLetters.select()

    def screen_change(self):
        self.game_window = Game(self.parent, self._width, self._height, self, self.modeVar.get())
        self.game_window.place(x=0, y=0)

