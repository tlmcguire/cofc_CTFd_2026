# Setup & Hosting Guide — CofC Cybersecurity Club Open House 2026

This covers standing up CTFd itself for the club's Open House event, adding the
challenge set from [`CTFd/challenges/CHALLENGES.md`](CTFd/challenges/CHALLENGES.md), and
running the event on the day. Solutions for every challenge are in
[`CTFd/challenges/SOLUTIONS.md`](CTFd/challenges/SOLUTIONS.md) — don't publish that file
anywhere members can see it before or during the event.

## 1. What you need

**Hardware:** nothing special. This is a single-session event for a club-sized group
(tens of people, not thousands), and CTFd itself is lightweight. Any of the following
will comfortably run the whole thing:

- Any laptop from the last ~8 years (2+ CPU cores, 4 GB+ RAM free) — including the one
  you're presenting from. Fine for an in-room event over the club's wifi.
- A cheap cloud VPS — 1–2 vCPU / 2 GB RAM (e.g. the smallest DigitalOcean droplet,
  Linode Nanode, or an AWS `t3.micro`) is comfortable headroom for this size of group.
  This is the better option if you want members to be able to keep playing after the
  meeting ends, from home, without your laptop staying on.
- Officers' desks/dorm rooms: don't overthink this — you do **not** need a rack server
  or anything from the "Hardware Option" line items in the semester schedule for this
  particular event. Those are for later weeks (physical lab, Proxmox, a domain
  controller, etc.) — this is just a web app.

**Software:**
- Docker + Docker Compose (recommended path — see below), **or** Python 3.11 and MySQL/
  MariaDB + Redis installed directly if you'd rather not use Docker.
- Any modern browser, for both hosting/admin and for players.

**Network:**
- If hosting on a laptop for an in-room event: everyone needs to be able to reach that
  laptop's IP address on the club's wifi. Confirm the venue's wifi doesn't isolate
  clients from each other (some university guest/eduroam networks do — ask IT or test
  ahead of time). If it's isolated, use the VPS option instead so everyone just hits a
  public URL.
- If hosting on a VPS: point a subdomain at it if you have one, or just hand out the
  IP address (`http://<vps-ip>:8000`). A real domain + HTTPS is nice-to-have, not
  required for a one-off club event.

## 2. Quickest path: Docker Compose

This repo already has a working `docker-compose.yml` (CTFd + MariaDB + Redis + nginx).
From the repo root:

```bash
docker compose up -d
```

First run will build the image and pull `mariadb`/`redis`/`nginx`, which takes a few
minutes. Once it's up:

- Visit `http://localhost` (nginx is on port 80) or `http://localhost:8000` (CTFd
  directly) from the host machine.
- From another device on the same network, replace `localhost` with the host machine's
  LAN IP (`ipconfig getifaddr en0` on macOS, `hostname -I` on Linux, `ipconfig` on
  Windows).

On Windows, install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
first (it includes Compose); the same `docker compose up -d` command works identically
in PowerShell or a WSL2 terminal.

To stop everything: `docker compose down`. Note that this repo's `docker-compose.yml`
stores the database and uploads in host folders under `.data/` (bind mounts), not
Docker-managed volumes — so `docker compose down -v` does **not** actually reset
anything here, and it's safe to run without wiping your event. To do a real full reset
(e.g. between semesters, or between test runs), stop the stack and delete that folder:

```bash
docker compose down
rm -rf .data
docker compose up -d
```

That brings back the first-run setup wizard from a genuinely clean database.

## 3. Fastest path for testing: skip the wizard entirely

If you just want to confirm the challenge set works — without clicking through the
setup wizard, creating an admin account, or adding all 33 challenges by hand — there's
a script that does all of that for you:

```bash
docker compose up -d
python3 scripts/seed_dev_ctf.py
```

This talks to the CTFd instance over HTTP (same as a browser would) and:

