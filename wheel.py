import math
import random
import time
import tkinter as tk
from tkinter import ttk


_PALETTE = [
    "#fc26a3", "#fd566e", "#fd9653", "#bdf159", "#6ef062",
    "#24efc2", "#26ccfa", "#4690fb", "#3c68eb", "#433dba",
]


def _assign_random_colors(count: int) -> list[str]:
    if count <= 0:
        return []

    if count==1:
        return [random.choice(_PALETTE)]

    colors = []
    available = _PALETTE
    random.shuffle(available)


    colors: list[str] = []
    first: str | None = None

    for i in range(count):
        prev = colors[-1] if colors else None
        choices = [c for c in available if c != prev]

        if not choices:
        #reshuffle if for some random reason the thing decides not to work
            available = _PALETTE[:]
            random.shuffle(available)
            choices = [c for c in available if c != prev]

        colors.append(random.choice(choices))




    
    if colors[-1] == colors[0]:
        for c in available:
            if c != colors[0] and c != colors[-2]:
                colors[-1] = c
                break

    return colors


class WheelPopup:
    def __init__(self, parent: tk.Misc, names: list[str]):
        self.names = [str(n) for n in names]
        self.colors = _assign_random_colors(len(self.names))
        self.rotation = 0.0#0000000000000000000000000000000000000 idk i crashed out then just asked chat (gpt) to fix it
        self.is_spinning = False
        self._spin_start_ts = 0.0
        self._spin_duration_s = 0.0
        self._spin_start_rotation = 0.0
        self._spin_total_degrees = 0.0
        self.popup = tk.Toplevel(parent)
        self.popup.title("Wheel")
        self.popup.geometry("700x750")
        self.popup.transient(parent)
        self.popup.grab_set()
        self.root = ttk.Frame(self.popup, padding= 16
        )
        self.root.pack (fill  = tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.root, highlightthickness = 0) # i regret naming it so long
        self.canvas.pack(fill = tk.BOTH, expand =True)

        spin_frame = ttk.Frame(self.root)
        spin_frame.pack(fill=tk.BOTH, expand = True)
        self.spin_btn = ttk.Button(spin_frame, text = "SPIN!", command = self._start_spin)
        self.spin_btn.pack(fill=tk.X, ipady = 8)

        btns=  ttk.Frame(self.root)
        btns.pack(fill= tk.X, pady=(10,0))
        ttk.Button(btns, text="Close", command = self.popup.destroy).pack(side = tk.RIGHT)

        self.popup.bind("<Configure>", lambda _e: self._draw())
        self.popup.after(0, self._draw)

    def _draw(self):
        self.canvas.delete("all")
        if not self.names:
            return

        w = max(self.canvas.winfo_width(), 1)
        h = max(self.canvas.winfo_height(), 1)

        size = min(w, h - 50)
        pad = max(int(size * 0.06), 12)
        r = (size / 2) - pad
        cx = w / 2
        cy = (h - 50) / 2
        bbox = (cx - r, cy - r, cx + r, cy + r)

        n = len(self.names)
        extent = 360.0 / n

        for i, color in enumerate(self.colors):
            start_angle = 90 - self.rotation - (i * extent)

            self.canvas.create_arc(
                bbox,
                start=start_angle,
                extent=-extent,
                fill=color,
                outline=""
            )

            label_angle = start_angle - (extent / 2)
            rad = math.radians(label_angle)
            tx = cx + (r * 0.6) * math.cos(rad)
            ty = cy - (r * 0.6) * math.sin(rad)

            self.canvas.create_text(
                tx, ty,
                text=self.names[i],
                font=("Red Hat Text", max(int(size * 0.035), 8), "bold"),
                angle=label_angle
            )

        #da pointer
    # i need to add this to not get lost in this AAAARGH code
    # idk why i selected python honestly at this point javascript woudl probably be easier
        pin_w = max(int(size * 0.04), 14)
        pin_h = max(int(size * 0.06), 22)
        py = cy - r

        self.canvas.create_polygon(
            cx, py,
            cx - (pin_w / 2), py - pin_h,
            cx + (pin_w / 2), py - pin_h,
            fill="black" #TODO: change to black if too hard to see
        )

    #WINNER! (this took SO long to code by myself)
    # this was so ragebait that i quit and ask five different ais and each one made it worse
    # so i had to paste from claude opus (i found 1 free chat / month somewhere on google) to tell me whats wrong
    def _winner_index(self) -> int:
        n = len(self.names)
        extent = 360.0 / n
        pointer_angle = 90.0 - 0.0001  # avoid boundary

        for i in range(n):
            start = (90 - self.rotation - i * extent) % 360
            end = (start - extent) % 360

            if start >= end:
                if end <= pointer_angle <= start:
                    return i
            else:
                if pointer_angle >= end or pointer_angle <= start:
                    return i

        return 0

    # ---------------- SPIN ----------------

    def _start_spin(self):
        if self.is_spinning or not self.names:
            return

        self.is_spinning = True
        self.spin_btn.config(state="disabled")

        self._spin_start_rotation = self.rotation % 360
        self._spin_total_degrees = random.randint(8, 12) * 360 + random.uniform(0, 360)
        self._spin_duration_s = 5.0
        self._spin_start_ts = time.monotonic()

        self._animate_spin()

    def _animate_spin(self):
        elapsed = time.monotonic() - self._spin_start_ts
        t = min(1.0, elapsed / self._spin_duration_s)

        eased = 1 - (1 - t) ** 3
        self.rotation = (self._spin_start_rotation + self._spin_total_degrees * eased) % 360

        self._draw()

        if t < 1.0:
            self.popup.after(16, self._animate_spin)
        else:
            self.is_spinning = False
            self.spin_btn.config(state="normal")
            self._show_winner()

    # ---------------- WINNER POPUP ----------------

    def _show_winner(self):
        idx = self._winner_index()
        winner = self.names[idx]
        color = self.colors[idx]

        win_popup = tk.Toplevel(self.popup)
        win_popup.title("Winner!")
        win_popup.geometry("500x400")
        win_popup.configure(bg=color)
        win_popup.grab_set()

        frame = tk.Frame(win_popup, bg=color)
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        tk.Label(
            frame,
            text=winner,
            font=("Red Hat Text", 48, "bold"),
            fg="white",
            bg=color
        ).pack(expand=True)

        tk.Label(
            frame,
            text="WINS!",
            font=("Red Hat Text", 32, "bold"),
            fg="white",
            bg=color
        ).pack()

        ttk.Button(frame, text="OK", command=win_popup.destroy).pack(pady=20)


def show_popup(parent: tk.Misc, names: list[str]):
    return WheelPopup(parent, names).popup
