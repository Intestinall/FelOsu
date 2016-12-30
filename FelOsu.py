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
from tinytag import TinyTag
import binascii

# music_file_path = "C:/Users/BW5442/Downloads/osu\\Songs\\10029 Koji Kondo - Lost Woods\\Lost Woods.mp3"
# list_dir = "C:/Users/BW5442/Downloads/FelOsu\\Songs\\10029 Koji Kondo - Lost Woods"
# artist_music = "Koji Kondo - Lost Woods"
# artist_list = "Koji Kondo"
# artist_list_lower = "koji kondo"
# artist_dic = " 'nano': 9 "
# folder_path = "C:/Users/BW5442/Downloads/FelOsu/Nouveau dossier"

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
  oo    oo ' oo     oo ' oo    oo '  oo    oo ' oo     oo ' oo    oo ' oo 000---oo\_"""

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


class GraphicalUserInterface:

    def __init__(self):
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
        root.iconbitmap(create_icon(iconhexdata))

        try:
            if "00000000001400" not in urllib.request.urlopen("https://osu.ppy.sh/forum/t/520493").read().decode("utf-8"):
                if askyesno("Update Available !", "An update is available,\ndo you want to download it ?"):
                    webbrowser.open("https://osu.ppy.sh/forum/t/520493")
        except:
            pass



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
        # BRACKET Remove
        for file in next(os.walk(destination_path))[2]:
            try:
                os.rename(destination_path + "\\" + file,
                          destination_path + "\\" + file.replace("-BRACKET1-", "[").replace("-BRACKET2-", "]"))
            except FileNotFoundError:
                pass
            except FileExistsError:
                os.remove(destination_path + "\\" + file)

        for directory in next(os.walk(destination_path))[1]:
            for file in directory:
                try:
                    os.rename(destination_path + "\\" + directory + "\\" + file,
                              destination_path + "\\" + directory + "\\"
                              + file.replace("-BRACKET1-", "[").replace("-BRACKET2-", "]"))
                except FileNotFoundError:
                    pass
                except FileExistsError:
                    os.remove(destination_path + "\\" + directory + "\\" + file)

        directory_path_view = next(os.walk(destination_path))

        # Bug 775
        if radio_value.get() == 2 or radio_value.get() == 3:
            for file in directory_path_view[2]:
                try:
                    if artist_dic.get(file.split(' - ')[0].lower()) >= int_spin_box_number:
                            move(destination_path + '\\' + file,
                                 destination_path + '\\' + file.split(' - ')[0].lower().title() + '\\' + file)
                except TypeError:
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
    regex = re.compile(r"[0-9]+\s(.)+\s-\s(.)+")

    list_dir = [x for x in next(os.walk(source + '\\Songs'))[1] if regex.search(x) is not None]
    len_list_dir = len(list_dir)

    for directory in list_dir:
        flag = False
        percent = round((loop_counter/len_list_dir)*100)

        for file in os.listdir(source + '\\Songs\\' + directory):
            if flag is True:
                break
            for extension_type in ['.mp3', '.MP3', '.ogg', '.OGG', '.m4a', '.M4A']:
                if file.endswith(extension_type):
                    music_file_path = source + '\\Songs\\' + directory + '\\' + file
                    if extension_type in [".ogg", ".OGG"]\
                            and TinyTag.get(music_file_path).duration < 30:
                        continue
                    if func.avoid_duplicates(loop_counter) is False:
                        func.copy_rename(music_file_path, loop_counter)
                        flag = True
                        break

        loop_counter += 1

        # TRAIN MOVEMENT
        var_int = ((326*loop_counter)/len_list_dir)
        if var_int <= 163:
            train_art.pack(side=LEFT, padx=var_int)
        else:
            train_art.pack(side=RIGHT, padx=326 - var_int)

        # PRINTING INFORMATION
        loading.set(" ______________________________________________________________\n"
                    "|                                                              |\n"
                    "|              Script in progress : " + str(loop_counter) + "/"
                    + str(len_list_dir) + " (" + str(percent) + "%)"
                    + " " * (22 - (len(str(loop_counter)) + len(str(len_list_dir)) + len(str(percent)))) + "|\n"
                    "|______________________________________________________________|")
        text_art.pack(side=TOP)
        root.update()
    func.script_to_end()

gui = GraphicalUserInterface()
func = Function()
gui.licence()
root.mainloop()