- Runs first-time setup if needed (or logs in if it's already done), using a fixed,
  clearly-labeled **dev-only** account: `admin` / `ChangeMe123!`.
- Forces challenge/score/account/registration visibility to **public**, so
  `http://localhost:8000/challenges` is browsable with no login at all.
- Creates every challenge from `CHALLENGES.md` via the API — name, category,
  description, points, flag, and attached file(s) — skipping any that already exist,
  so it's safe to re-run after you change a challenge file.

It's plain Python 3 standard library (no `pip install` needed) and only ever talks to
`http://localhost:8000` by default; pass a different URL as an argument if you've
changed the port. This is a development convenience only — for the actual event, follow
sections 5–6 below and pick your own admin password and visibility settings.

Verified end-to-end while writing this doc: fresh instance → run the script → all 33
challenges appear across 7 categories on `/challenges` with no login → registering a
normal player account and submitting each flag through the real CTFd API returns
`"status": "correct"` (and a deliberately wrong flag correctly comes back
`"status": "incorrect"`) → branding (name, logo, favicon, maroon/gold/teal color theme)
confirmed live in both light and dark mode.

## 4. Alternative: running without Docker

If Docker isn't available (locked-down lab machine, etc.), CTFd can run directly with
Python, backed by SQLite instead of MySQL for something this small:

```bash
pip install -r requirements.txt
python serve.py
```

This uses the default `CTFd/config.ini`, which is fine for a single-event, non-critical
deployment. It listens on `http://localhost:8000` by default. This path is only
recommended for a quick local test/dry-run before the event, not for the live event
itself — the Docker Compose path is more representative of a real deployment and easier
to reset cleanly.

## 5. First-run setup

On first visit, CTFd walks you through a setup wizard:

1. **Event name** — "CofC Cybersecurity Club Open House 2026," or whatever the current
   event is actually called.
2. **Admin account** — this is your organizer login; use a real password, this account
   can see every flag and every player's answers.
3. **User Mode** (Team Mode vs. User Mode) — for a first meeting where people don't know
   each other yet, **User Mode** (play as yourself, no teams) is usually the friendlier
   default; switch to **Team Mode** in later, more competitive events once the club has
   established teams.
4. **Visibility settings** — for an in-room event, "Public" scoreboard visibility is
   fine; you can hide challenges/scores from outsiders in Admin → Config → Visibility
   if you want it locked to logged-in members only.
5. Skip the logo/theme/Mail server steps for now — none of that matters for a single
   session. You can revisit Admin → Config any time.

## 6. Adding the challenges

There's no bulk-import file — the assets under `CTFd/challenges/` are just raw files,
not a CTFd export. For each row in
[`CHALLENGES.md`](CTFd/challenges/CHALLENGES.md), in the admin panel:

1. **Admin Panel → Challenges → + (Create)**
2. Pick a challenge type — **Standard** is correct for everything in this set.
3. Fill in **Name**, **Category**, **Points** (suggestions are in the table), and paste
   the description/flavor text from `CHALLENGES.md` into the **Description** field
   (Markdown is supported).
4. Under **Flags**, add one flag with type **Static**, exact match, and paste in the
   flag string from `CHALLENGES.md` (or read it straight from the corresponding file in
   `CTFd/challenges/flags/` — they match).
5. Under **Files**, upload the file(s) listed for that challenge so players can
   download them from the challenge page.
6. Save, then repeat for the rest. Budget about 45–60 minutes to create all 33.

A few challenges need a slightly different touch than "just attach the file":

- **Binary Search Game** — attach both `binary_challenge.sh` and
  `binary_challenge.bat` so players grab whichever matches their OS.
- **Static Analysis 101** — attach `static`, `ltdis.sh`, and `ltdis.bat` together.
- **Rockstar** — attach `lyrics.txt` and mention in the description that it should be
  pasted into <https://codewithrockstar.com/online> (an internet-connected browser is
  the only "tool" needed).
- **Bytecode Blues** — mention the required Python version (3.14.x) in the description
  so players aren't confused by a magic-number mismatch error; see `SOLUTIONS.md` for
  the exact wording.

Once everything's added, do a full pass yourself: download each file fresh from the
player-facing challenge page (not from your local repo checkout) and confirm the flag
you expect actually solves it. This catches upload mistakes (wrong file, stale version)
before members hit them live.

## 7. Branding

The event name, logo, favicon, and color theme all come from the club's official
"Design Components" deck, which is itself aligned with the College of Charleston's
brand guidelines (charleston.edu/marketing-communications) — maroon and gold as
primary, teal/mint as secondary, Cambria for headings, Calibri for body text. The
assets and the reasoning behind each color choice live in `CTFd/branding/`:

- `CTFd/branding/logos/` — the official logo lockups (horizontal, stacked, vertical;
  each in a light-background and a dark-background version), plus a cropped 32×32
  favicon.
- `CTFd/branding/theme.css` — the full color/typography override, with a comment
  explaining each choice (in particular: why dark mode uses mint/teal accents instead
  of a darkened maroon — the deck's own guidance is to never pair maroon with black
  alone).

`scripts/seed_dev_ctf.py` applies all of this automatically on the dev/test instance
(see `apply_branding()` in that script) — that's the fastest way to see it rendered
before deciding whether to use it as-is. To apply it to the real event instance by
hand:

1. **Event name**: already set during first-run setup (step 5 above) if you used the
   current official name. To change it later: Admin Panel → Config → General → **Event
   Name**.
2. **Logo**: Admin Panel → Config → General → **Style** tab → upload
   `CTFd/branding/logos/logo-horizontal-white.png` as the CTF Logo (white/dark-bg
   version — the navbar is maroon, so the light-background "-maroon" logos won't have
   enough contrast there).
3. **Favicon**: same Style tab → upload `CTFd/branding/logos/favicon-32.png` as the
   Small Icon (CTFd requires exactly 32×32).
4. **Full color theme**: Admin Panel → Config → General → **Style** tab → paste the
   contents of `CTFd/branding/theme.css`, wrapped in a `<style>...</style>` tag, into
   the **Theme Header** field. This is what actually recolors buttons, links, cards,
   and the navbar/header band — the single "Theme Color" field only controls one
   fallback color and isn't enough on its own.

Check both the light and dark theme (the moon icon in the navbar toggles it) after
applying — the CSS handles both, but it's worth a visual check since CTFd's built-in
dark mode is the default for most browsers/OS settings.

## 8. Running the event

- Post the URL and a QR code (most phone cameras scan QR codes natively) at the start
  of the meeting.
- Have officers/alumni float the room rather than sit at the front — most early
  questions are "is this the right encoding?" sanity checks, not stuck-for-an-hour
  problems, given the difficulty curve here.
- Consider disabling public registration afterward (Admin → Config) if you want the
  instance to keep existing for people to review solves, without new signups trickling
  in indefinitely.
- If you want the CTF to stay up after the meeting for members to keep practicing, the
  VPS option means you don't need to keep a laptop running — just leave the container
  up (`docker compose up -d` already runs detached).

## 9. Backing up / resetting for next time

- **Export everything** (all challenges, users, submissions): Admin Panel → Config →
  **Backup** tab → **Import & Export** — downloads a `.zip` you can keep or restore
  later via the same tab (or the repo's `import.py` script).
- To fully reset between semesters/events: export first (above) if you want an
  archive, then `docker compose down && rm -rf .data && docker compose up -d` gives you
  a genuinely clean instance and you'll see the first-run setup wizard again (see the
  note in section 2 — `-v` alone doesn't do this for this repo's compose setup).
