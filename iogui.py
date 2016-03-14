from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def pickfiles(name=None):
    root = Tk()
    root.withdraw()
    if name is None:
        filename = filedialog.askopenfilenames(parent=root,
                                               title="Choose DVHs ")
    else:
        filename = filedialog.askopenfilenames(parent=root, title=name)
    filename = list(filename)
    return filename


def pickdirectory():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(parent=root,
                                     title="Choose output directory")
    return folder
