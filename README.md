# qtile-configs

Use with caution...

This is my backup/share of my qtile setups. Beaware that it might change quickly some days.
I have also added (maybe not to smart) other dotfiles in this repo. For these I simply use 
a symlink.

For example the symlink to rofi:
```
  cd .config
  ln -s qtile/rofi rofi
```

Other stuff I use (for Ubuntu/Pop_OS!):
```
  sudo apt install kitty rofi i3lock-fancy amixer picom xautolock 
```

I have created a few additions that might be of interest to you:
- There are 10 groups, and if you run dual-screen setup they are dived on two screens.
- You can navigate between these (see key-bindings) independently on each screen. 
- I am re-using the "traverse.py" from the qtile-samples repository to change focus 
between windows/screens.
See code sections in these two + functions (plus the keybindings):

```
def next_group(qtile)
def prev_group(qtile)
```

NOTEs
- I use cursor keys instead of hjkl
- I my settings, I sometime assume that the user name is 'stefan' like: (/home/stefan/.config/qtile)
- I have swapped the LALT with LWIN...so my LEFT ALT is my super. See "mod" in config.py
- I sometime use the hostname (in config.py and autostart) to have different setups.
- Verify xrandr settings for your screen setup (in autostart.sh)
- There is a rofi-menu of all used keybindings => SUPER+F1
- The wallpaper was taken outside my house in march 2023 when we had a nice aurora/northern light in south of Sweden.


There is also an included virtualenv for running qtile in its own environment. Might be easier if you
have dependency problem. Note that this must be de-coupled from a user to work on login. 
So, copy the "create-qtile-env.sh" to /opt/venv (create this if it does not exist)

Like so:
```
  cd /opt
  mkdir venv
  sudo chown -R stefan:stefan venv # Replace with your username
  cd venv
  cp /home/stefan/.config/qtile/create-qtile-env.sh /opt/venv
  ./create-qtile-env.sh
```

After this you should see a "Qtile(venv)" session on login.

Good luck
Stefan
