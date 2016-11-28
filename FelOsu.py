import glob
import shutil
import tempfile
from collections import Counter
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *
import tkinter as tk
import webbrowser

# glob_search = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods\\Lost Woods.mp3"
# list_dir = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods"
# osu_directories_list = "10029 Koji Kondo - Lost Woods"
# artist_music = "Koji Kondo - Lost Woods"
# artist_list = "Koji Kondo"
# artist_list_lower = "koji kondo"
# artist_dic = " 'nano': 9 "
# folder_path = "C:/Users/BW5442/Downloads/FelOsu/Nouveau dossier"

license_text = '''        This program is free software: you can redistribute it and/or modify
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
        mentions above.'''

help_text = '''

         - "Yes" will put all the musics with the same artist in the same folder (and the folder's name
         will be the artist's name). But even if there is only one music for an artist, it will put it
         in a folder despite everything.

         - "Yes, but only from" is exactly the same except the fact that you set the number of musics
          of a same artist from which it will create a folder.

         - "Yes, but only artist(s) I choose" will : COMING SOON !'''

train_text = '''
     ___                     _          ___
    | __|       ___         | |        / _ \        ___      _  _
    | _|       / -_)        | |       | (_) |      (_-<     | +| |      . . . o o
  __|_|____  __\___|___  ___|_|_     __\___/__  ___/__/___  _\_,_|_             o
 |[] [] []| [] [] [] [] [_____(__   |[] [] []| [] [] [] [] [_____(__  ][]]_n_n__][.
 |________|_[_________]_[________]__|________|_[_________]_[________]_|__|________)<
  oo    oo 'oo      oo ' oo    oo '  oo    oo 'oo      oo ' oo    oo 'oo 0000---oo\_'''

rail_text = '#' * 135

cloud_text = '''
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
                  '''

mountain_text = '''
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
/        `.  / /        `-.   /  .-'   / .    .'  \    \  \  -   /  .-'   / .   .'   \    \   \\'''


