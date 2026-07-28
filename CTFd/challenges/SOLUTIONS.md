# Solutions — CofC Cyber Club Kickoff CTF

Companion write-up for [`CHALLENGES.md`](CHALLENGES.md). Categories are in the same
order as that file (Code Execution/Misc, then Linux Fundamentals, Networking, and Web
in the order those topics come up this semester, then Cryptography, Forensics, and
OSINT). Every solve path below works identically on macOS, Windows, and Linux — where a command
differs by OS, both versions are given. The only tool assumed beyond what ships with
the OS is **Python 3** (`python3` on macOS/Linux, `python` or `py` on Windows) — install
it from [python.org](https://www.python.org/downloads/) if it's missing.

Don't hand this out before the event — it has every flag in it.

---

## Code Execution / Misc

### First Script — `cofc{ju5t_run_1t}`

Download `run_me.py` and run it:

```bash
python3 run_me.py
```

The script Base64-decodes a short string and prints it. Reading the ~5 lines of source
first is a good habit before running any script — this one is short enough to check
that it only decodes and prints, nothing else.

---

### Environment Check — `cofc{env_v4rs_m4tter}`

Running `check.py` as-is just prints "Nothing to see here." Reading the source shows
why: it checks the environment variable `CTF_MODE` and only prints the flag when it
equals `unlocked`. Set that variable before running the script:

```bash
CTF_MODE=unlocked python3 check.py
```

```powershell
$env:CTF_MODE = "unlocked"
python check.py
```

---

### Binary Search Game — `cofc{10110101001}`

The script picks a secret number from 1–1000 and gives you 10 guesses, telling you
"higher" or "lower" after each one. 10 guesses is exactly enough — `2^10 = 1024 > 1000`
— *if* you guess with binary search (always guess the midpoint of the remaining range),
not randomly.

- **macOS/Linux:** `bash binary_challenge.sh`
- **Windows:** double-click `binary_challenge.bat`, or run it from Command Prompt

Strategy: first guess `500`. If "Lower," your new range is 1–499, guess `250`. If
"Higher," guess the midpoint of the new range. Keep halving the remaining range and
you'll always land on the number within 10 guesses.

---

### One Line Off — `cofc{f1x3d_1t}`

Running `broken.py` fails immediately:

```
SyntaxError: expected ':'
```

Python points at the exact line — a `def` line missing its trailing colon. Add the
colon and run it again:

```bash
python3 -c "
content = open('broken.py').read().replace('def get_flag()', 'def get_flag():')
open('fixed.py', 'w').write(content)
"
python3 fixed.py
```

Or just open the file in any text editor, add the `:` yourself, save, and run it.

---

### Look, Don't Touch — `cofc{red_herring}`

You do not need to run this binary (and on Windows or Apple Silicon, you can't — it's a
Linux/x86-64 ELF executable). Just look at the strings embedded in the file:

```bash
strings static | grep cofc
```

```powershell
Select-String -Path static -Pattern "cofc" -Encoding ascii
```

The provided `ltdis.sh` (macOS/Linux) / `ltdis.bat` (Windows) helper also does this for
you — it dumps a disassembly and a strings listing with file offsets — but for this
particular binary, plain `strings` alone already contains the flag. (The disassembly
step may print a warning about a missing `.text` section; that's expected and doesn't
stop the strings extraction from working.)

---

### Bytecode Blues — `cofc{pyc_1s_st1ll_c0de}`

`challenge.pyc` is compiled Python bytecode — no `.py` source is provided, but you don't
need it. A `.pyc` file is directly executable by a matching Python interpreter:

```bash
python3 challenge.pyc
```

This requires your `python3` to be **version 3.14.x** — `.pyc` files embed a
version-specific "magic number" and Python refuses to run a `.pyc` compiled by a
different minor version (you'll see an error like `bad magic number` or `RuntimeError:
Bad magic number in .pyc file` if it doesn't match). If your default Python is older or
newer, install 3.14 alongside it (via [pyenv](https://github.com/pyenv/pyenv),
[the official installer](https://www.python.org/downloads/), or your package manager)
and run it explicitly, e.g. `python3.14 challenge.pyc`.

If you'd rather decompile than match versions exactly, tools like
[`pycdc`](https://github.com/zrax/pycdc) read `.pyc` bytecode directly and reconstruct
readable Python source without needing to execute it at all.

---

### Rockstar — `cofc{rocknr0113r}`

`lyrics.txt` isn't song lyrics — it's a valid program in
[**Rockstar**](https://codewithrockstar.com/), an esoteric programming language
deliberately designed to read like a power ballad. Paste the file's contents into the
official online interpreter at <https://codewithrockstar.com/online>, click **Rock**,
and watch the output panel.

The tricky part: the output isn't the flag text — it's a column of **numbers**, one per
line, e.g. `114`, `111`, `99`, `107`, ... Rockstar's `shout` statement prints whatever a
variable currently holds, and here that's the ASCII code of each character, not the
character itself. Convert each number to its ASCII character and concatenate:

```python
codes = [114, 111, 99, 107, 110, 114, 48, 49, 49, 51, 114]  # whatever the interpreter printed
print(''.join(chr(c) for c in codes))
# rocknr0113r
```

Wrap that in `cofc{...}` for the full flag: `cofc{rocknr0113r}`.

---

### Keygen — `cofc{y0u_r3versed_the_l09ic}`

`keygen.py` is a password checker — run it with the wrong password and it just says
"Access denied," so guessing won't get you anywhere. Read the source instead: it applies
a small, fully reversible transform to whatever you type in, and compares the result to
a hardcoded target list.

```python
KEY = "cyberclub"

def transform(text):
    encoded = []
    for i, c in enumerate(text):
        shifted = (ord(c) + i * 3) % 256
        encoded.append(shifted ^ ord(KEY[i % len(KEY)]))
    return encoded
```

Since XOR and modular addition are both invertible, run the transform *backwards* over
the target list to recover the original input:

```python
KEY = "cyberclub"
TARGET = [26, 74, 25, 13, 12, 33, 228, 15, 232, 237, 250, 231, 230, 233, 241, 254, 250, 253, 5, 11, 199, 199]

password = []
for i, x in enumerate(TARGET):
    shifted = x ^ ord(KEY[i % len(KEY)])
    password.append(chr((shifted - i * 3) % 256))

print(''.join(password))   # y0u_r3versed_the_l09ic
```

Then run the script with that password to get the full flag:

```bash
python3 keygen.py y0u_r3versed_the_l09ic
# Access granted! cofc{y0u_r3versed_the_l09ic}
```

---

## Linux Fundamentals

### Hide and Seek — `cofc{hidden_files_arent_hidden}`

`data.zip` extracts into a small tree of folders. A plain `ls` (or Windows
Explorer's default view) won't show everything — files and folders whose name starts
with a `.` are conventionally hidden from normal directory listings, not actually
protected in any way.

```bash
unzip data.zip
find data -name ".*"        # macOS/Linux
```

```powershell
Get-ChildItem -Recurse -Force data | Where-Object { $_.Name -like ".*" }
```

That turns up `.config/.flag` a few levels down. `cat` it (or `Get-Content` on Windows)
to read the flag directly — no decoding involved, it was just out of sight.

---

### Needle in a Haystack — `cofc{grep_dash_r_saves_time}`

`logs.zip` extracts into roughly 150 near-identical log files across a handful of
nested folders. Opening them one at a time would take forever — a recursive search
across the whole tree finds the one line that matters in under a second:

```bash
unzip logs.zip
grep -r "cofc{" logs
```

```powershell
Get-ChildItem -Recurse logs | Select-String -Pattern "cofc"
```

Both commands search every file in every subfolder for the pattern and print the one
matching line along with which file it came from.

---

## Networking

### Subnet Math — `cofc{broadcast_10_42_17_255}`

`prompt.txt` gives an address and prefix length: `10.42.17.201/26`. A `/26` mask leaves
6 bits for hosts (`2^6 = 64` addresses total), so this subnet spans a block of 64
addresses. `201` in the last octet falls in the block from `192` to `255` (`192` is the
largest multiple of 64 that's `≤ 201`), so the network address is `10.42.17.192` and the
broadcast address — the last address in that block — is `10.42.17.255`.

If you'd rather not do the bit math by hand, Python's `ipaddress` module does it in two
lines, or any online subnet calculator works the same way:

```python
import ipaddress
net = ipaddress.ip_interface("10.42.17.201/26").network
print(net.broadcast_address)   # 10.42.17.255
```

Replace the dots with underscores to match the flag format: `cofc{broadcast_10_42_17_255}`.

---

### Dig Deeper — `cofc{security_defcon_org}`

DNS holds more record types than just the `A` record that maps a name to an IP.
`TXT` records carry arbitrary text, and organizations use them for all kinds of
things — domain ownership verification, SPF rules for email, and sometimes contact
information. Query `defcon.org`'s TXT records:

```bash
dig +short TXT defcon.org
```

```powershell
Resolve-DnsName -Name defcon.org -Type TXT
```

One of the returned strings is `security_contact=mailto:security@defcon.org` — a
real, published way to report a security issue to them directly, published the same
way a company might publish an SPF record. Swap the `@` and `.` for underscores to
get the flag: `cofc{security_defcon_org}`.

If `dig` isn't installed, any of the free online DNS lookup tools (MXToolbox,
Google's `dns.google`, etc.) return the same TXT records for the same domain.

---

### Sniffed — `cofc{pack3ts_dont_l13}`

`capture.pcap` is a packet capture — open it in [Wireshark](https://www.wireshark.org/)
(free, available for macOS/Windows/Linux) or with the command-line `tshark` that ships
alongside it. There's exactly one packet in the file.

Click the packet and look at the hex/ASCII pane at the bottom, or right-click it and
choose **Follow → UDP Stream** — the payload is a plaintext line that reads like an
HTTP request, with the flag sitting in it in the clear:

```bash
tshark -r capture.pcap -V
```

If Wireshark isn't installed yet, plain `strings` on the capture file finds the same
text, since it's stored as-is in the packet bytes:

```bash
strings capture.pcap | grep cofc
```

---

## Web

### View Source — `cofc{ctrl_u_is_ur_friend}`

Open `index.html` directly in a browser (double-click it, no server needed) and use
**View Page Source** — `Ctrl+U` on Windows/Linux, `Cmd+Option+U` on Safari, or
`Cmd+Option+I` then the Elements/Inspector tab in Chrome/Firefox on macOS. The flag is
sitting in an HTML comment (`<!-- ... -->`), which never renders on the page itself but
is always visible in the raw source — a browser's normal view only shows you the
rendered result, not everything the file actually contains.

You can also just read the file directly without a browser at all:

```bash
grep cofc index.html
```

---

## Cryptography

### The Numbers — `cofc{somanynumbers}`

The file is a single Base64 string — recognizable by the alphabet it uses (`A-Za-z0-9+/`)
and the `=` padding at the end.

```bash
python3 -c "import base64; print(base64.b64decode(open('the_numbers.txt').read()).decode())"
```

Or from a shell without Python: macOS/Linux have a `base64` command —
`base64 -d the_numbers.txt` (macOS) — and on Windows, PowerShell:
`[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-Content the_numbers.txt)))`.

---

### What's This? — `cofc{areyoulikingciphers}`

Every line in `whats_this.txt` is a rotation of the same underlying text by a different
amount — sliding each letter forward or backward through the alphabet by a fixed step.
Pick any line and try all 26 possible shifts against it; exactly one will read as
English.

```python
def shift(s, n):
    out = []
    for c in s:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            out.append(chr((ord(c) - base + n) % 26 + base))
        else:
            out.append(c)
    return ''.join(out)

