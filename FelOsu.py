import glob
import shutil
import tempfile
from collections import Counter
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.ttk import *
import tkinter as tk
import webbrowser

# globsearch = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods\\Lost Woods.mp3"
# listdir = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods"
# dirlist = "10029 Koji Kondo - Lost Woods"
# artistmusic = "Koji Kondo - Lost Woods"
# artistlist = "Koji Kondo"
# artistlistlower = "koji kondo"
# artistdic = " 'nano': 9 "
# folderpath = "C:/Users/BW5442/Downloads/FelOsu/Nouveau dossier"

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

         - "Yes" will put all the musics with the same artist in the same folder (and the name's folder
         will be the artist's name). But even if there is only music for one artist, it will put it
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
_                   _                                              _                                                         _                                            _
 ))              (`  ).                   _                     (`  ).                   _                                (`  ).                   _                   (`  ).                        _                __
  (             (     ).              .:(`  )`.                (     ).              .:(`  )`.                           (     ).              .:(`  )`.              (     ).                   .:(`  )`.           (
__ )           _(       '`.          :(   .    )              _(       '`.          :(   .    )                         _(       '`.          :(   .    )            _(       '`.                :(   .    )        ((
           .=(`(      .   )     .--  `.  (    ) )         .=(`(      .   )     .--  `.  (    ) )                    .=(`(      .   )     .--  `.  (    ) )       .=(`(      .   )     .--        `.  (    ) )        (
_._          ((    (..__.:'-'   .+(   )   ` _`  ) )         ((    (..__.:'-'   .+(   )   ` _`  ) )                    ((    (..__.:'-'   .+(   )   ` _`  ) )       ((    (..__.:'-'   .+(   )          ` _`  ) )      '..
   `.     `(       ) )       (   .  )     (   )  ._      `(       ) )       (   .  )   (  (   )         ._          `(       ) )       (   .  )     (   )        `(    __ ) )       (   .  )         (   )          ._
     )      ` __.:'   )     (   (_  ))     `-'.-(`  )      ` __.:'   )     (   (   )) (    `-'.       -(`  )          ` __.:'   )     (   ( _))    ((   `-'.     -(`  )              ` __.:'         )   (       ( _)) (
   )  )  ( )       --'       `- __.'         :(      ))           ( )       --'       `- __.'      :(      ))           ( )            --'         `- __.'       :(    ))         ( )                (--'         `- __.'
___.-'  (_.'          .')                    `(    )  ))         (_.'          .')                 `(    )  ))         (_.'                                     `(    )  ))       (_.'
                  (_  )                     ` __.:'                        (_  )                  ` __.:'                                                      ` __.:'
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
artistmusic = []
artistfolder = []
browsetext1 = StringVar()
browsetext2 = StringVar()

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
            root.quit()
            root.destroy()
            sys.exit(0)

    @staticmethod
    def licence():
        for widget in root.winfo_children():
            widget.destroy()
        frame1 = tk.Frame(root, borderwidth=5, relief=RAISED)
        frame2 = tk.Frame(frame1, borderwidth=5, relief=SUNKEN)
        frame1.pack(pady=10, padx=5)
        frame2.pack(pady=15, padx=15)
        tk.Label(frame2, text=license_text, bg='white').pack(padx=1, pady=2)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=15)
        Button(root, text="Next >", command=gui.browse, width=10).pack(side=RIGHT, pady=15)
        root.protocol("WM_DELETE_WINDOW", gui.exit_func)

    @staticmethod
    def browse():
        for widget in root.winfo_children():
            widget.destroy()
        global entry1, entry2
        framebrowsewindowup = LabelFrame(root, text=" osu! folder ", relief=GROOVE)
        framebrowsewindowbottom = LabelFrame(root, text=" Destination folder ", relief=GROOVE)
        framebrowsewindowup.pack(side=TOP, padx=30, pady=8, fill="both", expand="yes")
        framebrowsewindowbottom.pack(side=TOP, padx=30, pady=5, fill="both", expand="yes")
        Label(framebrowsewindowup, text="""\nPlease, indicate osu! folder""").pack(side=TOP)
        Button(framebrowsewindowup, text="Browse...",
               command=func.get_source, width=9).pack(side=RIGHT, padx=12, pady=20)
        entry1 = Entry(framebrowsewindowup, textvariable=browsetext1, width=70)
        entry1.pack(side=RIGHT, padx=15)
        Label(framebrowsewindowbottom,
              text="""\nPlease, indicate the folder where you want the files to be copied in""").pack(side=TOP)
        Button(framebrowsewindowbottom, text="Browse...", width=9,
               command=func.get_destination_path).pack(side=RIGHT, padx=12, pady=20)
        entry2 = Entry(framebrowsewindowbottom, textvariable=browsetext2, width=70)
        entry2.pack(side=RIGHT, padx=15)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=20)
        Button(root, text="Next >", command=func.browse_to_artist, width=10).pack(side=RIGHT, pady=20)
        Button(root, text="< Previous", command=gui.licence, width=10).pack(side=RIGHT, padx=12, pady=20)

    @staticmethod
    # Help window in browse window to help people with proposed choices
    def help_me():
        helpwindow = tk.Tk()
        helpwindow.minsize(580, 200)
        helpwindow.maxsize(580, 200)
        Label(helpwindow, text=help_text).pack()

    @staticmethod
    def artist_choice():
        for widget in root.winfo_children():
            widget.destroy()
        global radiovalue, spinbox
        framebrowsewindowtext = Frame(root, relief=GROOVE)
        framebrowsewindow1 = Frame(root, relief=FLAT)
        framebrowsewindow2 = Frame(root, relief=FLAT)
        framebrowsewindow3 = Frame(root, relief=FLAT)
        framebrowsewindow4 = Frame(root, relief=FLAT)
        framebrowsewindowtext.pack(padx=60, pady=50, fill="both", expand="yes")
        framebrowsewindow1.pack(padx=60, pady=5, fill="both", expand="yes")
        framebrowsewindow2.pack(padx=60, pady=5, fill="both", expand="yes")
        framebrowsewindow3.pack(padx=60, pady=5, fill="both", expand="yes")
        framebrowsewindow4.pack(padx=60, pady=5, fill="both", expand="yes")
        Label(framebrowsewindowtext, text="""
        Do you want to sort by artist ? For more precision, click "Help" in the bottom-left corner""").pack()
        radiovalue = IntVar()
        button1 = Radiobutton(framebrowsewindow1, text="No", variable=radiovalue, value=1)
        button2 = Radiobutton(framebrowsewindow2, text="Yes for all", variable=radiovalue, value=2)
        button3 = Radiobutton(framebrowsewindow3, text="Yes, but only from : ", variable=radiovalue, value=3)
        button4 = Radiobutton(framebrowsewindow4, text="Yes, but only some artist I want to choose",
                              variable=radiovalue, value=4)
        button1.pack(side=LEFT), button2.pack(side=LEFT), button3.pack(side=LEFT), button4.pack(side=LEFT)
        spinbox = Spinbox(framebrowsewindow3, from_=1, to=nbartistsmax, width=8, textvariable=1)
        spinbox.pack(side=LEFT)
        Label(framebrowsewindow3, text=" max = " + str(nbartistsmax)).pack(side=LEFT, padx=5)
        Button(root, text="Help", command=gui.help_me, width=10).pack(side=LEFT, padx=12, pady=20)
        Button(root, text="Exit", command=gui.exit_func, width=10).pack(side=RIGHT, padx=12, pady=20)
        Button(root, text="Next >", command=func.artist_to_script, width=10).pack(side=RIGHT, pady=20)
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
        browsetext1.set(source)

    @staticmethod
    # Open window which asks destination folder
    def get_destination_path():
        global destinationpath
        destinationpath = askdirectory(title="Please, indicate the folder where you want the files to be copied in"
                                             " (To create a new folder, press right mouse button and choose "
                                             "'New folder')")
        browsetext2.set(destinationpath)

    @staticmethod
    def remove_garbage():  # Replace all bracket to avoid glob.glob empty list issue
        listdirbase = glob.glob(source + "\\Songs\\*")
        for element in listdirbase:
            newpathname = element.replace("[", "-BRACKET1-").replace("]", "-BRACKET2-")
            if newpathname != element:  # If there not same, remove "[" and "]" to avoid glob.glob bug (list empty)
                os.rename(element, newpathname)
            else:
                pass
        script()

    @staticmethod
    def detect_choice():
        summusic = 0
        for extension in ['*.mp3', '.mp3', '*.ogg', '.ogg']:
            summusic += len(glob.glob(destinationpath + '\\' + extension))

        if (len(os.listdir(destinationpath)) - summusic) == 0 and summusic > 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'No\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
        elif len(os.listdir(destinationpath)) > 0 and summusic == 0:
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes for all\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
        elif (len(os.listdir(destinationpath)) - summusic) > 0 and summusic > 0:
            minnbmusic = 10000
            destinationfiles = []
            for extension in ['*.mp3', '.mp3', '*.ogg', '.ogg']:
                for element in glob.glob(destinationpath + '\\' + extension):
                    destinationfiles.append(element)
            for path in glob.glob(destinationpath + '\\*'):
                if (path not in destinationfiles) and ((len(glob.glob(path + "\\*"))) < minnbmusic):
                    minnbmusic = len(glob.glob(path + '\\*'))
            showinfo('Previous Setting Detected', 'We detect that you have already used this software with this\n'
                                                  'destination folder and chose the setting :\n'
                                                  ' - \'Yes but only from ' + str(minnbmusic) + ' occurrence(s)\'.\n'
                                                  'To avoid duplicates, we recommend you to choose the same setting.')
        else:
            pass

    @staticmethod
    def browse_to_artist():
        # Avoid folder errors
        if len(browsetext1.get()) == 0 and len(browsetext2.get()) == 0:
            showwarning("ErrorEmptyFields", "You have to enter osu! and destination folder !")
            return None
        if len(browsetext2.get()) == 0:
            showwarning("ErrorEmptyDestination", "You have to enter a destination folder !")
            return None
        if (os.path.exists(source + "\\Songs") is not True) or (len(os.listdir(source + "\\Songs")) == 0):
            showwarning("ErrorOsuNotFound", "You must enter a valid osu! folder !")
            return None
        if os.path.exists(browsetext2.get()) is not True:
            showwarning("ErrorDestinationNotValid", "You must enter a valid destination folder !")
            return None
        if browsetext1.get() == browsetext2.get():
            showwarning("ErrorSamePaths", "You must enter a different folders !")
            return None

        # Get all artist AND make all artist in lowercase to avoid case issues
        global artistlist
        artistlistlower = []
        artistlist = []
        notallowed = []
        dirlist = os.listdir(source + "\\Songs")
        #   Work only on osu folder (avoid issues with "tutorial" and co)
        regex = re.compile(r"^[\d]+[\s](.)+-(.)+")
        for element in dirlist:
            if regex.search(element) is not None:
                pass
            else:
                notallowed.append(element)
        for element in notallowed:
            dirlist.remove(element)

        #  Get all artist AND make all artist (with duplicates) in lowercase to avoid case issues
        #  AND
        #  Get all file music name like "artist - music name"
        for element in dirlist:
            namefolder = element.split()
            del namefolder[0]
            artistlistlower.append((" ".join(namefolder).split(" - ")[0]).lower())
            artistlist.append((" ".join(namefolder).split(" - ")[0]))
            artistmusic.append(" ".join(namefolder))

        #  Count max occurence of artist and make artist list
        global artistdic, nbartistsmax
        artistdic = Counter(artistlistlower)
        try:
            nbartistsmax = artistdic[max(artistdic, key=artistdic.get)]
        except ValueError:
            showwarning("ErrorOsuNotFound", "You must enter a valid osu! folder !")
            return None
        gui.artist_choice()

    @staticmethod
    def artist_to_script():  # Called by Artist_window()

        # Check if at least one option is chosen
        if radiovalue.get() == 0:
            showwarning("ErrorNothingSelected", "You have to choose one option")
            return None

        # Radio button choice path
        #  Do nothing with artist
        if radiovalue.get() == 1:
            func.remove_garbage()

        #   Create folder for each artist
        elif radiovalue.get() == 2:
            for artist in set(artistlist):
                #   Exception to avoid case problem again (like "lisa" and "LiSa")
                try:
                    os.mkdir(destinationpath + '\\' + str(artist.lower().capitalize()))
                    artistfolder.append(artist.lower().capitalize())
                except FileExistsError:
                    pass
            func.remove_garbage()

        #   Create folder from given value
        elif radiovalue.get() == 3:
            # Check if spin number is valuable
            try:
                int(spinbox.get())
                if int(spinbox.get()) < 1 or int(spinbox.get()) > nbartistsmax:
                    showwarning("ErrorSpinNumber", "You have to choose a number between 1 and " + str(nbartistsmax))
                    return None
            except ValueError:
                showwarning("ErrorSpinNumber", "You have to choose a number between 1 and " + str(nbartistsmax))
                return None

            for artist in set(artistlist):
                if artistdic.get(artist.lower()) >= int(spinbox.get()):
                    #   Exception to avoid case problem again (like "lisa" and "LiSa")
                    try:
                        os.mkdir(destinationpath + '\\' + str(artist.lower().capitalize()))
                        artistfolder.append(artist.lower().capitalize())
                    except FileExistsError:
                        pass
            func.remove_garbage()

        #   Manual selection
        elif radiovalue.get() == 4:
            showinfo("Coming Soon !", "This function will be implemented soon !")
            return None

    @staticmethod
    def mkdir_copy_rename():  # Check if file not already present and if not copy and rename it
        artistlowercapitalize = artistlist[counter].lower().capitalize()
        fileextension = globsearch.split(".")[-1]
        # Search if there is folder with artistmusic's artist name, if not just copy it a folderpath root
        if artistlowercapitalize in artistfolder:
            if os.path.exists(destinationpath + "\\" + artistlowercapitalize + "\\"
                              + artistmusic[counter] + "." + fileextension) is not True:
                shutil.copy(globsearch,
                            destinationpath + "\\" + artistlowercapitalize)
                os.rename(destinationpath + "\\" + artistlowercapitalize + "\\" + globsearch.split("\\")[-1],
                          destinationpath + "\\" + artistlowercapitalize + "\\"
                          + artistmusic[counter] + "." + fileextension)

        else:
            if os.path.exists(destinationpath + "\\" + artistmusic[counter] + "." + fileextension) is not True:
                shutil.copy(globsearch,
                            destinationpath)
                os.rename(destinationpath + "\\" + globsearch.split("\\")[-1],
                          destinationpath + "\\" + artistmusic[counter] + "." + fileextension)

    @staticmethod
    def avoid_duplicates():
        flag = False
        for element in os.listdir(destinationpath):
            noextension = element.split(".")
            del noextension[-1]
            if (element.split(".")[-1] == "mp3" or element.split(".")[-1] == "ogg") and noextension[0] == artistmusic[counter]:
                flag = True
                break
            else:
                if element.split(".")[-1] == "mp3" or element.split(".")[-1] == "ogg" and noextension[0] != artistmusic[counter]:
                    pass
                else:
                    for file in element:
                        if file == artistmusic[counter]:
                            flag = True
                            break
                        else:
                            pass
        if flag is False:
            func.mkdir_copy_rename()

    @staticmethod
    def script_to_end():
        for namefoldersrc in os.listdir(source + "\\Songs\\"):
            namefoldersrcmod = namefoldersrc.replace("-BRACKET1-", "[").replace("-BRACKET2-", "]")
            if namefoldersrc != namefoldersrcmod:
                os.rename(source + "\\Songs\\" + namefoldersrc, source + "\\Songs\\" + namefoldersrcmod)
        for element in os.listdir(destinationpath):
            if element.split('.')[-1] == "mp3" or element.split('.')[-1] == "ogg":
                pass
            else:
                if len(os.listdir(destinationpath + '\\' + element)) == 0:
                    shutil.rmtree(destinationpath + '\\' + element, ignore_errors=True)
        gui.end()


def script():
    # GRAPHICAL PART
    for widget in root.winfo_children():
        widget.destroy()
    loading = StringVar()
    moutainframe = Frame(root, relief=FLAT)
    trainframe = Frame(root, relief=FLAT)
    cloudart = Label(moutainframe, text=cloud_text, font='bold')
    textart = Label(moutainframe, font='bold', textvariable=loading)
    moutainart = Label(moutainframe, text=mountain_text, font='bold', anchor='s')
    trainart = Label(trainframe, text=train_text, font='bold')
    railart = Label(trainframe, text=rail_text, font='bold')

    # Configuration
    cloudart.configure(font=("Courier", 4))
    textart.configure(font=("Courier", 9))
    moutainart.configure(font=("Courier", 8))
    trainart.configure(font=("Courier", 5))
    railart.configure(font=("Courier", 7))

    # Pack
    moutainframe.pack(fill=BOTH, expand=TRUE, side=TOP)
    trainframe.pack(fill=BOTH, expand=TRUE, side=BOTTOM)
    cloudart.pack(side=TOP)
    moutainart.pack(side=BOTTOM)
    railart.pack(side=BOTTOM)

    global counter, globsearch
    # SCRIPTING PART
    counter = 0
    notallowed = []
    listdir = glob.glob(source + "\\Songs\\*")

    #   Work only on osu folder (avoid issues with "tutorial" and co)
    regex = re.compile(r"^([0-9])+[\s](.)+")
    for element in listdir:
        if regex.search(element.split('\\')[-1]) is not None:
            pass
        else:
            notallowed.append(element)
    for element in notallowed:
        listdir.remove(element)

    for element in listdir:
        percent = int((counter/len(listdir))*100)
        for extension in ["*.mp3", "*.ogg", "*.m4a", ".mp3", ".ogg", ".m4a"]:
            if len(glob.glob(element + "\\" + extension)) == 0:
                pass
            else:
                globsearch = glob.glob(element + "\\" + extension)[0]
                func.avoid_duplicates()
                break

        counter += 1

        # TRAIN MOVEMENT
        varint = ((326*counter)/len(listdir))
        if ((326*counter)/len(listdir)) <= 163:
            trainart.pack(side=LEFT, padx=varint)
        else:
            trainart.pack(side=RIGHT, padx=326-varint)

        # PRINTING INFORMATIONQ
        loading.set(" ______________________________________________________________\n"
                    "|                                                              |\n"
                    "|              Script in progress : " + str(counter) + "/"
                    + str(len(listdir)) + " (" + str(percent) + "%)"
                    + " " * (22 - (len(str(counter)) + len(str(len(listdir))) + len(str(percent)))) + "|\n"
                    "|______________________________________________________________|")
        textart.pack(side=TOP)
        root.update()
    func.script_to_end()

gui = GraphicalUserInterface()
func = Function()
gui.licence()
root.mainloop()
