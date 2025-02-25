import curses
import random
import time

stdscr = curses.initscr() # to initialize curses and set default settings to start
curses.noecho() # to turn off echo in  command prompt
curses.cbreak() # no need to press Enter
stdscr.keypad(True)
curses.curs_set(False)
stdscr.nodelay(True)

maxl = curses.LINES - 1
maxc = curses.COLS - 1 # to solve error

world = []
player_l = player_c = 0
foods = []
enemy = []
score = 0

def init():
    # the player
    global player_l, player_c
    for i in range(0, maxl+1):
        world.append([])
        for j in range(0, maxc+1):
            world[i].append(' ' if random.random() > 0.02 else '.')
    # foods
    for i in range(20):
        fl, fc = random_place()
        fa = random.randint(1000, 10000)
        foods.append((fl, fc, fa))
    # enemies
    for j in range(7):
        el, ec = random_place()
        enemy.append((el, ec))
    player_l, player_c = random_place()

def move_enemy():
    global playing, life
    for i in range(len(enemy)):
        el, ec = enemy[i]
        # enemies speed
        if random.random() > 0.94 :
            if el > player_l :
                el -= 1
        if random.random() > 0.94 :
            if ec > player_c :
                ec -= 1
        if random.random() > 0.94 :
            if el < player_l :
                el += 1
        if random.random() > 0.94 :
            if ec < player_c :
                ec += 1
        el = in_area(el, 0, maxl-1)
        ec = in_area(ec, 0, maxc-1)
        enemy[i] = (el, ec)
        if el == player_l and ec == player_c :
            stdscr.addstr(maxl//2, maxc//2, "YOU DIED!")
            stdscr.refresh()
            time.sleep(2)
            playing = False

def in_area(a, min, max):
    if a < min :
        return min
    elif a > max :
        return max
    else :
        return a

def random_place():
    x = random.randint(0, maxl)
    y = random.randint(0, maxc)
    while world[x][y] != ' ' :
        x = random.randint(0, maxl)
        y = random.randint(0, maxc)
    return x, y

def move(c):
    '''get one of asdw and go toward that direction'''
    global player_l, player_c
    if c == 'w'  and world[player_l-1][player_c] != '.' :
        player_l -= 1
    elif c == 's' and world[player_l+1][player_c] != '.' :
        player_l += 1
    elif c == 'a' and world[player_l][player_c-1] != '.' :
        player_c -= 1
    elif c == 'd' and world[player_l][player_c+1] != '.' :
        player_c += 1
    player_l = in_area(player_l, 0, maxl - 1)
    player_c = in_area(player_c, 0, maxc - 1)

def draw():
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j])
    stdscr.addstr(1, 1, f"score : {score}")
    # showing the foods
    for food in foods :
        fl, fc, fa = food
        stdscr.addch(fl, fc, '*')
    # showing enemies
    for e in enemy :
        el, ec = e
        stdscr.addch(el, ec, 'E')
    stdscr.addch(player_l, player_c, 'X')
    stdscr.refresh()

def check_food():
    global score, playing
    for i in range(len(foods)) :
        fl, fc, fa = foods[i]
        fa -= 1
        if fl == player_l and fc == player_c :
            score += 10
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
            if score > 1000 :
                stdscr.addstr(maxl//2, maxc//2, "YOU WON!")
                stdscr.refresh()
                time.sleep(2)
                playing = False
        if fa <= 0 :
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
        foods[i] = (fl, fc, fa)

init()
playing = True
while playing :
    try :
        c = stdscr.getkey()
    except :
        c = ''
    if c in 'asdw': # playing keys
         move(c)
    elif c == 'q': # key to exit
        playing = False  # Exit the while loop
    check_food()
    move_enemy()
    time.sleep(0.01)
    draw()