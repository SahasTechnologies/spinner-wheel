import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import os
import ctypes
import sys


if sys.platform == "win32":
    try:
        if hasattr(ctypes, 'windll'):
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

FONT_URL = "https://raw.githubusercontent.com/RedHatOfficial/RedHatFont/master/fonts/Proportional/RedHatText/variable/RedHatTextVF.ttf"
FONT_PATH = "RedHatTextVF.ttf"

def ensure_font():
    if not os.path.exists(FONT_PATH):
        try:
            urllib.request.urlretrieve(FONT_URL, FONT_PATH)
        except Exception as e:
            print(f"Font download failed: {e}")
            return False
            
    if sys.platform == "win32" and hasattr(ctypes, 'windll'):
        try:
            ctypes.windll.gdi32.AddFontResourceW(os.path.abspath(FONT_PATH))
        except Exception:
            pass
    return True

#impor tthe other fiel
try:
    import wheel
except ImportError:
    wheel = None

class SpinnerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Spin the Wheel")
        self.geometry("800x600")
        self.config(padx=30, pady=30)
        
        # Load 
        font_family = "Red Hat Text" if ensure_font() else "Arial"

        title_lbl = ttk.Label(self, text="Participant List", font=(font_family, 24, "bold"))
        title_lbl.pack(pady=(0, 20))

        inp_frame = ttk.Frame(self)
        inp_frame.pack(fill=tk.X, pady=10)

        self.entry = ttk.Entry(inp_frame, font=(font_family, 14))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 15))
        self.entry.bind("<Return>", lambda e: self.add())

        btn_add = ttk.Button(inp_frame, text="Add", command=self.add)
        btn_add.pack(side=tk.RIGHT)
        spin_frame = ttk.Frame(self)
        spin_frame.pack(side=tk.BOTTOM,fill = tk.X, pady=(20,0))
        btn_spin = ttk.Button(spin_frame, text="SPIN THE WHEEL!", command=self.spin)
        btn_spin.pack(fill = tk.X, expand=True, ipady=10)

        act_frame = ttk.Frame(self)
        act_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        btn_delete=ttk.Button(act_frame, text="Delete Selected", command = self.delete_item)
        btn_delete.pack(side=tk.LEFT, fill = tk.X, expand = True, padx = (0, 5))
        btn_nuke = ttk.Button(act_frame, text = "Delete All", command = self.nuke)
        btn_nuke.pack(side = tk.RIGHT, fill = tk.X, expand = True, padx=(5,0))

        lst_frame = ttk.Frame(self)
        lst_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        bar = ttk.Scrollbar(lst_frame)
        bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.namesbox = tk.Listbox(lst_frame, font=(font_family, 14), selectmode=tk.SINGLE, 
                                    yscrollcommand=bar.set, activestyle="none")
        self.namesbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bar.config(command=self.namesbox.yview)

    def add(self):
        val = self.entry.get().strip()
        if not val:
            messagebox.showwarning("Oops", "Type something first.")
            return
            
        self.namesbox.insert(tk.END, val)
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def delete_item(self):
        sel = self.namesbox.curselection()
        if not sel:
            messagebox.showwarning("Oops", "Select someone to delete.")
            return
        self.namesbox.delete(sel[0])
            
    def nuke(self):
        if messagebox.askyesno("Wait", "Nuke the whole list?"):
            self.namesbox.delete(0, tk.END)

    def spin(self):
        names = self.namesbox.get(0, tk.END)
        if not names:
            messagebox.showwarning("Oops", "Please add some names before spinning!")
            return
        if wheel is None:
            messagebox.showerror("Error", "Could not load the wheel module.")
            return
            
        # launchit
        wheel.show_popup(self, list(names))

def main():
    app = SpinnerApp()
    app.mainloop()

if __name__ == '__main__':
    main()
