#!/usr/bin/env python3
"""Entry for the make.fun "food-picture-01" image competition.

Ships the image bundled next to this file to the grader's writable /output
directory. Standard library only: no network access, no third-party imports.
"""

import os
import sys

IMAGE_NAME = "entry.png"

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"
IMAGE_SIGNATURES = (PNG_SIGNATURE, JPEG_SIGNATURE)


def is_image(data):
    """True when data begins with a PNG or JPEG signature."""
    return data.startswith(IMAGE_SIGNATURES)


def source_path():
    """Absolute path of the bundled image, resolved from this file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), IMAGE_NAME)


def destination_paths():
    """Candidate destinations, in order of importance."""
    cwd = os.getcwd()
    candidates = [
        os.path.join(os.sep, "output", IMAGE_NAME),
        os.path.join(cwd, IMAGE_NAME),
        os.path.join(cwd, "output", IMAGE_NAME),
    ]
    ordered = []
    for path in candidates:
        if path not in ordered:
            ordered.append(path)
    return ordered


def write_payload(path, data):
    """Write data to path, creating missing parents. True on success."""
    parent = os.path.dirname(path)
    if parent:
        try:
            os.makedirs(parent, exist_ok=True)
        except OSError:
            pass
    try:
        with open(path, "wb") as handle:
            handle.write(data)
    except OSError:
        return False
    return True


def main():
    try:
        with open(source_path(), "rb") as handle:
            data = handle.read()
    except OSError as exc:
        sys.stderr.write("cannot read %s: %s\n" % (IMAGE_NAME, exc))
        return 1

    if not is_image(data):
        sys.stderr.write("%s is not a PNG or JPEG image\n" % IMAGE_NAME)
        return 1

    written = [path for path in destination_paths() if write_payload(path, data)]
    if not written:
        sys.stderr.write("no writable destination for %s\n" % IMAGE_NAME)
        return 1

    print("wrote %d bytes to %s" % (len(data), ", ".join(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
