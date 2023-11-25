#!/bin/bash
xrandr --output DP-2 --auto --pos 2560x0 --output DP-0 --auto --pos 0x0
picom --config /home/stefan/.config/qtile/picom.conf &
nm-applet &
pasystray &
