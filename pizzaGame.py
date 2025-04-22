import curses, random, time


stdscr = curses.initscr() # to initialize curses and set default settings to start.
curses.noecho() # to turn off echo in  command prompt.
curses.cbreak() # no need to press Enter.
stdscr.keypad(True) # to active special keys.
curses.curs_set(False) # to remove blinking cursor.
stdscr.nodelay(True) # This code allows the program to keep running without pausing, even if the user doesn't provide input immediately.

# It is better if the player's movement range is one less than the rows and one less than the columns to avoid errors.
maxl = curses.LINES - 1
maxc = curses.COLS - 1

world = [] # whole of stdscr
player_l = player_c = 0 # players's location
foods = []
enemy = []
shoot = []
gun = []
score = 0
life = 3
player_direction = ''
fire_counter = 50


def init():
    global player_l, player_c
    # the game screen layout
    for i in range(0, maxl+1):
        world.append([])
        for j in range(0, maxc+1):
            # in the game screen, each position has a 98% probability of being a ' ' and a 2% probability of being a '.'
            world[i].append(' ' if random.random() > 0.02 else '.')

    # this section determines the locations where food items are placed in the game screen.
    for i in range(20):
        fl, fc = random_place() # location if food
        fa = random.randint(1000, 10000) # age of food
        foods.append((fl, fc, fa))
    
    # this section determines the locations where gun items are placed in the game screen.
    for i in range(10):
        gl, gc = random_place() # location if gun
        gun.append((gl, gc))

    # this section determines the locations where enemy items are placed in the game screen.
    for j in range(7):
        el, ec = random_place() # location of enemy
        enemy.append((el, ec))

    # the player will be placed in the middle of the screen game.
    player_l, player_c = maxl // 2, maxc // 2


def move_enemy():
    global playing, life, player_l, player_c

    for i in range(len(enemy)):
        el, ec = enemy[i]
        # Enemies move with a 5% chance on each update.
        if random.random() > 0.95 :
            if el > player_l :
                el -= 1
        if random.random() > 0.95 :
            if ec > player_c :
                ec -= 1
        if random.random() > 0.95 :
            if el < player_l :
                el += 1
        if random.random() > 0.95 :
            if ec < player_c :
                ec += 1

        el = in_area(el, 0, maxl-1)
        ec = in_area(ec, 0, maxc-1)
        enemy[i] = (el, ec)

        if el == player_l and ec == player_c :
            # If an enemy touches the player, one life is lost.
            if life > 0 :
                life -= 1
                player_l, player_c = maxl // 2, maxc // 2

            # If the player's life reaches zero, the player is destroyed.
            elif life == 0 :
                stdscr.addstr(maxl//2, maxc//2, "YOU DIED!")
                stdscr.refresh()
                time.sleep(2)
                playing = False


# this function is useful for keeping positions (like player or enemy) inside the game screen boundaries.
def in_area(a, min, max):
    if a < min :
        return min
    elif a > max :
        return max
    else :
        return a


# This function generates random coordinates (x, y) within the game screen, It also ensures that the chosen position is empty.
def random_place():
    x = random.randint(0, maxl)
    y = random.randint(0, maxc)

    while world[x][y] != ' ' :
        x = random.randint(0, maxl)
        y = random.randint(0, maxc)

    return x, y


def move(key):
    # get one of UP DOWN LEFT RIGHT keys and go toward that direction
    global player_l, player_c, player_direction

    if key == 'KEY_UP'  and world[player_l-1][player_c] != '.' :
        player_l -= 1
        player_direction = 'up'
    elif key == 'KEY_DOWN' and world[player_l+1][player_c] != '.' :
        player_l += 1
        player_direction = 'down'
    elif key == 'KEY_LEFT' and world[player_l][player_c-1] != '.' :
        player_c -= 1
        player_direction = 'left'
    elif key == 'KEY_RIGHT' and world[player_l][player_c+1] != '.' :
        player_c += 1
        player_direction = 'right'

    player_l = in_area(player_l, 0, maxl-1)
    player_c = in_area(player_c, 0, maxc-1)


def draw():
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i, j, world[i][j]) # Initially, the empty game field is drawn using '.' and ' ' characters.

    stdscr.addstr(1, 1, f"score : {score}")
    stdscr.addstr(2, 1, f"life : {life}")
    stdscr.addstr(3, 1, f"fire : {fire_counter}")

    # showing the foods
    for food in foods :
        fl, fc, fa = food
        stdscr.addch(fl, fc, '*')
    
    # showing the guns
    for g in gun :
        gl, gc = g
        stdscr.addch(gl, gc, '0')

    # showing enemies
    for e in enemy :
        el, ec = e
        stdscr.addch(el, ec, 'E')

    # showing shoots
    for sh in shoot :
        shl, shc, sh_side = sh
        stdscr.addch(shl, shc, 'o')

    # showing the player
    stdscr.addch(player_l, player_c, 'X')

    stdscr.refresh()


