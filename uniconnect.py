"""
=============================================================
  AnoTara? - University Exclusive Engagement Platform
  Batangas State University | CICS Alangilan
  UI: Tkinter  |  Database: Supabase REST API (urllib only)
=============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import hashlib
import datetime
import random
import json
import urllib.request
import urllib.parse

# ─────────────────────────────────────────────
#  SUPABASE REST CONFIG
# ─────────────────────────────────────────────

SUPABASE_URL = "https://bobokcrthddgrwfzihif.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJvYm9rY3J0aGRkZ3J3ZnppaGlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczNTkwMjUsImV4cCI6MjA5MjkzNTAyNX0.-IWajxKxwm8TIZqhRrvG9OiDGUEJya10ERR10_tqzNY"

HEADERS = {
    "apikey":        SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type":  "application/json",
    "Prefer":        "return=representation",
}


def sb_get(table, params=None):
    """GET rows from a Supabase table."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def sb_post(table, data):
    """INSERT a row into a Supabase table."""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req) as r:
        result = json.loads(r.read().decode())
        return result[0] if isinstance(result, list) and result else result


def sb_count(table, params=None):
    """Return the count of rows matching params using Content-Range header."""
    p = dict(params or {})
    p["select"] = "*"
    url = f"{SUPABASE_URL}/rest/v1/{table}?" + urllib.parse.urlencode(p)
    h = dict(HEADERS)
    h["Prefer"] = "count=exact"
    req = urllib.request.Request(url, headers=h, method="HEAD")
    with urllib.request.urlopen(req) as r:
        cr = r.headers.get("Content-Range", "*/0")
        try:
            return int(cr.split("/")[-1])
        except Exception:
            return 0


# ─────────────────────────────────────────────
#  CONSTANTS & THEME
# ─────────────────────────────────────────────

COLORS = {
    "bg":       "#0f172a",
    "sidebar":  "#1e293b",
    "card":     "#1e293b",
    "card2":    "#263347",
    "accent":   "#3b82f6",
    "accent2":  "#6366f1",
    "success":  "#22c55e",
    "warning":  "#f59e0b",
    "danger":   "#ef4444",
    "text":     "#f1f5f9",
    "subtext":  "#94a3b8",
    "border":   "#334155",
    "input_bg": "#0f172a",
    "hover":    "#2d4a7a",
    "white":    "#ffffff",
}

