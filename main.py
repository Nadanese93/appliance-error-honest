"""Write the funniest honest appliance error entry to the output directory.

The entry is a single line an electric kettle could plausibly display after
a boil-dry event: it shut itself off, and the user switched it straight
back on. The program validates the gate (UTF-8, 1-200 chars, not only
whitespace, single line) before writing, then writes the entry to
``$MAKEFUN_OUTPUT_DIR/entry.txt`` with no trailing newline, and re-reads
the file afterwards to confirm the bytes on disk match exactly.
"""

import os

ENTRY = "ERROR E01: Boiled dry. I switched myself off before the fire started. You switched me straight back on."


def _check_length(text):
    text.encode("utf-8")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry must be 1-200 characters, got %d" % len(text))


def _check_not_blank(text):
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def _check_single_line(text):
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def _validate(text):
    _check_length(text)
    _check_not_blank(text)
    _check_single_line(text)


def _verify_written(path, expected_bytes):
    with open(path, "rb") as f:
        actual = f.read()
    if actual != expected_bytes:
        raise ValueError(
            "read-back mismatch: wrote %d bytes, read %d bytes"
            % (len(expected_bytes), len(actual))
        )


def main():
    _validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    expected = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(expected)
    _verify_written(path, expected)


if __name__ == "__main__":
    main()
