#!/usr/bin/env python3

# A Matrix code-rain terminal animation, with fade effect.
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

DENSITY = 0.9 # percentage of terminal width to fill (default 0.9, max 1.0)
MOVERATE = 0.08 # seconds between updates (default 0.08) lower is faster
COLOR = 120 # HSV color for chains 1-360, 0 or None for randomized (Green is 120)
KANA = True # whether to include Japanese Katakana characters (default True)
ERASE = False # clear characters after end of chains for clean background (default False)

import random, string, os, time, sys # for randomization, terminal size, timing, arguments & input
if os.name == 'nt': import msvcrt # for Windows keyboard input
else: import termios, tty, select # for Linux keyboard input
if len(sys.argv[1:]): COLOR = int(sys.argv[1]) # if a color is passed as an argument, use it

class MatrixColumn:
    def __init__(self, column):
        self.column = column # store column number for this chain to print at
        self.color = COLOR if COLOR else random.randint(1,360) # random color if COLOR is 0
        self.start = -random.randint(0, termH := os.get_terminal_size().lines) # random start position
        self.end = random.randint(4, termH) # random end length, no bigger than terminal height
        self.speed = random.choices((1,2,3),cum_weights=(1,1.4,1.42))[0] # random speed, weighted towards 1
        kata = ''.join([chr(i) for i in range(0xFF71,0xFF9E)]) if KANA else '' # Katakana characters
        self.characters = string.printable.strip() + kata # possible characters to use
        self.chain = random.choices(self.characters,k=self.end) # randomize starting chain of characters
        self.done = False # when the chain has moved off screen, this is used to remove it
    def update(self):
        termH = os.get_terminal_size().lines # get terminal height
        if 0 < self.start <= termH+len(self.chain): # if chain is on screen
            for _ in range(self.speed): # using speed to track location, add random bold/dim characters
                self.chain.insert(0, random.choices(('','\x1b[1m','\x1b[2m'), weights=(4,1,1))[0] + random.choice(self.characters))
            self.chain = self.chain[:self.end] # trim list to end length
            if ERASE: self.chain.extend([' ']*self.speed) # add blank to end of chain, to clear chain ghosts
            for i, char in enumerate(self.chain): # loop through all characters
                # Rarely flip a character (e.g., 0.1% chance per character per update)
                if random.random() < 0.002 and char.strip():
                    prefix = ''
                    if char.startswith('\x1b[1m') or char.startswith('\x1b[2m'):
                        prefix = char[:4] #, char[4:] , _ 
                    self.chain[i] = prefix + random.choice(self.characters)
                if termH >= self.start-i > 0: # if currrent character is on screen
                    brightness = 1-(i/self.end)**2 if i < self.end else 0 # calculate brightness based on position in chain
                    r, g, b = hsv2rgb(self.color, bool(i), brightness) # convert HSV to RGB for color fade
                    print(f'\x1b[38;2;{int(r)};{int(g)};{int(b)}m\x1b[{self.start-i};{self.column}H{self.chain[i]}',end='\x1b[0m\b',flush=True)
        self.start += self.speed # move start position down by speed amount, to animate
        if self.start-len(self.chain) > termH: self.done = True # if end is off screen, mark as done, for removal

def hsv2rgb(h, s, v): # convert HSV color values to RGB
    if s == 0.0: v *= 255; return (v, v, v) # if s is 0, return greyscale
    h /= 360. # normalize h to 0-1
    i = int(h*6.) # calculate hue sector 0-5
    f = (h*6.)-i # calculate fractional part of h
    p, q, t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f))))
    v *= 255; i %= 6 # calculate RGB values based on sector
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def main():
    try:
        chains, taken = [], set() # list of MatrixColumns, set of used columns
        unused = set(range(1,os.get_terminal_size().columns+1)) # set of unused columns
        print('\x1b[2J\x1b[?25l\x1b]0;The Matrix',end='\a',flush=True) # clear screen, hide cursor, & set window title
        if os.name == 'posix': # if on Linux
            oldsettings = termios.tcgetattr(sys.stdin) # store old terminal settings
            tty.setcbreak(sys.stdin) # set terminal to cbreak mode (so input doesn't wait for enter)
        while True: # main loop
            FullCols = set(range(1,(termW := os.get_terminal_size().columns)+1)) # set of all columns, & store terminal width
            if unused.union(taken) != FullCols: unused = FullCols-taken # accounts for terminal resizing
            for _ in range(int(termW*DENSITY)-len(chains)): # fill Density% of the terminal width with MatrixColumns
                column = random.choice(list(unused)) # pick a random unused column
                chains.append(MatrixColumn(column)) # create a new MatrixColumn in that column
                taken.add(column) # add column to taken set
                unused.remove(column) # remove column from unused set
            for mcol in chains[:]: # loop through all MatrixColumns
                mcol.update() # run update function in each MatrixColumn
                if mcol.done: # remove MatrixColumns when they finish falling
                    taken.remove(mcol.column) # remove column from taken set
                    if mcol.column <= termW: unused.add(mcol.column) # add now unused column back to unused set
                    chains.remove(mcol) # remove finished MatrixColumn from list
            time.sleep(MOVERATE) # controls the speed of the animation
            if os.name == 'nt' and msvcrt.kbhit() and msvcrt.getch() in (b'\x1b',b'q'): break # ESC or q to quit
            elif os.name == 'posix' and sys.stdin in select.select([sys.stdin],[],[],0)[0] and sys.stdin.read(1) in ('\x1b','q'): break
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally: # ensures these run even if program is interrupted, so terminal functions properly on exit
        if os.name == 'posix': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldsettings) # restore terminal settings
        print('\x1b[0m\x1b[2J\x1b[H\x1b[?25h') # reset terminal and show cursor

if __name__ == '__main__':
    main() # by Nik
