#!/usr/bin/env python3

# A basic Matrix code-rain terminal animation.
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

COLOR = ['\x1b[32m','\x1b[92m'] # both greens for color variation
LEADER = '\x1b[97m' # white for first character in chains
DENSITY = 0.8 # percentage of terminal width to fill (default 0.8, max < 1.0)
MOVERATE = 0.1 # seconds between updates (default 0.1) lower is faster
KANA = True # whether to include Japanese Katakana characters (default True)

import random, os, string, time
if os.name == 'nt': import msvcrt
else: import sys, tty, termios, select

class MatrixColumn:
    def __init__(self, column):
        self.column = column
        self.start = -random.randint(0, termH := os.get_terminal_size().lines) # random start position
        self.end = self.start-random.randint(3, termH) # random end length, no bigger than terminal height
        self.speed = random.choice([1,1,2]) # 1/3 chance of double speed
        kata = ''.join([chr(i) for i in range(0xFF71,0xFF9E)]) if KANA else '' # Katakana characters
        self.characters = string.printable.strip() + kata # possible characters to use
        self.prechar = ''
        self.done = False
    def update(self):
        termH = os.get_terminal_size().lines # get terminal height
        if 0 < self.start <= termH+2: # if start is on screen
            character = random.choice(self.characters) # choose a random character
            print(f'{LEADER}\x1b[{self.start};{self.column}H{character}',end='\b',flush=True)
            print(f'{random.choice(COLOR)}\x1b[{self.start-1};{self.column}H{self.prechar}',end='\b',flush=True)
            if self.speed == 2: # if double speed
                addchar = random.choice(self.characters) # choose an additional random character for double speed
                print(f'{random.choice(COLOR)}\x1b[{self.start-1};{self.column}H{addchar}',end='\b',flush=True)
                print(f'{random.choice(COLOR)}\x1b[{self.start-2};{self.column}H{self.prechar}',end='\b',flush=True)
            if self.start <= termH: self.prechar = character
        if termH >= self.end > -1: # if end is on screen
            print(f'\x1b[{self.end};{self.column}H ',end='\b',flush=True)
            if self.speed == 2: print(f'\x1b[{self.end+1};{self.column}H ',end='\b',flush=True)
        self.start += self.speed # update start and end positions
        self.end += self.speed
        if self.end > termH: self.done = True # if end is off screen

def main():
    try:
        chains, taken = [], set() # list for MatrixColumns, set for taken columns
        print('\x1b[2J\x1b[?25l') # clear screen and hide cursor
        if os.name == 'posix': # if on Linux
            oldsettings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
        while True: # main loop
            termW = os.get_terminal_size().columns
            for _ in range(int(termW*DENSITY)-len(chains)): # fill Density% of the terminal width with MatrixColumns
                while (column := random.randint(1,termW)) in taken: pass # prevents overlapping columns, inefficient
                chains.append(MatrixColumn(column)) # spawn MatrixColumn at unused column, add to list for updating
                taken.add(column) # add column to taken set
            for mcol in chains: # loop through all MatrixColumns
                mcol.update() # run update function in each MatrixColumn
                if mcol.done: # remove MatrixColumns when they finish falling
                    taken.remove(mcol.column) # remove column from taken set
                    chains.remove(mcol) # then remove it from update list
            time.sleep(MOVERATE) # controls the speed of the animation
            if os.name == 'nt' and msvcrt.kbhit() and msvcrt.getch() in (b'\x1b', b'q'): break # ESC or q to quit
            elif os.name == 'posix' and sys.stdin in select.select([sys.stdin],[],[],0)[0] and sys.stdin.read(1) in ('\x1b','q'): break
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally:
        if os.name == 'posix': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldsettings)
        print('\x1b[0m\x1b[2J\x1b[?25h') # reset terminal and show cursor

if __name__ == '__main__':
    main() # by Nik
