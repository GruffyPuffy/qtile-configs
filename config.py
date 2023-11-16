# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import hook, bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.log_utils import logger

import traverse

import os
import subprocess

mod = "mod1"
terminal = guess_terminal()


groups = [Group(i) for i in "1234567890"]
left_groups  = [str(i) for i in "12345"]
right_groups = [str(i) for i in "67890"]
screen_groups = [left_groups, right_groups]


def next_group(qtile):
    #logger.warning("Next group called: " + str(qtile.current_screen))

    screen_index = qtile.current_screen.index
    #logger.warning("Screen index: " + str(screen_index))

    group_list = screen_groups[screen_index]
    #logger.warning("Screen groups: " + str(group_list))
    
    screen_info = qtile.get_screens()
    current_info = screen_info[screen_index]
    #logger.warning(str(current_info))
    
    current_group = current_info['group']
    current_group_index = group_list.index(current_group)
    #logger.warning("Group index:" + str(current_group_index))
    next_group_index = current_group_index + 1
    if next_group_index >= len(group_list):
        next_group_index = 0
    next_name = group_list[next_group_index]
    #logger.warning("Next Group:" + str(next_name))
    qtile.groups_map[next_name].toscreen(toggle=False)

def prev_group(qtile):
    #logger.warning("Next group called: " + str(qtile.current_screen))

    screen_index = qtile.current_screen.index
    #logger.warning("Screen index: " + str(screen_index))

    group_list = screen_groups[screen_index]
    #logger.warning("Screen groups: " + str(group_list))
    
    screen_info = qtile.get_screens()
    current_info = screen_info[screen_index]
    #logger.warning(str(current_info))
    
    current_group = current_info['group']
    current_group_index = group_list.index(current_group)
    #logger.warning("Group index:" + str(current_group_index))
    next_group_index = current_group_index - 1
    if next_group_index < 0:
        next_group_index = len(group_list)-1
    next_name = group_list[next_group_index]
    #logger.warning("Next Group:" + str(next_name))
    qtile.groups_map[next_name].toscreen(toggle=False)


keys = [

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    Key([mod, "shift", "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "shift", "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "shift", "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "shift", "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),

    # Navigation a la Stefan
    Key([mod, 'control'], 'Up', lazy.function(prev_group)),
    Key([mod, 'control'], 'Down', lazy.function(next_group)),
    Key([mod, 'control'], 'Left', lazy.prev_screen(), desc='Switch to screen to the right'),
    Key([mod, 'control'], 'Right', lazy.next_screen(), desc='Switch to screen to the left'),

    Key([mod], "m", lazy.window.toggle_maximize(), desc="Toggle maximize"),
   
    Key([mod], 'Up', lazy.function(traverse.up)),
    Key([mod], 'Down', lazy.function(traverse.down)),
    Key([mod], 'Left', lazy.function(traverse.left)),
    Key([mod], 'Right', lazy.function(traverse.right)),
    
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch "),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Spawn command launcher"),
    Key([mod], "b", lazy.spawn("google-chrome"), desc="Spawn Google Chrome"),
    Key([mod], "e", lazy.spawn("i3lock-fancy -p"), desc="Lock screen"),

    Key([], 'XF86AudioRaiseVolume', lazy.spawn("amixer sset Master 5%+")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("amixer sset Master 5%-")),
    Key([], 'XF86AudioMute', lazy.spawn("amixer sset Master toggle")),    
]

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(),
    layout.MonadWide(),
    layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(visible_groups=left_groups),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.CPUGraph(),
                #widget.BatteryIcon(),
                #widget.Battery(),
                widget.TextBox("   "),
                widget.Volume(fmt="Vol {}",
                              volume_down_cmd="amixer sset Master 5%-",
                              volume_up_cmd="amixer sset Master 5%+",
                              get_volume_command="amixer sget Master"),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                #widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Clock(format="%Y-%m-%d %H:%M"),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(visible_groups=right_groups),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.CPUGraph(),
                #widget.BatteryIcon(),
                #widget.Battery(),
                widget.TextBox("   "),
                widget.Volume(fmt="Vol {}",
                              volume_down_cmd="amixer sset Master 5%-",                              
                              volume_up_cmd="amixer sset Master 5%+",
                              get_volume_command="amixer sget Master"),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                #widget.StatusNotifier(),
                #widget.Systray(),
                #widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Clock(format="%Y-%m-%d %H:%M"),
                widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]


if len(screens) == 2:
    for i in groups:
        keys.extend([
            # Switch to group N
            Key(
                [mod], 
                i.name, 
                lazy.to_screen(0) if i.name in '12345' else lazy.to_screen(1),
                lazy.group[i.name].toscreen()
            ),

            # Move window to group N
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),),
        ])

else:
    for i in groups:
        keys.extend([
            # Switch to group N
            Key([mod], i.name, lazy.group[i.name].toscreen()),

            # Move window to group N
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),),
        ])


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])