def check_food():
    global score, playing

    for i in range(len(foods)) :
        fl, fc, fa = foods[i]
        fa -= 1 # Each time the player moves, the lifetime of each food item decreases by one.

        # Eating a food item grants 10 points and spawns a new one elsewhere on the game field.
        if fl == player_l and fc == player_c :
            score += 10
            fl, fc = random_place()
            fa = random.randint(1000, 10000)
            # If the score exceeds 1000, the player wins the game and the game ends.
            if score > 1000 : 
                stdscr.addstr(maxl//2, maxc//2, "YOU WON!")
                stdscr.refresh() # to display stdscr changes on the screen
                time.sleep(2)
                playing = False

        # If the food's lifetime ends, a new random food item will spawn.
        if fa <= 0 :
            fl, fc = random_place()
            fa = random.randint(1000, 10000)

        foods[i] = (fl, fc, fa)

def check_gun():
    global fire_counter
    # if the player eats the guns in game screen receives 10 more shots
    for i in range(len(gun)):
        gl, gc = gun[i]
        if player_l == gl and player_c == gc :
            fire_counter += 10
            gl, gc = random_place()
        gun[i] = (gl, gc)
    

# this function calculates the movement direction of fire based on the current player direction,
def fire(): # new
    global player_direction, fire_counter
    direction = {'right': (0, 1), 'left': (0, -1), 'up': (-1, 0), 'down': (1, 0)}
    # If the player has a shot, can shoot.
    if fire_counter :
        if player_direction :
            dl, dc = direction[player_direction]
        elif not(player_direction) :
            dl, dc = direction['up']
        fire_counter -= 1
        shoot.append((player_l + dl, player_c + dc, player_direction))


def move_fire():
    global score
    new_shoot = []
    # fire moves based on it's direction.
    for shl, shc, sh_side in shoot:
        if sh_side == 'right' and random.random() > 0.4:
            shc += 1
        elif sh_side == 'left' and random.random() > 0.4:
            shc -= 1
        elif sh_side == 'up' and random.random() > 0.4:
            shl -= 1
        elif sh_side == 'down' and random.random() > 0.4:
            shl += 1
        # fires are destroyed if they leave the game board.
        if shl < 0 or shl >= maxl-1 or shc < 0 or shc >= maxc-1 :
            continue
        # fires are destroyed if they hit obstacles.
        elif world[shl][shc] == '.':
            continue
        # If fires and enemies collide, both will be destroyed.
        hit_enemy = False
        for i in range(len(enemy)):
            el, ec = enemy[i]
            if shl == el and shc == ec :
                el, ec = random_place()
                enemy[i] = (el, ec)
                hit_enemy = True
            if hit_enemy :
                break
        if hit_enemy :
            score += 10
            continue
        new_shoot.append((shl, shc, sh_side))

    shoot[:] = new_shoot


# start
init()
playing = True

while playing :
    try :
        key = stdscr.getkey()
    except :
        key = ''
    valid_keys = ['KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'] # playing keys
    if key in valid_keys :
         move(key)
    elif key == 'q': # key to exit
        playing = False  # Exit the while loop
    elif key == ' ': # key to fire
        fire()

    check_food()
    check_gun()
    move_enemy()
    move_fire()
    time.sleep(0.01)
    draw()