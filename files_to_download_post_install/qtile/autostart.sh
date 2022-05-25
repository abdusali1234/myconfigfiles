#!/bin/sh

# Remap caps lock to escape
setxkbmap -option caps:escape &
# Nitrogen - so that the wallpaper stays up & that I can change the wallpaper without changing this file
nitrogen --restore &

# nm-applet
nm-applet &

# dunst

# more to come...

