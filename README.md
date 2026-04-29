# 🎓 AnoTara? — University Exclusive Engagement Platform

> A Python desktop application built with **Tkinter** (UI) and **Supabase** (cloud PostgreSQL database) that helps college students — especially introverts — discover organizations, connect with peers, and practice communication within a university-exclusive environment.

**Batangas State University | College of Informatics and Computing Sciences | CICS Alangilan**

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Supabase Setup](#-supabase-setup)
- [Usage Guide](#-usage-guide)
- [Database Schema](#-database-schema)
- [Data Structures Used](#-data-structures-used)
- [Program Flow](#-program-flow)
- [Project Structure](#-project-structure)
- [Contributors](#-contributors)

---

## 🌐 Overview

UniConnect solves three core problems faced by college students:

| Problem | Solution |
|---|---|
| Hard to find organizations | Searchable, category-filtered organization directory |
| Poor communication channels | Global chat room with guided icebreaker prompts |
| Difficulty finding peers | Interest-based peer matching ranked by shared affinities |

Access is restricted to **BSU university email addresses only** (`@g.batstate-u.edu.ph` / `@batstate-u.edu.ph`), ensuring a safe and exclusive campus environment.

---

## ✨ Features

### 🔐 Authentication
- Student registration with BSU university email domain validation
- Student ID format validation (`YY-XXXXX`, e.g. `21-12345`)
- SHA-256 password hashing — no plain-text passwords stored
- Persistent login backed by Supabase cloud database

### 🏠 Dashboard
- Live stat cards: orgs joined, messages sent, peers connected, engagement score
- Personal interest tags displayed as visual badges
- Daily icebreaker prompt (refreshable with one click)

### 🏛️ Organization Directory
- Browse all university organizations
- Filter by category: Academic, Technology, Arts, Advocacy, Communication, Leadership
- Live member count per organization
- One-click join with instant UI refresh

### 🤝 Peer Matching
- Uses **Python set intersection** to find students with shared interests
- Ranked by number of common interests (highest match first)
- Interest tags displayed as visual badges per peer card
- Connect with peers — stored permanently in Supabase

### 💬 Communication Hub
- Global campus chat room — all messages stored in Supabase
- Send messages with the Enter key or the Send button
- Color-coded messages: your messages vs others
- Sidebar with refreshable icebreaker and conversation starter prompts

### 📊 Engagement Report
- Full personal breakdown: orgs joined, messages sent, peers connected
- Participation rate vs total organizations
- Engagement Score formula: `(orgs × 10) + (messages × 2) + (peers × 5)`

### 🛠️ Admin Panel
- Platform-wide statistics at a glance
- Top 8 students leaderboard sorted by engagement score
- Per-organization member count sorted by most popular

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.8+ |
| **UI Framework** | Tkinter + ttk (built-in) |
| **Database** | Supabase (PostgreSQL) via REST API |
| **HTTP Client** | `urllib` (Python standard library) |
| **Security** | `hashlib` SHA-256 password hashing |
| **External Dependencies** | ❌ None — 100% Python standard library |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher**
- Tkinter (bundled with Python on Windows/macOS)
- A Supabase account and project (free tier works)

> **Linux users:** If tkinter is missing, run:
> ```bash
> sudo apt-get install python3-tk
> ```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/uniconnect.git
cd uniconnect

# 2. No pip install needed — runs entirely on standard library
python main.py
```

---

## 🗄️ Supabase Setup

Before running the app, you need to configure your Supabase database.

### Step 1 — Create a Supabase Project
1. Go to [supabase.com](https://supabase.com) and sign up for a free account
2. Create a new project and copy your **Project URL** and **anon key**

### Step 2 — Create the Tables
1. In your Supabase Dashboard, click **SQL Editor** (the `>_` icon in the sidebar)
2. Click **New query**, paste the SQL below, then click **Run**

```sql
-- Students
CREATE TABLE IF NOT EXISTS students (
    student_id    TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    interests     TEXT NOT NULL,
    role          TEXT DEFAULT 'student',
    joined_at     TEXT NOT NULL
);

-- Organizations
CREATE TABLE IF NOT EXISTS organizations (
    org_id      TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT NOT NULL,
    description TEXT NOT NULL
);

-- Memberships (student ↔ organization)
CREATE TABLE IF NOT EXISTS memberships (
    student_id TEXT REFERENCES students(student_id),
    org_id     TEXT REFERENCES organizations(org_id),
    joined_at  TEXT NOT NULL,
    PRIMARY KEY (student_id, org_id)
);

-- Peer connections
CREATE TABLE IF NOT EXISTS peer_connections (
    student_id   TEXT REFERENCES students(student_id),
    peer_id      TEXT REFERENCES students(student_id),
    connected_at TEXT NOT NULL,
    PRIMARY KEY (student_id, peer_id)
);

-- Chat messages
CREATE TABLE IF NOT EXISTS chat_messages (
    id          BIGSERIAL PRIMARY KEY,
    sender_id   TEXT NOT NULL,
    sender_name TEXT NOT NULL,
    message     TEXT NOT NULL,
    sent_at     TEXT NOT NULL
);

-- Seed organizations
INSERT INTO organizations (org_id, name, category, description) VALUES
  ('ORG001','Computer Science Society','Academic','A community for CS enthusiasts to collaborate on tech projects and hackathons.'),
  ('ORG002','Robotics Club','Technology','Build and program robots for competitions and real-world innovation challenges.'),
  ('ORG003','Math Wizards','Academic','Sharpen problem-solving skills through competitions and collaborative workshops.'),
  ('ORG004','Photography Guild','Arts','Capture moments, learn composition, and grow your photography skills together.'),
  ('ORG005','Environmental Advocates','Advocacy','Drive sustainability initiatives and environmental campaigns across campus.'),
  ('ORG006','Debate Society','Communication','Sharpen critical thinking, research skills, and public speaking confidence.'),
  ('ORG007','Game Developers Circle','Technology','Design, develop, and publish games from scratch using modern game engines.'),
  ('ORG008','Student Leaders Forum','Leadership','Develop leadership skills through community service and campus governance.'),
  ('ORG009','Music Ensemble','Arts','Play, compose, and perform music with fellow student musicians on campus.'),
  ('ORG010','Research & Innovation Hub','Academic','Conduct research projects and present findings at academic conferences.')
ON CONFLICT (org_id) DO NOTHING;

-- Disable Row Level Security (for development)
ALTER TABLE students         DISABLE ROW LEVEL SECURITY;
ALTER TABLE organizations    DISABLE ROW LEVEL SECURITY;
ALTER TABLE memberships      DISABLE ROW LEVEL SECURITY;
ALTER TABLE peer_connections DISABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages    DISABLE ROW LEVEL SECURITY;
```

### Step 3 — Add Your Keys to the App

Open `main.py` and update the config section near the top:

```python
SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key"
```

Find these values at:
> **Supabase Dashboard → Project Settings → API Keys → Legacy anon / service_role keys**

### Step 4 — Run

```bash
python main.py
```

---

## 📖 Usage Guide

### Register a New Account
1. Launch the app → click **"Don't have an account? Register"**
2. Enter Student ID in `YY-XXXXX` format (e.g. `21-12345`)
3. Enter your full name
4. Enter BSU email: `yourname@g.batstate-u.edu.ph`
5. Set a password (min 6 characters)
6. Select at least one interest
7. Click **Create Account**

### Login
1. Enter Student ID in `YY-XXXXX` format
2. Enter password
3. Click **Sign In**

### Promote a Student to Admin
Run this in the Supabase SQL Editor:
```sql
UPDATE students SET role = 'admin' WHERE student_id = 'YY-XXXXX';
```
Re-login to see the **Admin Panel** appear in the sidebar.

---

## 🗄️ Database Schema

```
students
├── student_id    TEXT  PK   (format: YY-XXXXX)
├── name          TEXT
├── email         TEXT  UNIQUE
├── password_hash TEXT       (SHA-256 hashed)
├── interests     TEXT       (comma-separated list)
├── role          TEXT       ('student' | 'admin')
└── joined_at     TEXT

organizations
├── org_id       TEXT  PK
├── name         TEXT
├── category     TEXT
└── description  TEXT

memberships
├── student_id   TEXT  FK → students
├── org_id       TEXT  FK → organizations
└── joined_at    TEXT

peer_connections
├── student_id   TEXT  FK → students
├── peer_id      TEXT  FK → students
└── connected_at TEXT

chat_messages
├── id           BIGSERIAL  PK  (auto-increment)
├── sender_id    TEXT
├── sender_name  TEXT
├── message      TEXT
└── sent_at      TEXT
```

---

## 🗂️ Data Structures Used

| Structure | Usage in Code | Justification |
|---|---|---|
| `dict` | Student session object, color/font constants, HTTP headers | O(1) key lookups; natural key-value mapping |
| `list` | Organization cards, chat messages, leaderboard entries, icebreakers | Ordered; supports sorting and iteration |
| `set` | Interest intersection in peer matching (`my_interests & peer_interests`) | Efficient `&` operator to find common items without duplicates |
| `tuple` | Org data rows, leaderboard entries before sorting | Immutable; safe for sorting and comparison |

---

## 🔄 Program Flow

```
START
  │
  ▼
UniConnectApp.__init__()
  └── _show_auth()  ←  hides main window, opens AuthWindow
        │
        ├── [Login]
        │     ├── validate Student ID format (YY-XXXXX)
        │     ├── sb_get("students") → match ID + hashed PW
        │     └── on success → _on_login(student)
        │
        └── [Register]
              ├── validate email domain, ID format, PW length, interests
              ├── sb_post("students") → insert new record into Supabase
              └── on success → _on_login(student)

_on_login(student)
  └── _build_main()
        ├── _build_sidebar()      ← Nav buttons + user avatar
        └── _show_dashboard()     ← Default landing page

Sidebar Navigation
  │
  ├── _show_dashboard()
  │     └── sb_count() × 3 → render stat cards + icebreaker widget
  │
  ├── _show_organizations()
  │     ├── sb_get("memberships")  → get student's joined orgs
  │     ├── sb_get("organizations") → filtered by category
  │     └── _join_org() → sb_post("memberships")
  │
  ├── _show_peer_matching()
  │     ├── sb_get("students") → all other registered students
  │     ├── set intersection (my_interests & peer_interests) → ranked list
  │     └── _connect_peer() → sb_post("peer_connections")
  │
  ├── _show_chat()
  │     ├── _load_chat() → sb_get("chat_messages", order by id)
  │     └── _send_message() → sb_post("chat_messages") → reload
  │
  ├── _show_report()
  │     └── sb_get() + sb_count() → aggregate personal stats and score
  │
  └── _show_admin()  [admin role only]
        └── sb_count() + sb_get() → platform-wide analytics + leaderboard
```

---

## 📁 Project Structure

```
uniconnect/
├── main.py        # Entire application — UI, Supabase REST, all logic
├── README.md      # This file
└── .gitignore
```

### Recommended `.gitignore`
```
__pycache__/
*.pyc
.env
*.db
```

> ⚠️ Never commit your `SUPABASE_KEY` to a public repository. Consider using a `.env` file and loading it with `os.environ` for production use.

---

## 🧩 Module Reference

| Function / Class | Description |
|---|---|
| `sb_get(table, params)` | GET rows from Supabase table via REST API |
| `sb_post(table, data)` | INSERT a new row into a Supabase table |
| `sb_count(table, params)` | Count matching rows using the `Content-Range` header |
| `hash_pw(pw)` | Returns SHA-256 hash of a password string |
| `valid_sid(sid)` | Validates Student ID format `YY-XXXXX` |
| `is_bsu_email(email)` | Checks for valid BSU email domain |
| `AuthWindow` | Tkinter `Toplevel` for login and registration flows |
| `UniConnectApp` | Main `Tk` application with sidebar navigation |
| `_show_dashboard()` | Live stat cards, interest tags, icebreaker widget |
| `_show_organizations()` | Filterable org directory with join functionality |
| `_refresh_orgs()` | Re-renders org cards on category filter change |
| `_join_org()` | Posts new membership to Supabase, refreshes list |
| `_show_peer_matching()` | Set-intersection peer ranking and connect flow |
| `_connect_peer()` | Posts peer connection record to Supabase |
| `_show_chat()` | Global chat room with scrolled text display |
| `_send_message()` | Posts message to Supabase and reloads chat |
| `_show_report()` | Aggregated personal engagement report |
| `_show_admin()` | Admin-only analytics panel with leaderboard |

---

## 📌 Objectives Fulfilled

- [x] **Centralized Organization Listings** — Searchable, category-filtered directory
- [x] **Facilitate Communication** — Guided icebreaker prompts + persistent global chat
- [x] **Enable Peer Matching** — Interest-based suggestions with connect feature
- [x] **Secure Authentication** — BSU email validation + SHA-256 hashed passwords
- [x] **Engagement Tracking** — Full report with score, orgs, peers, and messages
- [x] **Cloud Database** — Supabase PostgreSQL — data persists across all sessions and devices
- [x] **Graphical UI** — Full Tkinter desktop interface with dark theme
- [x] **Zero External Dependencies** — Only Python standard library required to run

---

## 👥 Contributors

**Batangas State University**
College of Informatics and Computing Sciences | CICS Alangilan
Course: *Introduction to Computing / Python Programming*

---

## 📄 License

This project is developed for **academic purposes only**.
© Batangas State University — College of Informatics and Computing Sciences
