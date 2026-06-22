import math, random
from PIL import Image, ImageDraw, ImageFont

random.seed(7)

MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
MONO2 = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
SANS  = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
SANS2 = "/usr/share/fonts/truetype/google-fonts/Poppins-SemiBold.ttf" if False else SANS

def font(path, size):
    return ImageFont.truetype(path, size)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

def save_gif(frames, name, duration=40, loop=0):
    path = f"/home/claude/gifs/{name}.gif"
    frames[0].save(path, save_all=True, append_images=frames[1:],
                    duration=duration, loop=loop, disposal=2)
    print("saved", path)

# ---------- 1. Animated gradient wave banner with title ----------
def make_01_wave_banner():
    W, H = 900, 200
    n_frames = 60
    frames = []
    title = "WELCOME TO MY PROFILE"
    f_title = font(SANS, 46)
    c1 = (88, 28, 217)
    c2 = (236, 64, 122)
    for i in range(n_frames):
        t = i / n_frames
        img = Image.new("RGB", (W, H), (15, 12, 30))
        d = ImageDraw.Draw(img)
        # gradient background shifting
        for x in range(0, W, 4):
            tt = (x / W + t) % 1.0
            col = lerp_color(c1, c2, (math.sin(tt * math.pi * 2) + 1) / 2)
            d.rectangle([x, 0, x + 4, H], fill=col)
        # wave at bottom
        wave_pts = [(0, H)]
        for x in range(0, W + 10, 10):
            y = H - 30 - 18 * math.sin((x / 60.0) + t * 2 * math.pi)
            wave_pts.append((x, y))
        wave_pts.append((W, H))
        d.polygon(wave_pts, fill=(15, 12, 30))
        # title text with gentle bob
        bob = 6 * math.sin(t * 2 * math.pi)
        bbox = d.textbbox((0, 0), title, font=f_title)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        d.text(((W - tw) / 2, (H - th) / 2 - 20 + bob), title, font=f_title, fill=(255, 255, 255))
        frames.append(img)
    save_gif(frames, "01_wave_banner", duration=45)

