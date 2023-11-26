#!/bin/sh
revert() {
    xset dpms 0 0 0
}
trap revert HUP INT TERM
xset +dpms dpms 25 25 25
/usr/bin/i3lock-fancy
revert
