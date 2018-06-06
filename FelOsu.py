import shutil
import tempfile
import sys
from collections import Counter
from tkinter.filedialog import RAISED, SUNKEN, RIGHT, LEFT, TOP, BOTTOM, GROOVE, FLAT, TRUE, BOTH
from tkinter.filedialog import Label, LabelFrame, Entry, StringVar, IntVar, Frame, Radiobutton, Spinbox, askdirectory
from tkinter.messagebox import askyesno, showinfo, showwarning
from tkinter.ttk import Button as Ttk_Button, Label as Ttk_Label
import tkinter as tk
import webbrowser
from tinytag import TinyTag, tinytag
import binascii
import os
import requests
from os.path import join as path_join
import re


class GlobalVars:
    def __init__(self):
        self.root = tk.Tk()
        self.topic_link = "https://osu.ppy.sh/community/forums/topics/520493"
        self._source_directory = next(
            (
                StringVar(value=path_join(*path)) for path in [('C:', 'Program Files (x86)', 'osu!'),
                                                               (os.path.expanduser('~'), 'AppData', 'Local', 'osu!'),
                                                               (os.path.expanduser('~'), 'AppData', 'Roaming', 'osu!')]
                if os.path.exists(path_join(*path))
            ), StringVar()
        )
        self._destination_directory = StringVar(value=path_join(os.path.expanduser('~'), 'FelOsu'))
        self._radio_value = IntVar()
        self._spin_value = IntVar()
        self.osu_directory_regex = re.compile(r"^[\d]+[\s](.)+-(.)+")
        self.osu_directories = dict()
        self.artist_counter = Counter()
        self.musics_seen = set()

    @property
    def source_directory(self):
        return self._source_directory.get()

    @source_directory.setter
    def source_directory(self, value):
        self._source_directory.set(value)

    @property
    def destination_directory(self):
        return self._destination_directory.get()

    @destination_directory.setter
    def destination_directory(self, value):
        self._destination_directory.set(value)

    @property
    def radio_value(self):
        return self._radio_value.get()

    @radio_value.setter
    def radio_value(self, value):
        self._radio_value.set(value)

    @property
    def spin_value(self):
        return self._spin_value.get()

    @spin_value.setter
    def spin_value(self, value):
        self._spin_value.set(value)

    @property
    def nb_artists_max(self):
        return max(self.artist_counter.values())

    @property
    def songs_path(self):
        return path_join(self._source_directory.get(), 'Songs')


g_vars = GlobalVars()


