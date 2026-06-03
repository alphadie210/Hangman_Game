
import tkinter       # GUI bnane k liye
import random        # random word choose k liye
import requests      # request+BeautifulSoup: web scrapping k liye in future agr words online source s lena chahye toh
from bs4 import BeautifulSoup      # html parsing k liye
from tkinter import messagebox     # pop up message dikhaane k liye

Rows = 25
Cols = 25
Tile_size = 25

word = ""         # actual word jo guess krna h
display_word =[]   # user ko dikhane k liye underscore + revealed letters    
wrong_guess = 0    # glt guess count krne k liye
label_word = None   #label word ko globally access krne k liye, taki update kr ske

#calculate the window size

window_width = Tile_size * Cols
window_height = Tile_size * Rows


class Box:
    def __init__(self, a, b):    # tiles ya positions manage krne k liye
        self.a = a
        self.b = b

window = tkinter.Tk()       # window bna li
window_bg = "tan"
window.configure(bg = window_bg)    # window ka background color set hogya
window.title("HAnGmAn")            # window title
window.resizable(False, False)      # window ka size fix kr diya (resize disabled)

label = tkinter.Label(window, text = "HeLLo! HAnGmAn",       # ek heading label jo window k top p show hoga
                      font = ("Consolas", 18, "bold"), 
                      fg = "firebrick4")
label.pack()

main_frame = tkinter.Frame(window, bg = window_bg)   # frame window k andr h aur isme canvas rkha h
main_frame_bg = "Beige"
main_frame.pack()


''' window_width = Tile_size * Cols   # 28 * 28 = 784
      window_height = Tile_size * Rows  # 28 * 28 = 784
      It means: 784 x 784 px hogya

borderwidth = 0, highlightthickness = 0
   Ye parameters canvas k around extra border ko remove kr dete h
   Mtlb canvas ek clean white area bnega '''


canvas = tkinter.Canvas(main_frame, bg = main_frame_bg, 
                        width = window_width, 
                        height = window_height, borderwidth = 0, 
                        highlightthickness = 0)     # isme drawing kr skte h
canvas.pack(expand = True, fill = "both")      # canvas ko window m display kr deta h

selected_option = tkinter.StringVar(value = "countries")    #var to store selected option

# game start krne k liye function

def start_game():
    global word, display_word, wrong_guess, label_word
    wrong_guess = 0    #reset counter

    # start hone k baad Hide all option buttons

    rb_countries.place_forget()
    rb_capitals.place_forget()
    rb_freedom_fighters.place_forget()
    btn_start.place_forget()

    # Choose word

    choice = selected_option.get()
    if choice == "countries":
        print("Countries selected")
        word = random.choice(get_countries()).lower()
    elif choice == "capitals":
        print("Capitals selected")
        word = random.choice(get_capitals()).lower()
    elif choice == "freedom_fighters":
        print("Freedom Fighters selected")
        word = random.choice(get_freedom_fighters()).lower()

    # reveal some letters
    reveal_count = max(1, len(word)//3)
    reveal_indices = random.sample(range(len(word)),reveal_count)

# words ko underscores + reveal letter k form m store krega

    display_word = []
    for i, ch in enumerate(word):       #jb ek list/string p loop chlaate ho, toh index + value dono ek saath deta h
        if ch == " ":     #agr space h toh usko direct space hi rkho
            display_word.append(" ")
        elif i in reveal_indices:      #plural of index
            display_word.append(ch)
        else:
            display_word.append("__")

     # ✅ Show word according to display mode
    label_word = tkinter.Label(window, text = " ".join(display_word), 
                               font = ("Consolas", 20),
                               wraplength = 600, 
                               justify = "center")
    label_word.place(relx = 0.5, rely = 0.8, anchor = "center")  #label ko window m place kr diya

    #Bind key press
    window.bind("<Key>", check_guess)       # jb user koi key press kre, function call hoga
    # us func ko event obj pass hota h jis m key press ki details hoti h
  

def get_countries():     # list scrape krne k liye
    url = ("https://geographyfieldwork.com/WorldCapitalCities.htm")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")   # table k rows nikal lo
    countries = []
    for row in rows[1:]:   # first row header hota h, skip kro
        cols = row.find_all("td")
        if len(cols) >= 2:  # ensure row m do column ho
            country = cols[0].text.strip()
            if country.isalpha():    #ensure country name m sirf letters ho, spaces ya special char na ho
                countries.append(country)
    return countries


def get_capitals():       # list scrape krne k liye
    url = ("https://geographyfieldwork.com/WorldCapitalCities.htm")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    capitals = []
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 2:
            capital = cols[1].text.strip()
            if capital.isalpha():
                capitals.append(capital)
    return capitals


def get_freedom_fighters():       # list scrape krne k liye
    url = "https://vajiramandravi.com/current-affairs/freedom-fighters-of-india/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")
    freedom_fighters = []
    for row in rows[1:]:
         cols = row.find_all("td")
         if len(cols) >= 2:
            fighter = cols[0].text.strip()
            if fighter.isalpha():
                freedom_fighters.append(fighter)
    return freedom_fighters


