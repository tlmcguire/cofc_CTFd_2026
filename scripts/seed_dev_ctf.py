#!/usr/bin/env python3
"""
Dev/test helper: get straight to a working challenges page.

Point this at a running CTFd instance (the one from `docker compose up -d`)
and it will:

  1. Run the first-time setup wizard for you (or log in if it's already been
     run), using a fixed, clearly-labeled dev admin account.
  2. Force challenge/score/account/registration visibility to "public" so you
     can view http://localhost:8000/challenges without logging in at all.
  3. Create every challenge from CTFd/challenges/CHALLENGES.md via the API,
     with its flag and file(s) attached -- skipping any that already exist,
     so it's safe to re-run after `docker compose down -v && up -d`.

This is a *development/testing* convenience, not how you'd run the real
event -- see SETUP.md for the actual event setup (your own admin password,
your own visibility choices, etc).

Usage:
    python3 scripts/seed_dev_ctf.py [base_url]

    base_url defaults to http://localhost:8000
"""
import io
import json
import mimetypes
import os
import re
import sys
import uuid
from http.cookiejar import CookieJar
from urllib.error import HTTPError
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEV_ADMIN = {
    "name": "admin",
    "email": "admin@ctfclub.local",
    "password": "ChangeMe123!",
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHALLENGES_DIR = os.path.join(REPO_ROOT, "CTFd", "challenges")

CHALLENGES = [
    {
        "name": "Hide and Seek",
        "category": "Linux Fundamentals",
        "value": 75,
        "description": "An archive of an old shared folder.",
        "files": ["Linux_Fundamentals/hide_and_seek/data.zip"],
        "flag": "cofc{hidden_files_arent_hidden}",
    },
    {
        "name": "Needle in a Haystack",
        "category": "Linux Fundamentals",
        "value": 100,
        "description": "A pile of old log files. One line doesn't belong.",
        "files": ["Linux_Fundamentals/haystack/logs.zip"],
        "flag": "cofc{grep_dash_r_saves_time}",
    },
    {
        "name": "Subnet Math",
        "category": "Networking",
        "value": 75,
        "description": "An IP address and a CIDR prefix.",
        "files": ["Networking/subnet_math/prompt.txt"],
        "flag": "cofc{broadcast_10_42_17_255}",
    },
    {
        "name": "Dig Deeper",
        "category": "Networking",
        "value": 75,
        "description": "A domain name. Flag format: replace @ and . with _.",
        "files": ["Networking/dig_deeper/prompt.txt"],
        "flag": "cofc{security_defcon_org}",
    },
    {
        "name": "Sniffed",
        "category": "Networking",
        "value": 150,
        "description": "A short recording of network traffic.",
        "files": ["Networking/sniffed/capture.pcap"],
        "flag": "cofc{pack3ts_dont_l13}",
    },
    {
        "name": "View Source",
        "category": "Web",
        "value": 50,
        "description": "A page that doesn't do much.",
        "files": ["Web/view_source/index.html"],
        "flag": "cofc{ctrl_u_is_ur_friend}",
    },
    {
        "name": "The Numbers",
        "category": "Cryptography",
        "value": 50,
        "description": "A base64-encoded string.",
        "files": ["Cryptography/the_numbers.txt"],
        "flag": "cofc{somanynumbers}",
    },
    {
        "name": "What's This?",
        "category": "Cryptography",
        "value": 75,
        "description": "Twenty-some lines that look almost identical. Only one of them is readable.",
        "files": ["Cryptography/whats_this.txt"],
        "flag": "cofc{areyoulikingciphers}",
    },
    {
        "name": "Hex Appeal",
        "category": "Cryptography",
        "value": 50,
        "description": "A string encoded in a different base.",
        "files": ["Cryptography/hex_appeal/message.txt"],
        "flag": "cofc{hex_is_just_base16}",
    },
    {
        "name": "Layers",
        "category": "Cryptography",
        "value": 75,
        "description": "Wrapped more than once.",
        "files": ["Cryptography/layers/layers.txt"],
        "flag": "cofc{ea5y_a5_1_2_3}",
    },
    {
        "name": "Repeat After Me",
        "category": "Cryptography",
        "value": 150,
        "description": "Another coded note.",
        "files": ["Cryptography/vigenere/cipher.txt"],
        "flag": "cofc{v1gen3re_is_c00l}",
    },
    {
        "name": "Between the Lines",
        "category": "Cryptography",
        "value": 200,
        "description": "A paragraph of text that reads a little wrong.",
        "files": ["Cryptography/substitution/message.txt"],
        "flag": "cofc{freq_u3ncy_an4lysis}",
    },
    {
        "name": "Crib Drag",
        "category": "Cryptography",
        "value": 200,
        "description": "An intercepted message.",
        "files": ["Cryptography/xor_crib/message.bin"],
        "flag": "cofc{kn0wn_pla1ntext_att4ck}",
    },
    {
        "name": "Small Fry",
        "category": "Cryptography",
        "value": 400,
        "description": "A keypair generated without much thought for size.",
        "files": ["Cryptography/rsa_small/params.txt"],
        "flag": "cofc{rs4_1s_ju5t_m4th}",
    },
    {
        "name": "Broken File",
        "category": "Forensics",
        "value": 100,
        "description": "The name looks encoded. The contents don't look right either.",
        "files": ["Forensics/Broken_File/ZmxhZw==.encr"],
        "flag": "cofc{g0od_w0rk_d3t3ct!ve}",
    },
    {
        "name": "Behind the Picture",
        "category": "Forensics",
        "value": 75,
        "description": "A photo with more stored in the file than what's visible.",
        "files": ["Forensics/Exif_cellent/welcome.png"],
        "flag": "cofc{m3tadata_m4tters}",
    },
    {
        "name": "Scan Me",
        "category": "Forensics",
        "value": 75,
        "description": "An image file.",
        "files": ["Forensics/Scan_Me/flyer.png"],
        "flag": "cofc{qr_c0des_are_ne4t}",
    },
    {
        "name": "Mystery File",
        "category": "Forensics",
        "value": 100,
        "description": "A file with an extension that means nothing.",
        "files": ["Forensics/Mystery_File/artifact.bin"],
        "flag": "cofc{ext3nsions_ar3_ju5t_lab3ls}",
    },
    {
        "name": "Won't Open",
        "category": "Forensics",
        "value": 150,
        "description": "This file refuses to open in anything.",
        "files": ["Forensics/Magic_Bytes/picture.png"],
        "flag": "cofc{sign4tures_matt3r}",
    },
    {
        "name": "Zip Lock",
        "category": "Forensics",
        "value": 175,
        "description": "Password protected, and not with much of one.",
        "files": ["Forensics/Zip_Lock/secure.zip"],
        "flag": "cofc{brut3_f0rc3_zip}",
    },
    {
        "name": "On the Air",
        "category": "Forensics",
        "value": 200,
        "description": "An audio file.",
        "files": ["Forensics/On_the_Air/transmission.wav"],
        "flag": "cofc{dit_dah_flag}",
    },
    {
        "name": "Hidden in Plain Sight",
        "category": "Forensics",
        "value": 225,
        "description": "A decent enough photo. Look closer.",
        "files": ["Forensics/Hidden_in_Plain_Sight/sunset.png"],
        "flag": "cofc{ste90_10_the_r3scue}",
    },
    {
        "name": "First Script",
        "category": "Code Execution",
        "value": 50,
        "description": "A short Python file. See what it does.",
        "files": ["Code_Execution/puzzle_script/run_me.py"],
        "flag": "cofc{ju5t_run_1t}",
    },
    {
        "name": "Environment Check",
        "category": "Code Execution",
        "value": 75,
        "description": "This script isn't ready to talk yet.",
        "files": ["Code_Execution/environment_check/check.py"],
        "flag": "cofc{env_v4rs_m4tter}",
    },
    {
        "name": "Binary Search Game",
        "category": "Code Execution",
        "value": 100,
        "description": "We're thinking of a number between 1 and 1000. Ten guesses. Run the .sh on macOS/Linux, the .bat on Windows.",
        "files": [
            "Code_Execution/binary_challenge/binary_challenge.sh",
            "Code_Execution/binary_challenge/binary_challenge.bat",
        ],
        "flag": "cofc{10110101001}",
    },
    {
        "name": "One Line Off",
        "category": "Code Execution",
        "value": 100,
        "description": "This doesn't run.",
        "files": ["Code_Execution/one_line_off/broken.py"],
        "flag": "cofc{f1x3d_1t}",
    },
    {
        "name": "Look, Don't Touch",
        "category": "Code Execution",
        "value": 100,
        "description": "A compiled program. You may not need to run it.",
        "files": [
            "Code_Execution/static_challenge/static",
            "Code_Execution/static_challenge/ltdis.sh",
            "Code_Execution/static_challenge/ltdis.bat",
        ],
        "flag": "cofc{red_herring}",
    },
    {
        "name": "Bytecode Blues",
        "category": "Code Execution",
        "value": 150,
        "description": "No source, just the compiled file. Requires Python 3.14.x -- see SOLUTIONS.md if yours is different.",
        "files": ["Code_Execution/bytecode_blues/challenge.pyc"],
        "flag": "cofc{pyc_1s_st1ll_c0de}",
    },
    {
        "name": "Rockstar",
        "category": "Code Execution",
        "value": 200,
        "description": "The file looks like song lyrics. Paste it into https://codewithrockstar.com/online and hit Rock.",
        "files": ["Code_Execution/rockstars/lyrics.txt"],
        "flag": "cofc{rocknr0113r}",
    },
    {
        "name": "Keygen",
        "category": "Code Execution",
        "value": 350,
        "description": "This program is picky about its password.",
        "files": ["Code_Execution/keygen/keygen.py"],
        "flag": "cofc{y0u_r3versed_the_l09ic}",
    },
    {
        "name": "Boarding Pass",
        "category": "OSINT",
        "value": 150,
        "description": "A boarding pass with the important parts blacked out. Flag format: cofc{flightnumber_departuretime_destinationcity}, all lowercase, 24-hour time.",
        "files": ["OSINT/boarding_pass/boarding_pass.png"],
        "flag": "cofc{zz0834_1842_frankfurt}",
    },
    {
        "name": "Low Tide",
        "category": "OSINT",
        "value": 150,
        "description": "A set of coordinates, and a note about a tidal schedule.",
        "files": ["OSINT/low_tide/note.txt"],
        "flag": "cofc{brr}",
    },
    {
        "name": "Trivia Run",
        "category": "OSINT",
        "value": 100,
        "description": "Three short cybersecurity history questions.",
        "files": ["OSINT/trivia_run/questions.txt"],
        "flag": "cofc{1999_1988_cfaa}",
    },
]


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # surface redirects as responses instead of following them


class Client:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")
        self.opener = build_opener(NoRedirect())
        self.cookies = {}
        self.nonce = None

    def _apply_cookies(self, headers):
        if self.cookies:
            headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in self.cookies.items())

    def _store_cookies(self, resp_headers):
        for key, value in resp_headers.items():
            if key.lower() == "set-cookie":
                name, _, rest = value.partition("=")
                val = rest.split(";", 1)[0]
                self.cookies[name.strip()] = val.strip()

    def request(self, method, path, data=None, headers=None, content_type=None):
        url = path if path.startswith("http") else self.base_url + path
        headers = dict(headers or {})
        self._apply_cookies(headers)
        if content_type:
            headers["Content-Type"] = content_type
        req = Request(url, data=data, headers=headers, method=method)
        try:
            resp = self.opener.open(req)
            status = resp.status
            body = resp.read()
            resp_headers = resp.headers
        except HTTPError as e:
            status = e.code
            body = e.read()
            resp_headers = e.headers
        self._store_cookies(resp_headers)
        location = resp_headers.get("Location")
        return status, body, location

    def get(self, path):
        return self.request("GET", path)

    def post_form(self, path, fields):
        body = "&".join(
            f"{k}=" + _urlquote(str(v)) for k, v in fields.items()
        ).encode()
        return self.request(
            "POST", path, data=body, content_type="application/x-www-form-urlencoded"
        )

    def post_json(self, path, obj):
        headers = {}
        if self.nonce:
            headers["CSRF-Token"] = self.nonce
        return self.request(
            "POST",
            path,
            data=json.dumps(obj).encode(),
            headers=headers,
            content_type="application/json",
        )

    def post_multipart(self, path, fields, file_field, file_path):
        boundary = uuid.uuid4().hex
        buf = io.BytesIO()

        def write_field(name, value):
            buf.write(f"--{boundary}\r\n".encode())
            buf.write(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
            buf.write(str(value).encode())
            buf.write(b"\r\n")

        for k, v in fields.items():
            write_field(k, v)

        filename = os.path.basename(file_path)
        ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        buf.write(f"--{boundary}\r\n".encode())
        buf.write(
            f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'.encode()
        )
        buf.write(f"Content-Type: {ctype}\r\n\r\n".encode())
        with open(file_path, "rb") as f:
            buf.write(f.read())
        buf.write(b"\r\n")
        buf.write(f"--{boundary}--\r\n".encode())

        return self.request(
            "POST",
            path,
            data=buf.getvalue(),
            content_type=f"multipart/form-data; boundary={boundary}",
        )


def _urlquote(s):
    from urllib.parse import quote_plus

    return quote_plus(s)


def extract_nonce(html_bytes):
    html = html_bytes.decode("utf-8", errors="replace")
    m = re.search(r"'csrfNonce':\s*\"([^\"]+)\"", html)
    if m:
        return m.group(1)
    m = re.search(r'name="nonce"\s+value="([^"]+)"', html)
    if m:
        return m.group(1)
    return None


def ensure_authenticated(client):
    status, body, location = client.get("/setup")
    if status in (301, 302, 303, 307, 308):
        print("CTFd is already set up -- logging in as the dev admin instead.")
        return login(client)

    nonce = extract_nonce(body)
    if not nonce:
        print("Could not find a setup form -- is this really a fresh CTFd instance?")
        sys.exit(1)

    print("Running first-time setup with the dev admin account...")
    fields = {
        "nonce": nonce,
        "ctf_name": "CofC Cyber Club Kickoff CTF (dev)",
        "ctf_description": "Local test instance -- seeded by scripts/seed_dev_ctf.py",
        "user_mode": "users",
        "challenge_visibility": "public",
        "account_visibility": "public",
        "score_visibility": "public",
        "registration_visibility": "public",
        "verify_emails": "false",
        "team_size": "",
        "ctf_theme": "core-beta",
        "name": DEV_ADMIN["name"],
        "email": DEV_ADMIN["email"],
        "password": DEV_ADMIN["password"],
    }
    status, body, location = client.post_form("/setup", fields)
    if status not in (200, 302):
        print(f"Setup POST failed unexpectedly (status {status}).")
        print(body[:2000])
        sys.exit(1)
    client.nonce = nonce
    print(f"Setup complete. Dev admin: {DEV_ADMIN['name']} / {DEV_ADMIN['password']}")


def refresh_nonce(client):
    # login_user() rotates session["nonce"], so any nonce captured before
    # authentication completed is stale -- pull a fresh one from an
    # authenticated page load before making any API calls.
    status, body, _ = client.get("/")
    nonce = extract_nonce(body)
    if nonce:
        client.nonce = nonce


def login(client):
    status, body, _ = client.get("/login")
    nonce = extract_nonce(body)
    fields = {
        "name": DEV_ADMIN["name"],
        "password": DEV_ADMIN["password"],
        "nonce": nonce,
    }
    status, body, location = client.post_form("/login", fields)
    if status not in (200, 302):
        print(
            "Login failed. If this instance was set up manually with a different "
            "admin account, either recreate the stack (`docker compose down -v && "
            "docker compose up -d`) or edit DEV_ADMIN in this script to match your "
            "real admin credentials."
        )
        sys.exit(1)
    client.nonce = nonce
    print(f"Logged in as {DEV_ADMIN['name']}.")


def force_public_visibility(client):
    for key in (
        "challenge_visibility",
        "account_visibility",
        "score_visibility",
        "registration_visibility",
    ):
        headers = {"CSRF-Token": client.nonce} if client.nonce else {}
        client.request(
            "PATCH",
            f"/api/v1/configs/{key}",
            data=json.dumps({"value": "public"}).encode(),
            headers=headers,
            content_type="application/json",
        )
    print("Visibility settings forced to public (no login needed to view challenges).")


def existing_challenge_names(client):
    status, body, _ = client.get("/api/v1/challenges?view=admin")
    if status != 200:
        return set()
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return set()
    return {c["name"] for c in data.get("data", [])}


def create_challenges(client):
    existing = existing_challenge_names(client)
    created, skipped = 0, 0

    for chal in CHALLENGES:
        if chal["name"] in existing:
            print(f"  [skip] {chal['name']} (already exists)")
            skipped += 1
            continue

        status, body, _ = client.post_json(
            "/api/v1/challenges",
            {
                "name": chal["name"],
                "category": chal["category"],
                "description": chal["description"],
                "value": chal["value"],
                "type": "standard",
                "state": "visible",
            },
        )
        if status != 200:
            print(f"  [FAIL] {chal['name']}: challenge create failed ({status})")
            print("        ", body[:500])
            continue
        challenge_id = json.loads(body)["data"]["id"]

        status, body, _ = client.post_json(
            "/api/v1/flags",
            {"challenge_id": challenge_id, "type": "static", "content": chal["flag"]},
        )
        if status != 200:
            print(f"  [FAIL] {chal['name']}: flag create failed ({status})")

        for rel_path in chal["files"]:
            full_path = os.path.join(CHALLENGES_DIR, rel_path)
            if not os.path.exists(full_path):
                print(f"  [FAIL] {chal['name']}: missing file {rel_path}")
                continue
            status, body, _ = client.post_multipart(
                "/api/v1/files",
                {"nonce": client.nonce, "type": "challenge", "challenge_id": challenge_id},
                "file",
                full_path,
            )
            if status != 200:
                print(f"  [FAIL] {chal['name']}: file upload failed for {rel_path} ({status})")

        print(f"  [ok]   {chal['name']}")
        created += 1

    print(f"\n{created} challenge(s) created, {skipped} already existed.")


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    print(f"Seeding CTFd at {base_url} ...")
    client = Client(base_url)

    try:
        client.get("/")
    except Exception as e:
        print(f"Could not reach {base_url} -- is `docker compose up -d` running? ({e})")
        sys.exit(1)

    ensure_authenticated(client)
    refresh_nonce(client)
    force_public_visibility(client)
    print("\nCreating challenges (skipping any that already exist)...")
    create_challenges(client)

    print(f"\nDone. Open {base_url}/challenges -- no login required.")
    print(f"Dev admin login (if you need it): {DEV_ADMIN['name']} / {DEV_ADMIN['password']}")


if __name__ == "__main__":
    main()
