import tkinter as tk
from random import randint
from tkinter import messagebox

ignoreChar = [38, 40, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 96, 97, 98, 99,
              100, 101, 102, 103, 104, 105, 106, 107, 109, 110, 111, 112,
              113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 186,
              187, 188, 189, 190, 191, 192, 193, 194, 219, 220, 221, 222]
keyboard = [list("QWERTYUIOP"), list("ASDFGHJKL"), list("ZXCVBNM")]
frameBoard = None

palavra = ""
acertou = False
varTxt = {}
linha = 0
entries = []
mode = 4
chances = 7
cont = {}
color = None


def PlacePlacar():
    frmPlacar = tk.Frame(frameBoard, relief="solid",
                         border=1, width=200, height=100)
    lblPlacar = tk.Label(frmPlacar, text="Score", font=("Arial", 15, "bold"))
    lblPlacar.place(x=0, y=0)
    # lblPlacar.place(x=90, y = 30)
    lblCertas = tk.Label(frmPlacar, text="0",  font=("Arial", 15, "bold"))
    lblCertas.place(x=10, y=35)
    lblErradas = tk.Label(frmPlacar, text="0",  font=("Arial", 15, "bold"))
    lblErradas.place(x=40, y=35)
    frmPlacar.place(x=0, y=0)


def PlaceKeyBoard(frame):
    # PlacePlacar()
    global keyboard, frameBoard
    fW = frame.cget("width")
    fH = frame.cget("height")
    lWidth = int((fW-fW/8) / (len(keyboard[0])))
    lHeight = lWidth
    place = len(keyboard[0])
    iX = (fW - (lWidth*place)-lWidth-place)/2
    iY = (fH - (lHeight*len(keyboard)))/2
    i = 0
    for lista in keyboard:
        # lWidth = int(fW / len(lista))
        for tecla in lista:
            t = tk.Label(frame, bg="gray", text=tecla)
            t.place(x=iX, y=iY, width=lWidth, height=lHeight)
            iX += int(lWidth+5)

        if (i == 1):
            t = tk.Label(frame, bg="gray", text="⌫", font=("Arial", 15))
            t.place(x=iX, y=iY, width=lWidth, height=lHeight)
        if (i == 2):
            t = tk.Label(frame, bg="gray", text="ENTER")
            t.place(x=iX, y=iY, width=lWidth*2.5, height=lHeight)

        place = len(keyboard[i])
        iX = (fW - (lWidth*place)-lWidth)/2
        iY += int(lWidth+10)
        i += 1
    frameBoard = frame


def DefWord():
    global palavra, mode
    path = str(mode) + "letras.txt"
    words = []
    with open(path, 'r') as file:
        for letra in file:
            words.append(letra.strip())
        palavra = words[randint(0, len(words))].upper()


def ResetCount():
    global cont
    for letra in palavra:
        cont[letra] = palavra.count(letra)


def Verificar():
    global acertou, frameBoard, palavra
    corretas = 0
    for i in range(0, mode):
        if entries[linha][i].get() in cont.keys() and cont[entries[linha][i].get()] > 0:
            if entries[linha][i].get() == palavra[i]:
                entries[linha][i].config(disabledbackground="SpringGreen2")
                cont[entries[linha][i].get()] -= 1
                for k in frameBoard.children:
                    if frameBoard.children[k].cget("text") == palavra[i]:
                        frameBoard.children[k].config(bg="SpringGreen2")

    for i in range(0, mode):
        if entries[linha][i].get() in palavra and entries[linha][i].cget("disabledbackground") == "gray40" and entries[linha][i].cget("disabledbackground") != "SpringGreen2" and cont[entries[linha][i].get()] != 0:  # AQ
            entries[linha][i].config(disabledbackground="RoyalBlue2")
            cont[entries[linha][i].get()] -= 1
        for k in frameBoard.children:
            if frameBoard.children[k].cget("text") in palavra:
                if frameBoard.children[k].cget("text") == entries[linha][i].get() and frameBoard.children[k].cget("bg") != "SpringGreen2":
                    frameBoard.children[k].config(bg="RoyalBlue2")
            elif frameBoard.children[k].cget("text") == entries[linha][i].get():
                frameBoard.children[k].config(bg="firebrick2")

    for i in range(0, mode):
        if entries[linha][i].cget("disabledbackground") == "SpringGreen2":
            corretas += 1

    if corretas == mode and linha < chances:
        acertou = True
        messagebox.showinfo("Acertou", "Parabéns você acertou a palavra!")
    elif not acertou and linha == chances:
        messagebox.showinfo("Acabaram as chances",
                            "Que pena, suas chances acabaram!")


def AttBoard():
    global linha, acertou, mode
    Verificar()
    if not acertou and linha < chances:
        for e in entries[linha]:
            e.config(state="disabled")
        linha += 1
        if linha < chances:
            for e in entries[linha]:
                e.config(state="normal")
            entries[linha][0].focus()
    else:
        for e in entries[linha]:
            e.config(state="disabled")


def BackSpace(event):
    KeyPressed(event)
    if event.widget.get() == "" and entries[linha].index(event.widget) > 0:
        entries[linha][entries[linha].index(event.widget) - 1].focus()
    else:
        if entries[linha].index(event.widget) > 0:
            entries[linha][entries[linha].index(event.widget) - 1].focus()