# ---------- 2. Typing text effect ----------
def make_02_typing_effect():
    W, H = 760, 130
    full = "console.log('Hello World, I am a Developer!');"
    f = font(MONO, 28)
    frames = []
    hold_end = 18
    n_type = len(full)
    total = n_type + hold_end + 10
    for i in range(total):
        img = Image.new("RGB", (W, H), (13, 17, 23))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([10, 10, W - 10, H - 10], radius=14, outline=(56, 139, 253), width=2)
        chars = min(i, n_type)
        text = full[:chars]
        cursor_on = (i // 6) % 2 == 0
        bbox = d.textbbox((0, 0), text, font=f)
        d.text((30, H / 2 - 18), text, font=f, fill=(126, 231, 135))
        cx = 30 + (bbox[2] - bbox[0])
        if cursor_on:
            d.rectangle([cx + 4, H / 2 - 16, cx + 14, H / 2 + 16], fill=(126, 231, 135))
        frames.append(img)
    save_gif(frames, "02_typing_effect", duration=70)

# ---------- 3. Animated skill progress bars ----------
def make_03_skill_bars():
    W, H = 760, 320
    skills = [("Python", 0.92, (56,139,253)), ("JavaScript", 0.85, (240,219,79)),
              ("React", 0.80, (97,218,251)), ("Docker", 0.75, (13,183,242))]
    f_label = font(SANS, 20)
    f_pct = font(MONO, 18)
    n_frames = 50
    frames = []
    for i in range(n_frames):
        t = min(1.0, i / (n_frames - 12))
        ease = 1 - (1 - t) ** 3
        img = Image.new("RGB", (W, H), (13, 17, 23))
        d = ImageDraw.Draw(img)
        y = 30
        for label, pct, color in skills:
            d.text((30, y), label, font=f_label, fill=(230, 230, 230))
            bar_x, bar_w, bar_h = 230, 460, 22
            d.rounded_rectangle([bar_x, y+2, bar_x+bar_w, y+2+bar_h], radius=11, fill=(40, 44, 52))
            cur = pct * ease
            d.rounded_rectangle([bar_x, y+2, bar_x + bar_w*cur, y+2+bar_h], radius=11, fill=color)
            d.text((bar_x+bar_w+12, y), f"{int(cur*100)}%", font=f_pct, fill=color)
            y += 70
        frames.append(img)
    for _ in range(15):
        frames.append(frames[-1])
    save_gif(frames, "03_skill_bars", duration=40)

# ---------- 4. Snake eating contribution squares ----------
def make_04_snake_contributions():
    cell = 18
    cols, rows = 30, 8
    W, H = cols*cell+20, rows*cell+20
    levels = [[random.choice([0,0,1,1,2,2,3,4]) for _ in range(cols)] for _ in range(rows)]
    palette = [(22,27,34), (14,68,41), (0,109,50), (38,166,65), (57,211,83)]
    path = []
    for r in range(rows):
        rng = range(cols) if r % 2 == 0 else range(cols-1, -1, -1)
        for c in rng:
            path.append((r, c))
    frames = []
    eaten = set()
    for i, pos in enumerate(path):
        eaten.add(pos)
        img = Image.new("RGB", (W, H), (13, 17, 23))
        d = ImageDraw.Draw(img)
        for r in range(rows):
            for c in range(cols):
                lvl = 0 if (r, c) in eaten else levels[r][c]
                x0, y0 = 10 + c*cell, 10 + r*cell
                d.rounded_rectangle([x0, y0, x0+cell-3, y0+cell-3], radius=3, fill=palette[lvl])
        # draw snake head
        r, c = pos
        x0, y0 = 10 + c*cell, 10 + r*cell
        d.rounded_rectangle([x0, y0, x0+cell-3, y0+cell-3], radius=4, fill=(255,255,255), outline=(57,211,83), width=2)
        frames.append(img)
    for _ in range(10):
        frames.append(frames[-1])
    save_gif(frames, "04_snake_contributions", duration=35)

# ---------- 5. Terminal boot sequence ----------
def make_05_terminal_boot():
    W, H = 760, 260
    lines = [
        "$ whoami",
        "developer",
        "$ cat skills.txt",
        "Python | JS | Go | Rust",
        "$ status --check",
        "[OK] All systems ready"
    ]
    f = font(MONO2, 20)
    frames = []
    rendered = []
    for line in lines:
        for k in range(0, len(line)+1, 1):
            rendered_copy = rendered + [line[:k]]
            for _ in range(2):
                frames.append(rendered_copy)
        rendered.append(line)
        for _ in range(6):
            frames.append(rendered.copy())

    def draw(rendered_lines, cursor_on):
        img = Image.new("RGB", (W, H), (1, 5, 10))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([8, 8, W-8, H-8], radius=12, outline=(46, 204, 113), width=2)
        y = 30
        for ln in rendered_lines:
            color = (46, 204, 113) if ln.startswith("$") else (180, 220, 200)
            d.text((28, y), ln, font=f, fill=color)
            y += 32
        if cursor_on:
            d.rectangle([28, y, 40, y+22], fill=(46, 204, 113))
        return img

    out = []
    for i, rl in enumerate(frames):
        out.append(draw(rl, (i // 5) % 2 == 0))
    for _ in range(12):
        out.append(out[-1])
    save_gif(out, "05_terminal_boot", duration=55)

# ---------- 6. Neon glow pulsing name tag ----------
def make_06_neon_glow_name():
    W, H = 700, 180
    text = "YOUR NAME"
    f = font(SANS, 54)
    n_frames = 40
    frames = []
    base = (10, 8, 20)
    glow_color = (0, 255, 200)
    for i in range(n_frames):
        t = i / n_frames
        glow = (math.sin(t*2*math.pi) + 1) / 2  # 0..1
        img = Image.new("RGB", (W, H), base)
        d = ImageDraw.Draw(img)
        bbox = d.textbbox((0,0), text, font=f)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        cx, cy = (W-tw)/2, (H-th)/2 - 10
        # layered glow via blurred-looking offset strokes
        layers = [(14, 0.15), (9, 0.25), (5, 0.4), (2, 0.7)]
        for radius, alpha in layers:
            a = alpha * (0.5 + 0.5*glow)
            col = lerp_color(base, glow_color, a)
            for dx in range(-radius, radius+1, max(1, radius//2)):
                for dy in range(-radius, radius+1, max(1, radius//2)):
                    if dx*dx+dy*dy <= radius*radius:
                        d.text((cx+dx, cy+dy), text, font=f, fill=col)
        d.text((cx, cy), text, font=f, fill=(255,255,255))
        frames.append(img)
    save_gif(frames, "06_neon_glow_name", duration=50)

# ---------- 7. Bouncing social icon dots row ----------
def make_07_bouncing_icons():
    W, H = 640, 160
    n_icons = 6
    labels = ["GH","TW","LI","IG","YT","WB"]
    colors = [(240,246,252),(29,161,242),(10,102,194),(225,48,108),(255,0,0),(46,204,113)]
    n_frames = 60
    frames = []
    spacing = W / (n_icons+1)
    radius = 32
    for i in range(n_frames):
        img = Image.new("RGB", (W, H), (13,17,23))
        d = ImageDraw.Draw(img)
        f = font(SANS, 16)
        for idx in range(n_icons):
            phase = i/n_frames*2*math.pi + idx*0.6
            y = H/2 + math.sin(phase)*28
            x = spacing*(idx+1)
            d.ellipse([x-radius, y-radius, x+radius, y+radius], fill=colors[idx])
            bbox = d.textbbox((0,0), labels[idx], font=f)
            tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
            d.text((x-tw/2, y-th/2-2), labels[idx], font=f, fill=(20,20,20))
        frames.append(img)
    save_gif(frames, "07_bouncing_icons", duration=40)

# ---------- 8. Animated gradient divider ----------
def make_08_gradient_divider():
    W, H = 900, 40
    n_frames = 50
    frames = []
    colors = [(255,0,150), (0,200,255), (150,255,0), (255,150,0)]
    for i in range(n_frames):
        t = i / n_frames
        img = Image.new("RGB", (W, H), (13,17,23))
        d = ImageDraw.Draw(img)
        for x in range(W):
            tt = (x / W + t) % 1.0
            seg = tt * len(colors)
            i0 = int(seg) % len(colors)
            i1 = (i0+1) % len(colors)
            frac = seg - int(seg)
            col = lerp_color(colors[i0], colors[i1], frac)
            d.line([(x, 0), (x, H)], fill=col, width=1)
        frames.append(img)
    save_gif(frames, "08_gradient_divider", duration=35)

# ---------- 9. Loading / building profile spinner ----------
def make_09_loading_spinner():
    W, H = 500, 200
    n_frames = 48
    frames = []
    f = font(SANS, 22)
    label = "Loading profile"
    for i in range(n_frames):
        t = i / n_frames
        img = Image.new("RGB", (W, H), (13,17,23))
        d = ImageDraw.Draw(img)
        cx, cy, r = W/2, H/2 - 20, 36
        n_dots = 10
        for k in range(n_dots):
            ang = 2*math.pi*k/n_dots + t*2*math.pi
            x = cx + r*math.cos(ang)
            y = cy + r*math.sin(ang)
            size = 4 + 4*((k/n_dots))
            fade = (k/n_dots)
            col = lerp_color((40,44,52), (88,166,255), fade)
            d.ellipse([x-size, y-size, x+size, y+size], fill=col)
        dots = "." * (1 + (i // 8) % 3)
        bbox = d.textbbox((0,0), label+dots, font=f)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        d.text(((W-tw)/2, cy+r+30), label+dots, font=f, fill=(200,200,200))
        frames.append(img)
    save_gif(frames, "09_loading_spinner", duration=45)

# ---------- 10. Animated "open to work" badge ----------
def make_10_open_to_work_badge():
    W, H = 460, 140
    n_frames = 36
    frames = []
    f = font(SANS, 22)
    text = "OPEN TO WORK"
    for i in range(n_frames):
        t = i / n_frames
        pulse = (math.sin(t*2*math.pi)+1)/2
        img = Image.new("RGB", (W, H), (13,17,23))
        d = ImageDraw.Draw(img)
        ring_r = 10 + pulse*6
        cx, cy = 60, H/2
        glow_col = lerp_color((20,80,40),(46,204,113), pulse)
        d.ellipse([cx-ring_r-10, cy-ring_r-10, cx+ring_r+10, cy+ring_r+10], outline=glow_col, width=3)
        d.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(46,204,113))
        bbox = d.textbbox((0,0), text, font=f)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        d.rounded_rectangle([100, H/2-th/2-14, 100+tw+30, H/2+th/2+14], radius=20,
                             outline=(46,204,113), width=2, fill=(18,24,20))
        d.text((115, H/2-th/2-2), text, font=f, fill=(255,255,255))
        frames.append(img)
    save_gif(frames, "10_open_to_work_badge", duration=55)

make_01_wave_banner()
make_02_typing_effect()
make_03_skill_bars()
make_04_snake_contributions()
make_05_terminal_boot()
make_06_neon_glow_name()
make_07_bouncing_icons()
make_08_gradient_divider()
make_09_loading_spinner()
make_10_open_to_work_badge()
print("DONE")