FONTS = {
    "title":   ("Segoe UI", 22, "bold"),
    "heading": ("Segoe UI", 14, "bold"),
    "subhead": ("Segoe UI", 11, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "label":   ("Segoe UI", 10, "bold"),
    "mono":    ("Consolas", 10),
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

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def ts() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def is_bsu_email(email: str) -> bool:
    return email.lower().endswith(("@g.batstate-u.edu.ph", "@batstate-u.edu.ph"))

def valid_sid(sid: str) -> bool:
    parts = sid.split("-")
    return (len(parts) == 2 and
            parts[0].isdigit() and len(parts[0]) == 2 and
            parts[1].isdigit() and len(parts[1]) == 5)

# ─────────────────────────────────────────────
#  REUSABLE UI COMPONENTS
# ─────────────────────────────────────────────

def styled_button(parent, text, command, bg=None, fg=None,
                  font=None, padx=20, pady=8, width=None):
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg or COLORS["accent"],
        fg=fg or COLORS["white"],
        font=font or FONTS["subhead"],
        relief="flat", cursor="hand2",
        padx=padx, pady=pady,
        activebackground=COLORS["hover"],
        activeforeground=COLORS["white"],
        bd=0,
    )
    if width:
        btn.config(width=width)
    return btn

def styled_entry(parent, show=None, width=30):
    return tk.Entry(
        parent,
        bg=COLORS["input_bg"], fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat", font=FONTS["body"],
        bd=0, show=show, width=width,
    )

def entry_frame(parent, label_text, show=None, width=30):
    f = tk.Frame(parent, bg=COLORS["bg"])
    tk.Label(f, text=label_text, bg=COLORS["bg"],
             fg=COLORS["subtext"], font=FONTS["small"]).pack(anchor="w")
    e = styled_entry(f, show=show, width=width)
    e.pack(fill="x", pady=(2, 0))
    tk.Frame(f, bg=COLORS["border"], height=1).pack(fill="x")
    return f, e

def card_frame(parent, **kwargs):
    defaults = dict(bg=COLORS["card"], relief="flat", bd=0)
    defaults.update(kwargs)
    return tk.Frame(parent, **defaults)

# ─────────────────────────────────────────────
#  AUTH WINDOWS
# ─────────────────────────────────────────────

class AuthWindow(tk.Toplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success
        self.title("AnoTara?")
        self.geometry("820x560")
        self.resizable(False, False)
        self.configure(bg=COLORS["bg"])
        self._show_login()

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ── LOGIN ──────────────────────────────────
    def _show_login(self):
        self._clear()

        left = tk.Frame(self, bg=COLORS["accent"], width=320)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🎓", bg=COLORS["accent"],
                 font=("Segoe UI", 48)).pack(pady=(80, 10))
        tk.Label(left, text="AnoTara?", bg=COLORS["accent"],
                 fg=COLORS["white"], font=("Segoe UI", 24, "bold")).pack()
        tk.Label(left, text="University Exclusive Platform",
                 bg=COLORS["accent"], fg="#dbeafe",
                 font=FONTS["body"]).pack(pady=4)
        tk.Label(left, text="Batangas State University",
                 bg=COLORS["accent"], fg="#bfdbfe",
                 font=FONTS["small"]).pack(pady=(0, 4))
        tk.Label(left, text="CICS Alangilan",
                 bg=COLORS["accent"], fg="#bfdbfe",
                 font=FONTS["small"]).pack()

        right = tk.Frame(self, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True)

        form = tk.Frame(right, bg=COLORS["bg"])
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(form, text="Welcome Back", bg=COLORS["bg"],
                 fg=COLORS["text"], font=FONTS["title"]).pack(pady=(0, 4))
        tk.Label(form, text="Sign in to your account", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=FONTS["body"]).pack(pady=(0, 28))

        sf, self._login_sid = entry_frame(form, "Student ID (e.g. 21-12345)")
        sf.pack(fill="x", pady=8)
        pf, self._login_pw = entry_frame(form, "Password", show="•")
        pf.pack(fill="x", pady=8)

        styled_button(form, "Sign In", self._do_login).pack(fill="x", pady=(20, 8))
        tk.Button(form, text="Don't have an account? Register",
                  bg=COLORS["bg"], fg=COLORS["accent"],
                  font=FONTS["small"], relief="flat", cursor="hand2",
                  activebackground=COLORS["bg"], activeforeground=COLORS["accent2"],
                  command=self._show_register).pack()

    def _do_login(self):
        sid = self._login_sid.get().strip()
        pw  = self._login_pw.get().strip()

        if not valid_sid(sid):
            messagebox.showerror("Error", "Student ID must be in format XX-XXXXX (e.g. 21-12345).", parent=self)
            return

        try:
            rows = sb_get("students", {
                "select":        "*",
                "student_id":    f"eq.{sid}",
                "password_hash": f"eq.{hash_pw(pw)}",
            })
        except Exception as e:
            messagebox.showerror("Error", f"Connection error:\n{e}", parent=self)
            return

        if not rows:
            messagebox.showerror("Error", "Invalid Student ID or password.", parent=self)
            return

        row = rows[0]
        student = {
            "id":        row["student_id"],
            "name":      row["name"],
            "email":     row["email"],
            "interests": row["interests"].split(","),
            "role":      row["role"],
            "joined":    row["joined_at"],
        }
        self.destroy()
        self.on_success(student)

    # ── REGISTER ───────────────────────────────
    def _show_register(self):
        self._clear()
        self.geometry("900x680")

        left = tk.Frame(self, bg=COLORS["accent2"], width=280)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(left, text="🎓", bg=COLORS["accent2"],
                 font=("Segoe UI", 48)).pack(pady=(70, 10))
        tk.Label(left, text="Join Us!", bg=COLORS["accent2"],
                 fg=COLORS["white"], font=("Segoe UI", 22, "bold")).pack()
        tk.Label(left, text="Connect. Discover. Grow.",
                 bg=COLORS["accent2"], fg="#e0e7ff",
                 font=FONTS["body"]).pack(pady=8)
        tk.Label(left, text="Only for BSU students\nwith @batstate-u email",
                 bg=COLORS["accent2"], fg="#c7d2fe",
                 font=FONTS["small"], justify="center").pack(pady=(30, 0))

        right = tk.Frame(self, bg=COLORS["bg"])
        right.pack(side="right", fill="both", expand=True)

        canvas = tk.Canvas(right, bg=COLORS["bg"], highlightthickness=0)
        sb_scroll = ttk.Scrollbar(right, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        form = tk.Frame(canvas, bg=COLORS["bg"], padx=40)
        fw = canvas.create_window((0, 0), window=form, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(fw, width=e.width))
        form.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        tk.Label(form, text="Create Account", bg=COLORS["bg"],
                 fg=COLORS["text"], font=FONTS["title"]).pack(pady=(30, 4))
        tk.Label(form, text="Fill in your details below", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=FONTS["body"]).pack(pady=(0, 20))

        sf, self._r_sid   = entry_frame(form, "Student ID (e.g. 21-12345)")
        sf.pack(fill="x", pady=6)
        nf, self._r_name  = entry_frame(form, "Full Name")
        nf.pack(fill="x", pady=6)
        ef, self._r_email = entry_frame(form, "University Email (@g.batstate-u.edu.ph)")
        ef.pack(fill="x", pady=6)
        pf, self._r_pw    = entry_frame(form, "Password (min 6 chars)", show="•")
        pf.pack(fill="x", pady=6)

        tk.Label(form, text="Select Your Interests",
                 bg=COLORS["bg"], fg=COLORS["subtext"],
                 font=FONTS["small"]).pack(anchor="w", pady=(14, 4))

        grid = tk.Frame(form, bg=COLORS["bg"])
        grid.pack(fill="x")
        self._interest_vars = {}
        for i, opt in enumerate(INTEREST_OPTIONS):
            var = tk.BooleanVar()
            self._interest_vars[opt] = var
            tk.Checkbutton(
                grid, text=opt, variable=var,
                bg=COLORS["bg"], fg=COLORS["text"],
                selectcolor=COLORS["accent"],
                activebackground=COLORS["bg"],
                font=FONTS["body"], anchor="w",
            ).grid(row=i // 3, column=i % 3, sticky="w", padx=8, pady=2)

        styled_button(form, "Create Account", self._do_register,
                      bg=COLORS["accent2"]).pack(fill="x", pady=(24, 8))
        tk.Button(form, text="Already have an account? Sign In",
                  bg=COLORS["bg"], fg=COLORS["accent"],
                  font=FONTS["small"], relief="flat", cursor="hand2",
                  activebackground=COLORS["bg"],
                  command=self._show_login).pack(pady=(0, 30))

    def _do_register(self):
        sid       = self._r_sid.get().strip()
        name      = self._r_name.get().strip()
        email     = self._r_email.get().strip()
        pw        = self._r_pw.get().strip()
        interests = [k for k, v in self._interest_vars.items() if v.get()]

        if not valid_sid(sid):
            messagebox.showerror("Error", "Student ID must be in format XX-XXXXX (e.g. 21-12345).", parent=self)
            return
        if not name:
            messagebox.showerror("Error", "Full name is required.", parent=self)
            return
        if not is_bsu_email(email):
            messagebox.showerror("Error", "Must use a valid BSU email (@g.batstate-u.edu.ph).", parent=self)
            return
        if len(pw) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.", parent=self)
            return
        if not interests:
            messagebox.showerror("Error", "Please select at least one interest.", parent=self)
            return

        try:
            sb_post("students", {
                "student_id":    sid,
                "name":          name,
                "email":         email,
                "password_hash": hash_pw(pw),
                "interests":     ",".join(interests),
                "role":          "student",
                "joined_at":     ts(),
            })
        except Exception as e:
            messagebox.showerror("Error", f"Student ID or Email already registered.\n{e}", parent=self)
            return

        messagebox.showinfo("Success", f"Welcome, {name}! Your account has been created. 🎉", parent=self)
        student = {"id": sid, "name": name, "email": email,
                   "interests": interests, "role": "student", "joined": ts()}
        self.destroy()
        self.on_success(student)


# ─────────────────────────────────────────────
#  MAIN APPLICATION WINDOW
# ─────────────────────────────────────────────

class AnoTaraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AnoTara?")
        self.geometry("1100x700")
        self.minsize(950, 620)
        self.configure(bg=COLORS["bg"])
        self.student = None
        self._show_auth()

    def _show_auth(self):
        self.withdraw()
        AuthWindow(self, self._on_login)

    def _on_login(self, student):
        self.student = student
        self.deiconify()
        self._build_main()

    def _build_main(self):
        for w in self.winfo_children():
            w.destroy()

        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(self, bg=COLORS["bg"])
        self.content.pack(side="right", fill="both", expand=True)

        self._build_sidebar()
        self._show_dashboard()

    def _build_sidebar(self):
        s = self.student
        tk.Label(self.sidebar, text="🎓 AnoTara?",
                 bg=COLORS["accent"], fg=COLORS["white"],
                 font=("Segoe UI", 13, "bold"), pady=16).pack(fill="x")

        av = tk.Frame(self.sidebar, bg=COLORS["sidebar"], pady=16)
        av.pack(fill="x")
        tk.Label(av, text=s["name"][0].upper(),
                 bg=COLORS["accent2"], fg=COLORS["white"],
                 font=("Segoe UI", 20, "bold"), width=3, height=1).pack()
        tk.Label(av, text=s["name"], bg=COLORS["sidebar"],
                 fg=COLORS["text"], font=FONTS["subhead"]).pack(pady=(6, 2))
        tk.Label(av, text=f"ID: {s['id']}", bg=COLORS["sidebar"],
                 fg=COLORS["subtext"], font=FONTS["small"]).pack()

        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(fill="x", padx=16, pady=8)

        nav_items = [
            ("🏠  Dashboard",     self._show_dashboard),
            ("🏛️  Organizations",  self._show_organizations),
            ("🤝  Peer Matching", self._show_peer_matching),
            ("💬  Chat Room",     self._show_chat),
            ("📊  My Report",     self._show_report),
        ]
        if s.get("role") == "admin":
            nav_items.append(("🛠️  Admin Panel", self._show_admin))

        for label, cmd in nav_items:
            tk.Button(
                self.sidebar, text=label, command=lambda c=cmd: c(),
                bg=COLORS["sidebar"], fg=COLORS["text"],
                font=FONTS["body"], relief="flat",
                anchor="w", padx=24, pady=10,
                activebackground=COLORS["hover"],
                activeforeground=COLORS["white"],
                cursor="hand2",
            ).pack(fill="x")

        tk.Frame(self.sidebar, bg=COLORS["border"], height=1).pack(
            fill="x", padx=16, side="bottom", pady=8)
        tk.Button(
            self.sidebar, text="⏻  Logout", command=self._logout,
            bg=COLORS["sidebar"], fg=COLORS["danger"],
            font=FONTS["body"], relief="flat",
            anchor="w", padx=24, pady=10,
            activebackground=COLORS["sidebar"], cursor="hand2",
        ).pack(fill="x", side="bottom")

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _page_title(self, title, subtitle=""):
        header = tk.Frame(self.content, bg=COLORS["bg"], pady=20)
        header.pack(fill="x", padx=30)
        tk.Label(header, text=title, bg=COLORS["bg"],
                 fg=COLORS["text"], font=FONTS["title"]).pack(anchor="w")
        if subtitle:
            tk.Label(header, text=subtitle, bg=COLORS["bg"],
                     fg=COLORS["subtext"], font=FONTS["body"]).pack(anchor="w")
        tk.Frame(self.content, bg=COLORS["border"], height=1).pack(fill="x", padx=30)

    # ── DASHBOARD ──────────────────────────────
    def _show_dashboard(self):
        self._clear_content()
        s = self.student
        self._page_title(f"Welcome, {s['name'].split()[0]}! 👋",
                         "Here's your activity overview")

        orgs_count  = sb_count("memberships",     {"student_id": f"eq.{s['id']}"})
        msgs_count  = sb_count("chat_messages",    {"sender_id":  f"eq.{s['id']}"})
        peers_count = sb_count("peer_connections", {"student_id": f"eq.{s['id']}"})
        score = orgs_count * 10 + msgs_count * 2 + peers_count * 5

        stats_row = tk.Frame(self.content, bg=COLORS["bg"])
        stats_row.pack(fill="x", padx=30, pady=20)

        for icon, val, lbl, color in [
            ("🏛️", str(orgs_count),  "Orgs Joined",      COLORS["accent"]),
            ("💬", str(msgs_count),  "Messages Sent",    COLORS["accent2"]),
            ("🤝", str(peers_count), "Peers Connected",  COLORS["success"]),
            ("⭐", str(score),       "Engagement Score", COLORS["warning"]),
        ]:
            card = tk.Frame(stats_row, bg=COLORS["card"])
            card.pack(side="left", expand=True, fill="both", padx=6, pady=4)
            tk.Label(card, text=icon, bg=COLORS["card"], font=("Segoe UI", 24)).pack(pady=(18, 0))
            tk.Label(card, text=val, bg=COLORS["card"], fg=color,
                     font=("Segoe UI", 28, "bold")).pack()
            tk.Label(card, text=lbl, bg=COLORS["card"], fg=COLORS["subtext"],
                     font=FONTS["small"]).pack(pady=(0, 18))

        bottom = tk.Frame(self.content, bg=COLORS["bg"])
        bottom.pack(fill="both", expand=True, padx=30, pady=10)

        ic = card_frame(bottom)
        ic.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(ic, text="Your Interests", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(ic, bg=COLORS["border"], height=1).pack(fill="x")
        wrap = tk.Frame(ic, bg=COLORS["card"], padx=16, pady=12)
        wrap.pack(fill="both")
        for interest in s["interests"]:
            tk.Label(wrap, text=f"  {interest}  ",
                     bg=COLORS["accent"], fg=COLORS["white"],
                     font=FONTS["small"], padx=4, pady=3).pack(side="left", padx=3, pady=3)

        ib_card = card_frame(bottom)
        ib_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        tk.Label(ib_card, text="💡 Icebreaker of the Day", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=12, padx=16).pack(anchor="w")
        tk.Frame(ib_card, bg=COLORS["border"], height=1).pack(fill="x")
        ib_text = tk.Label(ib_card, text=random.choice(ICEBREAKERS),
                           bg=COLORS["card"], fg=COLORS["subtext"],
                           font=FONTS["body"], wraplength=280, justify="left", padx=16, pady=16)
        ib_text.pack(anchor="w")
        styled_button(ib_card, "New Prompt 🔄",
                      lambda: ib_text.config(text=random.choice(ICEBREAKERS)),
                      bg=COLORS["card2"], pady=6, padx=14).pack(anchor="w", padx=16, pady=(0, 12))

    # ── ORGANIZATIONS ──────────────────────────
    def _show_organizations(self):
        self._clear_content()
        self._page_title("🏛️ Organization Directory", "Browse and join university organizations")

        joined_rows = sb_get("memberships", {
            "select":     "org_id",
            "student_id": f"eq.{self.student['id']}",
        })
        joined_ids = {r["org_id"] for r in joined_rows}

        bar = tk.Frame(self.content, bg=COLORS["bg"])
        bar.pack(fill="x", padx=30, pady=12)
        tk.Label(bar, text="Category:", bg=COLORS["bg"],
                 fg=COLORS["subtext"], font=FONTS["body"]).pack(side="left")

        cats_raw = sb_get("organizations", {"select": "category"})
        cats = ["All"] + sorted(set(r["category"] for r in cats_raw))

        self._cat_var = tk.StringVar(value="All")
        cat_menu = ttk.Combobox(bar, textvariable=self._cat_var,
                                values=cats, state="readonly", width=18)
        cat_menu.pack(side="left", padx=8)

        outer = tk.Frame(self.content, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=30, pady=8)

        canvas = tk.Canvas(outer, bg=COLORS["bg"], highlightthickness=0)
        sb_scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        org_inner = tk.Frame(canvas, bg=COLORS["bg"])
        cw = canvas.create_window((0, 0), window=org_inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        org_inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        cat_menu.bind("<<ComboboxSelected>>",
                      lambda e: self._refresh_orgs(org_inner, joined_ids))
        self._refresh_orgs(org_inner, joined_ids)

    def _refresh_orgs(self, frame, joined_ids):
        for w in frame.winfo_children():
            w.destroy()

        cat = self._cat_var.get()
        params = {"select": "*", "order": "name"}
        if cat != "All":
            params["category"] = f"eq.{cat}"
        orgs = sb_get("organizations", params)

        for org in orgs:
            org_id   = org["org_id"]
            name     = org["name"]
            category = org["category"]
            desc     = org["description"]
            member_count = sb_count("memberships", {"org_id": f"eq.{org_id}"})
            is_joined = org_id in joined_ids

            card = tk.Frame(frame, bg=COLORS["card"])
            card.pack(fill="x", pady=5)

            left = tk.Frame(card, bg=COLORS["card"])
            left.pack(side="left", fill="both", expand=True, padx=16, pady=14)

            top_row = tk.Frame(left, bg=COLORS["card"])
            top_row.pack(fill="x")
            tk.Label(top_row, text=name, bg=COLORS["card"],
                     fg=COLORS["text"], font=FONTS["subhead"]).pack(side="left")
            tk.Label(top_row, text=f" {category} ",
                     bg=COLORS["accent2"], fg=COLORS["white"],
                     font=FONTS["small"], padx=4).pack(side="left", padx=8)

            tk.Label(left, text=desc, bg=COLORS["card"],
                     fg=COLORS["subtext"], font=FONTS["body"],
                     wraplength=550, justify="left").pack(anchor="w", pady=(4, 2))
            tk.Label(left, text=f"👥 {member_count} members",
                     bg=COLORS["card"], fg=COLORS["subtext"],
                     font=FONTS["small"]).pack(anchor="w")

            btn_frame = tk.Frame(card, bg=COLORS["card"])
            btn_frame.pack(side="right", padx=16)

            if is_joined:
                tk.Label(btn_frame, text="✓ Joined",
                         bg=COLORS["card"], fg=COLORS["success"],
                         font=FONTS["subhead"]).pack()
            else:
                styled_button(btn_frame, "Join", padx=18, pady=6,
                              command=lambda oid=org_id, oname=name: self._join_org(oid, oname, joined_ids, frame)
                              ).pack()

    def _join_org(self, org_id, org_name, joined_ids, frame):
        try:
            sb_post("memberships", {
                "student_id": self.student["id"],
                "org_id":     org_id,
                "joined_at":  ts(),
            })
            joined_ids.add(org_id)
            messagebox.showinfo("Joined!", f"You have joined {org_name}! 🎉")
        except Exception:
            messagebox.showinfo("Info", "You are already a member.")
        self._refresh_orgs(frame, joined_ids)

    # ── PEER MATCHING ──────────────────────────
    def _show_peer_matching(self):
        self._clear_content()
        self._page_title("🤝 Peer Matching", "Find students who share your interests")

        my_interests = set(self.student["interests"])
        sid = self.student["id"]

        connected_ids = {r["peer_id"] for r in sb_get("peer_connections", {
            "select": "peer_id", "student_id": f"eq.{sid}"})}
        connected_ids |= {r["student_id"] for r in sb_get("peer_connections", {
            "select": "student_id", "peer_id": f"eq.{sid}"})}

        all_peers = sb_get("students", {
            "select":     "student_id,name,interests",
            "student_id": f"neq.{sid}",
        })

        matches = []
        for peer in all_peers:
            peer_interests = set(peer["interests"].split(","))
            common = my_interests & peer_interests
            if common:
                matches.append((len(common), peer["student_id"], peer["name"], common))
        matches.sort(reverse=True)

        outer = tk.Frame(self.content, bg=COLORS["bg"])
        outer.pack(fill="both", expand=True, padx=30, pady=12)

        canvas = tk.Canvas(outer, bg=COLORS["bg"], highlightthickness=0)
        sb_scroll = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb_scroll.set)
        sb_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=COLORS["bg"])
        cw = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        if not matches:
            tk.Label(inner, text="No peer matches yet.\nMore students need to register!",
                     bg=COLORS["bg"], fg=COLORS["subtext"],
                     font=FONTS["heading"], justify="center").pack(pady=60)
            return

        for rank, (score, peer_id, peer_name, common) in enumerate(matches[:10], 1):
            card = tk.Frame(inner, bg=COLORS["card"])
            card.pack(fill="x", pady=5)

            left = tk.Frame(card, bg=COLORS["card"])
            left.pack(side="left", fill="both", expand=True, padx=16, pady=14)

            top_row = tk.Frame(left, bg=COLORS["card"])
            top_row.pack(fill="x")
            tk.Label(top_row, text=f"#{rank}  {peer_name}",
                     bg=COLORS["card"], fg=COLORS["text"],
                     font=FONTS["subhead"]).pack(side="left")
            tk.Label(top_row, text=f"  {score} shared interests",
                     bg=COLORS["card"], fg=COLORS["success"],
                     font=FONTS["small"]).pack(side="left", padx=8)

            interests_row = tk.Frame(left, bg=COLORS["card"])
            interests_row.pack(fill="x", pady=(6, 0))
            for interest in list(common)[:6]:
                tk.Label(interests_row, text=f" {interest} ",
                         bg=COLORS["accent"], fg=COLORS["white"],
                         font=FONTS["small"], padx=3, pady=2).pack(side="left", padx=2)

            btn_frame = tk.Frame(card, bg=COLORS["card"])
            btn_frame.pack(side="right", padx=16)

            if peer_id in connected_ids:
                tk.Label(btn_frame, text="✓ Connected",
                         bg=COLORS["card"], fg=COLORS["success"],
                         font=FONTS["subhead"]).pack()
            else:
                styled_button(btn_frame, "Connect", padx=14, pady=6,
                              command=lambda pid=peer_id, pname=peer_name: self._connect_peer(pid, pname, connected_ids)
                              ).pack()

    def _connect_peer(self, peer_id, peer_name, connected_ids):
        try:
            sb_post("peer_connections", {
                "student_id":   self.student["id"],
                "peer_id":      peer_id,
                "connected_at": ts(),
            })
            connected_ids.add(peer_id)
            messagebox.showinfo("Connected!", f"You are now connected with {peer_name}! 🤝")
        except Exception:
            messagebox.showinfo("Info", "Already connected.")
        self._show_peer_matching()

    # ── CHAT ───────────────────────────────────
    def _show_chat(self):
        self._clear_content()
        self._page_title("💬 Global Chat Room", "Connect with fellow students campus-wide")

        main = tk.Frame(self.content, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=30, pady=10)

        ib_frame = tk.Frame(main, bg=COLORS["card2"], width=240)
        ib_frame.pack(side="right", fill="y", padx=(12, 0))
        ib_frame.pack_propagate(False)
        tk.Label(ib_frame, text="💡 Conversation Starters",
                 bg=COLORS["card2"], fg=COLORS["text"],
                 font=FONTS["subhead"], pady=12, padx=10).pack(anchor="w")
        tk.Frame(ib_frame, bg=COLORS["border"], height=1).pack(fill="x")
        self._ib_label = tk.Label(ib_frame, text=random.choice(ICEBREAKERS),
                                   bg=COLORS["card2"], fg=COLORS["subtext"],
                                   font=FONTS["small"], wraplength=210,
                                   justify="left", padx=12, pady=12)
        self._ib_label.pack(anchor="w")
        styled_button(ib_frame, "New Prompt", padx=10, pady=5,
                      bg=COLORS["accent2"],
                      command=lambda: self._ib_label.config(text=random.choice(ICEBREAKERS))
                      ).pack(padx=12, anchor="w")

        chat_frame = tk.Frame(main, bg=COLORS["bg"])
        chat_frame.pack(side="left", fill="both", expand=True)

        self._chat_display = scrolledtext.ScrolledText(
            chat_frame, bg=COLORS["card"], fg=COLORS["text"],
            font=FONTS["body"], relief="flat", state="disabled",
            wrap="word", padx=12, pady=8,
        )
        self._chat_display.pack(fill="both", expand=True)

        input_row = tk.Frame(chat_frame, bg=COLORS["sidebar"], pady=10)
        input_row.pack(fill="x", pady=(8, 0))

        self._chat_entry = tk.Entry(
            input_row, bg=COLORS["input_bg"], fg=COLORS["text"],
            insertbackground=COLORS["text"], font=FONTS["body"],
            relief="flat", bd=0,
        )
        self._chat_entry.pack(side="left", fill="x", expand=True, padx=(12, 8), ipady=8)
        self._chat_entry.bind("<Return>", lambda e: self._send_message())
        styled_button(input_row, "Send ➤", self._send_message,
                      padx=16, pady=8).pack(side="right", padx=12)

        self._load_chat()

    def _load_chat(self):
        msgs = sb_get("chat_messages", {
            "select": "sender_name,message,sent_at",
            "order":  "id.desc",
            "limit":  "50",
        })
        msgs = list(reversed(msgs))

        self._chat_display.configure(state="normal")
        self._chat_display.delete("1.0", "end")
        for row in msgs:
            sender = row["sender_name"]
            msg    = row["message"]
            sent   = row["sent_at"]
            is_me  = sender == self.student["name"]
            prefix = "You" if is_me else sender
            color  = COLORS["accent"] if is_me else COLORS["accent2"]
            self._chat_display.insert("end", f"[{sent}] ", "time")
            self._chat_display.insert("end", f"{prefix}: ", f"s_{sender}")
            self._chat_display.insert("end", f"{msg}\n")
            self._chat_display.tag_config("time", foreground=COLORS["subtext"])
            self._chat_display.tag_config(f"s_{sender}", foreground=color, font=FONTS["label"])

        self._chat_display.configure(state="disabled")
        self._chat_display.see("end")

    def _send_message(self):
        msg = self._chat_entry.get().strip()
        if not msg:
            return
        sb_post("chat_messages", {
            "sender_id":   self.student["id"],
            "sender_name": self.student["name"],
            "message":     msg,
            "sent_at":     ts(),
        })
        self._chat_entry.delete(0, "end")
        self._load_chat()

    # ── REPORT ─────────────────────────────────
    def _show_report(self):
        self._clear_content()
        s = self.student
        self._page_title("📊 My Engagement Report", "Track your campus participation")

        mem_rows = sb_get("memberships", {
            "select":     "org_id,joined_at",
            "student_id": f"eq.{s['id']}",
        })
        joined_orgs = []
        for r in mem_rows:
            org_data = sb_get("organizations", {
                "select": "name,category",
                "org_id": f"eq.{r['org_id']}",
            })
            if org_data:
                joined_orgs.append((org_data[0]["name"], org_data[0]["category"], r["joined_at"]))

        msg_count = sb_count("chat_messages", {"sender_id": f"eq.{s['id']}"})

        peer_rows = sb_get("peer_connections", {
            "select":     "peer_id",
            "student_id": f"eq.{s['id']}",
        })
        connected_peers = []
        for r in peer_rows:
            peer_data = sb_get("students", {
                "select":     "name",
                "student_id": f"eq.{r['peer_id']}",
            })
            if peer_data:
                connected_peers.append(peer_data[0]["name"])

        total_orgs = sb_count("organizations")
        score = len(joined_orgs) * 10 + msg_count * 2 + len(connected_peers) * 5
        pct   = round(len(joined_orgs) / total_orgs * 100, 1) if total_orgs else 0

        main = tk.Frame(self.content, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=30, pady=10)

        profile_card = card_frame(main)
        profile_card.pack(fill="x", pady=(0, 12))
        pc_inner = tk.Frame(profile_card, bg=COLORS["card"], padx=20, pady=16)
        pc_inner.pack(fill="x")
        tk.Label(pc_inner, text=s["name"], bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["heading"]).pack(anchor="w")
        tk.Label(pc_inner, text=f"Student ID: {s['id']}  |  {s['email']}",
                 bg=COLORS["card"], fg=COLORS["subtext"], font=FONTS["body"]).pack(anchor="w")
        tk.Label(pc_inner, text=f"Member since: {s.get('joined', 'N/A')}",
                 bg=COLORS["card"], fg=COLORS["subtext"], font=FONTS["small"]).pack(anchor="w")

        stats_row = tk.Frame(main, bg=COLORS["bg"])
        stats_row.pack(fill="x", pady=8)
        for val, lbl, color in [
            (f"{len(joined_orgs)}/{total_orgs}", "Orgs Joined",   COLORS["accent"]),
            (f"{pct}%",                          "Participation", COLORS["accent2"]),
            (str(msg_count),                     "Messages",      COLORS["success"]),
            (str(len(connected_peers)),           "Peers",         COLORS["warning"]),
            (str(score),                          "Score ⭐",      COLORS["danger"]),
        ]:
            c2 = tk.Frame(stats_row, bg=COLORS["card"])
            c2.pack(side="left", expand=True, fill="both", padx=4)
            tk.Label(c2, text=val, bg=COLORS["card"],
                     fg=color, font=("Segoe UI", 20, "bold"), pady=10).pack()
            tk.Label(c2, text=lbl, bg=COLORS["card"],
                     fg=COLORS["subtext"], font=FONTS["small"]).pack(pady=(0, 10))

        detail_row = tk.Frame(main, bg=COLORS["bg"])
        detail_row.pack(fill="both", expand=True, pady=8)

        orgs_card = card_frame(detail_row)
        orgs_card.pack(side="left", fill="both", expand=True, padx=(0, 6))
        tk.Label(orgs_card, text="Organizations", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=10, padx=14).pack(anchor="w")
        tk.Frame(orgs_card, bg=COLORS["border"], height=1).pack(fill="x")
        for name, cat, joined_at in joined_orgs:
            row = tk.Frame(orgs_card, bg=COLORS["card"])
            row.pack(fill="x", padx=14, pady=4)
            tk.Label(row, text=f"• {name}", bg=COLORS["card"],
                     fg=COLORS["text"], font=FONTS["body"]).pack(side="left")
            tk.Label(row, text=cat, bg=COLORS["card"],
                     fg=COLORS["subtext"], font=FONTS["small"]).pack(side="right")

        peers_card = card_frame(detail_row)
        peers_card.pack(side="right", fill="both", expand=True, padx=(6, 0))
        tk.Label(peers_card, text="Connected Peers", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=10, padx=14).pack(anchor="w")
        tk.Frame(peers_card, bg=COLORS["border"], height=1).pack(fill="x")
        for peer_name in connected_peers:
            tk.Label(peers_card, text=f"• {peer_name}", bg=COLORS["card"],
                     fg=COLORS["text"], font=FONTS["body"], padx=14, pady=4).pack(anchor="w")
        if not connected_peers:
            tk.Label(peers_card, text="No peers connected yet.\nTry Peer Matching!",
                     bg=COLORS["card"], fg=COLORS["subtext"],
                     font=FONTS["body"], padx=14, pady=14).pack(anchor="w")

    # ── ADMIN ──────────────────────────────────
    def _show_admin(self):
        self._clear_content()
        self._page_title("🛠️ Admin Panel", "Platform-wide analytics and management")

        total_students    = sb_count("students")
        total_orgs        = sb_count("organizations")
        total_msgs        = sb_count("chat_messages")
        total_memberships = sb_count("memberships")

        main = tk.Frame(self.content, bg=COLORS["bg"])
        main.pack(fill="both", expand=True, padx=30, pady=10)

        stats_row = tk.Frame(main, bg=COLORS["bg"])
        stats_row.pack(fill="x", pady=(0, 16))
        for val, lbl in [
            (total_students,    "Total Students"),
            (total_orgs,        "Organizations"),
            (total_msgs,        "Chat Messages"),
            (total_memberships, "Total Memberships"),
        ]:
            sc = card_frame(stats_row)
            sc.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(sc, text=str(val), bg=COLORS["card"],
                     fg=COLORS["accent"], font=("Segoe UI", 26, "bold"), pady=10).pack()
            tk.Label(sc, text=lbl, bg=COLORS["card"],
                     fg=COLORS["subtext"], font=FONTS["small"]).pack(pady=(0, 10))

        bottom = tk.Frame(main, bg=COLORS["bg"])
        bottom.pack(fill="both", expand=True)

        ts_card = card_frame(bottom)
        ts_card.pack(side="left", fill="both", expand=True, padx=(0, 8))
        tk.Label(ts_card, text="⭐ Top Students", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=10, padx=14).pack(anchor="w")
        tk.Frame(ts_card, bg=COLORS["border"], height=1).pack(fill="x")

        all_students = sb_get("students", {"select": "student_id,name"})
        leaderboard = []
        for st in all_students:
            sid   = st["student_id"]
            sname = st["name"]
            o = sb_count("memberships",      {"student_id": f"eq.{sid}"})
            m = sb_count("chat_messages",    {"sender_id":  f"eq.{sid}"})
            p = sb_count("peer_connections", {"student_id": f"eq.{sid}"})
            leaderboard.append((o * 10 + m * 2 + p * 5, sname))
        leaderboard.sort(reverse=True)

        for rank, (score, sname) in enumerate(leaderboard[:8], 1):
            row = tk.Frame(ts_card, bg=COLORS["card"])
            row.pack(fill="x", padx=14, pady=4)
            tk.Label(row, text=f"#{rank}  {sname}", bg=COLORS["card"],
                     fg=COLORS["text"], font=FONTS["body"]).pack(side="left")
            tk.Label(row, text=f"{score} pts", bg=COLORS["card"],
                     fg=COLORS["warning"], font=FONTS["small"]).pack(side="right")

        org_card = card_frame(bottom)
        org_card.pack(side="right", fill="both", expand=True, padx=(8, 0))
        tk.Label(org_card, text="🏛️ Organization Membership", bg=COLORS["card"],
                 fg=COLORS["text"], font=FONTS["subhead"], pady=10, padx=14).pack(anchor="w")
        tk.Frame(org_card, bg=COLORS["border"], height=1).pack(fill="x")

        orgs = sb_get("organizations", {"select": "org_id,name"})
        org_counts = [(org["name"], sb_count("memberships", {"org_id": f"eq.{org['org_id']}"}))
                      for org in orgs]
        org_counts.sort(key=lambda x: -x[1])

        for org_name, cnt in org_counts:
            row = tk.Frame(org_card, bg=COLORS["card"])
            row.pack(fill="x", padx=14, pady=4)
            tk.Label(row, text=org_name, bg=COLORS["card"],
                     fg=COLORS["text"], font=FONTS["body"]).pack(side="left")
            tk.Label(row, text=f"{cnt} members", bg=COLORS["card"],
                     fg=COLORS["subtext"], font=FONTS["small"]).pack(side="right")

    # ── LOGOUT ─────────────────────────────────
    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.student = None
            for w in self.winfo_children():
                w.destroy()
            self._show_auth()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = AnoTaraApp()
    app.mainloop()