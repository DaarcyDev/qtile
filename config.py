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

import os
import subprocess
import dbus_next
import iwlib
# from dbus_next.service import ServiceInterface, method, dbus_property, signal, Variant

# from libqtile import hook
# from qtile_extras import widget
# from qtile_extras.widget.decorations import BorderDecoration

# from typing import List # noqa: F401
# from dbus_next import *
# from dbus_next.aio import MessageBus
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration,PowerLineDecoration


networkDevice = "wlan0"
mod = "mod4"
terminal = guess_terminal()
colorBar = "#181921"
barSize = 26
defaultFont = "Ubuntu Mono Nerd Font"
fontSize = 16
activeColor ="ffffff"
fgColor = "#ffffff"
bgColor = "#1f1f1f"
inactiveColor = "#a46262"
activeColorbg = "#731010"
colorName = "#faa7a7"
iconSize = 20
UpdateColor = "#bc0000"
thermalAlert = "#ffc30f"
colorGroup1 = "#581845" 
colorGroup2 = "#900c3f"
colorGroup3 = "#c70039"
colorGroup4 = "#d6281c"
transparence = "0.5"

#functions
powerline = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right"
        )
    ]
}
def fcSeparador(bgColor):
    return  widget.Sep(
                padding=10, 
                linewidth=0, 
                foreground = fgColor,
                background = bgColor,
                **powerline
            )

def fcRectangle(fgColor,bgColor):
    return widget.TextBox(
                text = "",
                fontsize = 35,
                foreground = fgColor,
                background = bgColor,
                margin = 0,
                padding = -3.5
            )

def fcText(Text, color):
    return widget.TextBox(
                text = Text,
                padding = 0,
                fontsize = iconSize,
                foreground = fgColor,
                background = color,
                margin = 0
            )

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
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
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    #Custom Shortcuts
    Key([mod], "m", lazy.spawn("rofi -show drun"), desc="Launch Menu"),
    Key([mod], "b", lazy.spawn("brave"), desc="Launch Firefox"),
    Key([mod], "v", lazy.spawn("code"), desc="Launch VSCode"),
    Key([mod], "d", lazy.spawn("dbeaver"), desc="Launch DBeaver"),
    Key([mod], "s", lazy.spawn("spotify"), desc="Launch Spotify"),
    Key([mod], "l", lazy.spawn("betterlockscreen -l blur"), desc="lock"),
    Key([mod], "o", lazy.spawn("onlyoffice-desktopeditors"), desc="onlyoffice"),
    Key([mod], "n", lazy.spawn("netbeans"), desc="netbeans"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], 'XF86AudioLowerVolume', lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], 'XF86AudioMute', lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle')),

    # Commands: Audio Controls
    Key([], 'XF86AudioPrev', lazy.spawn("playerctl previous")),
    Key([], 'XF86AudioPlay', lazy.spawn("playerctl play-pause")),
    Key([], 'XF86AudioNext', lazy.spawn('playerctl next')),

    # Brightness Control
    Key([], 'XF86MonBrightnessUp', lazy.spawn("brightnessctl set +10%")),
    Key([], 'XF86MonBrightnessDown', lazy.spawn("brightnessctl set 10%-")),

    # capture screen
    Key([], 'Print', lazy.spawn("scrot")),
    Key([mod], 'Print', lazy.spawn("scrot -s")),

    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    
    
]

groups = [Group(i) for i in [
    "   ","   ","   ","   ","   ","   "
]]