line = open('whats_this.txt').readlines()[0].strip()
for n in range(26):
    print(n, shift(line, n))
```

Run that (any line works — they're all rotations of each other) and scan the 26 outputs
for the one that reads `cofc{areyoulikingciphers}`. This also runs fine pasted into
[CyberChef](https://gchq.github.io/CyberChef/)'s "ROT13 Brute Force" recipe.

---

### Hex Appeal — `cofc{hex_is_just_base16}`

The file is a long string of only `0-9a-f`. That's hexadecimal — each pair of
characters is one byte.

```python
s = open('hex_appeal/message.txt').read().strip()
print(bytes.fromhex(s).decode())
```

```bash
xxd -r -p message.txt        # macOS/Linux
```

```powershell
-join ((Get-Content message.txt).Trim() -split '(..)' | Where-Object {$_} | ForEach-Object {[char][convert]::ToInt32($_,16)})
```

---

### Layers — `cofc{ea5y_a5_1_2_3}`

Peel one layer at a time. The file is Base64 → decoding that gives you a hex string →
decoding *that* gives you Base64 again → decoding that gives the flag.

```python
import base64
s = open('layers/layers.txt').read().strip()
step1 = base64.b64decode(s).decode()      # a hex string
step2 = bytes.fromhex(step1).decode()     # another base64 string
step3 = base64.b64decode(step2).decode()  # the flag
print(step3)
```

If you don't recognize what layer you're looking at: pure Base64 uses `A-Za-z0-9+/=`
only; a hex string uses only `0-9a-f`. Look at the character set of what you've
decoded so far to know what to try next.

---

### Repeat After Me — `cofc{v1gen3re_is_c00l}`

This isn't a single fixed shift — decoding `cipher.txt` with any one ROT amount (like
in *What's This?*) won't produce clean text, because the shift amount changes letter to
letter. That's a Vigenère cipher: each letter's shift comes from the corresponding
letter of a repeating keyword. The description points at "where this club calls
home" — the club is at the **College of Charleston**, so the keyword is `charleston`.

```python
def vig_decrypt(text, key):
    out, ki = [], 0
    for c in text:
        if c.isalpha():
            base = ord('a') if c.islower() else ord('A')
            k = ord(key[ki % len(key)].lower()) - ord('a')
            out.append(chr((ord(c) - base - k) % 26 + base))
            ki += 1
        else:
            out.append(c)
    return ''.join(out)

