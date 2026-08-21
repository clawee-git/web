#!/usr/bin/env python3
"""embed-cli-help.py — inject verbatim CLI help sections into page slots.

Sources: docs/clawee/cli-help.md, docs/claweed/cli-help.md (each: a top
`# <binary> — CLI reference` block, then one or more `## <heading>` sections
— a one-line summary paragraph followed by the first fenced ``` block, the
verbatim help page for that heading).

Pages mark slots as:
    <!-- cli-embed: <binary> <section path> -->
    ...
    <!-- /cli-embed -->
where "<binary> <section path>" is the exact text of a `## ` heading in the
matching source md (e.g. "clawee gateway use", or the top page as "clawee").

--write   rewrites every slot's interior in place across docs/*/index.html.
--check   prints DRIFT/UNKNOWN SECTION lines for any slot that would change
          or names a section that does not exist; exits 1 if any, else 0
          silently. Unknown section is an error in both modes.

Only the bytes strictly between the paired comments are ever touched.
"""
import glob
import html
import re
import sys

SOURCES = {
    "clawee": "docs/clawee/cli-help.md",
    "claweed": "docs/claweed/cli-help.md",
}

HEADING_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
SLOT_OPEN_RE = re.compile(r"<!-- cli-embed: (.+?) -->")
SLOT_CLOSE = "<!-- /cli-embed -->"


class FormatError(Exception):
    pass


def parse_sections(md_text, source_path):
    """Return {heading text: (summary, fence_body)} for one source md."""
    sections = {}
    headings = list(HEADING_RE.finditer(md_text))
    for i, m in enumerate(headings):
        heading = m.group(1).strip()
        body_start = m.end()
        body_end = headings[i + 1].start() if i + 1 < len(headings) else len(md_text)
        body = md_text[body_start:body_end]

        lines = body.split("\n")
        # Skip leading blank lines, then find the first fenced ``` block —
        # everything in between (if anything) is the summary paragraph.
        # (Some sections, e.g. the top-level binary page, have no summary
        # at all: heading -> blank -> fence.)
        idx = 0
        while idx < len(lines) and lines[idx].strip() == "":
            idx += 1
        fence_start = None
        for j in range(idx, len(lines)):
            if lines[j].strip() == "```":
                fence_start = j
                break
        if fence_start is None:
            raise FormatError(
                f"{source_path}: section {heading!r} has no fenced block"
            )
        summary = " ".join(
            l.strip() for l in lines[idx:fence_start] if l.strip() != ""
        ).strip()
        fence_close = None
        for j in range(fence_start + 1, len(lines)):
            if lines[j].strip() == "```":
                fence_close = j
                break
        if fence_close is None:
            raise FormatError(
                f"{source_path}: section {heading!r} has an unterminated fenced block"
            )
        fence_body = "\n".join(lines[fence_start + 1 : fence_close])

        if heading in sections:
            raise FormatError(f"{source_path}: duplicate section heading {heading!r}")
        sections[heading] = (summary, fence_body)
    return sections


def load_all_sections():
    sections = {}
    for binary, path in SOURCES.items():
        with open(path, encoding="utf-8") as f:
            text = f.read()
        sections[binary] = parse_sections(text, path)
    return sections


def render_slot(summary, fence_body):
    return (
        "\n"
        f'<p class="mut">{html.escape(summary)}</p>\n'
        f'<pre class="help">{html.escape(fence_body)}</pre>\n'
    )


def find_slots(page_text, page_path):
    """Yield (slot_name, open_start, open_end, close_start, close_end) for
    every top-level slot in page_text, in document order. Raises
    FormatError on nested or unpaired markers."""
    slots = []
    pos = 0
    length = len(page_text)
    while True:
        open_m = SLOT_OPEN_RE.search(page_text, pos)
        close_idx = page_text.find(SLOT_CLOSE, pos)
        if open_m is None and close_idx == -1:
            break
        if open_m is None:
            raise FormatError(f"{page_path}: unpaired {SLOT_CLOSE!r} with no opening marker")
        if close_idx == -1:
            raise FormatError(
                f"{page_path}: slot {open_m.group(1)!r} has no matching {SLOT_CLOSE!r}"
            )
        if close_idx < open_m.start():
            raise FormatError(f"{page_path}: unpaired {SLOT_CLOSE!r} before any opening marker")
        # Reject a second opening marker before this one's close (nesting).
        next_open = SLOT_OPEN_RE.search(page_text, open_m.end())
        if next_open is not None and next_open.start() < close_idx:
            raise FormatError(
                f"{page_path}: nested cli-embed marker inside slot {open_m.group(1)!r}"
            )
        slot_name = open_m.group(1).strip()
        slots.append((slot_name, open_m.start(), open_m.end(), close_idx, close_idx + len(SLOT_CLOSE)))
        pos = close_idx + len(SLOT_CLOSE)
    _ = length
    return slots


def process_page(page_path, sections, write):
    with open(page_path, encoding="utf-8") as f:
        text = f.read()

    slots = find_slots(text, page_path)
    if not slots:
        return [], text, False

    problems = []
    changed = False
    out = []
    cursor = 0
    for slot_name, o_start, o_end, c_start, c_end in slots:
        binary = slot_name.split(" ", 1)[0]
        binary_sections = sections.get(binary)
        entry = binary_sections.get(slot_name) if binary_sections is not None else None
        if entry is None:
            problems.append(f"UNKNOWN SECTION {page_path} {slot_name}")
            continue
        summary, fence_body = entry
        wanted_interior = render_slot(summary, fence_body)
        current_interior = text[o_end:c_start]
        if current_interior != wanted_interior:
            if write:
                changed = True
            else:
                problems.append(f"DRIFT {page_path} {slot_name}")
        if write and entry is not None:
            out.append(text[cursor:o_end])
            out.append(wanted_interior)
            cursor = c_start

    if write:
        out.append(text[cursor:])
        new_text = "".join(out)
        return problems, new_text, changed
    return problems, text, False


def main(argv):
    if len(argv) != 1 or argv[0] not in ("--write", "--check"):
        print("usage: embed-cli-help.py --write|--check", file=sys.stderr)
        return 2
    write = argv[0] == "--write"

    try:
        sections = load_all_sections()
    except (FormatError, OSError) as e:
        print(f"ERROR {e}", file=sys.stderr)
        return 1

    problems = []
    had_error = False
    for page_path in sorted(glob.glob("docs/*/index.html")):
        try:
            page_problems, new_text, changed = process_page(page_path, sections, write)
        except FormatError as e:
            print(f"ERROR {e}", file=sys.stderr)
            had_error = True
            continue
        problems.extend(page_problems)
        if write and changed:
            with open(page_path, "w", encoding="utf-8") as f:
                f.write(new_text)

    for line in problems:
        print(line)

    if had_error or problems:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