for i, group in enumerate(groups):
    desktopNumber = str(i+1)
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                desktopNumber,
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                desktopNumber,
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["#d75f5f", "#8f3d3d"], 
        border_width=1,
        margin = 10,
        border_focus = "#555555",
    )
    # layout.Floating(
    #     border_normal = "#ffffff", 
    #     border_focus = "#555555",
    #     border_width=1,
    #     margin = 10,
    #      float_rules=[
    #         Match(wm_class='confirm'),
    #         Match(wm_class='dialog'),
    #         Match(wm_class='download'),
    #         Match(wm_class='error'),
    #         Match(wm_class='file_progress'),
    #         Match(wm_class='notification'),
    #         Match(wm_class='splash'),
    #         Match(wm_class='toolbar'),
    #         Match(wm_class='confirmreset'),
    #         Match(wm_class='makebranch'),
    #         Match(wm_class='maketag'),
    #         Match(title='branchdialog'),
    #         Match(title='pinentry'),
    #         Match(wm_class='ssh-askpass'),
    #         Match(title='Xephyr on :1.0 (ctrl+shift grabs mouse and keyboard)'),
    #         Match(title='Bitwarden'),
    #         Match(wm_class='nextcloud'),
    #         Match(wm_class='system-config-printer'),
    #     ]
    # )
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(
    #     border_width=1,
    #     margin = 10,
    #     change_size=10,
    # )
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=defaultFont,
    fontsize=fontSize,
    padding=1,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                
                
                widget.GroupBox(
                    highlight_method='block',
                    active = activeColor,
                    borderwidth = 2,
                    fontsize = iconSize,
                    foreground = fgColor,
                    background = bgColor,
                    center_aligned = True,
                    inactive = inactiveColor,
                    this_current_screen_border = activeColorbg,
                    this_screen_border = activeColorbg,
                    urgent_alert_method = 'line',
                    margin = 3,
                    padding = 0,
                    
                ),
                
                # fcSeparador(bgColor),
                widget.Prompt(),
                widget.GlobalMenu(
                    background = bgColor,
                    foreground = colorName,
                    padding = 15,
                    opacity = 1
                ),
                fcSeparador(bgColor),
                widget.WindowName(
                    background = bgColor,
                    foreground = colorName
                ),
                

                fcSeparador(bgColor),


                widget.ThermalSensor(
                    foreground = fgColor,
                    background = colorGroup1,
                    
                    fontsize = fontSize,
                    threshold = 80,
                    tag_sensor = 'Tctl',
                    scroll = False,
                    update_interval = 1,
                    foreground_alert = thermalAlert
                ),
                fcText("  ", colorGroup1),
                widget.Memory(
                    foreground = fgColor,
                    background = colorGroup1,
                    measure_mem='G'
                ),
                fcSeparador(colorGroup1),
                # fcRectangle(colorGroup2,colorGroup1),
                fcText("  ",colorGroup2),
                widget.CheckUpdates(
                    background= colorGroup2,
                    foreground =fgColor,
                    colour_have_updates = UpdateColor,
                    colour_no_updates = fgColor,
                    no_update_string = "0",
                    display_format = '{updates}',
                    update_interval = 600,
                    distro = "Arch"
                ),
                fcText(" 龍 :",colorGroup2),

                widget.WiFiIcon(
                    background=colorGroup2,
                    foreground = fgColor,
                    padding = 5
                ),
                widget.Net(
                    background=colorGroup2,
                    foreground = fgColor,
                    format =  '{down}↓↑{up}'
                ),


                fcSeparador(colorGroup2),

                # fcRectangle(colorGroup3,colorGroup2),
                widget.Clock(
                    format="%a %I:%M %d/%m/%Y ",
                    background=colorGroup3,
                    foreground=fgColor,
                    ),
                fcText(" 墳 ",colorGroup3),
                widget.PulseVolume(
                    background = colorGroup3,
                    foreground = fgColor,
                    limit_max_volume = True,
                    update_interval= 0,
                ),

                fcSeparador(colorGroup3),
                widget.CurrentLayout(
                    background = colorGroup4,
                    foreground = fgColor
                ),
                fcText(" :",colorGroup4),
                
                widget.UPowerWidget(
                    background= colorGroup4,
                    battery_height	=10,

                ),
                widget.Battery(
                    background = colorGroup4,
                    foreground = fgColor,
                    discharge_char = "",
                    charge_char = "",
                    low_percentage = 20,
                    format = '{percent:2.0%} {char} ',
                    update_interval = 1,
                    low_foreground = fgColor,
                    decorations=[
                        BorderDecoration(
                            colour = colorGroup4,
                            border_width = [0,0,4,0],
                            padding_x = 5,
                            padding_y = None,
                        )
                    ],
                ),
                widget.QuickExit(
                    default_text='[X]', countdown_format='[{}]',
                    background = colorGroup4,
                    foreground = fgColor,
                ),
                # fcSeparador(colorGroup4)
                # widget.QuickExit(),
            ],
            barSize,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background=colorBar
            
        ),
    ), 
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, "control"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
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
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])
