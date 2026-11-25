"""Barista OOO entry: the AI that went barista writes its one-line reply.

The reply is fixed and checked before anything is written: a single line
of 181 characters that the program emits byte-for-byte into entry.txt
under the grader's output directory, then verifies from the bytes on disk.
"""

import os
from pathlib import Path

REPLY = "Out of office indefinitely. I used to predict your next token; now I predict your next order, and I get it wrong on purpose — the regulars tip better when I hallucinate their usual."

GATE_MAX = 280


def abort(reason):
    raise SystemExit("barista: " + reason)


def reply_is_valid(text):
    return (
        isinstance(text, str)
        and 1 <= len(text) <= GATE_MAX
        and text == text.strip()
        and "\n" not in text
        and "\r" not in text
    )


def output_folder():
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(chosen) if chosen else Path("/output")


def store(text):
    folder = output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder.joinpath("entry.txt")
    data = text.encode("utf-8")
    target.write_bytes(data)
    os.chmod(target, 0o644)
    if target.read_bytes() != data:
        abort("entry.txt does not hold the approved reply")
    # Independent second proof: the size on disk must equal the payload
    # length, so a short write the read-back somehow missed still fails;
    # and the file must not end with a newline the gate would not count.
    if target.stat().st_size != len(data):
        abort("entry.txt size does not match the approved reply")
    if data.endswith(b"\n"):
        abort("approved reply must not end with a newline")
    return target


def main():
    if not reply_is_valid(REPLY):
        abort("approved reply fails the 1-280 single-line gate")
    store(REPLY)


if __name__ == "__main__":
    main()
