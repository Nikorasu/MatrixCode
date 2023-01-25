# A Matrix-style Code-Rain animation

This is a Python terminal animation, designed to mimic the look of "the code"
as seen in the movie "The Matrix".
It doesn't use the curses library, and should work on both Windows and Linux.
If your terminal can't display unicode characters, set KANA to False.

## `matrix.py`

This was my original simple method, which merely prints random characters in
columns, without storing them, then prints empty spaces a randomly set distance
above the start, to erase as it animates down. It uses the terminal default
colors for dark green, bright green, & white. Tho those can be customized, and
I also added a few other configurable options to the top of the files.

## `matrix2.py`

More advanced version, has a nice fade-effect, supports custom colors, and even
has a random color rainbow-mode. The color can be specified using HSV hue
values _(1-360)_, either by editing the COLOR setting on line 8, or from the
terminal as an argument when running the code. Any integer from 1 to 360 is
valid, 0 is reserved for the random color mode. Default is 120 for Green.
Other common colors:
> Orange = 30, Yellow = 60, Blue = 240, Purple = 270, Pink = 300, Red = 360

So in order to change the color to Blue, run using: `python matrix2.py 240`

Or to use the random color mode, run using: `python matrix2.py 0`

---

If you like my projects and want to help me keep making more,
please consider donating on [my Ko-fi page!](https://ko-fi.com/nik85)
Thanks!

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F1F4GRRWB)

---

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.
        If not, see: https://www.gnu.org/licenses/gpl-3.0.html

Copyright (c) 2022  Nikolaus Stromberg - nikorasu85@gmail.com
