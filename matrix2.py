#!/usr/bin/env python3

# A Matrix code-rain terminal animation, with fade effect.
# Copyright (C) 2022  Nik Stromberg - nikorasu85@gmail.com

DENSITY = 0.9 # percentage of terminal width to fill (default 0.9, max 1.0)
MOVERATE = 0.08 # seconds between updates (default 0.08) lower is faster
COLOR = 0 # HSV color for chains 1-360, 0 or None for randomized (Green is 120)
KANA = True # whether to include Japanese Katakana characters (default True)

import random, os, string, time
if os.name == 'nt': import msvcrt
else: import sys, tty, termios, select

class MatrixColumn:
    def __init__(self, column):
        self.column = column
        self.color = COLOR if COLOR else random.randint(1,360) # random color if COLOR is 0
        self.start = -random.randint(0, termH := os.get_terminal_size().lines) # random start position
        self.end = random.randint(4, termH) # random end length, no bigger than terminal height
        self.speed = random.choice([1,1,2]) # 1/3 chance of double speed
        kata = ''.join([chr(i) for i in range(0xFF71,0xFF9E)]) if KANA else '' #'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜｦﾝ'
        self.characters = string.printable.strip() + kata # possible characters to use
        self.chain = random.choices(self.characters,k=self.end) # randomize starting chain of characters
        self.done = False
    def update(self):
        termH = os.get_terminal_size().lines # get terminal height
        if 0 < self.start <= termH+len(self.chain): # if start is on screen
            newchar = random.choice(['','','\x1b[1m','\x1b[2m']) + random.choice(self.characters) # new character with random bold
            print(f'\x1b[97m\x1b[{self.start};{self.column}H{newchar}',end='\x1b[0m\b',flush=True) #x1b[38;2;255;255;255m
            for i, char in enumerate(self.chain): # loop through all characters
                if termH >= self.start-i-1 > 0: # if characters are on screen
                    brightness = 1-(i/self.end)**2 if i < self.end else 0 # calculate brightness based on position in chain
                    r, g, b = hsv2rgb(self.color,1,brightness) # convert HSV to RGB for color fade
                    print(f'\x1b[38;2;{int(r)};{int(g)};{int(b)}m\x1b[{self.start-i-1};{self.column}H{char}',end='\x1b[0m\b',flush=True)
            self.chain.insert(0,newchar) # insert newchar at start of chain
            if self.speed == 2: # if this chain is double speed
                addchar = random.choice(self.characters) # pick an additional character for double speed
                self.chain.insert(0,random.choice(['','','\x1b[1m','\x1b[2m']) + addchar) # add it with random formatting
            self.chain = self.chain[:self.end] # trim list to end length
            self.chain.extend([' ',' ']) # add 2 blank spaces to end of chain, to erase old characters when printed
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
        print('\x1b[2J\x1b[?25l') # clear screen and hide cursor
        if os.name == 'posix': # if on Linux       
            oldsettings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin)
        while True: # main loop
            FullCols = set(range(1,(termW := os.get_terminal_size().columns)+1)) # set of all columns, & store terminal width
            if unused.union(taken) != FullCols: unused = FullCols-taken # accounts for terminal resizing
            for _ in range(int(termW*DENSITY)-len(chains)): # fill Density% of the terminal width with MatrixColumns
                column = random.choice(list(unused)) # pick a random unused column
                chains.append(MatrixColumn(column)) # create a new MatrixColumn in that column
                taken.add(column) # add column to taken set
                unused.remove(column) # remove column from unused set
            for mcol in chains: # loop through all MatrixColumns
                mcol.update() # run update function in each MatrixColumn
                if mcol.done: # remove MatrixColumns when they finish falling
                    taken.remove(mcol.column) # remove column from taken set
                    if mcol.column <= termW: unused.add(mcol.column) # add now unused column back to unused set
                    chains.remove(mcol) # remove finished MatrixColumn from list
            time.sleep(MOVERATE) # controls the speed of the animation
            if os.name == 'nt' and msvcrt.kbhit() and msvcrt.getch() in (b'\x1b', b'q'): break # ESC or q to quit
            elif sys.stdin in select.select([sys.stdin],[],[],0)[0] and sys.stdin.read(1) in ('\x1b','q'): break
    except KeyboardInterrupt: pass # catch Ctrl+C
    finally:
        if os.name == 'posix': termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldsettings)
        print('\x1b[0m\x1b[2J\x1b[?25h') # reset terminal and show cursor

if __name__ == '__main__':
    main() # by Nik