def KeyReleased(event):
    global varTxt, entries, linha, color, acertou
    for k in frameBoard.children:
        if frameBoard.children[k].cget("text") == event.char.upper():
            frameBoard.children[k].config(bg=color)
    if event.keycode >= 65 and event.keycode <= 90 or event.keycode == 39 or event.keycode == 37:
        if len(event.widget.get()) == 1 and event.keycode != 32 and event.keycode != 39 and event.keycode != 37:
            for k in varTxt.keys():
                if event.widget.winfo_name() == k:
                    varTxt[k].set(varTxt[k].get().upper())
                    if entries[linha].index(event.widget) < mode-1:
                        entries[linha][entries[linha].index(
                            event.widget) + 1].focus()
        elif event.keycode == 39 and entries[linha].index(event.widget) < mode-1:
            entries[linha][entries[linha].index(event.widget) + 1].focus()
        elif event.keycode == 37 and entries[linha].index(event.widget) > 0:
            entries[linha][entries[linha].index(event.widget) - 1].focus()
        else:
            txt = event.widget.get()[0:1].upper()
            for k in varTxt.keys():
                if event.widget.winfo_name() == k:
                    varTxt[k].set(txt)
            if entries[linha].index(event.widget) < mode-1 and event.keycode != 37:
                entries[linha][entries[linha].index(event.widget) + 1].focus()
    elif (event.widget.get() == " ") or (event.keycode in ignoreChar):
        txt = ""
        for k in varTxt.keys():
            if event.widget.winfo_name() == k:
                varTxt[k].set(txt)
    elif event.keycode == 8:
        for k in frameBoard.children:
            if frameBoard.children[k].cget("text") == "⌫":
                frameBoard.children[k].config(bg="gray50")
    elif event.keycode == 13:
        proceed = False if linha == chances-1 else True
        allLetters = True
        if linha < chances:
            for i in entries[linha]:
                if i.get() == "":
                    allLetters = False
            for k in frameBoard.children:
                if frameBoard.children[k].cget("text") == "ENTER":
                    frameBoard.children[k].config(bg="gray50")
            if proceed and linha <= chances and not acertou and allLetters:
                ResetCount()
                AttBoard()
            elif not proceed and allLetters:
                AttBoard()
                messagebox.showinfo("Acabaram as chances",
                                "Que pena, suas chances acabaram!")
        else:
            pass
    else:
        pass


def KeyPressed(event):
    global color
    # print(event.keycode)
    if event.keycode == 8:
        for k in frameBoard.children:
            if frameBoard.children[k].cget("text") == "⌫":
                frameBoard.children[k].config(bg="SpringGreen2")
    elif event.keycode == 13:
        for k in frameBoard.children:
            if frameBoard.children[k].cget("text") == "ENTER":
                frameBoard.children[k].config(bg="SpringGreen2")
    else:
        for k in frameBoard.children:
            if frameBoard.children[k].cget("text") == event.char.upper():
                color = frameBoard.children[k].cget("bg")
                frameBoard.children[k].config(bg="SpringGreen3")


def CreateBoard(frame):
    global varTxt, entries, mode, chances
    entWid = 70
    entHei = 70
    for i in range(chances):
        row = []
        for j in range(mode):
            wrt = tk.StringVar(frame)
            e = tk.Entry(frame, border=1, relief="solid", textvariable=wrt,
                         justify=tk.CENTER, font=('Georgia 20 bold'),
                         background="gray30", disabledbackground="gray40",
                         disabledforeground="gray0")
            e.bind("<KeyRelease>", KeyReleased)
            e.bind("<KeyPress-BackSpace>", BackSpace, "+")
            e.bind("<KeyPress-Delete>", BackSpace, "+")
            e.bind('<KeyPress>', KeyPressed, "+")
            varTxt[e.winfo_name()] = wrt
            row.append(e)
        entries.append(row)
    tW = frame.cget("width")
    tH = frame.cget("height")
    kBoardWidth = round(tW/2)
    kBoardHeight = kBoardWidth/2
    place = (entHei + entWid)/1.9
    frmKeyBoard = tk.Frame(frame, bg=frame.cget(
        "bg"), width=kBoardWidth, height=kBoardHeight)
    frmX = int((tW - (kBoardWidth))/2)
    frmY = int((tH - (kBoardHeight+place * chances) - place)/2)
    PlaceKeyBoard(frmKeyBoard)
    frmKeyBoard.place(x=frmX, y=frmY)

    xP = int((tW - (place * mode))/2)
    yP = int((tH - (place * chances)+kBoardHeight)/2)
    for i in range(chances):
        for j in range(mode):
            if i != 0:
                entries[i][j].config(state="disabled")
            elif i == 0 and j == 0:
                entries[i][j].focus()
            entries[i][j].place(x=xP, y=yP, width=entWid,
                                height=entHei, bordermode="outside")
            xP += place
        xP = int((tW - (place * mode))/2)
        yP += place


width = 800
height = 900
root = tk.Tk()
x = round((root.winfo_screenwidth() - width)/2)
y = round((root.winfo_screenheight() - height)/2)
root.geometry(f"{width}x{height}+{x}+{y}")
root.resizable(0, 0)
root.title("TermoGamePy")
DefWord()

frmBoard = tk.Frame(root, bg="gray25", width=width, height=height)
frmBoard.place(x=0, y=0)
CreateBoard(frmBoard)
root.mainloop()
