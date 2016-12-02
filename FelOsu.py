from shutil import rmtree, copy, move
import tempfile
from glob import glob
from collections import Counter
from tkinter.filedialog import *
from tkinter.messagebox import askyesno, showinfo, showwarning
from tkinter.ttk import *
import tkinter as tk
import webbrowser
import urllib.request

# music_file_path = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods\\Lost Woods.mp3"
# list_dir = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods"
# artist_music = "Koji Kondo - Lost Woods"
# artist_list = "Koji Kondo"
# artist_list_lower = "koji kondo"
# artist_dic = " 'nano': 9 "
# folder_path = "C:/Users/BW5442/Downloads/FelOsu/Nouveau dossier"

license_text = """        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.

        You have to mention "Based on Darkaird work" if you reuse this software.

        By clicking "Next >" button, it means that you read those conditions
        mentions above."""

help_text = """

         - "Yes" will put all the musics with the same artist in the same folder (and the folder's name
         will be the artist's name). But even if there is only one music for an artist, it will put it
         in a folder despite everything.

         - "Yes, but only from" is exactly the same except the fact that you set the number of musics
          of a same artist from which it will create a folder.
"""

train_text = """
     ___                     _          ___
    | __|       ___         | |        / _ \        ___      _  _
    | _|       / -_)        | |       | (_) |      (_-<     | +| |      . . . o o
  __|_|____  __\___|___  ___|_|_     __\___/__  ___/__/___  _\_,_|_             o
 |[] [] []| [] [] [] [] [_____(__   |[] [] []| [] [] [] [] [_____(__  ][]]_n_n__][.
 |________|_[_________]_[________]__|________|_[_________]_[________]_|__|________)<
  oo    oo 'oo      oo ' oo    oo '  oo    oo 'oo      oo ' oo    oo 'oo 0000---oo\_"""

rail_text = "#" * 135

cloud_text = """
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

mountain_text = """
                             ^    _                                _     ^
  ^            ^        .-.      / \        _                     / \        _           ^
            ^          /   \    /^./\__   _/ \             ^     /^./\__   _/ \\
          _        .--'\/\_ \__/.      \ /    \  ^   ___        /.      \ /    \  ^^_
         / \_    _/ ^      \/  __  :'   /\/\  /\  __/   \      /__  :'   /\/\  /\_./ \\
        /    \  /    .'   _/  /  \   ^ /    \/  \/ .`'\_/\    /  \   ^ /    \/  \/ .`'\\  ^
       /\/\  /\/ :' __  ^/  ^/    `--./.'  ^  `-.\ _    _:\ _/    `--./.'  ^  `-.\ _  _\\
      /    \/  \  _/  \-' __/.' ^ _   \_   .'\   _/ \ .  __/ \   ' ^ _   \_   .'\   _/  \\
    /\  .-   `. \/     \ / -.   _/ \ -. `_/   \ /    `._/  ^  \    _/ \ -. `_/   \ /    `\\
 __/  `-.__ ^   / .-'.--'    . /    `--./ .-'  `-.  `-. `.  -  `. /    `--./ .-'  `-.  `-. \__
