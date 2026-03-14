import tkinter as tk
from tkinter import ttk


_PALETTE = [
    "#fc26a3",
    "#fd566e",
    "#fd9653",
    "#bdf159",
    "#6ef062",
    "#24efc2",
    "#26ccfa",
    "#4690fb",
    "#3c68eb",
    "#433dba",
]

def _assign_colors(count: int) -> list[str]:
    if count <= 0:
        return []

    if count==1:
        return [_PALETTE[0]]

    colors: list[str] = []
    first: str | None = None

    for i in range(count):
        prev = colors[-1] if colors else None
        candidates = [_PALETTE[i % len(_PALETTE)]] + _PALETTE

        for c in candidates:
            if c == prev:
                continue
            if i == count - 1 and first is not None and c == first:
                continue

            colors.append(c)
            if first is None:
                first = c
            break
        else:
            colors.append(_PALETTE[0])

    return colors

def _draw_wheel(canvas: tk.Canvas, names: list[str], colors: list[str]) -> None:
    canvas.delete("all")
    if not names:
        return

    w = max(canvas.winfo_width(), 1)
    h = max(canvas.winfo_height(), 1)
    size = min(w, h)

    pad = max(int(size * 0.06), 12)
    r = (size/ 2) - pad
    cx = w/2
    cy = h/2

    bbox = (cx - r, cy - r, cx + r, cy + r)

    n = len(names)
    extent = 360/n
    start = 90

    font_family = "Red Hat Text"
    font_size = max(int(size * 0.035), 10)

    for i, name in enumerate(names):
        seg_start = start - (i * extent)
        canvas.create_arc(
            bbox,
            start = seg_start,
            extent = -extent,
            fill = colors[i],
            outline = "",
        )

        if n ==1 :
            label_deg = 90
            text_angle = 270
        
        else:
            step = 360/(n * 2) #calc angle
            label_deg= (2*i+1) * step
            text_angle = label_deg

        label_rad = math.radians(label_deg)
        tx = cx + (r * 0.62) * math.cos(label_rad)
        ty = cy - (r * 0.62) * math.sin(label_rad)
        #bro i just came back fro mtuition i dont ened sin cos tan

        canvas.create_text(
            tx,
            ty,
            text=str(name),
            fill="white",
            font=(font_family, font_size, "bold"),
            width = int(r * 0.85),
            justify="center",
            angle = text_angle
        )

    pin_w = max(int(size * 0.04), 14)
    pin_h = max(int(size * 0.06), 22)
    px = cx + r + (pad * 0.2)
    py = cy

    canvas.create_polygon(
        px,
        py,
        px + pin_w,
        py - (pin_h /2),
        px + pin_w,
        py + (pin_h / 2),
        fill="black",
        outline="black",
    )

def _debounced_redraw(popup: tk.Toplevel, canvas: tk.Canvas, names:list[str], colors: list[str]) -> None:
    after_id = getattr(popup, "_wheel_after_id", None )

    if after_id is not None and after_id != "":
        try:
            popup.after_canvel(after_id)
        except Exception:
            pass
    
    def _do() -> None:
        _draw_wheel(canvas, names, colors)

    popup._wheel_after_id = popup.after(50, _do)



def show_popup(parent: tk.Misc, names: list[str]) -> tk.TopLevel:
    popup = tk.TopLevel(parent)
    popup.title("Wheel")
    popup.geometry("700x700")
    popup.transient(parent)
    popup.grab_set()

    root = ttk.Frame(popup, padding=16)
    root.pack(fill=tk.BOTH, expand = True)
    colors = _assign_colors(len(names))
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    popup.bind(
        "<Configure>",
        lambda _e: _debounced_redraw(popup, canvas, names, colors),


    )
    popup.after(0, lambda: _draw_wheel(canvas, names, colors))
    
    btns = ttk.Frame(root)
    btns.pack(fill=tk.X, pady=(12, 0))

    close_btn = ttk.Button(btns, text="Close", command=popup.destroy)
    close_btn.pack(side=tk.RIGHT)

    popup.wait_visibility()
    popup.focus_set()
    return popup