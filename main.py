import os
import sys
import random
import time

try:
    import msvcrt
    def read_key():
        key = msvcrt.getch()
        if key in (b'\x00', b'\xe0'):
            sub_key = msvcrt.getch()
            if sub_key == b'H': return 'up'
            if sub_key == b'P': return 'down'
            if sub_key == b'K': return 'left'
            if sub_key == b'M': return 'right'
        if key in (b'\r', b'\n'): return 'enter'
        return key.decode("utf-8", errors="ignore").lower()

    def get_key_non_blocking():
        if msvcrt.kbhit():
            return read_key()
        return None

    def wait_for_key():
        return read_key()

except ImportError:
    import select
    import tty
    import termios
    def read_raw_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch1 = sys.stdin.read(1)
            if ch1 == '\x1b':
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    ch2 = sys.stdin.read(1)
                    if ch2 == '[':
                        ch3 = sys.stdin.read(1)
                        if ch3 == 'A': return 'up'
                        if ch3 == 'B': return 'down'
                        if ch3 == 'D': return 'left'
                        if ch3 == 'C': return 'right'
            if ch1 in ('\r', '\n'): return 'enter'
            return ch1.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def get_key_non_blocking():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            rlist, _, _ = select.select([sys.stdin], [], [], 0)
            if rlist:
                return read_raw_char()
            return None
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def wait_for_key():
        return read_raw_char()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

os.system("")

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE_BG = "\033[47m\033[30m"
GRAY = "\033[90m"

TILE_COLORS = {
    0: "\033[90m",
    2: "\033[97m",
    4: "\033[36m",
    8: "\033[32m",
    16: "\033[33m",
    32: "\033[35m",
    64: "\033[31m",
    128: "\033[93m",
    256: "\033[92m",
    512: "\033[96m",
    1024: "\033[95m",
    2048: "\033[91m",
}