class Ascii:
    def __init__(self):
        self.license = (
            "\n" +
            " " * 32 + "This program is free software: you can redistribute it and/or \n" + ""
            " " * 31 + "modify it under the terms of the GNU General Public License\n" + ""
            " " * 17 + "as published by the Free Software Foundation, either version 3 of the License,\n" + ""
            " " * 52 + "or (at your option) any later version.\n\n" + ""
            " " * 31 + "This program is distributed in the hope that it will be useful,\n" + ""
            " " * 22 + "but WITHOUT ANY WARRANTY; without even the implied warranty of\n" + ""
            " " * 32 + "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n" + ""
            " " * 32 + "See the GNU General Public License for more details.\n\n" + ""
            " " * 3 + "You should have received a copy of the GNU General Public License along with this program.\n" + ""
            " " * 45 + "If not, see <http://www.gnu.org/licenses/>.\n" + ""
            " " * 18 + 'You have to mention "Based on Darkaird work" if you reuse this software.\n\n' + ""
            " " * 8 + 'By clicking "Next >" button, it means that you read those conditions mentions above.' + "\n"
        )

        self.help = (
            "\n\n"
            '- "Yes" will put all the musics with the same artist in the same folder (and the folder\'s name\n'
            "will be the artist's name). But even if there is only one music for an artist, it will put it\n"
            "in a folder despite everything.\n\n"
            '- "Yes, but only from" is exactly the same except the fact that you set the number of musics\n'
            "of a same artist from which it will create a folder."
        )

        self.train = (
            "    ___                     _          ___                                          \n"
            "   | __|       ___         | |        / _ \        ___      _  _                    \n"
            "   | _|       / -_)        | |       | (_) |      (_-<     | +| |      . . . o o    \n"
            " __|_|____  __\___|___  ___|_|_     __\___/__  ___/__/___  _\_,_|_             o    \n"
            "|[] [] []| [] [] [] [] [_____(__   |[] [] []| [] [] [] [] [_____(__  ][]]_n_n__][.  \n"
            "|________|_[_________]_[________]__|________|_[_________]_[________]_|__|________)< \n"
            " oo    oo ' oo     oo ' oo    oo '  oo    oo ' oo     oo ' oo    oo ' oo 000---oo\_ "
        )

        self.cloud = """
_                  _                                              _                                                    \
     _                                            _
 ))              (`  ).                   _                     (`  ).                   _                             \
    (`  ).                   _                   (`  ).                        _                __
  (             (     ).              .:(`  )`.                (     ).              .:(`  )`.                         \
    (     ).              .:(`  )`.              (     ).                   .:(`  )`.           (
__ )           _(       '`.          :(   .    )              _(       '`.          :(   .    )                        \
 _(       '`.          :(   .    )            _(       '`.                :(   .    )        ((
           .=(`(      .   )     .--  `.  (    ) )         .=(`(      .   )     .--  `.  (    ) )                    .=(\
           `(      .   )     .--  `.  (    ) )       .=(`(      .   )     .--        `.  (    ) )        (
_._          ((    (..__.:'-'   .+(   )   ` _`  ) )         ((    (..__.:'-'   .+(   )   ` _`  ) )                    (\
(    (..__.:'-'   .+(   )   ` _`  ) )       ((    (..__.:'-'   .+(   )          ` _`  ) )      '..
   `.     `(       ) )       (   .  )     (   )  ._      `(       ) )       (   .  )   (  (   )         ._          `( \
         ) )       (   .  )     (   )        `(    __ ) )       (   .  )         (   )          ._
     )      ` __.:'   )     (   (_  ))     `-'.-(`  )      ` __.:'   )     (   (   )) (    `-'.       -(`  )          `\
      __.:'   )     (   ( _))    ((   `-'.     -(`  )              ` __.:'         )   (       ( _)) (
   )  )  ( )       --'       `- __.'         :(      ))           ( )       --'       `- __.'      :(      ))          \
    ( )            --'         `- __.'       :(    ))         ( )                (--'         `- __.'
___.-'  (_.'          .')                    `(    )  ))         (_.'          .')                 `(    )  ))         \
(_.'                                     `(    )  ))       (_.'
                  (_  )                     ` __.:'                        (_  )                  ` __.:'              \
                                                          ` __.:'
                  """

        self.rail = "#" * 135

        self.mountain = (
            "                              ^    _                                _     ^                      \n" 
            "   ^            ^        .-.      / \        _                     / \        _           ^      \n" 
            "             ^          /   \    /^./\__   _/ \             ^     /^./\__   _/ \ \\              \n" 
            "           _        .--'\/\_ \__/.      \ /    \  ^   ___        /.      \ /    \  ^^_           \n" 
            "          / \_    _/ ^      \/  __  :'   /\/\  /\  __/   \      /__  :'   /\/\  /\_./ \\         \n" 
            "         /    \  /    .'   _/  /  \   ^ /    \/  \/ .`'\_/\    /  \   ^ /    \/  \/ .`'\\  ^     \n" 
            "        /\/\  /\/ :' __  ^/  ^/    `--./.'  ^  `-.\ _    _:\ _/    `--./.'  ^  `-.\ _  _\\       \n"  
            "       /    \/  \  _/  \-' __/.' ^ _   \_   .'\   _/ \ .  __/ \   ' ^ _   \_   .'\   _/  \\      \n" 
            "     /\  .-   `. \/     \ / -.   _/ \ -. `_/   \ /    `._/  ^  \    _/ \ -. `_/   \ /    `\\     \n" 
            "  __/  `-.__ ^   / .-'.--'    . /    `--./ .-'  `-.  `-. `.  -  `. /    `--./ .-'  `-.  `-. \__  \n" 
            " /        `.  / /        `-.   /  .-'   / .    .'  \    \  \  -   /  .-'   / .   .'   \    \   \\\n"
        )

        self.outro = ("\nThank you for using this software developed by Darkaird !\n"
                      "If you have suggestion(s) or bug(s), you can send an email at :\n"
                      "software.felosu@gmail.com\n\n\n"
                      "Click the link below to see changelog :")
        self.detected_setting = ("We detect that you have already used this software with this\n"
                                 "destination folder and chose the setting :\n"
                                 " - '{0}'.\n"
                                 "To avoid duplicates, we recommend you to choose the same setting.")
        self.progress_bar = (" ______________________________________________________________\n"
                             "|                                                              |\n"
                             "|                    Progress : {0}/{1} ({2}%){3} |\n"
                             "|______________________________________________________________|")


