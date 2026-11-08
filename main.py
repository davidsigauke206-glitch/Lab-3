import os
import random
import winsound
import tkinter as tk
from tkinter import messagebox

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "0123456789"

# folder where this file is, so bg.png and music.wav are always found
FOLDER = os.path.dirname(os.path.abspath(__file__))


# ---------- 1. Key generation (variant 7) ----------
def generate_key(word):
    word = word.upper()                 # "master" -> "MASTER"

    # blocks 1 and 3: letters of the word in random order
    letters = list(word)                # string -> list of letters
    random.shuffle(letters)             # shuffle the list (перемешать)
    block1 = "".join(letters[:3])       # first 3 letters (срез / slice)
    block3 = "".join(letters[3:])       # last 3 letters

    # block 2: letter's number in the alphabet, keep only the last digit
    digits = ""
    for letter in word:
        # index starts at 0, so +1:  M -> 13
        number = ALPHABET.index(letter) + 1
        # 13 -> "3" (остаток от деления)
        digits = digits + str(number % 10)

    return block1 + "-" + digits + "-" + block3


# ---------- 2. Input check ----------
def is_valid(word):
    if len(word) != 6:                  # must be exactly 6 characters
        return False
    for letter in word.upper():
        if letter not in ALPHABET:      # only Latin letters A-Z allowed
            return False
    return True


# ---------- 3. Key animation (bonus task / допзадание) ----------
def animate_key(key, frame=0):
    # how many symbols have stopped (целочисленное деление)
    locked = frame // 3

    shown = ""
    for i in range(len(key)):
        if i < locked or key[i] == "-":
            # this symbol is already final
            shown = shown + key[i]
        else:
            # still spinning: random letter or digit
            shown = shown + random.choice(ALPHABET + DIGITS)

    key_label.config(text=shown)

    if locked < len(key):
        # draw the next frame in 40 ms
        window.after(40, animate_key, key, frame + 1)
    else:
        key_label.config(fg="lime")     # key is ready -> turn green
        button.config(state="normal")   # turn the button back on


# ---------- 4. Button click ----------
def on_click():
    word = entry.get().strip()          # read the input, remove spaces
    if not is_valid(word):
        messagebox.showerror(
            "Ошибка", "Введите слово ровно из 6 латинских букв (A-Z)")
        return                          # stop here, don't make a key
    key = generate_key(word)
    button.config(state="disabled")     # button off while animating
    key_label.config(fg="white")
    animate_key(key)                    # start the animation


# ---------- 5. Music (bonus task / допзадание) ----------
def start_music():
    # ASYNC = play in background, LOOP = repeat forever
    winsound.PlaySound(
        os.path.join(FOLDER, "music.wav"),
        winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)


def on_close():
    winsound.PlaySound(None, 0)         # stop the music
    window.destroy()                    # close the window


# ---------- 6. Window (главное окно) ----------
window = tk.Tk()
window.title("Halo Keygen")

# background: picture from the game (bg.png is next to main.py)
bg_image = tk.PhotoImage(file=os.path.join(FOLDER, "bg.png"))
# window size = picture size
window.geometry(str(bg_image.width()) + "x" + str(bg_image.height()))
window.resizable(False, False)          # user can't resize the window

bg_label = tk.Label(window, image=bg_image)
# picture covers the whole window
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# text label (метка); relx=0.5 -> middle of the window
hint = tk.Label(window, text="Введите слово из 6 букв:",
                font=("Arial", 14, "bold"), bg="black", fg="white")
hint.place(relx=0.5, rely=0.06, anchor="center")

# input field (поле ввода)
entry = tk.Entry(window, font=("Consolas", 16), justify="center", width=12)
entry.place(relx=0.5, rely=0.12, anchor="center")

# button (кнопка): command = function to run on click (no brackets!)
button = tk.Button(window, text="Сгенерировать", font=("Arial", 12, "bold"),
                   bg="gold", command=on_click)
button.place(relx=0.5, rely=0.18, anchor="center")

# key field (поле для ключа)
key_label = tk.Label(window, text="XXX-XXXXXX-XXX",
                     font=("Consolas", 20, "bold"), bg="black", fg="lime")
key_label.place(relx=0.5, rely=0.25, anchor="center")

# what happens when you click X
window.protocol("WM_DELETE_WINDOW", on_close)
start_music()
# event loop (цикл обработки событий), always the last line
window.mainloop()