/        `.  / /        `-.   /  .-'   / .    .'  \    \  \  -   /  .-'   / .   .'   \    \   \\"""


root = tk.Tk()
artist_folder = []
browse_text1 = StringVar()
browse_text2 = StringVar()
radio_value = IntVar()
spin_var = IntVar()

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)


class GraphicalUserInterface:

    def __init__(self):
        root.iconbitmap(default=ICON_PATH)
        root.minsize(665, 400)
        root.maxsize(665, 400)
        root.title("FelOsu")

    @staticmethod
    def exit_func():
        if askyesno("Exit", "Do you want to quit? "):
            try:
                func.script_to_end()
                root.quit()
                sys.exit(0)
            except:
                root.quit()
                sys.exit(0)

    @staticmethod
    def licence():
        for widget in root.winfo_children():
            widget.destroy()
        frame1 = tk.Frame(root, borderwidth=5, relief=RAISED)
        frame2 = tk.Frame(frame1, borderwidth=5, relief=SUNKEN)
        frame1.pack(pady=13, padx=5)
        frame2.pack(pady=12, padx=12)
        tk.Label(frame2, text=license_text, bg="white").pack(padx=1, pady=2)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=15)
        Button(root, text="Next >", command=gui.browse, width=10).pack(side=RIGHT, pady=15)
        root.protocol("WM_DELETE_WINDOW", gui.exit_func)
        if "00000000001300" not in urllib.request.urlopen("https://osu.ppy.sh/forum/t/520493").read().decode("utf-8"):
            if askyesno("Update Available !", "An update is available,\ndo you want to download it ?"):
                webbrowser.open("https://osu.ppy.sh/forum/t/520493")


    @staticmethod
    def browse():
        for widget in root.winfo_children():
            widget.destroy()
        frame_browse_window_up = LabelFrame(root, text=" osu! folder ", relief=GROOVE)
        frame_browse_window_bottom = LabelFrame(root, text=" Destination folder ", relief=GROOVE)
        frame_browse_window_up.pack(side=TOP, padx=30, pady=8, fill="both", expand="yes")
        frame_browse_window_bottom.pack(side=TOP, padx=30, pady=5, fill="both", expand="yes")
        Label(frame_browse_window_up, text="\nPlease, indicate osu! folder").pack(side=TOP)
        Button(frame_browse_window_up, text="Browse...",
               command=func.get_source, width=9).pack(side=RIGHT, padx=12, pady=20)
        entry1 = Entry(frame_browse_window_up, textvariable=browse_text1, width=70)
        entry1.pack(side=RIGHT, padx=15)
        Label(frame_browse_window_bottom,
              text="\nPlease, indicate the folder where you want the files to be copied in").pack(side=TOP)
        Button(frame_browse_window_bottom, text="Browse...", width=9,
               command=func.get_destination_path).pack(side=RIGHT, padx=12, pady=20)
        entry2 = Entry(frame_browse_window_bottom, textvariable=browse_text2, width=70)
        entry2.pack(side=RIGHT, padx=15)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=20)
        Button(root, text="Next >", command=func.browse_to_artist, width=10).pack(side=RIGHT, pady=20)
        Button(root, text="< Previous", command=gui.licence, width=10).pack(side=RIGHT, padx=12, pady=20)

    @staticmethod
    # Help window in browse window to help people with proposed choices
    def help_me():
        help_window = tk.Tk()
        help_window.minsize(580, 200)
        help_window.maxsize(580, 200)
        Label(help_window, text=help_text).pack()

    @staticmethod
    def artist_choice():
        for widget in root.winfo_children():
            widget.destroy()
        global radio_value
        frame_browse_window_text = Frame(root, relief=GROOVE)
        frame_browse_window1 = Frame(root, relief=FLAT)
        frame_browse_window2 = Frame(root, relief=FLAT)
        frame_browse_window3 = Frame(root, relief=FLAT)
        frame_browse_window_text.pack(padx=60, pady=50, fill="both", expand="yes")
        frame_browse_window1.pack(padx=60, pady=5, fill="both", expand="yes")
        frame_browse_window2.pack(padx=60, pady=5, fill="both", expand="yes")
        frame_browse_window3.pack(padx=60, pady=5, fill="both", expand="yes")
        Label(frame_browse_window_text, text="""
        Do you want to sort by artist ? For more precision, click "Help" in the bottom-left corner""").pack()
        button1 = Radiobutton(frame_browse_window1, text="No", variable=radio_value, value=1)
        button2 = Radiobutton(frame_browse_window2, text="Yes for all", variable=radio_value, value=2)
        button3 = Radiobutton(frame_browse_window3, text="Yes, but only from : ", variable=radio_value, value=3)
        button1.pack(side=LEFT), button2.pack(side=LEFT), button3.pack(side=LEFT)
        spinbox = Spinbox(frame_browse_window3, from_=1, to=nb_artists_max, width=8, textvariable=spin_var)
        spinbox.pack(side=LEFT)
        Label(frame_browse_window3, text=" max = " + str(nb_artists_max)).pack(side=LEFT, padx=5)
        Button(root, text="Help", command=gui.help_me, width=10).pack(side=LEFT, padx=12, pady=20)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=20)
        Button(root, text="Next >", command=lambda: func.artist_to_script(spinbox.get()), width=10)\
            .pack(side=RIGHT, pady=20)
        Button(root, text="< Previous", command=gui.browse, width=10).pack(side=RIGHT, padx=12, pady=20)
        func.detect_choice()
        func.pre_check_radio_button(button1, button2, button3)

    @staticmethod
    def end():
        for widget in root.winfo_children():
            widget.destroy()
        frame = tk.Frame(root, relief=GROOVE, borderwidth=4)
        text = Label(frame, text="""Thank you for using this software developed by Darkaird !

