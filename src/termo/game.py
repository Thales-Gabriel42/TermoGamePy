import tkinter as tk
from random import randint
from tkinter import messagebox
import os, sys


class Game(tk.Frame):
    def __init__(self, parent, w, h, _menu, _mode):
        tk.Frame.__init__(self, parent)
        self.config(width=w, height=h, bg="gray25")
        self.ignoreChar = [38, 40, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 96, 97, 98, 99,
                           100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 111, 112,
                           113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 186,
                           187, 188, 189, 190, 191, 192, 193, 194, 219, 220, 221, 222]
        self.keyboard = [list("QWERTYUIOP"), list(
            "ASDFGHJKL"), list("ZXCVBNM")]
        self._width = w
        self._height = h
        self.word = ""
        self.isRight = False
        self.varTxt = {}
        self.row = 0
        self.entries = []
        self.mode = _mode
        self.chances = 7
        self.count = {}
        self.color = None
        self.menu = _menu
        self.proceed = True

        tk.Button(self, text='Menu', command=self.screen_change).place(x=0, y=0)

        self.define_word()
        self.create_board()

    def place_keyboard(self):
        fW = self.frmKeyBoard.cget("width")
        fH = self.frmKeyBoard.cget("height")
        lWidth = int((fW-fW/8) / (len(self.keyboard[0])))
        lHeight = lWidth
        place = len(self.keyboard[0])
        iX = (fW - (lWidth*place)-lWidth-place)/2
        iY = (fH - (lHeight*len(self.keyboard)))/2
        i = 0
        for lista in self.keyboard:
            for tecla in lista:
                t = tk.Label(self.frmKeyBoard, bg="gray", text=tecla)
                t.place(x=iX, y=iY, width=lWidth, height=lHeight)
                iX += int(lWidth+5)

            if (i == 1):
                t = tk.Label(self.frmKeyBoard, bg="gray",
                             text="⌫", font=("Arial", 15))
                t.place(x=iX, y=iY, width=lWidth, height=lHeight)
            if (i == 2):
                t = tk.Label(self.frmKeyBoard, bg="gray", text="ENTER")
                t.place(x=iX, y=iY, width=lWidth*2.5, height=lHeight)

            place = len(self.keyboard[i])
            iX = (fW - (lWidth*place)-lWidth)/2
            iY += int(lWidth+10)
            i += 1

    def define_word(self):
        path = self.resource_path(".\\src\\termo\\data\\" + str(self.mode) + "letters.txt")
        words = []
        with open(path, 'r') as file:
            for word in file:
                words.append(word.strip())
            self.word = words[randint(0, len(words))]
            
    def reset_count(self):
        for letter in self.word:
            self.count[letter] = self.word.count(letter)

    def verify_letters(self):
        rightLetters = 0
        for i in range(0, self.mode):
            if self.entries[self.row][i].get() in self.count.keys():
                if self.count[self.entries[self.row][i].get()] > 0:
                    if self.entries[self.row][i].get() == self.word[i]:
                        self.entries[self.row][i].config(
                            disabledbackground="SpringGreen2")
                        self.count[self.entries[self.row][i].get()] -= 1
                        for k in self.frmKeyBoard.children:
                            if self.frmKeyBoard.children[k].cget("text") == self.word[i]:
                                self.frmKeyBoard.children[k].config(
                                    bg="SpringGreen2")

        for i in range(0, self.mode):
            if self.entries[self.row][i].get() in self.word and self.entries[self.row][i].cget("disabledbackground") != "SpringGreen2" and self.count[self.entries[self.row][i].get()] != 0:
                self.entries[self.row][i].config(
                    disabledbackground="RoyalBlue2")
                self.count[self.entries[self.row][i].get()] -= 1
            for k in self.frmKeyBoard.children:
                if self.frmKeyBoard.children[k].cget("text") in self.word:
                    if self.frmKeyBoard.children[k].cget("text") == self.entries[self.row][i].get() and self.frmKeyBoard.children[k].cget("bg") != "SpringGreen2":
                        self.frmKeyBoard.children[k].config(bg="RoyalBlue2")
                elif self.frmKeyBoard.children[k].cget("text") == self.entries[self.row][i].get():
                    self.frmKeyBoard.children[k].config(bg="firebrick2")

        for i in range(0, self.mode):
            if self.entries[self.row][i].cget("disabledbackground") == "SpringGreen2":
                rightLetters += 1
        if rightLetters == self.mode and self.row < self.chances:
            self.isRight = True
            messagebox.showinfo("Congratulations", "Congratulations! The word is correct!")
        elif not self.isRight and self.row == self.chances-1:
            messagebox.showinfo("Out of chances",
                                "What a shame! You are out of chances.")

    def update_board(self):
        self.verify_letters()
        if not self.isRight and self.row < self.chances:
            for e in self.entries[self.row]:
                e.config(state="disabled")
            self.row += 1
            if self.row < self.chances:
                for e in self.entries[self.row]:
                    e.config(state="normal")
                self.entries[self.row][0].focus()
            self.reset_count()              
        else:
            for e in self.entries[self.row]:
                e.config(state="disabled")

    def backspace_press(self, event):
        if self.proceed:
            self.key_pressed(event)
            if event.widget.get() == "" and self.entries[self.row].index(event.widget) > 0:
                self.entries[self.row][self.entries[self.row].index(
                    event.widget) - 1].focus()
            else:
                if self.entries[self.row].index(event.widget) > 0:
                    self.entries[self.row][self.entries[self.row].index(
                        event.widget) - 1].focus()

    def key_released(self, event):
        if self.proceed:
            for k in self.frmKeyBoard.children:
                if self.frmKeyBoard.children[k].cget("text") == event.char.upper():
                    self.frmKeyBoard.children[k].config(bg=self.color)
            if event.keycode >= 65 and event.keycode <= 90 or event.keycode == 39 or event.keycode == 37:
                if len(event.widget.get()) == 1 and event.keycode != 32 and event.keycode != 39 and event.keycode != 37:
                    for k in self.varTxt.keys():
                        if event.widget.winfo_name() == k:
                            self.varTxt[k].set(self.varTxt[k].get().upper())
                            if self.entries[self.row].index(event.widget) < self.mode-1:
                                self.entries[self.row][self.entries[self.row].index(
                                    event.widget) + 1].focus()
                elif event.keycode == 39 and self.entries[self.row].index(event.widget) < self.mode-1:
                    self.entries[self.row][self.entries[self.row].index(
                        event.widget) + 1].focus()
                elif event.keycode == 37 and self.entries[self.row].index(event.widget) > 0:
                    self.entries[self.row][self.entries[self.row].index(
                        event.widget) - 1].focus()
                else:
                    txt = event.widget.get()[0:1].upper()
                    for k in self.varTxt.keys():
                        if event.widget.winfo_name() == k:
                            self.varTxt[k].set(txt)
                    if self.entries[self.row].index(event.widget) < self.mode-1 and event.keycode != 37:
                        self.entries[self.row][self.entries[self.row].index(
                            event.widget) + 1].focus()
            elif (event.widget.get() == " ") or (event.keycode in self.ignoreChar):
                txt = ""
                for k in self.varTxt.keys():
                    if event.widget.winfo_name() == k:
                        self.varTxt[k].set(txt) 
            elif event.keycode == 8:
                for k in self.frmKeyBoard.children:
                    if self.frmKeyBoard.children[k].cget("text") == "⌫":
                        self.frmKeyBoard.children[k].config(bg="gray50")
            elif event.keycode == 13:
                self.proceed = False if self.row == self.chances else True
                allLetters = True
                if self.row < self.chances:
                    for i in self.entries[self.row]:
                        if i.get() == "":
                            allLetters = False
                    for k in self.frmKeyBoard.children:
                        if self.frmKeyBoard.children[k].cget("text") == "ENTER":
                            self.frmKeyBoard.children[k].config(bg="gray50")
                    if self.proceed and self.row <= self.chances and not self.isRight and allLetters:
                        self.reset_count()
                        self.update_board()
                else:
                    pass
            else:
                pass

    def key_pressed(self, event):
        if self.proceed:
            if event.keycode == 8:
                for k in self.frmKeyBoard.children:
                    if self.frmKeyBoard.children[k].cget("text") == "⌫":
                        self.frmKeyBoard.children[k].config(bg="SpringGreen2")
            elif event.keycode == 13:
                for k in self.frmKeyBoard.children:
                    if self.frmKeyBoard.children[k].cget("text") == "ENTER":
                        self.frmKeyBoard.children[k].config(bg="SpringGreen2")
            else:
                for k in self.frmKeyBoard.children:
                    if self.frmKeyBoard.children[k].cget("text") == event.char.upper():
                        self.color = self.frmKeyBoard.children[k].cget("bg")
                        self.frmKeyBoard.children[k].config(bg="SpringGreen3")

    def create_board(self):
        entWid = 70
        entHei = 70
        for i in range(self.chances):
            row = []
            for j in range(self.mode):
                wrt = tk.StringVar(self)
                e = tk.Entry(self, border=1, relief="solid", textvariable=wrt,
                             justify=tk.CENTER, font=('Georgia 20 bold'),
                             background="gray30", disabledbackground="gray40",
                             disabledforeground="gray0")
                e.bind("<KeyRelease>", self.key_released)
                e.bind("<KeyPress-BackSpace>", self.backspace_press, "+")
                e.bind("<KeyPress-Delete>", self.backspace_press, "+")
                e.bind('<KeyPress>', self.key_pressed, "+")
                self.varTxt[e.winfo_name()] = wrt
                row.append(e)
            self.entries.append(row)
        tW = self._width
        tH = self._height
        kBoardWidth = round(tW/2)
        kBoardHeight = kBoardWidth/2
        place = (entHei + entWid)/1.9
        self.frmKeyBoard = tk.Frame(self, bg=self.cget(
            "bg"), width=kBoardWidth, height=kBoardHeight)
        frmX = int((tW - (kBoardWidth))/2)
        frmY = int((tH - (kBoardHeight+place * self.chances) - place)/2)
        self.place_keyboard()
        self.frmKeyBoard.place(x=frmX, y=frmY)

        xP = int((tW - (place * self.mode))/2)
        yP = int((tH - (place * self.chances)+kBoardHeight)/2)
        for i in range(self.chances):
            for j in range(self.mode):
                if i != 0:
                    self.entries[i][j].config(state="disabled")
                elif i == 0 and j == 0:
                    self.entries[i][j].focus()
                self.entries[i][j].place(x=xP, y=yP, width=entWid,
                                         height=entHei, bordermode="outside")
                xP += place
            xP = int((tW - (place * self.mode))/2)
            yP += place

    def screen_change(self):
        self.place_forget()
        self.menu.place(x=0, y=0)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)