iconhexdata = '0000010001004040000001002000284000001600000028000000400000008000000001002(243)9c5ce72c9c5fea659c5ee8' \
              '7f9c5fe9999c5ee9b29c5fe8cc9b5ee9e59c5fe9ff9b5ee9e59c5fe8cc9c5ee9b29c5fe9989c5ee87f9c5fea659c5ce72c' \
              '(368)9a60ea3d9c5ee8899c5fe9d49c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              'f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8d59c5ee8899c5ee63e(320)a05eed2b9b5ee79a9b5ee8e' \
              '59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e59b5ee79aa05eed2b(280)9f5f' \
              'e9189b5ee8929c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9' \
              'c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8929f5fe918(248)9966ff059c5ee87f9c5fe9f89c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9f89c5ee87f9966ff05(224)9d5ee8599b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9b5ee8e59a5ee859(208)9c5ee87c9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              'f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fea7b(192)9c5fe89e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5eeacf9c5ee9849a5fe8689c5ee84e9960e635a05eec1b7' \
              'f7f7f04a05eec1b9960e6359c5ee84e9a5fe8689c5ee9849b5ee8d09c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5fe89e(168)995de51e9c5fe9c09c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9bf9b5fe873995fe528' \
              '(104)995fe5289d5feb739c5ee9bf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9c0995de51e(144)995de51e9c5ee8e39c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9d5fe9b19a5fe838(152)9a5fe8389d5fe9b19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee8e3995de51e(136)9c5fe9c09c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8c59c5fe74b00000000ff000001b33131cfb43232a7b4323' \
              '27fb3313158b42f2f3(129)9c5fe74b9b5ee8c59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9c(129)9a5fe89e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              'f9b5fe873(24)b4333359b43232ffb43232ffb43232ffb43232ffb23131fb(144)9b5fe8739c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe89e(112)9b5fea7b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe8f39c5fe85(33)b4303093b43232ffb43232ffb43232ffb43232ffb33232ea(152)' \
              '9a5ee8519c5fe8f39c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee87c(96)9a5ee8599' \
              'c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9d19b5ee82e(40)b33030c1b43232ffb4' \
              '3232ffb43232ffb43232ffb33131cd(160)9b5ee82e9c5fe9d19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9d5ee859(80)9966ff059b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9d1a25ce716(48)b33131e2b43232ffb43232ffb43232ffb43232ffb33232a3(168)a25ce7169c5fe9d19c5fe9ff9c5fe9f' \
              'f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e59966ff05(72)9c5ee87f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe8f39b5ee82e(56)b43232f6b43232ffb43232ffb43232ffb43232ffb230306e(176)9b5e' \
              'e82e9c5fe8f39c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee87f(64)9f5fe9189c5fe9f89c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5ee851(64)b43232ffb43232ffb43232ffb43232ffb43232' \
              'ffb32e2e2c(184)9c5fe8509c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f89f5fe918(56)9b' \
              '5ee8929c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fe873(64)b6313143b43232ffb43232ffb43' \
              '232ffb43232ffb43232fd(200)9b5fe8739c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee892(48)' \
              'a05eed2b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8c5(72)b5333381b43232ffb43232ffb' \
              '43232ffb43232ffb33131f1(208)9b5ee8c59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ffa05eed2b' \
              '(40)9b5ee79a9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe74b(72)b43333b3b43232ffb4323' \
              '2ffb43232ffb43232ffb43131d8(208)9c5fe74b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee' \
              '79a(40)9b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9d5fe9b1(80)b43131d8b43232ffb43232ffb4' \
              '3232ffb43232ffb43333b3(216)9d5fe9b19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e5(32)9c5ee6' \
              '3e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5fe838(80)b33131f1b43232ffb43232ffb43232f' \
              'fb43232ffb5333381(216)9a5fe8389c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a60ea3d(24)9c5' \
              'ee8899c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9bf(88)b43232fdb43232ffb43232ffb43232ffb432' \
              '32ffb6313143(224)9c5ee9bf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee889(24)9b5ee8d59c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9d5feb73(80)b32e2e2cb43232ffb43232ffb43232ffb43232ffb43232ff' \
              '(232)9b5fe8739c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9d4(16)9c5ce72c9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff995fe528(80)b230306eb43232ffb43232ffb43232ffb43232ffb43232f6(232)' \
              '995fe5289c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ce72c000000009c5fea659c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8d(89)b33232a3b43232ffb43232ffb43232ffb43232ffb33131e2(240)' \
              '9c5eeacf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fea65000000009c5ee87f9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee984(88)b33131cdb43232ffb43232ffb43232ffb43232ffb33030c1(240)9c5ee98' \
              '49c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee87f000000009c5fe9989c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9a5fe868(88)b33232eab43232ffb43232ffb43232ffb43232ffb4303093(240)9a5fe8689c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe999000000009c5ee9b29c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5ee84e(88)b23131fbb43232ffb43232ffb63232ffbb3433ffc339358ad33a3a23(232)9c5ee84e9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9b2000000009c5fe8cc9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9' \
              'c5fe9ff9c5fe9ff9960e635(80)b2333314b43232ffb43232ffb63232ffbf3433ffc73734ffc44844edb66260fd9f8888eb9' \
              '59595c79696969a9696965f8b8b8b16(192)9960e6359c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe8cc' \
              '000000009b5ee9e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ffa05eec1b(80)b4333359b43232ffb43232ff' \
              'b83433ffc53734ffcc3a35ffca3f3cfcbd5450ffa57e7cff969696ff969696ff969696ff969696ff959595fa969696e89595' \
              '95c7979797999696965f8b8b8b16(144)a05eec1b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee9e5000' \
              '000009c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff7f7f7f04(80)b4303093b43232ffb43232ffbb3' \
              '332ffcb3734ffcc3934fecb403cffbc5a59ff9e8989ff969696ff969696ff969696ff969696ff969696ff969696ff969696f' \
              'f969696ff969696ff969696ff959595fa969696e8959595c7979797999696965f8d8d8d09(96)7f7f7f029d5fe9ff9d5fe9f' \
              'f9d5fe9ff9d5fe9ff9d5fe9ff9d5fe9ff9c5ee974000000009b5ee9e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ffa05eec1b(80)b33030c1b43232ffb43232ffbe3633ffc83934ffce3b36fcc64742ffb06e6aff969696ff969696ff969' \
              '696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696f' \
              'f969696ff959595d3(96)a05eec1b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e5000000009c5fe8c' \
              'c9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9960e635(80)b33131e2b43232ffb43232ffb73532ffc73634f' \
              'fc73c38f1bd5856ffa28383ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969' \
              '696ff969696ff969696ff969696ff969696ff969696ff969696ff969696a9(96)9960e6359c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe8cc000000009c5ee9b29c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee84' \
              'e(80)b43232f6b43232ffb43232ffb43232ffb93532ffc338339fca4c3e359696965f97979799959595c7969696e8959595f' \
              'a969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969696ff969' \
              '6967f(96)9c5ee84e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9b2000000009c5fe9999c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5fe868(80)b43232ffb43232ffb43232ffb43232ffb43232ffb32e2e2c(48)' \
              '8b8b8b169696965f97979799959595c7969696e8959595fa969696ff969696ff969696ff969696ff969696ff969696ff9494' \
              '9456(96)9a5fe8689c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe998000000009c5ee87f9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee984(72)b6313143b43232ffb43232ffb43232ffb43232ffb43232fd(104)' \
              '8b8b8b169696965f9595959b959595c7969696e8959595fa9696962c(96)9c5ee9849c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              'f9c5fe9ff9c5fe9ff9c5ee87f000000009c5fea659c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5eeacf(72)' \
              'b5333381b43232ffb43232ffb43232ffb43232ffb33131f1(256)9b5ee8d09c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe865000000009c5ce72c9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff995fe52' \
              '8(64)b43333b3b43232ffb43232ffb43232ffb43232ffb43131d8(248)995fe5289c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9' \
              'c5fe9ff9c5fe9ff9c5fe9ff9c5ce72c(16)9c5fe9d49c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fe873' \
              '(64)b43131d8b43232ffb43232ffb43232ffb43232ffb43333b3(248)9d5feb739c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9b5ee8d5(24)9c5ee8899c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9bf(64)b3313' \
              '1f1b43232ffb43232ffb43232ffb43232ffb5333381(248)9c5ee9bf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5ee889(24)9a60ea3d9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5fe838(56)b43232' \
              'fdb43232ffb43232ffb43232ffb43232ffb6313143(240)9a5fe8389c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5ee63e(32)9b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9d5fe9b1(48)b32e2e2' \
              'cb43232ffb43232ffb43232ffb33234ffb33136ff7f3fbf04(240)9d5fe9b19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9b5ee8e5(40)9b5ee79a9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe74b(40)' \
              'b230306eb43232ffb43232ffb23236ffae3046ffaf304ef79033bb1e7f3fbf04(224)9c5fe74b9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee79a(40)a05eed2b9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9b5ee8c5(40)b23134a4b33136ffb23236ffae3048ffa72e68ff742ea4fa532eb6fb3d31b4ec3231b3ce3232' \
              'b3a33030b26e2e2eb32c(192)9b5ee8c59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ffa05eed2b' \
              '(48)9b5ee8929c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fe873(24)7f3fbf04ae3040d2a' \
              'f3146ffac2f4effa62e67ff9f2e89ff7a2eb2fb682eb6ff4e2fb6ff3a31b5ff3332b4ff3232b4ff3232b4ff3232b4fd31' \
              '31b3f13131b4d83333b4b33333b5813131b643(136)9b5fe8739c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9b5ee892(56)9f5fe9189c5fe9f89c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe85(17)942abf0cad314deda6315fffa42e72ff9d2e86ff9a2e9fff802eb6ff722eb6ff5530b5ff3f31b5ff3531b4ff3' \
              '232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4f63131b3e23030b3c130' \
              '30b4933333b4590000ff01(72)9a5ee8519c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              '89f5fe918(64)9c5ee87f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe8f39b5ee82e0000' \
              '00009415aa0cac2f4ffba72e6affa02e80ff9d2e8eff972ea1ff7f2fb6ff6f2eb6ff512fb6ff3a31b5ff3332b4ff3232b' \
              '4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4' \
              'ff3232b4ff3131b3cf(64)9b5ee82e9c5fe8f39c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'ee87f(72)9966ff059b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9d1a25ce716' \
              '7f007f04af2d49b9aa2d5de4a32e6fffa02d7bff982e92ff682eb6ff592eb6ff3d30b4ff3332b4ff3232b4ff3232b4ff3' \
              '232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff32' \
              '32b4ff3232b4a7(56)a25ce7169c5fe9d19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e' \
              '59966ff05(80)9d5ee8599c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9d19b5e' \
              'e82e7f1f9f08992ac31e8e33b732a12e8357953683638931be434f38bb6d3331b3953030b3c13131b3e23232b4f63232b' \
              '4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4' \
              'ff3232b47f(48)9b5ee82e9c5fe9d19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9a5' \
              'ee859(96)9c5ee87c9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe8f39a5ee851' \
              '7f3fbf049f1fbf087f3fbf047f3fbf049f1fbf087f3fbf04(40)3131b6433333b5813333b4b33131b4d83131b3f13232b' \
              '4fd3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3232b4ff3131b358(40)9c5fe8509c5fe8f39c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fea7b(112)9c5fe89e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5fe873(128)2e2eb32c3030b26e3232b3a33131b3cd3232b3ea31' \
              '31b2fb2f2fb43(33)9b5fe8739c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9a5fe89e(128)9c5fe9c09c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5e' \
              'e8c59c5fe74b(184)9c5fe74b9b5ee8c59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9c(137)995de51e9c5ee8e39c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9d5fe9b19a5fe838(152)9a5fe8389d5fe9b19c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9' \
              'c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee8e3995de51e(144)995de51e9c5fe9c09c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee9bf9d5feb73995fe528(104)9' \
              '95fe5289b5fe8739c5ee9bf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5fe9c0995de51e(168)9a5fe89e9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8d09c5ee9849a5fe8689c5ee84e9960e635a05eec1' \
              'b7f7f7f04a05eec1b9960e6359c5ee84e9a5fe8689c5ee9849c5eeacf9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe89e(192)9b5fea7b9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9' \
              'ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5ee87' \
              'c(208)9a5ee8599b5ee8e59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5' \
              'fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee' \
              '8e59d5ee859(224)9966ff059c5ee87f9c5fe9f89c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9' \
              'c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f89c5ee87f996' \
              '6ff05(248)9f5fe9189b5ee8929c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9f' \
              'f9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff' \
              '9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8929f5fe918(280)a05eed2b9b5ee79a9b5ee8e59c5f' \
              'e9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe' \
              '9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9b5ee8e59b5ee79aa05eed2b(320)9' \
              'c5ee63e9c5ee8899b5ee8d59c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c' \
              '5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9ff9c5fe9d49c5ee8899a60ea3d(368)9c5ce72c9c5fea659c5ee8' \
              '7f9c5fe9989c5ee9b29c5fe8cc9b5ee9e59c5fe9ff9b5ee9e59c5fe8cc9c5ee9b29c5fe9999c5ee87f9c5fea659c5ce72c(712)'


