# CofC Cyber Club — Kickoff CTF Challenge Set

This is the challenge set for the Week 1–2 "Introduction to the Club & CTF Basics" meeting.
It's meant to be a simple, welcoming introductory CTF that covers foundational computer
science and light security concepts — most challenges are easy/medium, with a couple of
harder ones for members who want to push further. Everything here can be solved on a
laptop running macOS, Windows, or Linux with nothing more than a terminal, Python 3, and
(for a couple of challenges) an unzip tool, an image viewer, an audio player, or a
browser — all things that already ship with the OS.

**Category order below follows the semester schedule.** Code Execution/Misc is this
event's own topic; Linux Fundamentals, Networking, and Web line up with the Tuesday/
Thursday topics coming up in Weeks 3–19, so solving through the categories in order
gives new members a short, low-stakes preview of where the semester is headed.
Cryptography, Forensics, and OSINT are threaded throughout the whole set since they're
foundational skills rather than a single week's topic.

None of this is wired into CTFd's database automatically — there's no bulk-import file
in this repo. You (the organizer) create each challenge by hand in the CTFd admin panel:
**Admin Panel → Challenges → Create**, fill in the fields below, attach the listed
file(s), and paste in the flag. See [`../../SETUP.md`](../../SETUP.md) at the repo root
for how to stand up CTFd itself and for step-by-step instructions on adding challenges —
including a script that does all of this for you on a local test instance.

Solve walkthroughs for every challenge (for you to check against, or to hand out after
the event / to hint-givers) are in [`SOLUTIONS.md`](SOLUTIONS.md).

Point values below are suggestions for a dynamic or static scoring setup — tune to taste.

---

## Code Execution / Misc — this meeting's own topic

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| First Script | Easy | 50 | `Code_Execution/puzzle_script/run_me.py` |
| Environment Check | Easy | 75 | `Code_Execution/environment_check/check.py` |
| Binary Search Game | Easy | 100 | `Code_Execution/binary_challenge/binary_challenge.sh`, `binary_challenge.bat` (see note below) |
| One Line Off | Easy | 100 | `Code_Execution/one_line_off/broken.py` |
| Look, Don't Touch | Easy | 100 | `Code_Execution/static_challenge/static`, `ltdis.sh`, `ltdis.bat` |
| Bytecode Blues | Medium | 150 | `Code_Execution/bytecode_blues/challenge.pyc` |
| Rockstar | Medium | 200 | `Code_Execution/rockstars/lyrics.txt` |
| Keygen | **Medium/Hard** | 350 | `Code_Execution/keygen/keygen.py` |

**Note on Binary Search Game:** attach *both* `binary_challenge.sh` and
`binary_challenge.bat` to the same challenge. macOS/Linux players run the `.sh` in a
terminal (`bash binary_challenge.sh`); Windows players double-click or run the `.bat`
in Command Prompt. Same game, same flag, OS-appropriate script — nobody needs WSL or a
second OS to play.

**Note on Look, Don't Touch:** the `static` file is a Linux ELF binary and will not
*execute* on Windows or Apple Silicon Macs — that's fine, it isn't meant to be run.
The challenge only requires basic file inspection (`strings`, a hex viewer, or the
provided `ltdis.sh`/`ltdis.bat` helper), which works identically on all three OSes.

### First Script
> A short Python file. See what it does.

Flag: `cofc{ju5t_run_1t}`

### Environment Check
> This script isn't ready to talk yet.

Flag: `cofc{env_v4rs_m4tter}`

### Binary Search Game
> We're thinking of a number between 1 and 1000. Ten guesses. `nc <host> <port>` to
> play, or run the attached script directly.

Flag: `cofc{10110101001}`

### One Line Off
> This doesn't run.

Flag: `cofc{f1x3d_1t}`

### Look, Don't Touch
> A compiled program. You may not need to run it.

Flag: `cofc{red_herring}`

### Bytecode Blues
> No source, just the compiled file. Requires Python 3.14.x — see `SOLUTIONS.md`
> if yours is different.

Flag: `cofc{pyc_1s_st1ll_c0de}`

### Rockstar
> The file looks like song lyrics.

Flag: `cofc{rocknr0113r}`

### Keygen
> This program is picky about its password.

Flag: `cofc{y0u_r3versed_the_l09ic}`

---

## Linux Fundamentals — previews Weeks 3–4 (command line & file systems)

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| Hide and Seek | Easy | 75 | `Linux_Fundamentals/hide_and_seek/clubhouse.zip` |
| Needle in a Haystack | Easy | 100 | `Linux_Fundamentals/haystack/logs.zip` |

### Hide and Seek
> An archive of an old shared folder.

Flag: `cofc{hidden_files_arent_hidden}`

### Needle in a Haystack
> A pile of old log files. One line doesn't belong.

Flag: `cofc{grep_dash_r_saves_time}`

---

## Networking — previews Weeks 5–6 and 11–12 (networking basics & traffic analysis)

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| Subnet Math | Easy | 75 | `Networking/subnet_math/prompt.txt` |
| Sniffed | Medium | 150 | `Networking/sniffed/capture.pcap` |

### Subnet Math
> An address for one of the club's laptops.

Flag: `cofc{broadcast_10_42_17_255}`

### Sniffed
> A short recording of network traffic.

Flag: `cofc{pack3ts_dont_l13}`

---

## Web — previews Weeks 18–19 (web & database server setup)

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| View Source | Easy | 50 | `Web/view_source/index.html` |

### View Source
> A page that doesn't do much.

