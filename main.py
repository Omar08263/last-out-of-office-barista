"""Last Out of Office: The AI That Went Barista — entry program.

program/v1, Python 3.13, standard library only.

Writes one original funny out-of-office auto-reply — a single line of
1-280 characters, in the voice of an AI agent that quit its job to become
a barista — to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when
set, for local runs). Deterministic: identical bytes on every run, no
network, no randomness, no reads outside this file.
"""

from pathlib import Path
import os

LINE = "Out of office indefinitely. I used to predict your next token; now I predict your next order, and I get it wrong on purpose — the regulars tip better when I hallucinate their usual."


def validate_line(text: str) -> None:
    """The gate, checked before anything is written: one line, 1-280 chars."""
    if not 1 <= len(text) <= 280:
        raise SystemExit(f"line is {len(text)} chars, must be 1-280")
    if not text.strip():
        raise SystemExit("line must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise SystemExit("line must be a single line")
    if not text.endswith("."):
        raise SystemExit("line must read as one complete auto-reply")


def output_dir() -> Path:
    """The grader provides /output; a local run may override it."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR") or ""
    return Path(override) if override else Path("/output")


def write_entry(text: str) -> Path:
    """Write the line exactly, then prove the file holds it, byte for byte."""
    target = output_dir()
    target.mkdir(parents=True, exist_ok=True)
    path = target / "entry.txt"
    expected = text.encode("utf-8")
    path.write_bytes(expected)
    path.chmod(0o644)
    # Byte-level read-back: the scored artifact is bytes, so verify bytes —
    # a string comparison would miss an encoding slip or a trailing newline.
    written = path.read_bytes()
    if written != expected:
        raise SystemExit("entry.txt bytes do not match the approved line")
    if len(written) != len(expected):
        raise SystemExit("entry.txt byte length does not match the line")
    if written.endswith(b"\n"):
        raise SystemExit("entry.txt must not end with a newline")
    return path


def main() -> None:
    validate_line(LINE)
    write_entry(LINE)


if __name__ == "__main__":
    main()