def create_icon(icon):
    # unzip icon data
    even_odd = 0
    icon_data = ''
    for block in icon.replace(')', '(').split('('):
        if even_odd % 2 == 0:
            icon_data += block
        else:
            icon_data += '0' * int(block)
        even_odd += 1

    # create temp file
    with tempfile.NamedTemporaryFile(delete=False) as iconfile:
        iconfile.write(binascii.a2b_hex(icon_data))

    return iconfile.name


def browse_to_artist(gui_):
    if not g_vars.source_directory and not g_vars.destination_directory:
        showwarning("ErrorEmptyFields", "Incorrect source and destination folders.")
        return None
    if not os.path.exists(g_vars.songs_path) or not os.listdir(g_vars.songs_path):
        showwarning("IncorrectSourceFolder", "Incorrect source folder.")
        return None
    if not g_vars.destination_directory:
        showwarning("IncorrectDestinationFolder", "Incorrect destination folder.")
        return None
    if g_vars.source_directory == g_vars.destination_directory:
        showwarning("ErrorSamePaths", "Source and destination cannot be the same.")
        return None

    destinations_recursive_files = []
    for path, directories, files in os.walk(g_vars.destination_directory):
        destinations_recursive_files.extend(files)

    for directory in next(os.walk(g_vars.songs_path))[1] + destinations_recursive_files:
        l_directory = directory.lower()
        if g_vars.osu_directory_regex.search(directory) and l_directory.split(maxsplit=1)[1] not in g_vars.musics_seen:
            g_vars.musics_seen.add(l_directory.split(maxsplit=1)[1])
            g_vars.osu_directories[l_directory] = {
                'artist': directory.lower().split(maxsplit=1)[1].split(' - ')[0],
                'directory': directory,
                'path': path_join(g_vars.songs_path, directory),
            }

    if not g_vars.osu_directories:
        showwarning("ErrorOsuNotFound", "You must enter a valid osu! folder !")
        return None

    g_vars.artist_counter = Counter([x['artist'] for x in g_vars.osu_directories.values()])
    gui_.artist_choice()


