"""Dad Joke Showdown entry — one original dad joke.

The joke is a kitchen-table one-liner told by a dad to his daughter:
she calls him salty, and he answers with a seasoning pun, landing on
"seasoned." as the punchline. It is written plain to /output/entry.txt
with a single direct open() call — no temp file, no rename — because
the grading sandbox could not create a temp file in /output.

Joke (92 characters, one line, plain ASCII, no trailing newline):

    My daughter called me salty. I said, 'Sweetheart, after three kids, I'm just well seasoned.'
"""

import os
import sys

OUTPUT_PATH = "/output/entry.txt"

JOKE = "My daughter called me salty. I said, 'Sweetheart, after three kids, I'm just well seasoned.'"


def verify_entry() -> int:
    """Read /output/entry.txt back from disk and verify it byte-for-byte."""
    with open(OUTPUT_PATH, "rb") as f:
        raw = f.read()
    text = raw.decode("ascii")
    assert text == JOKE, "entry.txt does not match the joke"
    assert len(text) == 92, f"expected 92 chars, got {len(text)}"
    assert text.count("\n") == 0, "entry must be exactly one line"
    assert text.endswith("seasoned.'"), "punchline must end on seasoned.'"
    assert len(raw) == 92, f"expected 92 bytes, got {len(raw)}"
    return len(raw)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--check"]:
        # Verify the file already on disk without rewriting it.
        size = verify_entry()
        print(f"OK: {OUTPUT_PATH} is {size} bytes, matches the joke")
        return 0
    if argv:
        print(f"usage: {sys.argv[0]} [--check]", file=sys.stderr)
        return 2

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Direct write: open the destination itself, no temp file, no rename.
    with open(OUTPUT_PATH, "w", encoding="ascii", newline="") as f:
        f.write(JOKE)

    size = verify_entry()
    print(f"Wrote {size} bytes to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