def play_snake():
    WIDTH, HEIGHT = 20, 10
    snake = [
        [HEIGHT // 2, WIDTH // 2],
        [HEIGHT // 2, WIDTH // 2 - 1],
        [HEIGHT // 2, WIDTH // 2 - 2]
    ]
    direction = 'd'
    score = 0

    def spawn_food(snake_body):
        while True:
            food = [random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1)]
            if food not in snake_body:
                return food

    food = spawn_food(snake)

    def draw_frame():
        clear_screen()
        print(f"{BOLD}Score: {YELLOW}{score}{RESET} | Use {CYAN}[WASD / Arrows]{RESET} to move, {RED}[q]{RESET} to quit")
        print(MAGENTA + "+" + "-" * (WIDTH * 2) + "-+" + RESET)
        
        for r in range(HEIGHT):
            line = MAGENTA + "|" + RESET
            for c in range(WIDTH):
                cell = [r, c]
                if cell == snake[0]:
                    head_char = {'w': '^', 's': 'v', 'a': '<', 'd': '>'}.get(direction, '>')
                    line += f"{BOLD}{YELLOW} {head_char}{RESET}"
                elif cell in snake[1:]:
                    line += f"{GREEN} o{RESET}"
                elif cell == food:
                    line += f"{BOLD}{RED} *{RESET}"
                else:
                    line += "  "
            line += MAGENTA + " |" + RESET
            print(line)
            
        print(MAGENTA + "+" + "-" * (WIDTH * 2) + "-+" + RESET)

    last_update_time = time.time()
    game_speed = 0.15

    while True:
        key = get_key_non_blocking()
        if key == 'q':
            break
        elif key in ('w', 'up'): key = 'w'
        elif key in ('s', 'down'): key = 's'
        elif key in ('a', 'left'): key = 'a'
        elif key in ('d', 'right'): key = 'd'
        else: key = None

        if key in ['w', 'a', 's', 'd']:
            if (key == 'w' and direction != 's') or \
               (key == 's' and direction != 'w') or \
               (key == 'a' and direction != 'd') or \
               (key == 'd' and direction != 'a'):
                direction = key

        if time.time() - last_update_time > game_speed:
            last_update_time = time.time()
            
            head = list(snake[0])
            if direction == 'w': head[0] -= 1
            elif direction == 's': head[0] += 1
            elif direction == 'a': head[1] -= 1
            elif direction == 'd': head[1] += 1

            if head[0] < 0 or head[0] >= HEIGHT or head[1] < 0 or head[1] >= WIDTH:
                draw_frame()
                print(f"\n{RED}Game Over! You hit the wall.{RESET} Final Score: {YELLOW}{score}{RESET}")
                time.sleep(1.5)
                break

            if head in snake:
                draw_frame()
                print(f"\n{RED}Game Over! You bit yourself.{RESET} Final Score: {YELLOW}{score}{RESET}")
                time.sleep(1.5)
                break

            snake.insert(0, head)

            if head == food:
                score += 10
                food = spawn_food(snake)
            else:
                snake.pop()

            draw_frame()
        time.sleep(0.01)

def play_flappy():
    WIDTH, HEIGHT = 25, 12
    bird_y = HEIGHT // 2
    bird_velocity = 0.0
    gravity = 0.45
    lift = -1.5
    pipes = []
    score = 0

    def spawn_pipe():
        gap_y = random.randint(2, HEIGHT - 3)
        pipes.append({'x': WIDTH - 1, 'gap_y': gap_y})

    def draw_frame():
        clear_screen()
        print(f"{BOLD}Score: {YELLOW}{score}{RESET} | Press {CYAN}[w / Up / Space]{RESET} to Flap, {RED}[q]{RESET} to Quit")
        print(BLUE + "+" + "-" * (WIDTH * 2) + "+" + RESET)
        
        grid = [["  " for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
        for p in pipes:
            px = p['x']
            py = p['gap_y']
            if 0 <= px < WIDTH:
                for r in range(HEIGHT):
                    if r < py - 1 or r > py + 1:
                        grid[r][px] = f"{GREEN}▒▒{RESET}"
                        
        int_bird_y = int(round(bird_y))
        if 0 <= int_bird_y < HEIGHT:
            grid[int_bird_y][3] = f"{BOLD}{YELLOW}>(o){RESET}"
            
        for r in range(HEIGHT):
            line = BLUE + "|" + RESET + "".join(grid[r]) + BLUE + "|" + RESET
            print(line)
            
        print(BLUE + "+" + "-" * (WIDTH * 2) + "+" + RESET)

    last_update_time = time.time()
    pipe_timer = time.time()
    game_speed = 0.18

    spawn_pipe()

    while True:
        key = get_key_non_blocking()
        if key == 'q':
            break
        elif key in ('w', 'up', ' '):
            bird_velocity = lift

        if time.time() - last_update_time > game_speed:
            last_update_time = time.time()
            
            bird_velocity += gravity
            bird_y += bird_velocity
            
            if time.time() - pipe_timer > 2.5:
                spawn_pipe()
                pipe_timer = time.time()
                
            for p in pipes:
                p['x'] -= 1
                
            if pipes and pipes[0]['x'] < 0:
                pipes.pop(0)
                score += 10
                
            int_bird_y = int(round(bird_y))
            if int_bird_y < 0 or int_bird_y >= HEIGHT:
                draw_frame()
                print(f"\n{RED}Game Over! You hit the boundary.{RESET} Final Score: {YELLOW}{score}{RESET}")
                time.sleep(1.5)
                break
                
            hit_pipe = False
            for p in pipes:
                if p['x'] == 3:
                    if int_bird_y < p['gap_y'] - 1 or int_bird_y > p['gap_y'] + 1:
                        hit_pipe = True
                        break
                        
            if hit_pipe:
                draw_frame()
                print(f"\n{RED}Game Over! You hit a pipe.{RESET} Final Score: {YELLOW}{score}{RESET}")
                time.sleep(1.5)
                break

            draw_frame()
        time.sleep(0.01)

def play_2048():
    numbers = [[0] * 4 for _ in range(4)]
    score = 0

    def draw_frame():
        clear_screen()
        print(f"{BOLD}Score: {YELLOW}{score}{RESET} | Use {CYAN}[WASD / Arrows]{RESET} to move, {RED}[q]{RESET} to quit")
        print(CYAN + "+------+------+------+------+" + RESET)
        for r in range(4):
            line = CYAN + "|" + RESET
            for c in range(4):
                val = numbers[r][c]
                color = TILE_COLORS.get(val, "\033[93m")
                if val == 0:
                    line += f"{GRAY}  .   {RESET}" + CYAN + "|" + RESET
                else:
                    line += f"{BOLD}{color}{val:^6}{RESET}" + CYAN + "|" + RESET
            print(line)
            print(CYAN + "+------+------+------+------+" + RESET)

    def add_new_number():
        empty_cells = [(r, c) for r in range(4) for c in range(4) if numbers[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            numbers[r][c] = random.choice([2, 4])

    def compress(mat):
        new_mat = [[0] * 4 for _ in range(4)]
        changed = False
        for i in range(4):
            pos = 0
            for j in range(4):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    if pos != j:
                        changed = True
                    pos += 1
        return new_mat, changed

    def merge(mat):
        nonlocal score
        changed = False
        for i in range(4):
            for j in range(3):
                if mat[i][j] != 0 and mat[i][j] == mat[i][j + 1]:
                    mat[i][j] *= 2
                    score += mat[i][j]
                    mat[i][j + 1] = 0
                    changed = True
        return mat, changed

    def reverse(mat):
        return [list(reversed(row)) for row in mat]

    def transpose(mat):
        return [[mat[j][i] for j in range(4)] for i in range(4)]

    def move_left(grid):
        new_grid, c1 = compress(grid)
        new_grid, c2 = merge(new_grid)
        new_grid, _ = compress(new_grid)
        return new_grid, c1 or c2

    def move_right(grid):
        rev = reverse(grid)
        new_grid, c1 = compress(rev)
        new_grid, c2 = merge(new_grid)
        new_grid, _ = compress(new_grid)
        return reverse(new_grid), c1 or c2

    def move_up(grid):
        trans = transpose(grid)
        new_grid, c1 = compress(trans)
        new_grid, c2 = merge(new_grid)
        new_grid, _ = compress(new_grid)
        return transpose(new_grid), c1 or c2

    def move_down(grid):
        trans = transpose(grid)
        rev = reverse(trans)
        new_grid, c1 = compress(rev)
        new_grid, c2 = merge(new_grid)
        new_grid, _ = compress(new_grid)
        final_grid = reverse(new_grid)
        return transpose(final_grid), c1 or c2

    def is_game_over(grid):
        for r in range(4):
            for c in range(4):
                if grid[r][c] == 0: return False
        for r in range(4):
            for c in range(3):
                if grid[r][c] == grid[r][c + 1]: return False
        for r in range(3):
            for c in range(4):
                if grid[r][c] == grid[r + 1][c]: return False
        return True

    add_new_number()
    add_new_number()

    while True:
        draw_frame()
        if is_game_over(numbers):
            print(f"\n{RED}Game Over! No more moves available.{RESET} Final Score: {YELLOW}{score}{RESET}")
            time.sleep(2)
            break

        key = wait_for_key()
        made_move = False

        if key in ('w', 'up'): numbers, made_move = move_up(numbers)
        elif key in ('a', 'left'): numbers, made_move = move_left(numbers)
        elif key in ('s', 'down'): numbers, made_move = move_down(numbers)
        elif key in ('d', 'right'): numbers, made_move = move_right(numbers)
        elif key == 'q': break
        else: continue

        if made_move:
            add_new_number()

def main_menu():
    options = ["Snake", "Flappy Bird", "2048", "Exit Arcade"]
    selected_idx = 0

    while True:
        clear_screen()
        print(MAGENTA + "========================================" + RESET)
        print(f"{BOLD}{CYAN}         TERMINAL ARCADE SUITE          {RESET}")
        print(MAGENTA + "========================================" + RESET)
        print(f"{GRAY} Use [Up/Down] arrows or [W/S] to select{RESET}")
        print(f"{GRAY} Press [Enter] to start                 {RESET}")
        print(MAGENTA + "----------------------------------------" + RESET)

        for idx, option in enumerate(options):
            if idx == selected_idx:
                print(f" {BOLD}{YELLOW}➔  [ {CYAN}{option:^13}{YELLOW} ]{RESET}")
            else:
                print(f"    {GRAY}  {option:^15}  {RESET}")

        print(MAGENTA + "========================================" + RESET)

        key = wait_for_key()

        if key in ('w', 'up'):
            selected_idx = (selected_idx - 1) % len(options)
        elif key in ('s', 'down'):
            selected_idx = (selected_idx + 1) % len(options)
        elif key in ('enter', ' '):
            if selected_idx == 0:
                play_snake()
            elif selected_idx == 1:
                play_flappy()
            elif selected_idx == 2:
                play_2048()
            elif selected_idx == 3:
                clear_screen()
                print(f"{GREEN}Thanks for playing! Goodbye.{RESET}")
                break
        elif key in ('1', '2', '3', '4'):
            idx = int(key) - 1
            if idx == 3:
                clear_screen()
                print(f"{GREEN}Thanks for playing! Goodbye.{RESET}")
                break
            selected_idx = idx

if __name__ == "__main__":
    main_menu()