ct = open('vigenere/cipher.txt').read().strip()
print(vig_decrypt(ct, "charleston"))
```

Without the keyword hint, [dcode.fr's Vigenère tool](https://www.dcode.fr/vigenere-cipher)
can brute-force short keys, or you could crib-drag knowing the plaintext starts with
`cofc{` (same idea as Crib Drag, below).

---

### Between the Lines — `cofc{freq_u3ncy_an4lysis}`

`message.txt` is a full paragraph, not a short string — every letter has been swapped
for a different letter, consistently, throughout the whole thing (a monoalphabetic
substitution cipher). Because it's long enough, English letter frequency gives it away:
`E`, `T`, `A`, `O`, `I`, `N` are the most common letters in English, short repeated
words are probably "the" or "and," a lone letter is almost always "a" or "I," and so on.

The fastest way to actually solve one by hand is a dedicated solver — paste the
ciphertext into [quipqiup.com](https://quipqiup.com/) and let it work out the mapping.
Once you have the substitution alphabet, apply it to the whole paragraph (not just the
parts that look important) — the flag is embedded in running text near the end, in the
same `cofc{...}` shape as everything else, and falls out once the rest of the paragraph
reads as English.

---

### Crib Drag — `cofc{kn0wn_pla1ntext_att4ck}`

`message.bin` is XORed with a short, *repeating* key — that's the vulnerability. Every
flag in this event follows the same `cofc{` prefix, so XOR the first 5 ciphertext bytes
against that known plaintext to recover the start of the key:

```python
data = open('xor_crib/message.bin', 'rb').read()
crib = b"cofc{"
key_guess = bytes(data[i] ^ crib[i] for i in range(len(crib)))
print(key_guess)   # b'sease' -- notice it's just "sea" repeating
```

Once you see the key repeat (`s`, `e`, `a`, `s`, `e`, ...), you have the full key
(`sea`) and can decrypt everything:

```python
key = b"sea"
flag = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
print(flag.decode())
```

---

### Small Fry — `cofc{rs4_1s_ju5t_m4th}`

`params.txt` gives you a public RSA modulus `n`, exponent `e`, and ciphertext `c`. RSA's
security depends on `n` being hard to factor — this one was generated with far-too-small
primes on purpose, so it isn't.

**Step 1 — factor `n`.** Install `sympy` (`pip install sympy`) and run:

```python
from sympy import factorint
n = 3149218012374485551776734308950137661994453614468580739203
print(factorint(n))
```

This takes roughly a minute or two on a laptop (sympy's pure-Python factoring, no extra
libraries). It'll be dramatically faster if you `pip install gmpy2` first (sympy uses it
automatically when present), or if you paste `n` into
[factordb.com](http://factordb.com/) and let their backend factor it for you.

**Step 2 — decrypt.** Once you have the two prime factors `p` and `q`:

```python
n = 3149218012374485551776734308950137661994453614468580739203
e = 65537
c = 1688256656290170237088439451000769643642959611801835308273
p, q = 48850955997579085512722537987, 64465842030410865299804906369  # from step 1

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)          # modular inverse (Python 3.8+)
m = pow(c, d, n)             # RSA decryption
print(m.to_bytes((m.bit_length() + 7) // 8, 'big').decode())
```

---

## Forensics

### Broken File — `cofc{g0od_w0rk_d3t3ct!ve}`

Two clues stacked on top of each other. First, the filename itself,
`ZmxhZw==.encr`, is Base64 (that `==` padding again):

```bash
python3 -c "import base64; print(base64.b64decode('ZmxhZw=='))"
# b'flag'
```

That confirms you're in the right place, but doesn't decrypt anything — the *contents*
of the file are separately XORed with a single repeating byte. Since flags in this
event all start with `cofc{`, brute-force all 256 possible single-byte keys and keep
the one that produces clean, printable text starting with `cofc{`:

```python
data = open('ZmxhZw==.encr', 'rb').read()
for k in range(256):
    dec = bytes(b ^ k for b in data)
    try:
        s = dec.decode('ascii')
    except UnicodeDecodeError:
        continue
    if s.startswith('cofc{'):
        print(k, s)
```

Only one key (`0x42`) produces a clean result.

---

### Behind the Picture — `cofc{m3tadata_m4tters}`

Image files carry metadata alongside the pixel data — comments, author, camera info,
GPS coordinates on real photos, etc. The flag here is sitting in the PNG's text
metadata. Cross-platform, the simplest tool is `strings` (macOS/Linux, built in) or a
one-line PowerShell equivalent on Windows — no image-specific tooling required, since
PNG metadata is stored as plain text in the file:

```bash
strings welcome.png | grep cofc
```

```powershell
Select-String -Path welcome.png -Pattern "cofc" -Encoding utf8
```

Or, in Python with Pillow (`pip install pillow`):

```python
from PIL import Image
print(Image.open('welcome.png').text)
```

---

### Scan Me — `cofc{qr_c0des_are_ne4t}`

`flyer.png` is a QR code. Any phone camera or QR scanner app will read it directly —
point your phone's camera at the image on screen. If you'd rather do it on a computer,
most browsers can decode a QR code from an uploaded image via free online decoders, or
with Python (`pip install opencv-python`):

```python
import cv2
img = cv2.imread('flyer.png')
data, points, _ = cv2.QRCodeDetector().detectAndDecode(img)
print(data)
```

---

### Mystery File — `cofc{ext3nsions_ar3_ju5t_lab3ls}`

`artifact.bin` has a made-up extension that doesn't tell you anything true about the
file. An extension is just a naming convention — what a file *actually* is comes from
its contents, specifically the first few bytes (the "magic number"). Check what the
file really is instead of trusting its name:

```bash
file artifact.bin
```

```powershell
Format-Hex artifact.bin | Select-Object -First 1
```

The first bytes are `50 4B 03 04` — `PK..`, the signature of a ZIP archive. Rename the
file to end in `.zip` and extract it normally:

```bash
cp artifact.bin artifact.zip
unzip artifact.zip
cat note.txt
```

---

### Won't Open — `cofc{sign4tures_matt3r}`

The file is *supposed* to be a PNG, but it won't open — `file picture.png` (macOS/Linux)
reports it as generic `data`, not an image. Every file format starts with a "magic
number" that identifies it; a valid PNG always starts with the 8 bytes
`89 50 4E 47 0D 0A 1A 0A`. Open the file in a hex editor (or hex-dump it) and check the
first 8 bytes:

```bash
xxd picture.png | head -1
```

```powershell
Format-Hex picture.png | Select-Object -First 1
```

They won't match the correct PNG signature — every byte has been flipped (XORed with
`0xFF`). Fix the first 8 bytes to `89 50 4E 47 0D 0A 1A 0A` and save. A quick Python fix
(reads the broken file, patches just the header, writes a new copy) works everywhere:

```python
with open('picture.png', 'rb') as f:
    data = bytearray(f.read())
data[:8] = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
with open('picture_fixed.png', 'wb') as f:
    f.write(data)
```

Open `picture_fixed.png` in any image viewer — the flag is rendered as text in the
picture.

---

### Zip Lock — `cofc{brut3_f0rc3_zip}`

`secure.zip` is password-protected, but the password is a short numeric PIN — small
enough to brute-force with nothing but Python's built-in `zipfile` module (no external
tools, no wordlists):

```python
import zipfile
zf = zipfile.ZipFile('secure.zip')
name = zf.namelist()[0]
for i in range(10000):
    pw = f"{i:04d}".encode()
    try:
        zf.read(name, pwd=pw)
        print("password:", pw)
        break
    except RuntimeError:
        continue
    except zipfile.BadZipFile:
        continue  # wrong password that happened to pass the 1-byte check first
```

Catch both exception types, not just `RuntimeError` — classic zip encryption only
verifies the password with a single check byte before decrypting, so roughly 1 in 256
*wrong* passwords will pass that check and only fail later, when the decrypted bytes'
checksum doesn't match (`BadZipFile: Bad CRC-32`). That's expected; just keep going.

This finishes in well under a second and prints the 4-digit PIN. Extract the archive
with that password (`unzip -P <pin> secure.zip` on macOS/Linux, or enter it when
prompted by Windows Explorer / 7-Zip) to read the flag out of the extracted text file.

---

### On the Air — `cofc{dit_dah_flag}`

`transmission.wav` is a series of short and long tones — Morse code. Play it and listen
for the rhythm (a "dit" is short, a "dah" is roughly three times as long), or look at
the waveform in any audio editor / Audacity, where dots and dashes are visually obvious
as short and long pulses.

Standard Morse timing: a longer silence between letters, and a much longer silence
between words. Decoding the tones gives three words —`DIT`, `DAH`, `FLAG` — separated
by those longer word-gaps. Lowercase them and join with underscores to match the flag
format used throughout this event:

```python
words = ["DIT", "DAH", "FLAG"]
print("cofc{" + "_".join(w.lower() for w in words) + "}")
```

If you don't want to decode it by ear, any online Morse-to-text tool works from the
audio directly, or you can write a short script that measures the duration of each tone
burst in the `.wav` file's samples and classifies short vs. long.

---

### Hidden in Plain Sight — `cofc{ste90_10_the_r3scue}`

Classic LSB (least significant bit) steganography: the flag's text is hidden one bit
at a time in the *lowest* bit of each pixel's red channel, which is far too subtle to
notice by eye. Requires Pillow (`pip install pillow`):

```python
from PIL import Image

img = Image.open('sunset.png')
pixels = img.load()
width, height = img.size

bits = []
for y in range(height):
    for x in range(width):
        r, g, b = pixels[x, y]
        bits.append(str(r & 1))

chars = []
for i in range(0, len(bits), 8):
    byte = bits[i:i+8]
    if len(byte) < 8:
        break
    chars.append(chr(int(''.join(byte), 2)))
    if ''.join(chars).endswith("#####END#####"):
        break

print(''.join(chars).split("#####END#####")[0])
```

The bits are read left-to-right, top-to-bottom, one bit per pixel, 8 bits per character,
until a `#####END#####` marker.

---

## OSINT

### Boarding Pass — `cofc{zz0834_1842_frankfurt}`

Passenger name, origin, destination, flight number, and departure time are all
blacked out in the printed fields — but the QR code was generated from the full,
unredacted data. Boarding pass barcodes/QR codes are readable by a phone camera, a
free online decoder, or `zbar` on a computer:

```bash
zbarimg boarding_pass.png
```

That decodes to a string laid out like a real BCBP (Bar Coded Boarding Pass) record:
passenger name, PNR, origin, destination, carrier and flight number, a departure
time, a date, class, seat, and a check-in sequence number —
`...YUL FRA ZZ0834 1842...` among them. `FRA` is an IATA airport code, not a word —
looking it up turns up Frankfurt Airport, in Germany. Put flight number, departure
time, and destination city together in the order the challenge asks for:

```
cofc{zz0834_1842_frankfurt}
```

Note: don't try to verify the flight number itself against a live flight tracker —
this is fictional data, and airlines do reuse real flight numbers for real routes.
The only external lookup this challenge needs is the airport code.

Real airline boarding passes have leaked more than intended this same way before —
the barcode and the printed side don't always carry the same amount of information,
and the format they're encoded in (IATA calls it BCBP) is a public, documented
standard, not something proprietary to any one airline.

---

### Low Tide — `cofc{brr}`

Dropping `57.0228, -7.44306` into Google Maps or Google Earth lands on a small airport
on a Scottish island, sitting right at the edge of a wide bay. Switch to satellite
view and the "runways" are painted lines across open sand.

This is Barra Airport in the Outer Hebrides — the only airport in the world where
scheduled flights land on a tidal beach. Its runway is only usable at low tide, which
is exactly what the note in the file is describing without naming it. Its IATA code,
found the same way you'd look up any airport code, is `BRR`.

---

### Trivia Run — `cofc{1999_1988_cfaa}`

Three separate lookups, in order:

1. MITRE's CVE list went public in **1999**.
2. The Morris worm, generally credited as the first worm to spread across the early
   internet, was released in **1988**.
3. Its author became the first person convicted under the **CFAA** (Computer Fraud
   and Abuse Act).

Put them in order, lowercase, joined with underscores: `1999_1988_cfaa`.
