import tkinter as tk
from .game import Game


class Menu(tk.Frame):
    def __init__(self, parent, _width, _height):
        tk.Frame.__init__(self, parent, width=_width, height=_height)
        self.parent = parent
        self._width = _width
        self._height = _height
        tk.Button(self, text="Jogar", command=self.muda_tela).place(x=0, y=0)

    def muda_tela(self):
        self.janela_jogo = Game(self.parent, self._width, self._height, self)
        self.janela_jogo.place(x=0, y=0)
