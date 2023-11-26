#!/bin/bash
if [ "$HOSTNAME" = "stefan-eos" ]; then
    picom --config /home/stefan/.config/qtile/picom.conf &
else
    xrandr --output DP-2 --auto --pos 2560x0 --output DP-0 --auto --pos 0x0
    picom --config /home/stefan/.config/qtile/picom.conf &
    nm-applet &
    pasystray &
fi

# Lock-screen
xautolock -time 20 -locker /usr/bin/i3lock-fancy -detectsleep &