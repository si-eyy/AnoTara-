"""
=============================================================
  AnoTara? - University Exclusive Engagement Platform
  Batangas State University | CICS Alangilan
  UI: Tkinter (Modern Redesign) | Database: Supabase REST
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib, datetime, random, json
import urllib.request, urllib.parse

# ─────────────────────────────────────────────
#  SUPABASE REST
# ─────────────────────────────────────────────
SUPABASE_URL = "https://bobokcrthddgrwfzihif.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvYm9rY3J0aGRkZ3J3ZnppaGlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczNTkwMjUsImV4cCI6MjA5MjkzNTAyNX0.-IWajxKxwm8TIZqhRrvG9OiDGUEJya10ERR10_tqzNY"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

def sb_get(table, params=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())

def sb_post(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode())
        return result[0] if isinstance(result, list) and result else result

def sb_count(table, params=None):
    p = dict(params or {}); p["select"] = "*"
    url = f"{SUPABASE_URL}/rest/v1/{table}?" + urllib.parse.urlencode(p)
    h = dict(HEADERS); h["Prefer"] = "count=exact"
    req = urllib.request.Request(url, headers=h, method="HEAD")
    with urllib.request.urlopen(req) as r:
        cr = r.headers.get("Content-Range", "*/0")
        try: return int(cr.split("/")[-1])
        except: return 0

# ─────────────────────────────────────────────
#  DESIGN SYSTEM
# ─────────────────────────────────────────────
C = {
    "bg":          "#0d1117",
    "bg2":         "#161b22",
    "sidebar":     "#0d1117",
    "card":        "#161b22",
    "card_hover":  "#1c2128",
    "border":      "#21262d",
    "accent":      "#2f81f7",
    "accent2":     "#8b5cf6",
    "accent3":     "#06b6d4",
    "success":     "#3fb950",
    "warning":     "#d29922",
    "danger":      "#f85149",
    "text":        "#e6edf3",
    "subtext":     "#7d8590",
    "muted":       "#484f58",
    "white":       "#ffffff",
    "nav_active":  "#1c2128",
    "tag_bg":      "#1f2937",
}

F = {
    "title":   ("Segoe UI", 20, "bold"),
    "heading": ("Segoe UI", 13, "bold"),
    "subhead": ("Segoe UI", 11, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "label":   ("Segoe UI", 10, "bold"),
    "nav":     ("Segoe UI", 10),
    "big":     ("Segoe UI", 26, "bold"),
    "xl":      ("Segoe UI", 32, "bold"),
}

ICEBREAKERS = [
    "What's a project you're currently excited about? 🚀",
    "If you could master any skill overnight, what would it be? ✨",
    "What's the most interesting thing you've learned this week? 📚",
    "What organization on campus would you love to explore? 🏛️",
    "Share a fun fact about yourself! 🎉",
    "What's your go-to study spot on campus? ☕",
    "What tech trend are you most curious about? 💻",
    "If you had a superpower, what would it be and why? 🦸",
    "What's the best advice you've ever received? 💡",
    "What hobby would you pick up if you had unlimited free time? 🎨",
]

INTEREST_OPTIONS = [
    "Programming", "Robotics", "Mathematics", "Photography",
    "Environment", "Debate", "Game Dev", "Leadership",
    "Music", "Sports", "Research", "Arts",
]

NAV_ICONS = {
    "Dashboard":     "⊞",
    "Organizations": "◈",
    "Peer Matching": "⊕",
    "Chat Room":     "◉",
    "My Report":     "⊟",
    "Admin Panel":   "◆",
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def ts(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
def is_bsu_email(e): return e.lower().endswith(("@g.batstate-u.edu.ph","@batstate-u.edu.ph"))
def valid_sid(sid):
    parts = sid.split("-")
    return len(parts)==2 and parts[0].isdigit() and len(parts[0])==2 and parts[1].isdigit() and len(parts[1])==5

# ─────────────────────────────────────────────
#  ROUNDED FRAME HELPER (canvas-based)
# ─────────────────────────────────────────────
def rounded_frame(parent, bg=None, radius=15, border_color=None, **kwargs):
    """Returns a plain tk.Frame; visually we just use bg consistently."""
    bg = bg or C["card"]
    f = tk.Frame(parent, bg=bg, **kwargs)
    return f

# ─────────────────────────────────────────────
#  REUSABLE UI COMPONENTS
# ─────────────────────────────────────────────
def btn(parent, text, command, bg=None, fg=None, font=None, padx=18, pady=9, radius=8):
    b = tk.Button(
        parent, text=text, command=command,
        bg=bg or C["accent"], fg=fg or C["white"],
        font=font or F["subhead"],
        relief="flat", cursor="hand2",
        padx=padx, pady=pady,
        activebackground=C["card_hover"],
        activeforeground=C["white"], bd=0,
    )
    return b

def entry_field(parent, label, show=None, width=32):
    wrap = tk.Frame(parent, bg=C["bg"])
    tk.Label(wrap, text=label, bg=C["bg"], fg=C["subtext"], font=F["small"]).pack(anchor="w", pady=(0,3))
    inner = tk.Frame(wrap, bg=C["card"], highlightthickness=1,
                     highlightbackground=C["border"], highlightcolor=C["accent"])
    inner.pack(fill="x")
    e = tk.Entry(inner, bg=C["card"], fg=C["text"], insertbackground=C["text"],
                 relief="flat", font=F["body"], bd=6, show=show, width=width)
    e.pack(fill="x")
    return wrap, e

def section_title(parent, text, subtitle=""):
    f = tk.Frame(parent, bg=C["bg"])
    tk.Label(f, text=text, bg=C["bg"], fg=C["text"], font=F["title"]).pack(anchor="w")
    if subtitle:
        tk.Label(f, text=subtitle, bg=C["bg"], fg=C["subtext"], font=F["body"]).pack(anchor="w", pady=(2,0))
    tk.Frame(f, bg=C["border"], height=1).pack(fill="x", pady=(12,0))
    return f

def tag_label(parent, text, bg=None, fg=None):
    return tk.Label(parent, text=f"  {text}  ",
                    bg=bg or C["accent"], fg=fg or C["white"],
                    font=F["small"], padx=5, pady=3,
                    relief="flat")

def stat_card(parent, icon, value, label, color):
    card = tk.Frame(parent, bg=C["card"], highlightthickness=1,
                    highlightbackground=C["border"])
    card.pack(side="left", expand=True, fill="both", padx=5, pady=2)

    inner = tk.Frame(card, bg=C["card"], padx=18, pady=18)
    inner.pack(fill="both", expand=True)

    top = tk.Frame(inner, bg=C["card"])
    top.pack(fill="x")
    tk.Label(top, text=icon, bg=C["card"], fg=color,
             font=("Segoe UI", 20)).pack(side="left")

    tk.Label(inner, text=value, bg=C["card"], fg=color,
             font=F["xl"]).pack(anchor="w", pady=(8,2))
    tk.Label(inner, text=label, bg=C["card"], fg=C["subtext"],
             font=F["small"]).pack(anchor="w")
    return card

# ─────────────────────────────────────────────
#  STYLE CONFIG
# ─────────────────────────────────────────────
def apply_ttk_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground=C["card"],
                    background=C["card"],
                    foreground=C["text"],
                    bordercolor=C["border"],
                    arrowcolor=C["subtext"],
                    selectbackground=C["accent"],
                    selectforeground=C["white"],
                    font=F["body"])
    style.configure("Vertical.TScrollbar",
                    background=C["bg2"],
                    troughcolor=C["bg"],
                    bordercolor=C["bg"],
                    arrowcolor=C["muted"],
                    relief="flat")
    style.map("Vertical.TScrollbar",
              background=[("active", C["muted"])])

# ─────────────────────────────────────────────
#  AUTH WINDOW
# ─────────────────────────────────────────────
class AuthWindow(tk.Toplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("AnoTara?")
        self.geometry("860x580")
        self.resizable(False, False)
        self.configure(bg=C["bg"])
        apply_ttk_style()
        self._show_login()

    def _clear(self):
        for w in self.winfo_children(): w.destroy()

    # ── LOGIN ──────────────────────────────────
    def _show_login(self):
        self._clear()

        # Left panel
        left = tk.Frame(self, bg=C["accent"], width=300)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        center_l = tk.Frame(left, bg=C["accent"])
        center_l.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_l, text="🎓", bg=C["accent"], font=("Segoe UI", 52)).pack(pady=(0,12))
        tk.Label(center_l, text="AnoTara?", bg=C["accent"], fg=C["white"],
                 font=("Segoe UI", 22, "bold")).pack()
        tk.Label(center_l, text="University Exclusive Platform", bg=C["accent"],
                 fg="#dbeafe", font=F["body"]).pack(pady=(6,2))
        tk.Frame(center_l, bg="#93c5fd", height=1, width=160).pack(pady=10)
        tk.Label(center_l, text="Batangas State University", bg=C["accent"],
                 fg="#bfdbfe", font=F["small"]).pack()
        tk.Label(center_l, text="CICS Alangilan", bg=C["accent"],
                 fg="#bfdbfe", font=F["small"]).pack(pady=(2,0))

        # Right panel
        right = tk.Frame(self, bg=C["bg"])
        right.pack(side="right", fill="both", expand=True)

        form = tk.Frame(right, bg=C["bg"])
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form, text="Welcome Back 👋", bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 18, "bold")).pack(pady=(0,4))
        tk.Label(form, text="Sign in to your account", bg=C["bg"],
                 fg=C["subtext"], font=F["body"]).pack(pady=(0,24))

        sf, self._sid = entry_field(form, "🎫  Student ID  (e.g. 21-12345)")
        sf.pack(fill="x", pady=6)
        pf, self._pw = entry_field(form, "🔒  Password", show="•")
        pf.pack(fill="x", pady=6)

        btn(form, "Sign In  →", self._do_login).pack(fill="x", pady=(20,10))
        tk.Button(form, text="Don't have an account?  Register →",
                  bg=C["bg"], fg=C["accent"], font=F["small"],
                  relief="flat", cursor="hand2",
                  activebackground=C["bg"], activeforeground=C["accent2"],
                  command=self._show_register).pack()

    def _do_login(self):
        sid = self._sid.get().strip()
        pw  = self._pw.get().strip()
        if not valid_sid(sid):
            messagebox.showerror("Error", "Student ID must be in format XX-XXXXX (e.g. 21-12345).", parent=self)
            return
        try:
            rows = sb_get("students", {"select":"*","student_id":f"eq.{sid}","password_hash":f"eq.{hash_pw(pw)}"})
        except Exception as e:
            messagebox.showerror("Connection Error", str(e), parent=self)
            return
        if not rows:
            messagebox.showerror("Error", "Invalid Student ID or password.", parent=self)
            return
        r = rows[0]
        student = {"id":r["student_id"],"name":r["name"],"email":r["email"],
                   "interests":r["interests"].split(","),"role":r["role"],"joined":r["joined_at"]}
        self.destroy()
        self.on_success(student)

    # ── REGISTER ───────────────────────────────
    def _show_register(self):
        self._clear()
        self.geometry("900x680")

        left = tk.Frame(self, bg=C["accent2"], width=270)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        cl = tk.Frame(left, bg=C["accent2"])
        cl.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(cl, text="🎓", bg=C["accent2"], font=("Segoe UI", 52)).pack(pady=(0,12))
        tk.Label(cl, text="Join Us!", bg=C["accent2"], fg=C["white"],
                 font=("Segoe UI", 22, "bold")).pack()
        tk.Label(cl, text="Connect. Discover. Grow.", bg=C["accent2"],
                 fg="#e0e7ff", font=F["body"]).pack(pady=6)
        tk.Frame(cl, bg="#a5b4fc", height=1, width=140).pack(pady=8)
        tk.Label(cl, text="BSU students only\n@batstate-u email required",
                 bg=C["accent2"], fg="#c7d2fe", font=F["small"], justify="center").pack()

        right = tk.Frame(self, bg=C["bg"])
        right.pack(side="right", fill="both", expand=True)

        canvas = tk.Canvas(right, bg=C["bg"], highlightthickness=0)
        sb_s = ttk.Scrollbar(right, orient="vertical", command=canvas.yview,
                              style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=sb_s.set)
        sb_s.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        form = tk.Frame(canvas, bg=C["bg"], padx=44)
        fw = canvas.create_window((0,0), window=form, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(fw, width=e.width))
        form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        tk.Label(form, text="Create Account", bg=C["bg"], fg=C["text"],
                 font=("Segoe UI", 18, "bold")).pack(pady=(30,4))
        tk.Label(form, text="Fill in your details below", bg=C["bg"],
                 fg=C["subtext"], font=F["body"]).pack(pady=(0,20))

        sf, self._r_sid   = entry_field(form, "🎫  Student ID  (e.g. 21-12345)")
        sf.pack(fill="x", pady=5)
        nf, self._r_name  = entry_field(form, "👤  Full Name")
        nf.pack(fill="x", pady=5)
        ef, self._r_email = entry_field(form, "✉️  University Email  (@g.batstate-u.edu.ph)")
        ef.pack(fill="x", pady=5)
        pf, self._r_pw    = entry_field(form, "🔒  Password  (min 6 chars)", show="•")
        pf.pack(fill="x", pady=5)

        tk.Label(form, text="Select Your Interests", bg=C["bg"],
                 fg=C["subtext"], font=F["small"]).pack(anchor="w", pady=(16,6))

        grid = tk.Frame(form, bg=C["bg"])
        grid.pack(fill="x")
        self._ivars = {}
        for i, opt in enumerate(INTEREST_OPTIONS):
            var = tk.BooleanVar()
            self._ivars[opt] = var
            cb = tk.Checkbutton(grid, text=opt, variable=var,
                                bg=C["bg"], fg=C["text"],
                                selectcolor=C["accent"],
                                activebackground=C["bg"],
                                font=F["body"], anchor="w",
                                cursor="hand2")
            cb.grid(row=i//3, column=i%3, sticky="w", padx=6, pady=3)

        btn(form, "Create Account  →", self._do_register,
            bg=C["accent2"]).pack(fill="x", pady=(24,8))
        tk.Button(form, text="Already have an account?  Sign In →",
                  bg=C["bg"], fg=C["accent"], font=F["small"],
                  relief="flat", cursor="hand2",
                  activebackground=C["bg"],
                  command=self._show_login).pack(pady=(0,30))

    def _do_register(self):
        sid   = self._r_sid.get().strip()
        name  = self._r_name.get().strip()
        email = self._r_email.get().strip()
        pw    = self._r_pw.get().strip()
        ints  = [k for k,v in self._ivars.items() if v.get()]

        if not valid_sid(sid):
            messagebox.showerror("Error","Student ID must be in format XX-XXXXX (e.g. 21-12345).",parent=self); return
        if not name:
            messagebox.showerror("Error","Full name is required.",parent=self); return
        if not is_bsu_email(email):
            messagebox.showerror("Error","Must use a valid BSU email (@g.batstate-u.edu.ph).",parent=self); return
        if len(pw)<6:
            messagebox.showerror("Error","Password must be at least 6 characters.",parent=self); return
        if not ints:
            messagebox.showerror("Error","Please select at least one interest.",parent=self); return

        try:
            sb_post("students",{"student_id":sid,"name":name,"email":email,
                                "password_hash":hash_pw(pw),"interests":",".join(ints),
                                "role":"student","joined_at":ts()})
        except Exception as e:
            messagebox.showerror("Error",f"Student ID or Email already registered.\n{e}",parent=self); return

        messagebox.showinfo("Success!",f"Welcome, {name}! 🎉 Your account has been created.",parent=self)
        student={"id":sid,"name":name,"email":email,"interests":ints,"role":"student","joined":ts()}
        self.destroy()
        self.on_success(student)


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class AnoTaraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnoTara?")
        self.geometry("1160x720")
        self.minsize(1000, 640)
        self.configure(bg=C["bg"])
        self.student = None
        apply_ttk_style()
        self._show_auth()

    def _show_auth(self):
        self.withdraw()
        AuthWindow(self, self._on_login)

    def _on_login(self, student):
        self.student = student
        self.deiconify()
        self._build_main()

    def _build_main(self):
        for w in self.winfo_children(): w.destroy()
        self.sidebar = tk.Frame(self, bg=C["sidebar"], width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.content = tk.Frame(self, bg=C["bg"])
        self.content.pack(side="right", fill="both", expand=True)
        self._build_sidebar()
        self._show_dashboard()

    # ── SIDEBAR ────────────────────────────────
    def _build_sidebar(self):
        s = self.student

        # Logo bar
        logo = tk.Frame(self.sidebar, bg=C["accent"], pady=18)
        logo.pack(fill="x")
        tk.Label(logo, text="🎓  AnoTara?", bg=C["accent"], fg=C["white"],
                 font=("Segoe UI", 12, "bold")).pack()

        # Divider
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(fill="x")

        # Avatar
        av = tk.Frame(self.sidebar, bg=C["sidebar"], pady=20, padx=16)
        av.pack(fill="x")
        av_inner = tk.Frame(av, bg=C["accent2"], width=46, height=46)
        av_inner.pack_propagate(False)
        av_inner.pack()
        tk.Label(av_inner, text=s["name"][0].upper(), bg=C["accent2"], fg=C["white"],
                 font=("Segoe UI", 18, "bold")).place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(av, text=s["name"], bg=C["sidebar"], fg=C["text"],
                 font=F["subhead"]).pack(pady=(10,2))
        tk.Label(av, text=f"ID: {s['id']}", bg=C["sidebar"],
                 fg=C["subtext"], font=F["small"]).pack()

        # Divider
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(fill="x", padx=16, pady=4)

        # Nav section label
        tk.Label(self.sidebar, text="NAVIGATION", bg=C["sidebar"],
                 fg=C["muted"], font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=20, pady=(8,4))

        nav_items = [
            ("Dashboard",     self._show_dashboard),
            ("Organizations", self._show_organizations),
            ("Peer Matching", self._show_peer_matching),
            ("Chat Room",     self._show_chat),
            ("My Report",     self._show_report),
        ]
        if s.get("role") == "admin":
            nav_items.append(("Admin Panel", self._show_admin))

        self._nav_btns = []
        for label, cmd in nav_items:
            icon = NAV_ICONS.get(label, "○")
            f = tk.Frame(self.sidebar, bg=C["sidebar"], cursor="hand2")
            f.pack(fill="x", padx=8, pady=2)

            lbl = tk.Label(f, text=f"  {icon}   {label}", bg=C["sidebar"],
                           fg=C["subtext"], font=F["nav"],
                           anchor="w", pady=10, padx=10)
            lbl.pack(fill="x")

            def make_cmd(c=cmd, frame=f, label_w=lbl):
                def on_click(e=None):
                    for btn_f, btn_l in self._nav_btns:
                        btn_f.config(bg=C["sidebar"])
                        btn_l.config(bg=C["sidebar"], fg=C["subtext"])
                    frame.config(bg=C["nav_active"])
                    label_w.config(bg=C["nav_active"], fg=C["text"])
                    c()
                return on_click

            cb = make_cmd()
            f.bind("<Button-1>", cb)
            lbl.bind("<Button-1>", cb)
            self._nav_btns.append((f, lbl))

        # Logout at bottom
        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(
            fill="x", padx=16, side="bottom", pady=8)
        logout_f = tk.Frame(self.sidebar, bg=C["sidebar"], cursor="hand2")
        logout_f.pack(fill="x", padx=8, pady=4, side="bottom")
        logout_l = tk.Label(logout_f, text="  ⏻   Logout", bg=C["sidebar"],
                            fg=C["danger"], font=F["nav"], anchor="w", pady=10, padx=10)
        logout_l.pack(fill="x")
        logout_f.bind("<Button-1>", lambda e: self._logout())
        logout_l.bind("<Button-1>", lambda e: self._logout())

    def _clear_content(self):
        for w in self.content.winfo_children(): w.destroy()

    def _scrollable_page(self):
        """Returns (outer_canvas, inner_frame) for a scrollable content page."""
        canvas = tk.Canvas(self.content, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(self.content, orient="vertical", command=canvas.yview,
                           style="Vertical.TScrollbar")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        inner = tk.Frame(canvas, bg=C["bg"])
        cw = canvas.create_window((0,0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        return canvas, inner

    def _page_header(self, parent, icon, title, subtitle=""):
        hdr = tk.Frame(parent, bg=C["bg"], padx=30, pady=24)
        hdr.pack(fill="x")
        title_row = tk.Frame(hdr, bg=C["bg"])
        title_row.pack(fill="x")
        tk.Label(title_row, text=icon, bg=C["bg"], fg=C["accent"],
                 font=("Segoe UI", 18)).pack(side="left", padx=(0,10))
        tk.Label(title_row, text=title, bg=C["bg"], fg=C["text"],
                 font=F["title"]).pack(side="left", anchor="s")
        if subtitle:
            tk.Label(hdr, text=subtitle, bg=C["bg"], fg=C["subtext"],
                     font=F["body"]).pack(anchor="w", pady=(4,0))
        tk.Frame(parent, bg=C["border"], height=1).pack(fill="x", padx=30)

    # ── DASHBOARD ──────────────────────────────
    def _show_dashboard(self):
        self._clear_content()
        s = self.student
        _, inner = self._scrollable_page()

        self._page_header(inner, "⊞", f"Welcome back, {s['name'].split()[0]}!", "Here's your activity overview")

        pad = tk.Frame(inner, bg=C["bg"], padx=30, pady=20)
        pad.pack(fill="both", expand=True)

        orgs_c  = sb_count("memberships",     {"student_id": f"eq.{s['id']}"})
        msgs_c  = sb_count("chat_messages",    {"sender_id":  f"eq.{s['id']}"})
        peers_c = sb_count("peer_connections", {"student_id": f"eq.{s['id']}"})
        score   = orgs_c*10 + msgs_c*2 + peers_c*5

        # Stat cards row
        stats = tk.Frame(pad, bg=C["bg"])
        stats.pack(fill="x", pady=(0,20))
        stat_card(stats, "🏛️", str(orgs_c),  "Orgs Joined",      C["accent"])
        stat_card(stats, "💬", str(msgs_c),  "Messages Sent",    C["accent2"])
        stat_card(stats, "🤝", str(peers_c), "Peers Connected",  C["success"])
        stat_card(stats, "⭐", str(score),   "Engagement Score", C["warning"])

        # Bottom row
        bot = tk.Frame(pad, bg=C["bg"])
        bot.pack(fill="both", expand=True)

        # Interests card
        ic = tk.Frame(bot, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        ic.pack(side="left", fill="both", expand=True, padx=(0,8), pady=4)
        hdr2 = tk.Frame(ic, bg=C["card"], padx=18, pady=14)
        hdr2.pack(fill="x")
        tk.Label(hdr2, text="🏷️  Your Interests", bg=C["card"],
                 fg=C["text"], font=F["subhead"]).pack(anchor="w")
        tk.Frame(ic, bg=C["border"], height=1).pack(fill="x")
        wrap = tk.Frame(ic, bg=C["card"], padx=18, pady=14)
        wrap.pack(fill="both")
        for interest in s["interests"]:
            lbl = tk.Label(wrap, text=interest, bg=C["accent"], fg=C["white"],
                           font=F["small"], padx=10, pady=4)
            lbl.pack(side="left", padx=3, pady=3)

        # Icebreaker card
        ib = tk.Frame(bot, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        ib.pack(side="right", fill="both", expand=True, padx=(8,0), pady=4)
        hdr3 = tk.Frame(ib, bg=C["card"], padx=18, pady=14)
        hdr3.pack(fill="x")
        tk.Label(hdr3, text="💡  Icebreaker of the Day", bg=C["card"],
                 fg=C["text"], font=F["subhead"]).pack(anchor="w")
        tk.Frame(ib, bg=C["border"], height=1).pack(fill="x")
        ib_body = tk.Frame(ib, bg=C["card"], padx=18, pady=14)
        ib_body.pack(fill="both", expand=True)
        ib_txt = tk.Label(ib_body, text=random.choice(ICEBREAKERS),
                          bg=C["card"], fg=C["subtext"],
                          font=F["body"], wraplength=260, justify="left")
        ib_txt.pack(anchor="w", pady=(0,14))
        btn(ib_body, "🔄  New Prompt",
            lambda: ib_txt.config(text=random.choice(ICEBREAKERS)),
            bg=C["tag_bg"], pady=7, padx=14).pack(anchor="w")

    # ── ORGANIZATIONS ──────────────────────────
    def _show_organizations(self):
        self._clear_content()

        joined_ids = {r["org_id"] for r in sb_get("memberships",
            {"select":"org_id","student_id":f"eq.{self.student['id']}"})}

        _, inner = self._scrollable_page()
        self._page_header(inner, "◈", "Organization Directory",
                          "Browse and join university organizations")

        # Filter bar
        bar = tk.Frame(inner, bg=C["bg"], padx=30, pady=12)
        bar.pack(fill="x")
        tk.Label(bar, text="Filter by Category:", bg=C["bg"],
                 fg=C["subtext"], font=F["small"]).pack(side="left")
        cats_raw = sb_get("organizations", {"select":"category"})
        cats = ["All"] + sorted(set(r["category"] for r in cats_raw))
        self._cat_var = tk.StringVar(value="All")
        cat_menu = ttk.Combobox(bar, textvariable=self._cat_var,
                                values=cats, state="readonly", width=20)
        cat_menu.pack(side="left", padx=10)

        list_pad = tk.Frame(inner, bg=C["bg"], padx=30)
        list_pad.pack(fill="both", expand=True)

        cat_menu.bind("<<ComboboxSelected>>",
                      lambda e: self._refresh_orgs(list_pad, joined_ids))
        self._refresh_orgs(list_pad, joined_ids)

    def _refresh_orgs(self, frame, joined_ids):
        for w in frame.winfo_children(): w.destroy()
        cat = self._cat_var.get()
        params = {"select":"*","order":"name"}
        if cat != "All": params["category"] = f"eq.{cat}"
        orgs = sb_get("organizations", params)

        CAT_COLORS = {
            "Academic":"#2f81f7","Technology":"#8b5cf6","Arts":"#ec4899",
            "Advocacy":"#22c55e","Communication":"#f59e0b","Leadership":"#06b6d4",
        }

        for org in orgs:
            oid      = org["org_id"]
            name     = org["name"]
            cat_name = org["category"]
            desc     = org["description"]
            mem_cnt  = sb_count("memberships", {"org_id": f"eq.{oid}"})
            joined   = oid in joined_ids
            cat_c    = CAT_COLORS.get(cat_name, C["accent"])

            card = tk.Frame(frame, bg=C["card"], highlightthickness=1,
                            highlightbackground=C["border"])
            card.pack(fill="x", pady=5)

            # Left accent bar
            accent_bar = tk.Frame(card, bg=cat_c, width=4)
            accent_bar.pack(side="left", fill="y")

            body = tk.Frame(card, bg=C["card"], padx=18, pady=16)
            body.pack(side="left", fill="both", expand=True)

            top = tk.Frame(body, bg=C["card"])
            top.pack(fill="x")
            tk.Label(top, text=name, bg=C["card"], fg=C["text"],
                     font=F["heading"]).pack(side="left")
            tk.Label(top, text=f"  {cat_name}  ", bg=cat_c, fg=C["white"],
                     font=F["small"], padx=6, pady=2).pack(side="left", padx=10)

            tk.Label(body, text=desc, bg=C["card"], fg=C["subtext"],
                     font=F["body"], wraplength=600, justify="left").pack(anchor="w", pady=(6,4))
            tk.Label(body, text=f"👥  {mem_cnt} member{'s' if mem_cnt!=1 else ''}",
                     bg=C["card"], fg=C["muted"], font=F["small"]).pack(anchor="w")

            btn_area = tk.Frame(card, bg=C["card"], padx=20, pady=20)
            btn_area.pack(side="right", fill="y")
            if joined:
                tk.Label(btn_area, text="✓  Joined", bg=C["card"],
                         fg=C["success"], font=F["subhead"]).pack(expand=True)
            else:
                btn(btn_area, "  Join  ", padx=18, pady=8,
                    command=lambda o=oid, n=name: self._join_org(o, n, joined_ids, frame)).pack(expand=True)

    def _join_org(self, org_id, org_name, joined_ids, frame):
        try:
            sb_post("memberships",{"student_id":self.student["id"],"org_id":org_id,"joined_at":ts()})
            joined_ids.add(org_id)
            messagebox.showinfo("Joined!", f"You joined {org_name}! 🎉")
        except:
            messagebox.showinfo("Info", "You are already a member.")
        self._refresh_orgs(frame, joined_ids)

    # ── PEER MATCHING ──────────────────────────
    def _show_peer_matching(self):
        self._clear_content()
        _, inner = self._scrollable_page()
        self._page_header(inner, "⊕", "Peer Matching",
                          "Find students who share your interests")

        sid = self.student["id"]
        my_ints = set(self.student["interests"])

        connected = {r["peer_id"] for r in sb_get("peer_connections",
            {"select":"peer_id","student_id":f"eq.{sid}"})}
        connected |= {r["student_id"] for r in sb_get("peer_connections",
            {"select":"student_id","peer_id":f"eq.{sid}"})}

        peers = sb_get("students",{"select":"student_id,name,interests","student_id":f"neq.{sid}"})
        matches = []
        for p in peers:
            pi = set(p["interests"].split(","))
            common = my_ints & pi
            if common:
                matches.append((len(common), p["student_id"], p["name"], common))
        matches.sort(reverse=True)

        pad = tk.Frame(inner, bg=C["bg"], padx=30, pady=12)
        pad.pack(fill="both", expand=True)

        if not matches:
            empty = tk.Frame(pad, bg=C["card"], highlightthickness=1,
                             highlightbackground=C["border"])
            empty.pack(fill="x", pady=20)
            tk.Label(empty, text="🔍\n\nNo peer matches yet.\nMore students need to register!",
                     bg=C["card"], fg=C["subtext"], font=F["heading"],
                     justify="center", pady=40).pack()
            return

        for rank, (score, peer_id, peer_name, common) in enumerate(matches[:10], 1):
            card = tk.Frame(pad, bg=C["card"], highlightthickness=1,
                            highlightbackground=C["border"])
            card.pack(fill="x", pady=5)

            # Rank badge
            rank_f = tk.Frame(card, bg=C["accent"] if rank<=3 else C["tag_bg"], width=48)
            rank_f.pack(side="left", fill="y")
            rank_f.pack_propagate(False)
            tk.Label(rank_f, text=f"#{rank}", bg=rank_f["bg"], fg=C["white"],
                     font=F["subhead"]).place(relx=0.5,rely=0.5,anchor="center")

            body = tk.Frame(card, bg=C["card"], padx=16, pady=14)
            body.pack(side="left", fill="both", expand=True)
            top = tk.Frame(body, bg=C["card"])
            top.pack(fill="x")
            tk.Label(top, text=peer_name, bg=C["card"], fg=C["text"],
                     font=F["heading"]).pack(side="left")
            tk.Label(top, text=f"  {score} shared interest{'s' if score!=1 else ''}",
                     bg=C["success"]+"22", fg=C["success"],
                     font=F["small"], padx=8, pady=2).pack(side="left", padx=10)

            tags = tk.Frame(body, bg=C["card"])
            tags.pack(fill="x", pady=(8,0))
            for i in list(common)[:6]:
                tk.Label(tags, text=i, bg=C["accent"]+"33", fg=C["accent3"],
                         font=F["small"], padx=8, pady=3).pack(side="left", padx=3)

            btn_a = tk.Frame(card, bg=C["card"], padx=20, pady=20)
            btn_a.pack(side="right", fill="y")
            if peer_id in connected:
                tk.Label(btn_a, text="✓  Connected", bg=C["card"],
                         fg=C["success"], font=F["subhead"]).pack(expand=True)
            else:
                btn(btn_a, "  Connect  ", padx=18, pady=7,
                    command=lambda pid=peer_id, pn=peer_name: self._connect_peer(pid, pn, connected)).pack(expand=True)

    def _connect_peer(self, peer_id, peer_name, connected):
        try:
            sb_post("peer_connections",{"student_id":self.student["id"],"peer_id":peer_id,"connected_at":ts()})
            connected.add(peer_id)
            messagebox.showinfo("Connected!", f"You are now connected with {peer_name}! 🤝")
        except:
            messagebox.showinfo("Info", "Already connected.")
        self._show_peer_matching()

    # ── CHAT ───────────────────────────────────
    def _show_chat(self):
        self._clear_content()
        self._page_header(self.content, "◉", "Global Chat Room",
                          "Connect with fellow students campus-wide")

        main = tk.Frame(self.content, bg=C["bg"])
        main.pack(fill="both", expand=True, padx=30, pady=12)

        # Sidebar panel
        side = tk.Frame(main, bg=C["card"], width=230,
                        highlightthickness=1, highlightbackground=C["border"])
        side.pack(side="right", fill="y", padx=(10,0))
        side.pack_propagate(False)

        tk.Label(side, text="💡  Starters", bg=C["card"], fg=C["text"],
                 font=F["subhead"], pady=14, padx=16).pack(anchor="w")
        tk.Frame(side, bg=C["border"], height=1).pack(fill="x")
        self._ib = tk.Label(side, text=random.choice(ICEBREAKERS),
                            bg=C["card"], fg=C["subtext"],
                            font=F["small"], wraplength=196, justify="left",
                            padx=14, pady=14)
        self._ib.pack(anchor="w")
        btn(side, "🔄 New", lambda: self._ib.config(text=random.choice(ICEBREAKERS)),
            bg=C["tag_bg"], padx=12, pady=6).pack(padx=14, anchor="w")

        # Chat area
        chat = tk.Frame(main, bg=C["bg"])
        chat.pack(side="left", fill="both", expand=True)

        self._chat_disp = scrolledtext.ScrolledText(
            chat, bg=C["card"], fg=C["text"],
            font=F["body"], relief="flat", state="disabled",
            wrap="word", padx=14, pady=10,
            highlightthickness=1, highlightbackground=C["border"])
        self._chat_disp.pack(fill="both", expand=True)

        # Input row
        inp = tk.Frame(chat, bg=C["card"],
                       highlightthickness=1, highlightbackground=C["border"])
        inp.pack(fill="x", pady=(8,0))
        self._chat_entry = tk.Entry(inp, bg=C["card"], fg=C["text"],
                                    insertbackground=C["text"], font=F["body"],
                                    relief="flat", bd=0)
        self._chat_entry.pack(side="left", fill="x", expand=True, padx=14, ipady=10)
        self._chat_entry.bind("<Return>", lambda e: self._send_message())
        btn(inp, "Send  ➤", self._send_message, padx=18, pady=10).pack(side="right", padx=10, pady=6)

        self._load_chat()

    def _load_chat(self):
        msgs = list(reversed(sb_get("chat_messages",
            {"select":"sender_name,message,sent_at","order":"id.desc","limit":"50"})))
        self._chat_disp.configure(state="normal")
        self._chat_disp.delete("1.0","end")
        for row in msgs:
            sender = row["sender_name"]
            is_me  = sender == self.student["name"]
            color  = C["accent"] if is_me else C["accent2"]
            prefix = "You" if is_me else sender
            self._chat_disp.insert("end", f"[{row['sent_at']}] ", "time")
            self._chat_disp.insert("end", f"{prefix}: ", f"s_{sender}")
            self._chat_disp.insert("end", f"{row['message']}\n")
            self._chat_disp.tag_config("time", foreground=C["muted"])
            self._chat_disp.tag_config(f"s_{sender}", foreground=color, font=F["label"])
        self._chat_disp.configure(state="disabled")
        self._chat_disp.see("end")

    def _send_message(self):
        msg = self._chat_entry.get().strip()
        if not msg: return
        sb_post("chat_messages",{"sender_id":self.student["id"],
                                  "sender_name":self.student["name"],
                                  "message":msg,"sent_at":ts()})
        self._chat_entry.delete(0,"end")
        self._load_chat()

    # ── REPORT ─────────────────────────────────
    def _show_report(self):
        self._clear_content()
        _, inner = self._scrollable_page()
        s = self.student
        self._page_header(inner, "⊟", "My Engagement Report",
                          "Track your campus participation")

        pad = tk.Frame(inner, bg=C["bg"], padx=30, pady=16)
        pad.pack(fill="both", expand=True)

        mem_rows = sb_get("memberships",{"select":"org_id,joined_at","student_id":f"eq.{s['id']}"})
        joined_orgs = []
        for r in mem_rows:
            od = sb_get("organizations",{"select":"name,category","org_id":f"eq.{r['org_id']}"})
            if od: joined_orgs.append((od[0]["name"],od[0]["category"],r["joined_at"]))

        msg_count = sb_count("chat_messages",{"sender_id":f"eq.{s['id']}"})
        peer_rows = sb_get("peer_connections",{"select":"peer_id","student_id":f"eq.{s['id']}"})
        connected_peers = []
        for r in peer_rows:
            pd = sb_get("students",{"select":"name","student_id":f"eq.{r['peer_id']}"})
            if pd: connected_peers.append(pd[0]["name"])

        total_orgs = sb_count("organizations")
        score = len(joined_orgs)*10 + msg_count*2 + len(connected_peers)*5
        pct   = round(len(joined_orgs)/total_orgs*100,1) if total_orgs else 0

        # Profile card
        pc = tk.Frame(pad, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        pc.pack(fill="x", pady=(0,16))
        pc_l = tk.Frame(pc, bg=C["accent2"], width=6)
        pc_l.pack(side="left", fill="y")
        pc_b = tk.Frame(pc, bg=C["card"], padx=20, pady=16)
        pc_b.pack(fill="x")
        tk.Label(pc_b, text=s["name"], bg=C["card"], fg=C["text"],
                 font=F["heading"]).pack(anchor="w")
        tk.Label(pc_b, text=f"Student ID: {s['id']}  ·  {s['email']}",
                 bg=C["card"], fg=C["subtext"], font=F["body"]).pack(anchor="w", pady=(2,0))
        tk.Label(pc_b, text=f"Member since: {s.get('joined','N/A')}",
                 bg=C["card"], fg=C["muted"], font=F["small"]).pack(anchor="w")

        # Stats
        sr = tk.Frame(pad, bg=C["bg"])
        sr.pack(fill="x", pady=(0,16))
        for val, lbl, color in [
            (f"{len(joined_orgs)}/{total_orgs}", "Orgs Joined",   C["accent"]),
            (f"{pct}%",                           "Participation", C["accent2"]),
            (str(msg_count),                      "Messages",      C["success"]),
            (str(len(connected_peers)),            "Peers",         C["warning"]),
            (str(score),                           "Score ⭐",      C["danger"]),
        ]:
            c2 = tk.Frame(sr, bg=C["card"], highlightthickness=1,
                          highlightbackground=C["border"])
            c2.pack(side="left", expand=True, fill="both", padx=4)
            tk.Label(c2, text=val, bg=C["card"], fg=color,
                     font=("Segoe UI", 18, "bold"), pady=12).pack()
            tk.Label(c2, text=lbl, bg=C["card"], fg=C["subtext"],
                     font=F["small"]).pack(pady=(0,12))

        # Detail row
        dr = tk.Frame(pad, bg=C["bg"])
        dr.pack(fill="both", expand=True)

        oc = tk.Frame(dr, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        oc.pack(side="left", fill="both", expand=True, padx=(0,6))
        tk.Label(oc, text="🏛️  Organizations", bg=C["card"], fg=C["text"],
                 font=F["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(oc, bg=C["border"], height=1).pack(fill="x")
        for nm, ct, _ in joined_orgs:
            row = tk.Frame(oc, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            tk.Label(row, text=f"●  {nm}", bg=C["card"], fg=C["text"],
                     font=F["body"]).pack(side="left")
            tk.Label(row, text=ct, bg=C["card"], fg=C["muted"],
                     font=F["small"]).pack(side="right")

        peers_c2 = tk.Frame(dr, bg=C["card"], highlightthickness=1,
                            highlightbackground=C["border"])
        peers_c2.pack(side="right", fill="both", expand=True, padx=(6,0))
        tk.Label(peers_c2, text="🤝  Connected Peers", bg=C["card"], fg=C["text"],
                 font=F["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(peers_c2, bg=C["border"], height=1).pack(fill="x")
        for pn in connected_peers:
            tk.Label(peers_c2, text=f"●  {pn}", bg=C["card"], fg=C["text"],
                     font=F["body"], padx=16, pady=5).pack(anchor="w")
        if not connected_peers:
            tk.Label(peers_c2, text="No peers connected yet.\nTry Peer Matching! 🔍",
                     bg=C["card"], fg=C["subtext"], font=F["body"],
                     padx=16, pady=16, justify="left").pack(anchor="w")

    # ── ADMIN ──────────────────────────────────
    def _show_admin(self):
        self._clear_content()
        _, inner = self._scrollable_page()
        self._page_header(inner, "◆", "Admin Panel",
                          "Platform-wide analytics and management")

        pad = tk.Frame(inner, bg=C["bg"], padx=30, pady=16)
        pad.pack(fill="both", expand=True)

        ts_count = sb_count("students")
        to_count = sb_count("organizations")
        tm_count = sb_count("chat_messages")
        tmem     = sb_count("memberships")

        stats = tk.Frame(pad, bg=C["bg"])
        stats.pack(fill="x", pady=(0,20))
        stat_card(stats, "👥", str(ts_count), "Total Students",    C["accent"])
        stat_card(stats, "🏛️", str(to_count), "Organizations",     C["accent2"])
        stat_card(stats, "💬", str(tm_count), "Chat Messages",     C["success"])
        stat_card(stats, "📋", str(tmem),     "Total Memberships", C["warning"])

        bot = tk.Frame(pad, bg=C["bg"])
        bot.pack(fill="both", expand=True)

        # Leaderboard
        lb = tk.Frame(bot, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        lb.pack(side="left", fill="both", expand=True, padx=(0,8))
        tk.Label(lb, text="⭐  Top Students", bg=C["card"], fg=C["text"],
                 font=F["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(lb, bg=C["border"], height=1).pack(fill="x")

        all_st = sb_get("students",{"select":"student_id,name"})
        board = []
        for st in all_st:
            sid = st["student_id"]
            o = sb_count("memberships",     {"student_id":f"eq.{sid}"})
            m = sb_count("chat_messages",   {"sender_id": f"eq.{sid}"})
            p = sb_count("peer_connections",{"student_id":f"eq.{sid}"})
            board.append((o*10+m*2+p*5, st["name"]))
        board.sort(reverse=True)

        RANK_COLORS = [C["warning"], C["subtext"], C["accent3"]]
        for rank, (sc, nm) in enumerate(board[:8], 1):
            row = tk.Frame(lb, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            rc = RANK_COLORS[rank-1] if rank<=3 else C["muted"]
            tk.Label(row, text=f"#{rank}", bg=C["card"], fg=rc,
                     font=F["subhead"], width=3).pack(side="left")
            tk.Label(row, text=nm, bg=C["card"], fg=C["text"],
                     font=F["body"]).pack(side="left", padx=8)
            tk.Label(row, text=f"{sc} pts", bg=C["card"], fg=C["warning"],
                     font=F["small"]).pack(side="right")

        # Org membership
        oc = tk.Frame(bot, bg=C["card"], highlightthickness=1,
                      highlightbackground=C["border"])
        oc.pack(side="right", fill="both", expand=True, padx=(8,0))
        tk.Label(oc, text="🏛️  Organization Membership", bg=C["card"], fg=C["text"],
                 font=F["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(oc, bg=C["border"], height=1).pack(fill="x")

        orgs = sb_get("organizations",{"select":"org_id,name"})
        org_counts = [(o["name"], sb_count("memberships",{"org_id":f"eq.{o['org_id']}"})) for o in orgs]
        org_counts.sort(key=lambda x:-x[1])
        max_cnt = max((c for _,c in org_counts), default=1) or 1

        for on, cnt in org_counts:
            row = tk.Frame(oc, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            tk.Label(row, text=on, bg=C["card"], fg=C["text"], font=F["body"]).pack(anchor="w")
            bar_bg = tk.Frame(row, bg=C["border"], height=4)
            bar_bg.pack(fill="x", pady=(3,0))
            bar_fill = tk.Frame(bar_bg, bg=C["accent"], height=4)
            bar_fill.place(relwidth=cnt/max_cnt, relheight=1)
            tk.Label(row, text=f"{cnt} members", bg=C["card"], fg=C["muted"],
                     font=F["small"]).pack(anchor="e")

    # ── LOGOUT ─────────────────────────────────
    def _logout(self):
        if messagebox.askyesno("Logout","Are you sure you want to logout?"):
            self.student = None
            for w in self.winfo_children(): w.destroy()
            self._show_auth()

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = AnoTaraApp()
    app.mainloop()