root = tk.Tk()
artist_music = []
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
        tk.Label(frame2, text=license_text, bg='white').pack(padx=1, pady=2)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=15)
        Button(root, text="Next >", command=gui.browse, width=10).pack(side=RIGHT, pady=15)
        root.protocol("WM_DELETE_WINDOW", gui.exit_func)

    @staticmethod
    def browse():
        for widget in root.winfo_children():
            widget.destroy()
        frame_browse_window_up = LabelFrame(root, text=" osu! folder ", relief=GROOVE)
        frame_browse_window_bottom = LabelFrame(root, text=" Destination folder ", relief=GROOVE)
        frame_browse_window_up.pack(side=TOP, padx=30, pady=8, fill="both", expand="yes")
        frame_browse_window_bottom.pack(side=TOP, padx=30, pady=5, fill="both", expand="yes")
        Label(frame_browse_window_up, text="""\nPlease, indicate osu! folder""").pack(side=TOP)
        Button(frame_browse_window_up, text="Browse...",
               command=func.get_source, width=9).pack(side=RIGHT, padx=12, pady=20)
        entry1 = Entry(frame_browse_window_up, textvariable=browse_text1, width=70)
        entry1.pack(side=RIGHT, padx=15)
        Label(frame_browse_window_bottom,
              text="""\nPlease, indicate the folder where you want the files to be copied in""").pack(side=TOP)
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
        global radio_value, spinbox
        frame_browse_window_text = Frame(root, relief=GROOVE)
        frame_browse_window1 = Frame(root, relief=FLAT)
        frame_browse_window2 = Frame(root, relief=FLAT)
        frame_browse_window3 = Frame(root, relief=FLAT)
        frame_browse_window4 = Frame(root, relief=FLAT)
        frame_browse_window_text.pack(padx=60, pady=50, fill="both", expand="yes")
        frame_browse_window1.pack(padx=60, pady=5, fill="both", expand="yes")
        frame_browse_window2.pack(padx=60, pady=5, fill="both", expand="yes")
        frame_browse_window3.pack(padx=60, pady=5, fill="both", expand="yes")
        frame_browse_window4.pack(padx=60, pady=5, fill="both", expand="yes")
        Label(frame_browse_window_text, text="""
        Do you want to sort by artist ? For more precision, click "Help" in the bottom-left corner""").pack()
        button1 = Radiobutton(frame_browse_window1, text="No", variable=radio_value, value=1)
        button2 = Radiobutton(frame_browse_window2, text="Yes for all", variable=radio_value, value=2)
        button3 = Radiobutton(frame_browse_window3, text="Yes, but only from : ", variable=radio_value, value=3)
        button4 = Radiobutton(frame_browse_window4, text="Yes, but only some artist I want to choose",
                              variable=radio_value, value=4)
        button1.pack(side=LEFT), button2.pack(side=LEFT), button3.pack(side=LEFT), button4.pack(side=LEFT)
        spinbox = Spinbox(frame_browse_window3, from_=1, to=nb_artists_max, width=8, textvariable=spin_var)
        spinbox.pack(side=LEFT)
        Label(frame_browse_window3, text=" max = " + str(nb_artists_max)).pack(side=LEFT, padx=5)
        Button(root, text="Help", command=gui.help_me, width=10).pack(side=LEFT, padx=12, pady=20)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=20)
        Button(root, text="Next >", command=lambda: func.artist_to_script(spinbox.get()), width=10)\
            .pack(side=RIGHT, pady=20)
        Button(root, text="< Previous", command=gui.browse, width=10).pack(side=RIGHT, padx=12, pady=20)
        func.detect_choice()

    @staticmethod
    def end():
        for widget in root.winfo_children():
            widget.destroy()
        frame = tk.Frame(root, relief=GROOVE, borderwidth=4)
        text = Label(frame, text="""Thank you for using this software developed by Darkaird !

If you have suggestion(s) or bug(s), you can send an email at :
software.felosu@gmail.com

Click the link below to see if an update is available :
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
    def remove_garbage():  # Replace all bracket to avoid glob.glob empty list issue
        for element in glob.glob(source + "\\Songs\\*"):
            new_path_name = element.replace("[", "-BRACKET1-").replace("]", "-BRACKET2-")
            if new_path_name != element:  # If there not same, remove "[" and "]" to avoid glob.glob bug (list empty)
                os.rename(element, new_path_name)
            else:
                pass
        script()

    @staticmethod
    def detect_choice():
        global min_nb_occurrences
        directory_number = len(next(os.walk(destination_path))[1])
        file_number = len(next(os.walk(destination_path))[2])

        if directory_number == 0 and file_number > 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'No\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
        elif directory_number > 0 and file_number == 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes for all\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
        elif directory_number > 0 and file_number > 0:
            min_nb_occurrences = min([len(glob.glob(destination_path + '\\' + directories + '\\*')) for directories in
                                      next(os.walk(destination_path))[1]])
            spin_var.set(min_nb_occurrences)
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes but only from ' + str(min_nb_occurrences) +
                                                  ' occurrence(s)\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
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
        global artist_list
        artist_list_lower = []
        artist_list = []

        #   Work only on osu folder (avoid issues with "tutorial" and co)
        regex = re.compile(r"^[\d]+[\s](.)+-(.)+")
        osu_directories_list = [x for x in os.listdir(source + "\\Songs") if regex.search(x) is not None]

        #  Get all artist AND make all artist (with duplicates) in lowercase to avoid case issues
        #  AND
        #  Get all file music name like "artist - music name"
        for element in osu_directories_list:
            name_folder = element.split()
            del name_folder[0]
            artist_list_lower.append((" ".join(name_folder).split(" - ")[0]).lower())
            artist_list.append((" ".join(name_folder).split(" - ")[0]))
            artist_music.append(" ".join(name_folder))

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
            func.remove_garbage()

        #   Create folder for each artist
        elif radio_value.get() == 2:
            for artist in set(artist_list):
                #   Exception to avoid case problem again (like "lisa" and "LiSa")
                try:
                    os.mkdir(destination_path + '\\' + str(artist.lower().title()))
                    artist_folder.append(artist.lower().title())
                except FileExistsError:
                    pass
            func.remove_garbage()

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

            func.remove_garbage()

        #   Manual selection
        elif radio_value.get() == 4:
            showinfo("Coming Soon !", "This function will be implemented soon !")
            return None

    @staticmethod
    def copy_rename():  # Check if file not already present and if not copy and rename it
        artist_lower_title = artist_list[counter].lower().title().replace("-BRACKET1-", "[").replace("-BRACKET2-", "]")
        file_extension = glob_search.split(".")[-1]
        # Search if there is folder with artist_music's artist name, if not just copy it a folder_path root
        if artist_lower_title in artist_folder:
            if os.path.exists(destination_path + "\\" + artist_lower_title + "\\"
                              + artist_music[counter] + "." + file_extension) is not True:
                shutil.copy(glob_search,
                            destination_path + "\\" + artist_lower_title)
                os.rename(destination_path + "\\" + artist_lower_title + "\\" + glob_search.split("\\")[-1],
                          destination_path + "\\" + artist_lower_title + "\\"
                          + artist_music[counter] + "." + file_extension)

        else:
            if os.path.exists(destination_path + "\\" + artist_music[counter] + "." + file_extension) is not True:
                shutil.copy(glob_search,
                            destination_path)
                os.rename(destination_path + "\\" + glob_search.split("\\")[-1],
                          destination_path + "\\" + artist_music[counter] + "." + file_extension)

    @staticmethod
    def avoid_duplicates():
        flag = False
        for element in os.listdir(destination_path):
            try:
                for file in os.listdir(destination_path + '\\' + element):
                    if file.lower() == (artist_music[counter].lower() + '.' + file.lower().split('.')[-1]):
                        flag = True
                        break
                    else:
                        pass
            except NotADirectoryError:
                if element.lower() == (artist_music[counter].lower() + '.' + element.lower().split('.')[-1]):
                    flag = True
                    break
                else:
                    pass
        if flag is False:
            func.copy_rename()

    @staticmethod
    def script_to_end():
        # Replace Bracket
        for name_folder_src in os.listdir(source + "\\Songs\\"):
            name_folder_src_mod = name_folder_src.replace("-BRACKET1-", "[").replace("-BRACKET2-", "]")
            if name_folder_src != name_folder_src_mod:
                os.rename(source + "\\Songs\\" + name_folder_src, source + "\\Songs\\" + name_folder_src_mod)

        # Bug 775
        for file in next(os.walk(destination_path))[2]:
            if artist_dic.get(file.replace("-BRACKET1-", "[").replace("-BRACKET2-", "]").split(' - ')[0].lower()) \
                    >= int_spin_box_number:
                shutil.move(destination_path + '\\' + file, destination_path + '\\'
                            + file.split(' - ')[0].lower().title() + '\\' + file)

        # Check if number of file in directories < int_spin_box_number
        for directory in next(os.walk(destination_path))[1]:
            if len(os.listdir(destination_path + '\\' + directory)) < int_spin_box_number:
                for file in os.listdir(destination_path + '\\' + directory):
                    shutil.move(destination_path + '\\' + directory + '\\' + file, destination_path + '\\' + file)

        # Remove directories with 0 files
        for element in os.listdir(destination_path):
            if element.split('.')[-1] == "mp3" or element.split('.')[-1] == "ogg" \
                    or element.split('.')[-1] == "MP3" or element.split('.')[-1] == "OGG":
                pass
            else:
                if len(os.listdir(destination_path + '\\' + element)) == 0:
                    shutil.rmtree(destination_path + '\\' + element, ignore_errors=True)

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

    global counter, glob_search
    # SCRIPTING PART
    counter = 0
    not_allowed = []
    list_dir = glob.glob(source + "\\Songs\\*")

    #   Work only on osu folder (avoid issues with "tutorial" and co)
    regex = re.compile(r"^([0-9])+[\s](.)+")
    for element in list_dir:
        if regex.search(element.split('\\')[-1]) is not None:
            pass
        else:
            not_allowed.append(element)
    for element in not_allowed:
        list_dir.remove(element)

    for element in list_dir:
        percent = int(round((counter/len(list_dir))*100))
        for extension in ["*.mp3", "*.ogg", "*.m4a", ".mp3", ".ogg", ".m4a"]:
            if len(glob.glob(element + "\\" + extension)) == 0:
                pass
            else:
                glob_search = glob.glob(element + "\\" + extension)[0]
                func.avoid_duplicates()
                break

        counter += 1

        # TRAIN MOVEMENT
        var_int = ((326*counter)/len(list_dir))
        if ((326*counter)/len(list_dir)) <= 163:
            train_art.pack(side=LEFT, padx=var_int)
        else:
            train_art.pack(side=RIGHT, padx=326-var_int)

        # PRINTING INFORMATION
        loading.set(" ______________________________________________________________\n"
                    "|                                                              |\n"
                    "|              Script in progress : " + str(counter) + "/"
                    + str(len(list_dir)) + " (" + str(percent) + "%)"
                    + " " * (22 - (len(str(counter)) + len(str(len(list_dir))) + len(str(percent)))) + "|\n"
                    "|______________________________________________________________|")
        text_art.pack(side=TOP)
        root.update()
    func.script_to_end()

gui = GraphicalUserInterface()
func = Function()
gui.licence()
root.mainloop()
