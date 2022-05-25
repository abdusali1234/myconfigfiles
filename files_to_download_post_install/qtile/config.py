
from typing import List  # noqa: F401

from libqtile.log_utils import logger
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os, subprocess

mod = "mod4"
alt = "mod1"
terminal ="kitty"
keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([alt], "Tab", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    # Shortcuts for commonly used apps
    Key([mod], "f", lazy.spawn("firefox"), desc= "Opens Firefox"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "z", lazy.spawn("zathura"), desc ="Opens PDF viewer"),
    Key([alt], "space", lazy.spawn("rofi -show run"),
        desc="launch rofi"),
    Key([mod], "s",
        lazy.spawn("scrot -b 'Screenshot-%d-%m-%Y-%H-%M-%S'.png -e 'mv $f ~/Pictures/screenshots/'"),
        desc="Take screenshots"),

    # Change the volume if your keyboard has special volume keys.
    Key(
        [], "XF86AudioRaiseVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB+"),
        desc="Increase volume"
    ),
    Key(
        [], "XF86AudioLowerVolume",
        lazy.spawn("amixer -c 0 -q set Master 2dB-"),
        desc="Decrease volume"
    ),
    Key(
        [], "XF86AudioMute",
        lazy.spawn("amixer -c 0 -q set Master toggle"),
        desc="mute audio"
    ),
    Key(
        [mod], "Home",
        lazy.spawn("light -A 5"),
        desc="increase brightness by 5%"
    ),
    Key(
        [mod], "End",
        lazy.spawn("light -U 5"),
        desc="Decrease brightness by 5%"
    )
]

# colours!!!!!!
black = ["#282828", "#3c3836"]
red = ["#cc241d", "#fb4934"]
green = ["#98971a", "#b8bb26"]
yellow = ["#d79921", "#fabd2f"]
blue = ["#458588", "#83a598"]
purple = ["#b16286", "#d3869b"]
aqua = ["#689d6a", "#8ec07c"]
white = ["#8ec07c", "#ebdbb2"]
orange = ["#d65d0e", "#fe8019"]

groups = [Group(""),
          Group(""),
          Group(""),
          Group(""),
          Group(""),
          Group(""),
          Group(""),
          Group(""),
          Group("misc")]

for i, grp in enumerate(groups):
    Group(i)
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], str(i + 1), lazy.group[grp.name].toscreen(),
            desc="Switch to group {}".format(grp.name)),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], str(i + 1), lazy.window.togroup(grp.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(grp.name))
            ])

layouts = [
    layout.Columns(border_focus_stack='#d75f5f'),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Jetbrains Mono',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.CurrentLayout(background=black[0]),
                widget.GroupBox(active=orange[0], background=black[0]),
                widget.Prompt(background=black[0]),
                widget.WindowName(background=black[0]),
                widget.Chord(
                    chords_colors={
                        'launch': ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(background=black[0]),
                widget.Battery(background=black[0],
                               charge_char='+',
                               discharge_char='',
                               unknown_char='',
                               format='{char}{percent:2.0%}'),
                widget.Volume(background=black[0],
                              emoji=True),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p', background=black[0]),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True



# autostart certain applications 
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/mij/.config/qtile/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