# Widgets section / user ko category select krne k liye buttons

rb_countries = tkinter.Radiobutton(window, text = "Countries", 
                    variable = selected_option, 
                    value = "countries", 
                    fg = "steelblue4", 
                    font = ("Comic Sans MS", 15, "bold"))
                    
rb_capitals = tkinter.Radiobutton(window, text = "Capitals", 
                    variable = selected_option, 
                    value = "capitals",
                    fg = "navy",
                    font = ("Comic Sans MS", 15, "bold"))
                    
rb_freedom_fighters = tkinter.Radiobutton(window, text = "Freedom Fighters", 
                    variable = selected_option, 
                    value = "freedom_fighters",
                    fg = "midnightblue",
                    font = ("Comic Sans MS", 15, "bold"))
                    
# jo key press hui h usko guess k form m leta h

def check_guess(event):
    global display_word, word, wrong_guess, label_word
    guess = event.char.lower()      #jo key press hui h
 
# agr guess shi h toh word update krega

    if guess in word:
        for i, ch in enumerate(word):
            if ch == guess:
                display_word[i] = guess

        label_word.config(text = " ".join(display_word))

# agr glt h toh hangman ka ek part draw hoga

    else:
        wrong_guess += 1
        if wrong_guess == 1: draw_gallows()
        elif wrong_guess == 2: draw_head()
        elif wrong_guess == 3: draw_body()
        elif wrong_guess == 4: draw_left_arm()
        elif wrong_guess == 5: draw_right_arm()
        elif wrong_guess == 6: draw_left_leg()
        elif wrong_guess == 7: draw_right_leg()

# win/lose condition check krta h

    if "__"not in display_word:
        messagebox.showinfo("Result","You Win!")
        btn_restart.place(relx = 0.5, rely = 0.9, anchor = "center")
    elif wrong_guess == 7: 
        messagebox.showinfo("Result","Game Over!")
        label_word.config(text = " ".join(word))   # underlined jgh pr word show hoga
        btn_restart.place(relx = 0.5, rely = 0.9, anchor = "center")

# restart Function section

def restart_game():
    global wrong_guess, label_word
    wrong_guess = 0
    canvas.delete("all")

    if label_word:
        label_word.destroy()   # label clear
        label_word = None

    window.unbind("<Key>")    #key bind remove kr diya, taki restart hone k baad user key press kr k game start ho ske

# game restart hone p buttons vps show krega
    rb_countries.place(relx=0.5, rely=0.5, anchor="center")
    rb_capitals.place(relx=0.5, rely=0.4, anchor="center")
    rb_freedom_fighters.place(relx=0.5, rely=0.6, anchor="center")
    btn_start.place(relx=0.5, rely=0.7, anchor="center")
    btn_restart.place_forget()

# start aur restart k buttons
btn_start = tkinter.Button(window, text = "Start Game", command = start_game,
               font = ("Helvetica", 18, "bold"), 
               fg = "hotpink4")

btn_restart = tkinter.Button(window, text = "Restart Game", command = restart_game,
                            font = ("Helvetica", 15, "bold"),
                            fg = "mediumpurple2")

rb_countries.place(relx = 0.5, rely = 0.5, anchor = "center")
rb_capitals.place(relx = 0.5, rely = 0.4, anchor = "center")
rb_freedom_fighters.place(relx = 0.5, rely = 0.6, anchor = "center")
btn_start.place(relx = 0.5, rely = 0.7, anchor = "center")


center_x = window_width // 2
center_y = window_height // 2

#X‑axis (horizontal)
'''center_x + value → right side jaata hai
center_x - value → left side jaata hai'''

# Y‑axis (vertical)
'''center_y + value → neeche jaata hai
center_y - value → upar jaata hai'''

def draw_gallows():
    canvas.create_line(center_x - 50, center_y + 120, center_x + 70, center_y + 120)     #base
    canvas.create_line(center_x - 25, center_y + 120, center_x - 25, center_y - 160)    #pole
    canvas.create_line(center_x - 25, center_y - 160, center_x + 75, center_y - 160)   #top
    canvas.create_line(center_x + 75, center_y - 160, center_x +75, center_y - 120)    # rope
    canvas.create_line(center_x - 25, center_y - 120, center_x + 25, center_y - 160)   # support beam

def draw_head():
    canvas.create_oval(center_x + 50, center_y - 120, center_x + 100, center_y - 70)

def draw_body():
    canvas.create_line(center_x + 75, center_y - 70, center_x + 75, center_y + 40)

def draw_left_arm():
    canvas.create_line(center_x + 75, center_y - 40, center_x + 35, center_y + 5)

def draw_right_arm():
    canvas.create_line(center_x + 75, center_y - 40, center_x + 115, center_y + 5)

def draw_left_leg():
    canvas.create_line(center_x + 75, center_y + 40, center_x + 50, center_y + 95)

def draw_right_leg():
    canvas.create_line(center_x + 75, center_y + 40, center_x + 100, center_y + 95)

        
window.mainloop()