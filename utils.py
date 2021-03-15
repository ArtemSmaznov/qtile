from datetime import datetime as time
import os

from libqtile import widget

import lib.widgets as my_widget
import settings.preferences as user
import theme.default as theme

kbr_index = 0


def power_line(position, w):
    current_color = theme.power_line_colors[position]
    next_color = theme.power_line_colors[position - 1]
    return [
        widget.TextBox(
            text='',
            foreground=current_color,
            background=next_color,
            padding=-10,
            fontsize=48
        ),
        *w(current_color),
        my_widget.separator(3, current_color),
    ]


def switch_keyboard_layout(qtile):
    global kbr_index

    if kbr_index+1 < len(user.languages):
        kbr_index = kbr_index + 1
    else:
        kbr_index = 0
    qtile.cmd_spawn('setxkbmap ' + user.languages[kbr_index])

############################################################################
# Volume
############################################################################


def volume_increase(qtile):
    qtile.cmd_spawn('amixer -q sset Master on ' + str(user.volume_step) + '%+')


def volume_decrease(qtile):
    qtile.cmd_spawn('amixer -q sset Master on ' + str(user.volume_step) + '%-')


def volume_mute(qtile):
    qtile.cmd_spawn('amixer -q sset Master toggle')

############################################################################
# Screenshots
############################################################################


def screenshot(type='full'):
    def action(qtile):
        path = os.path.expanduser(user.screenshot_location)
        format = str(time.now().strftime(user.screenshot_filename)) + '.png'

        if type == 'full':
            command = 'maim -u -m 1 '
        elif type == 'area':
            command = 'maim -u -B -s -n -m 1 '
        elif type == 'window':
            command = 'maim -u -B -i $(xdotool getactivewindow) -m 1 '
        else:
            command = 'maim -u -m 1 '

        qtile.cmd_spawn(command + path + format, shell=True)
        # copying to clipboard does work for me even directly from the terminal
        # qtile.cmd_spawn(
        #     'xclip -selection clipboard -t image/png -i ' + path + format)

    return action
