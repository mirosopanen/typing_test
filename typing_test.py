import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the speed typing test")
    stdscr.addstr("\nPress any key to begin")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):

    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM:  {wpm}")
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)


def get_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()


def wpm_test(stdscr):
    text = get_text()
    curr_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:

        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(curr_text) / (time_elapsed/60)) / 5)

        stdscr.clear()
        display_text(stdscr, text, curr_text, wpm)

        stdscr.refresh()

        if "".join(curr_text) == text:
            stdscr.nodelay(False)
            break

        try:

            key = stdscr.getkey()

        except:
            continue

        if ord(key) == 27:
            break
        if key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(curr_text) > 0:
                curr_text.pop()

        elif len(curr_text) < len(text):
            curr_text.append(key)


def main(stdscr):

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:

        wpm_test(stdscr)
        stdscr.addstr(2, 0, "Completed...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break


wrapper(main)