Flag: `cofc{ctrl_u_is_ur_friend}`

---

## Cryptography

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| The Numbers | Easy | 50 | `Cryptography/the_numbers.txt` |
| What's This? | Easy | 75 | `Cryptography/whats_this.txt` |
| Hex Appeal | Easy | 50 | `Cryptography/hex_appeal/message.txt` |
| Layers | Easy | 75 | `Cryptography/layers/layers.txt` |
| Repeat After Me | Medium | 150 | `Cryptography/vigenere/cipher.txt` |
| Between the Lines | Medium | 200 | `Cryptography/substitution/message.txt` |
| Crib Drag | Medium | 200 | `Cryptography/xor_crib/message.bin` |
| Small Fry | **Hard** | 400 | `Cryptography/rsa_small/params.txt` |

### The Numbers
> Left behind after the last meeting.

Flag: `cofc{somanynumbers}`

### What's This?
> Twenty-some lines that look almost identical. Only one of them is readable.

Flag: `cofc{areyoulikingciphers}`

### Hex Appeal
> Another leftover note. Different alphabet this time.

Flag: `cofc{hex_is_just_base16}`

### Layers
> Wrapped more than once.

Flag: `cofc{ea5y_a5_1_2_3}`

### Repeat After Me
> Another coded note.

Flag: `cofc{v1gen3re_is_c00l}`

### Between the Lines
> A paragraph about the club that reads a little wrong.

Flag: `cofc{freq_u3ncy_an4lysis}`

### Crib Drag
> An intercepted message.

Flag: `cofc{kn0wn_pla1ntext_att4ck}`

### Small Fry
> A keypair generated without much thought for size.

Flag: `cofc{rs4_1s_ju5t_m4th}`

---

## Forensics

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| Broken File | Easy | 100 | `Forensics/Broken_File/ZmxhZw==.encr` |
| Behind the Picture | Easy | 75 | `Forensics/Exif_cellent/welcome.png` |
| Scan Me | Easy | 75 | `Forensics/Scan_Me/flyer.png` |
| Mystery File | Easy | 100 | `Forensics/Mystery_File/artifact.bin` |
| Won't Open | Easy/Medium | 150 | `Forensics/Magic_Bytes/picture.png` |
| Zip Lock | Medium | 175 | `Forensics/Zip_Lock/secure.zip` |
| On the Air | Medium | 200 | `Forensics/On_the_Air/transmission.wav` |
| Hidden in Plain Sight | Medium | 225 | `Forensics/Hidden_in_Plain_Sight/sunset.png` |

### Broken File
> The name looks encoded. The contents don't look right either.

Flag: `cofc{g0od_w0rk_d3t3ct!ve}`

### Behind the Picture
> An old photo, posted without much thought.

Flag: `cofc{m3tadata_m4tters}`

### Scan Me
> Printed for a flyer, never explained.

Flag: `cofc{qr_c0des_are_ne4t}`

### Mystery File
> A file with an extension that means nothing.

Flag: `cofc{ext3nsions_ar3_ju5t_lab3ls}`

### Won't Open
> This file refuses to open in anything.

Flag: `cofc{sign4tures_matt3r}`

### Zip Lock
> Password protected, and not with much of one.

Flag: `cofc{brut3_f0rc3_zip}`

### On the Air
> An old recording from the club's radio night.

Flag: `cofc{dit_dah_flag}`

### Hidden in Plain Sight
> A decent enough photo. Look closer.

Flag: `cofc{ste90_10_the_r3scue}`

---

## OSINT

Real places, real history, nobody's actual accounts or personal information. A search
engine and a map get you through this section. This is also the one place in the event
where knowing something off the top of your head is worth as much as knowing how to
run a script.

| Challenge | Difficulty | Suggested Points | Files to attach |
|---|---|---|---|
| Boarding Pass | Medium | 150 | `OSINT/boarding_pass/boarding_pass.png` |
| Low Tide | Medium | 150 | `OSINT/low_tide/note.txt` |
| Trivia Run | Easy | 100 | `OSINT/trivia_run/questions.txt` |

### Boarding Pass
> A torn boarding pass. Most of it is blacked out.

Flag: `cofc{knoxville}`

### Low Tide
> Coordinates from an old flight log, and a line about the schedule.

Flag: `cofc{brr}`

### Trivia Run
> Three short questions about how this all started.

Flag: `cofc{1999_1988_cfaa}`

---

## Suggested play order for a 60–90 minute kickoff session

Following the category order above tracks the semester's own arc, so it's a reasonable
default sequence. Within each category, easiest first:

1. **Code Execution / Misc** — First Script → Environment Check → Binary Search Game →
   One Line Off → Look, Don't Touch → Bytecode Blues → Rockstar → Keygen
2. **Linux Fundamentals** — Hide and Seek → Needle in a Haystack
3. **Networking** — Subnet Math → Sniffed
4. **Web** — View Source
5. **Cryptography** — The Numbers → Hex Appeal → What's This? → Layers → Repeat After
   Me → Crib Drag → Between the Lines → Small Fry
6. **Forensics** — Behind the Picture → Scan Me → Broken File → Mystery File → Zip
   Lock → Won't Open → On the Air → Hidden in Plain Sight
7. **OSINT** — Trivia Run → Boarding Pass → Low Tide

New members who only get through Code Execution, Linux Fundamentals, and Networking in
one sitting have still touched a little of everything coming later in the semester —
Cryptography, Forensics, and OSINT reward whoever wants to keep going.
