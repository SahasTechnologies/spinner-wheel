# Spinner Wheel

Spinner wheel is an interactive python app for running wheels offline (first time has to be online though). Built with the Tkinter module in Python.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Hackatime](https://hackatime-badge.hackclub.com/U09QBEKG4S0/spinner-wheel)

## Features

### **1. Interactive Names List**
Add names with the 'Add' button, delete participants, delete all and scroll the list with this very nice GUI. I achieved this with Tkinter's `Listbox` widget with `Scrollbar` for ease of use. For the confirmation popups I used `messagebox.askyesno()`, especially for all the destructive actions like deleting everybody.

### **2. Spinny wheel**
I don't really think i have to explain this... but ok; The wheel spins with random totation and decelerates very nicely and resizes automatically with the window. I got this to work with Tkinter's `canvas`  thingy with `create_arc_` for wheen segments. THe animation uses `time.monotomic()` for timing with the frame rate, and the deceleration uses `1 - (1 - t)^3` (formula from ChatGPT)
oh right i better add an MIT license so that I dont get blamed if this stops working

### **3. Colours (or coloUrs if you are american)**
Sadly, I had to use colors without the u everywhere in my code since this python and all other languages like to use american engligh :C there should be a feature like `language = english.australian` yk
Anyway, I colour picked the colours from some random dreamstime image on google which look nice and poppy and are not so pastel that you can't see the white text (since I have tried with black text and it does not look good at all). I also made sure that no two touching colours will ever be the same and they will shuffle every time you generate a wheel. This includes wraparound so no two slices will have same colour. I did this with the `assign_random_colours()` function (ikr i suffered with these long variable names to make it easy for people to actually read the code but its probably still unreadable); this funciton filters out the previous colour when selecting the next colout, and shuffles again if the constraints cant be met for some reason (if your python decides to not like this code and bug out like mine did). Then the final check ensures that `colors[-1] != colors[0]` (see what i mean im not used to colors without u)

### **4. the font**
see... the arial font is not really that good (like it is, huge kudos to the person who made arial, its just... _so_ good that literally everything uses arial) so I used Red Hat Text Instead. I made sure this can work on Windows 11 but idk how to really do it on mac and the ai wont tell me either, so you just get to stick with arial sorry. I got the windows one to work with `urllib.request.urlretrieve()` to get it directly from the Red Hat GitHub repo (also so that if they ever update it for whatever reason this would too)

### ** 5. high dpi**
I dont know if this can be coutned as a feature, but if you are using Tkinter then yes definetly since it was so pixellated when I first started it up, now at least it is a bit better. On windows at least, I use `ctypes.windll.shcore.SetProcessDpiAwareness(1)` to get the resoluton of monitor

### **6. Winner Announcement**
A new popup appears with `show_winner()` whe nthe wheel spinning is done, I don't really know what else to say about this

## Installation
If you want to install it, just use the pypi package that I will send out in a bit (on test.pypi.org since i ont want to interfere with the real one)