If you have suggestion(s) or bug(s), you can send an email at :
software.felosu@gmail.com

Click the link below to see changelog :
""")
        Button(root, text="Exit", command=lambda: sys.exit(0), width=10).pack(side=BOTTOM, padx=12, pady=20)
        text.configure(font=("Courier", 9))
        text.pack(side=TOP, padx=10, pady=10)
        frame.pack(padx=60, pady=60, fill="both", expand="yes")
        link = tk.Label(frame, text="FelOsu Update & News", fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", func.callback)


class Function:
    @staticmethod
    def callback(event):
        webbrowser.open_new(r"https://osu.ppy.sh/forum/t/520493")

    @staticmethod
    # Open window which asks osu! folder
    def get_source():
        global source
        source = askdirectory(title="Please, indicate osu! folder")
        browse_text1.set(source)

    @staticmethod
    # Open window which asks destination folder
    def get_destination_path():
        global destination_path
        destination_path = askdirectory(title="Please, indicate the folder where you want the files to be copied in"
                                              " (To create a new folder, press right mouse button and choose "
                                              "'New folder')")
        browse_text2.set(destination_path)

    @staticmethod
    def detect_choice():
        global min_nb_occurrences, pre_check
        directory_number = len(next(os.walk(destination_path))[1])
        file_number = len(next(os.walk(destination_path))[2])

        if directory_number == 0 and file_number > 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'No\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
            pre_check = 1

        elif directory_number > 0 and file_number == 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes for all\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
            pre_check = 2

        elif directory_number > 0 and file_number > 0:
            min_nb_occurrences = min([len(glob(destination_path + '\\' + directories + '\\*')) for directories in
                                      next(os.walk(destination_path))[1]])
            spin_var.set(min_nb_occurrences)
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes but only from ' + str(min_nb_occurrences) +
                                                  ' occurrence(s)\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
            pre_check = 3

        else:
            pre_check = 0
            pass

    @staticmethod
    def pre_check_radio_button(btn1, btn2, btn3):
        if pre_check == 1:
            btn1.invoke()
        elif pre_check == 2:
            btn2.invoke()
        elif pre_check == 3:
            btn3.invoke()
        else:
            pass

    @staticmethod
    def browse_to_artist():
        # Avoid folder errors
        if len(browse_text1.get()) == 0 and len(browse_text2.get()) == 0:
            showwarning("ErrorEmptyFields", "You have to enter osu! and destination folder !")
            return None
        if len(browse_text2.get()) == 0:
            showwarning("ErrorEmptyDestination", "You have to enter a destination folder !")
            return None
        if (os.path.exists(source + "\\Songs") is not True) or (len(os.listdir(source + "\\Songs")) == 0):
            showwarning("ErrorOsuNotFound", "You must enter a valid osu! folder !")
            return None
        if os.path.exists(browse_text2.get()) is not True:
            showwarning("ErrorDestinationNotValid", "You must enter a valid destination folder !")
            return None
        if browse_text1.get() == browse_text2.get():
            showwarning("ErrorSamePaths", "You must enter a different folders !")
            return None

        # Get all artist AND make all artist in lowercase to avoid case issues
        global artist_list, artist_music

        #   Work only on osu folder (avoid issues with "tutorial" and co)
        regex = re.compile(r"^[\d]+[\s](.)+-(.)+")

        #  Get all artist AND make all artist (with duplicates) in lowercase to avoid case issues
        #  AND
        #  Get all file music name like "artist - music name"
        osu_directories_list = [x for x in os.listdir(source + "\\Songs") if regex.search(x) is not None]
        artist_list_lower = [(" ".join(x.split()[1:])).split(" - ")[0].lower() for x in osu_directories_list]
        artist_list = [(" ".join(x.split()[1:])).split(" - ")[0] for x in osu_directories_list]
        artist_music = [(" ".join(x.split()[1:])) for x in osu_directories_list]

        #  Count max occurrence of artist and make artist list
        global artist_dic, nb_artists_max
        artist_dic = Counter(artist_list_lower)
        try:
            nb_artists_max = artist_dic[max(artist_dic, key=artist_dic.get)]
        except ValueError:
            showwarning("ErrorOsuNotFound", "You must enter a valid osu! folder !")
            return None
        gui.artist_choice()

    @staticmethod
    def artist_to_script(spin_box_number):  # Called by Artist_window()
        global int_spin_box_number
        int_spin_box_number = int(spin_box_number)

        # Check if at least one option is chosen
        if radio_value.get() == 0:
            showwarning("ErrorNothingSelected", "You have to choose one option")
            return None

        # Radio button choice path
        #  Do nothing with artist
        if radio_value.get() == 1:
            script()

        #   Create folder for each artist
        elif radio_value.get() == 2:
            for artist in set(artist_list):
                #   Exception to avoid case problem again (like "lisa" and "LiSa")
                try:
                    os.mkdir(destination_path + '\\' + str(artist.lower().title()))
                    artist_folder.append(artist.lower().title())
                except FileExistsError:
                    pass
            script()

        #   Create folder from given value
        elif radio_value.get() == 3:
            # Check if spin number is valuable
            try:
                int(spin_box_number)
                if int(spin_box_number) < 1 or int(spin_box_number) > nb_artists_max:
                    showwarning("ErrorSpinNumber", "You have to choose a number between 1 and " + str(nb_artists_max))
                    return None
            except ValueError:
                showwarning("ErrorSpinNumber", "You have to choose a number between 1 and " + str(nb_artists_max))
                return None

            for artist in set(artist_list):
                if artist_dic.get(artist.lower()) >= int(spin_box_number):
                    #   Exception to avoid case problem again (like "lisa" and "LiSa")
                    os.makedirs(destination_path + '\\' + str(artist.lower().title()), exist_ok=True)
                    artist_folder.append(artist.lower().title())

            script()

    @staticmethod
    def copy_rename(music_path, counter):  # Check if file not already present and if not copy and rename it
        artist_lower_title = artist_list[counter].lower().title()
        file_extension = music_path.split(".")[-1]
        file_name = music_path.split("\\")[-1]
        # Search if there is folder with artist_music's artist name, if not just copy it a folder_path root
        if artist_lower_title in artist_folder:
            copy(music_path, destination_path + "\\" + artist_lower_title)
            os.rename(destination_path + "\\" + artist_lower_title + "\\" + file_name,
                      destination_path + "\\" + artist_lower_title + "\\"
                      + artist_music[counter] + "." + file_extension)
        else:
            copy(music_path, destination_path)
            os.rename(destination_path + "\\" + file_name,
                      destination_path + "\\" + artist_music[counter] + "." + file_extension)

    @staticmethod
    def avoid_duplicates(counter):
        for destination_file in next(os.walk(destination_path))[2]:
            if destination_file.lower().startswith(artist_music[counter].lower() + '.'):
                return True

        for destination_directory in next(os.walk(destination_path))[1]:
            for file in os.listdir(destination_path + '\\' + destination_directory):
                if file.lower().startswith(artist_music[counter].lower() + '.'):
                    return True

        return False

    @staticmethod
    def script_to_end():
        directory_path_view = next(os.walk(destination_path))

        # Bug 775
        if radio_value.get() == 2 or radio_value.get() == 3:
            for file in directory_path_view[2]:
                if artist_dic.get(file.split(' - ')[0].lower()) >= int_spin_box_number:
                    try:
                        move(destination_path + '\\' + file,
                             destination_path + '\\' + file.split(' - ')[0].lower().title() + '\\' + file)
                    except FileNotFoundError:
                        pass

        # Check if number of file in directories < int_spin_box_number
        for directory in directory_path_view[1]:
            if len(os.listdir(destination_path + '\\' + directory)) < int_spin_box_number or radio_value.get() == 1:
                for file in os.listdir(destination_path + '\\' + directory):
                    move(destination_path + '\\' + directory + '\\' + file, destination_path + '\\' + file)

        # Remove directories with 0 files
        for directory in directory_path_view[1]:
            if len(os.listdir(destination_path + '\\' + directory)) == 0:
                rmtree(destination_path + '\\' + directory, ignore_errors=True)

        gui.end()


def script():
    # GRAPHICAL PART
    for widget in root.winfo_children():
        widget.destroy()
    loading = StringVar()
    mountain_frame = Frame(root, relief=FLAT)
    train_frame = Frame(root, relief=FLAT)
    cloud_art = Label(mountain_frame, text=cloud_text, font='bold')
    text_art = Label(mountain_frame, font='bold', textvariable=loading)
    mountain_art = Label(mountain_frame, text=mountain_text, font='bold', anchor='s')
    train_art = Label(train_frame, text=train_text, font='bold')
    rail_art = Label(train_frame, text=rail_text, font='bold')

    # Configuration
    cloud_art.configure(font=("Courier", 4))
    text_art.configure(font=("Courier", 9))
    mountain_art.configure(font=("Courier", 8))
    train_art.configure(font=("Courier", 5))
    rail_art.configure(font=("Courier", 7))

    # Pack
    mountain_frame.pack(fill=BOTH, expand=TRUE, side=TOP)
    train_frame.pack(fill=BOTH, expand=TRUE, side=BOTTOM)
    cloud_art.pack(side=TOP)
    mountain_art.pack(side=BOTTOM)
    rail_art.pack(side=BOTTOM)

    # SCRIPTING PART
    loop_counter = 0
    #   Work only on osu folder (avoid issues with "tutorial" and co)
    regex = re.compile(r"^([0-9])+[\s](.)+")

    list_dir = [x for x in next(os.walk(source + '\\Songs'))[1] if regex.search(x) is not None]
    for directory in list_dir:
        percent = int(round((loop_counter/len(list_dir))*100))

        for file in os.listdir(source + '\\Songs\\' + directory):
            for extension_type in ['.mp3', '.MP3' '.ogg', '.m4a']:
                if file.endswith(extension_type):
                    music_file_path = source + '\\Songs\\' + directory + '\\' + file
                    if func.avoid_duplicates(loop_counter) is False:
                        func.copy_rename(music_file_path, loop_counter)
                        break

        loop_counter += 1
        # TRAIN MOVEMENT
        var_int = ((326*loop_counter)/len(list_dir))
        if var_int <= 163:
            train_art.pack(side=LEFT, padx=var_int)
        else:
            train_art.pack(side=RIGHT, padx=326-var_int)

        # PRINTING INFORMATION
        loading.set(" ______________________________________________________________\n"
                    "|                                                              |\n"
                    "|              Script in progress : " + str(loop_counter) + "/"
                    + str(len(list_dir)) + " (" + str(percent) + "%)"
                    + " " * (22 - (len(str(loop_counter)) + len(str(len(list_dir))) + len(str(percent)))) + "|\n"
                    "|______________________________________________________________|")
        text_art.pack(side=TOP)
        root.update()
    func.script_to_end()

gui = GraphicalUserInterface()
func = Function()
gui.licence()
root.mainloop()
