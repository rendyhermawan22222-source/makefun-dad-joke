#!/usr/bin/env python3
"""Dad Joke Showdown entry.

Writes one original dad joke to /output/entry.txt, then reads the file
back and verifies it a second time from disk. The joke is a single line
of plain ASCII, at most 200 characters, with the punchline as the last
word:

    My daughter called me salty. I said, 'Sweetheart, after three kids,
    I'm just well seasoned.'

The pun chain is salty -> seasoned: the daughter's insult is answered
with the cooking word that owns it. It is written to be told out loud
by a father at the table, needs no explaining, and every word earns
its place.

Usage:
    python3 main.py            write /output/entry.txt and verify it
    python3 main.py --check    only verify the file already on disk
"""

import os
import sys
import tempfile

JOKE = (
    "My daughter called me salty. "
    "I said, 'Sweetheart, after three kids, I'm just well seasoned.'"
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200
PUNCHLINE = "seasoned.'"


def check_text(text, where):
    """First-pass checks on a joke string, before it touches disk."""
    problems = []
    if not text or not text.strip():
        problems.append("%s: entry is empty or whitespace only" % where)
    if "\n" in text or "\r" in text:
        problems.append("%s: entry must be exactly one line" % where)
    if len(text) > MAX_CHARS:
        problems.append(
            "%s: entry is %d characters, over the %d limit"
            % (where, len(text), MAX_CHARS)
        )
    try:
        text.encode("ascii")
    except UnicodeEncodeError:
        problems.append("%s: entry must be plain ASCII" % where)
    if not text.rstrip().endswith(PUNCHLINE):
        problems.append("%s: punchline must be the last word" % where)
    return problems


def check_file(path):
    """Second-pass checks: read the written file back and re-assert
    everything from disk, so a bad write can never pass silently."""
    problems = []
    try:
        with open(path, "rb") as handle:
            raw = handle.read()
    except OSError as exc:
        return ["cannot read %s: %s" % (path, exc)]
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError:
        return ["%s: file is not plain ASCII" % path]
    if text != JOKE:
        problems.append("%s: file contents differ from the joke" % path)
    if raw.endswith(b"\n"):
        problems.append("%s: file must not end with a trailing newline" % path)
    if len(raw) != len(JOKE):
        problems.append(
            "%s: file is %d bytes, expected %d" % (path, len(raw), len(JOKE))
        )
    problems.extend(check_text(text, path))
    return problems


def write_entry():
    """Write atomically: temp file in the same directory, then rename,
    so the gate never sees a half-written entry."""
    directory = os.path.dirname(OUTPUT_PATH)
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="ascii") as handle:
            handle.write(JOKE)
        os.replace(tmp_path, OUTPUT_PATH)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main(argv):
    check_only = "--check" in argv
    if not check_only:
        problems = check_text(JOKE, "joke")
        if problems:
            for problem in problems:
                print("FAIL: " + problem, file=sys.stderr)
            return 1
        write_entry()
    problems = check_file(OUTPUT_PATH)
    if problems:
        for problem in problems:
            print("FAIL: " + problem, file=sys.stderr)
        return 1
    print(
        "OK: %s holds exactly 1 line, %d characters, ASCII, "
        "punchline at the end" % (OUTPUT_PATH, len(JOKE))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