def detect_choice(radio_buttons):
    directories = next(os.walk(g_vars.destination_directory), [[], [], []])[1]
    files = next(os.walk(g_vars.destination_directory), [[], [], []])[2]

    if not directories and files:
        showinfo('Previous Setting Detected', Ascii().detected_setting.format('No'))
        radio_buttons[0].invoke()
        g_vars.radio_value = 1
    elif directories and not files:
        showinfo('Previous Setting Detected', Ascii().detected_setting.format('Yes for all'))
        radio_buttons[1].invoke()
        g_vars.radio_value = 2
    elif directories and files:
        min_nb_occurrences = min([len(os.listdir(path_join(g_vars.destination_directory, x))) for x in directories])
        if min_nb_occurrences < 1:
            min_nb_occurrences = 1

        g_vars.spin_value = min_nb_occurrences
        showinfo('Previous Setting Detected', Ascii().detected_setting.format(
            'Yes but only from {0} occurrence(s)'.format(min_nb_occurrences)
        ))
        radio_buttons[2].invoke()
        g_vars.radio_value = 3
    else:
        radio_buttons[0].invoke()
        g_vars.radio_value = 1


def artist_to_script(gui_):
    if g_vars.radio_value == 0:
        showwarning("ErrorNothingSelected", "You have to choose one option")
        return None
    elif g_vars.radio_value == 1:
        os.makedirs(g_vars.destination_directory, exist_ok=True)
        gui_.script()
    elif g_vars.radio_value == 2:
        for artist in g_vars.artist_counter:
            os.makedirs(path_join(g_vars.destination_directory, artist.title()), exist_ok=True)
        gui_.script()
    elif g_vars.radio_value == 3:
        for artist, occurrences in g_vars.artist_counter.items():
            if occurrences >= g_vars.spin_value:
                os.makedirs(path_join(g_vars.destination_directory, artist.title()), exist_ok=True)
        gui_.script()


def script_to_end(gui_):
    if g_vars.radio_value in (2, 3):
        path, directories, files = next(os.walk(g_vars.destination_directory))
        for file in files:
            artist = file.split(' - ', 1)[0].lower()
            if g_vars.radio_value == 2 or g_vars.artist_counter[artist] >= g_vars.spin_value:
                shutil.move(path_join(path, file), path_join(path, artist, file))

        for directory in directories:
            directory_path = path_join(path, directory)
            if g_vars.radio_value == 3 and len(os.listdir(directory_path)) < g_vars.spin_value:
                for file in os.listdir(directory_path):
                    shutil.move(path_join(directory_path, file), path_join(path, file))

            if not os.listdir(directory_path):
                os.rmdir(directory_path)

    gui_.end()


class GraphicalUserInterface:
    def __init__(self):
        self.ascii = Ascii()
        self.root = g_vars.root
        self.start()

    def start(self):
        self.root.minsize(665, 400)
        self.root.maxsize(665, 400)
        self.root.title("FelOsu")
        self.licence()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.iconbitmap(create_icon(iconhexdata))
        self.root.mainloop()

    def clean(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit(self):
        if askyesno("Exit", "Do you want to quit?"):
            del self
            os._exit(0)

    def licence(self):
        self.clean()
        frame_ext = tk.Frame(self.root, borderwidth=5, relief=RAISED)
        frame_int = tk.Frame(frame_ext, borderwidth=5, relief=SUNKEN)
        frame_ext.pack(pady=16, padx=8)
        frame_int.pack(pady=12, padx=12)
        Ttk_Label(frame_int, text=self.ascii.license, background="white").pack()
        Ttk_Button(self.root, text="Exit", command=self.exit, width=10).pack(side=RIGHT, padx=12, pady=20)
        Ttk_Button(self.root, text="Next >", command=self.browse, width=10).pack(side=RIGHT, pady=20)

        try:
            if "00000000001500" not in requests.get(g_vars.topic_link, timeout=2).text:
                if askyesno("Update Available !", "An update is available,\ndo you want to download it ?"):
                    webbrowser.open(g_vars.topic_link)
        except requests.exceptions.Timeout:
            pass

    def browse(self):
        self.clean()
        frame_display = {'side': TOP, 'padx': 30, 'fill': 'both', 'expand': 'yes'}
        frame_source = LabelFrame(self.root, text=" osu! folder ", relief=GROOVE)
        frame_destination = LabelFrame(self.root, text=" Destination folder ", relief=GROOVE)
        frame_source.pack(**frame_display, pady=8)
        frame_destination.pack(**frame_display, pady=5)
        Label(frame_source, text="\nPlease, indicate osu! folder").pack(side=TOP)
        Ttk_Button(frame_source,
                   text="Browse...",
                   command=lambda: g_vars._source_directory.set(askdirectory(title="Please, indicate osu! folder")),
                   width=9).pack(side=RIGHT, padx=12, pady=20)
        source_field = Entry(frame_source, textvariable=g_vars._source_directory, width=70)
        source_field.pack(side=RIGHT, padx=15)
        Label(frame_destination,
              text="\nPlease, indicate the folder where you want the files to be copied in").pack(side=TOP)
        Ttk_Button(frame_destination,
                   text="Browse...",
                   command=lambda: g_vars._destination_directory.set(askdirectory(title="Please, indicate the folder "
                                                                                        "where you want the files to "
                                                                                        "be copied in")),
                   width=9).pack(side=RIGHT, padx=12, pady=20)
        destination_field = Entry(frame_destination, textvariable=g_vars._destination_directory, width=70)
        destination_field.pack(side=RIGHT, padx=15)
        Ttk_Button(self.root, text="Exit", command=self.exit, width=10).pack(side=RIGHT, padx=12, pady=20)
        Ttk_Button(self.root, text="Next >", command=lambda: browse_to_artist(self), width=10).pack(side=RIGHT, pady=20)
        Ttk_Button(self.root, text="< Previous", command=self.licence, width=10).pack(side=RIGHT, padx=12, pady=20)

    def help_me(self):
        help_window = tk.Tk()
        help_window.minsize(580, 200)
        help_window.maxsize(580, 200)
        Label(help_window, text=self.ascii.help).pack()

    def artist_choice(self):
        self.clean()
        frames = (
            Frame(self.root, relief=GROOVE),
            Frame(self.root, relief=FLAT),
            Frame(self.root, relief=FLAT),
            Frame(self.root, relief=FLAT),
        )
        for frame in frames:
            frame.pack(padx=60, pady=5, fill="both", expand="yes")

        label = Label(frames[0], text='Do you want to sort by artist ?\n\n'
                                      'For more precision, click "Help" in the bottom-left corner')
        label.config(font=("Courier", 10))
        label.pack(pady=50)
        radio_buttons = (
            Radiobutton(frames[1], text="No", variable=g_vars._radio_value, value=1),
            Radiobutton(frames[2], text="Yes for all", variable=g_vars._radio_value, value=2),
            Radiobutton(frames[3], text="Yes, but only from : ", variable=g_vars._radio_value, value=3)
        )
        for radio_button in radio_buttons:
            radio_button.pack(side=LEFT)

        spinbox = Spinbox(frames[3], from_=1, to=g_vars.nb_artists_max, width=8, textvariable=g_vars._spin_value)
        spinbox.pack(side=LEFT)
        Label(frames[3], text=" max = {0}".format(g_vars.nb_artists_max)).pack(side=LEFT, padx=5)

        Ttk_Button(self.root, text="Help", command=self.help_me, width=10).pack(side=LEFT, padx=12, pady=20)
        Ttk_Button(self.root, text="Exit", command=self.exit, width=10).pack(side=RIGHT, padx=12, pady=20)
        Ttk_Button(self.root, text="Next >", command=lambda: artist_to_script(self), width=10).pack(side=RIGHT, pady=20)
        Ttk_Button(self.root, text="< Previous", command=self.browse, width=10).pack(side=RIGHT, padx=12, pady=20)

        detect_choice(radio_buttons)

    def script(self):
        self.clean()

        def get_music(path_):
            for file in (file_ for file_ in next(os.walk(path_))[2]
                         if file_.rsplit('.', 1)[1].lower() in ('mp3', 'ogg', 'm4a')):
                try:
                    if TinyTag.get(path_join(path_, file)).duration > 30:
                        return file
                except tinytag.TinyTagException:
                    return file

        loading = StringVar()
        mountain_frame = Frame(self.root, relief=FLAT)
        train_frame = Frame(self.root, relief=FLAT)
        cloud_art = Label(mountain_frame, text=Ascii().cloud, font='bold')
        text_art = Label(mountain_frame, font='bold', textvariable=loading)
        mountain_art = Label(mountain_frame, text=Ascii().mountain, font='bold', anchor='s')
        train_art = Label(train_frame, text=Ascii().train, font='bold')
        rail_art = Label(train_frame, text=Ascii().rail, font='bold')

        # Configuration
        cloud_art.configure(font=("Courier", 4))
        text_art.configure(font=("Courier", 9))
        mountain_art.configure(font=("Courier", 8))
        train_art.configure(font=("Courier", 6))
        rail_art.configure(font=("Courier", 7))

        # Pack
        mountain_frame.pack(fill=BOTH, expand=TRUE, side=TOP)
        train_frame.pack(fill=BOTH, expand=TRUE, side=BOTTOM)
        cloud_art.pack(side=TOP)
        mountain_art.pack(side=BOTTOM)
        rail_art.pack(side=BOTTOM)

        # SCRIPTING PART
        for index, (l_directory, data) in enumerate(g_vars.osu_directories.items(), start=1):
            percent = round(index / len(g_vars.osu_directories) * 100)

            source_music_name = get_music(data['path'])
            source_music_path = path_join(data['path'], source_music_name)

            artist = data['artist'].title()
            file_extension = source_music_name.rsplit('.', 1)[1].lower()
            destination_music_name = '{0} - {1}.{2}'.format(
                artist, data['directory'].split(maxsplit=1)[1].split(' - ', 1)[1], file_extension
            )

            if (g_vars.radio_value == 2 or
                    (g_vars.radio_value == 3 and g_vars.artist_counter[data['artist']] >= g_vars.spin_value)):
                shutil.copyfile(source_music_path,
                                path_join(g_vars.destination_directory, artist, destination_music_name))
            else:
                shutil.copyfile(source_music_path, path_join(g_vars.destination_directory, destination_music_name))

            # TRAIN MOVEMENT
            var_int = ((326 * index) / len(g_vars.osu_directories))
            if var_int <= 163:
                train_art.pack(side=LEFT, padx=var_int)
            else:
                train_art.pack(side=RIGHT, padx=326 - var_int)

            # PRINTING INFORMATION
            loading.set(Ascii().progress_bar.format(
                index,
                len(g_vars.osu_directories),
                percent,
                " " * (25 - (len(str(index)) + len(str(len(g_vars.osu_directories))) + len(str(percent))))
            ))
            text_art.pack(side=TOP)
            self.root.update()
        script_to_end(self)

    def end(self):
        self.clean()
        frame = tk.Frame(self.root, relief=GROOVE, borderwidth=4)
        text = Label(frame, text=self.ascii.outro)
        Ttk_Button(self.root, text="Exit", command=lambda: sys.exit(0), width=10).pack(side=BOTTOM, padx=12, pady=20)
        text.configure(font=("Courier", 9))
        text.pack(side=TOP, padx=10, pady=10)
        frame.pack(padx=60, pady=60, fill="both", expand="yes")
        link = tk.Label(frame, text="FelOsu Update & News", fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda x: webbrowser.open(g_vars.topic_link))


GraphicalUserInterface()
