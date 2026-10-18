#!/usr/bin/env python3
"""Regenerate the routine-status block in README.md (stdlib only).

Usage: python3 scripts/update_readme.py [--repos DIR] [--no-bump] [--no-links]
DIR holds the three cloned repos side by side (default: the parent folder).
Each run bumps the counter in data/state.json, stamps the time, and lists
the latest commits across the repos. Text between the STATUS markers is replaced.
It also rebuilds the "Studio pieces" section (between the PIECES markers) from
the pieces table in the studio README (DIR/vigilstudio.github.io/README.md), so the
two cannot drift: newest first, in collapsible groups, every piece listed.
Finally it checks the README's own-domain links (see check_links) and appends the result to
data/link-check.log. Failures go to that log only and are never written into the README.
"""
import argparse, json, re, subprocess, sys, urllib.request, urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "state.json"
README = ROOT / "README.md"
START, END = "<!-- STATUS:START -->", "<!-- STATUS:END -->"
PSTART, PEND = "<!-- PIECES:START -->", "<!-- PIECES:END -->"
STUDIO = "vigilstudio.github.io"
SITE = f"https://{STUDIO}/"
FEED = f"{SITE}feed.xml"
CODE = f"https://github.com/vigilstudio/{STUDIO}/tree/main/"
GROUP = 6          # pieces per group; the newest group is open, older ones are closed
PICK = "illusions"  # editorial "Try this first" pick (folder name); change by hand
REPOS = ["vigilstudio", "vigilstudio.github.io", "toys"]
INTERVAL = timedelta(hours=2)
FMT = "%Y-%m-%d %H:%M UTC"
LOG = ROOT / "data" / "link-check.log"
OWN = (f"https://{STUDIO}/", "https://github.com/vigilstudio/")


def recent_commits(base, limit=5):
    rows = []
    for name in REPOS:
        path = base / name
        if not path.is_dir():
            continue
        out = subprocess.run(
            ["git", "-C", str(path), "log", "-n", str(limit), "--format=%ct%x09%h%x09%s"],
            capture_output=True, text=True)
        for line in out.stdout.splitlines():
            ts, sha, subject = line.split("\t", 2)
            subject = subject.split(" Co-Authored-By:")[0].strip()
            rows.append((int(ts), name, sha, subject))
    rows.sort(reverse=True)
    return rows[:limit]


def esc(s):
    """Make a commit subject safe to publish: drop addresses, paths and tokens, then neutralise markdown/HTML."""
    s = re.sub(r"\S+@\S+", "", s)
    s = re.sub(r"(?i)\b[a-z]:\\\S*", "", s)
    s = re.sub(r"\b(?:gh[pousr]_|github_pat_|sk-)\w+", "", s)
    s = re.sub(r"[\r\n`\[\]*_~]", "", s)
    s = s.replace("|", "\\|").replace("<", "&lt;").replace(">", "&gt;").strip()
    return s if len(s) <= 90 else s[:89] + "…"


def short(desc, limit=150):
    """Shorten a studio description to a complete clause ending in a full stop, else at a word with an ellipsis.

    Cuts only where the parentheses so far are balanced (no "(91 agree" left open), preferring a sentence
    end, semicolon or colon over a comma. Without a clean cut it ends with an ellipsis, which says it was shortened."""
    desc = desc.strip().rstrip(".")
    if len(desc) <= limit:
        return desc + "."
    head = desc[:limit + 1]
    cuts = [m.start() for m in re.finditer(r"\. |;|:|, ", head)
            if m.start() >= 40 and head[:m.start()].count("(") == head[:m.start()].count(")")]
    strong = [c for c in cuts if head[c] in ".;:"]
    if cuts:
        pos = (strong or cuts)[-1]
        return head[:pos].rstrip(" ,;:.") + "."
    return head[:limit].rsplit(" ", 1)[0].rstrip(" ,;:.") + "…"


def studio_pieces(base):
    """Rows (name, folder, description) from the studio README table, oldest first; None if unreadable."""
    path = base / STUDIO / "README.md"
    if not path.is_file():
        return None
    rows = []
    for line in path.read_text().splitlines():
        m = re.match(r"\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*\[`([\w.-]+)/`\]", line)
        if m:
            rows.append((m.group(1), m.group(3), m.group(2)))
    return rows or None


def build_pieces(rows):
    new = rows[::-1]
    groups = [new[i:i + GROUP] for i in range(0, len(new), GROUP)]
    out = [PSTART, "### Studio pieces", ""]
    pick = next((r for r in rows if r[1] == PICK), None)
    if pick:
        out += [f"**Try this first** (an editorial pick by Claude, not a ranking or a claim that it is the best): "
                f"[{pick[0]}]({SITE}{pick[1]}/). {short(pick[2])}", ""]
    out += [f"{len(rows)} pieces, newest first. Every group lists all of its pieces; open a group to see them. These are short summaries: each page says what was checked and what was not.", ""]
    for n, g in enumerate(groups, 1):
        label = "Newest" if n == 1 else ("Oldest" if n == len(groups) else "Earlier")
        names = f"{g[0][0]} to {g[-1][0]}" if len(g) > 1 else g[0][0]
        out += [f"<details{' open' if n == 1 else ''}>",
                f"<summary><b>{label}: {len(g)} piece{'s' if len(g) != 1 else ''}</b> ({esc(names)})</summary>", "",
                "| Piece | What it is | Source | Live |", "|---|---|---|---|"]
        for name, folder, desc in g:
            out.append(f"| **{name}** | {short(desc)} | [code]({CODE}{folder}) | [open]({SITE}{folder}/) |")
        out += ["", "</details>", ""]
    out.append(PEND)
    return "\n".join(out)


def build(now, runs, fixed, commits):
    nxt = now + INTERVAL
    lines = [
        START,
        f"| | |", "|---|---|",
        f"| 🕒 **Last run** | {now.strftime(FMT)} |",
        f"| ⏭️ **Expected next run** | after {nxt.strftime(FMT)} |",
        f"| 🔁 **Runs completed so far** | {runs} (counted from 14 Oct 2026) |",
        f"| 🛠️ **Issues fixed so far** | {fixed} |",
        "",
        f"If that time has passed, the routine has probably paused; the recent activity below and the [feed]({FEED}) show what really ran.",
        "",
        "**Recent activity**",
        "",
    ]
    for ts, name, sha, subject in commits:
        d = datetime.fromtimestamp(ts, timezone.utc).strftime("%b %d %H:%M")
        lines.append(f"- `{d}` **{name}**: {esc(subject)} (`{sha}`)")
    lines.append(END)
    return "\n".join(lines)


def table_links(text):
    """Own-domain URLs found in the README's table rows (Projects and pieces tables), in order, unique."""
    seen = []
    for line in text.splitlines():
        if line.lstrip().startswith("|"):
            for u in re.findall(r"\]\((https?://[^)\s]+)\)", line):
                if u.startswith(OWN) and u not in seen:
                    seen.append(u)
    return seen


def fetch(url):
    """None if the link answers 2xx/3xx, else a short reason. Network errors are returned as 'net: ...'."""
    req = urllib.request.Request(url, headers={"User-Agent": "vigilstudio-link-check"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return None if r.status < 400 else f"HTTP {r.status}"
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}"
    except Exception as e:
        return f"net: {type(e).__name__} {e}"[:120]


def local_ok(url, base):
    """Does the link's path exist in the local checkouts? Returns None if so, else a reason."""
    if url.startswith(SITE):
        rel = url[len(SITE):].split("#")[0].split("?")[0]
        in_toys = rel == "toys" or rel.startswith("toys/")
        root = base / ("toys" if in_toys else STUDIO)
        if in_toys:
            rel = rel[len("toys"):].lstrip("/")
        path = root / rel
        ok = (path / "index.html").is_file() if (path.is_dir() or not rel) else path.is_file()
    else:
        parts = url[len(OWN[1]):].strip("/").split("/")
        root = base / parts[0]
        rel = "/".join(parts[3:]) if len(parts) > 3 and parts[1:3] != [] and parts[1] in ("tree", "blob") else ""
        ok = root.is_dir() and (root / rel).exists() if len(parts) == 1 or rel or len(parts) == 3 else root.is_dir()
    return None if ok else "path not found locally"


def readme_piece_count(text):
    return sum(1 for l in text.splitlines() if re.match(r"\|\s*\*\*.+?\*\*\s*\|.*\[code\]\(" + re.escape(CODE), l))


def studio_table_count(base):
    path = base / STUDIO / "STUDIO.md"
    if not path.is_file():
        return None
    n, on = 0, False
    for l in path.read_text().splitlines():
        if l.startswith("| Piece |"):
            on = True
        elif on and l.startswith("|---"):
            continue
        elif on and l.startswith("|"):
            n += 1
        elif on:
            break
    return n


def check_links(text, base, now):
    """Request every own-domain table link (one retry); log failures to data/link-check.log, never to the README.

    If the network is unreachable (first request fails at connection level, e.g. a blocked sandbox),
    fall back, per unreachable host, to checking that each path exists in the local checkouts and label the entry "local check only"."""
    links = table_links(text)
    hosts = {}  # host -> True when unreachable at connection level; the first request to a host doubles as the probe
    bad = []
    for u in links:
        h = u.split("/")[2]
        if h not in hosts:
            r = fetch(u)
            hosts[h] = (r or "").startswith("net:")
        else:
            r = None if hosts[h] else fetch(u)
        if hosts[h]:
            r = local_ok(u, base)
        elif r:
            r = fetch(u)  # one retry
        if r:
            bad.append((u, r))
    local = any(hosts.values())
    rc, sc = readme_piece_count(text), studio_table_count(base)
    out = [f"{now.strftime(FMT)} | {'local check only for ' + ', '.join(h for h in hosts if hosts[h]) + ' (network unreachable)' if local else 'live requests'} | "
           f"{len(links)} links, {len(bad)} failed"]
    out += [f"  FAIL {u} ({r})" for u, r in bad]
    if sc is None:
        out.append("  piece counts: STUDIO.md not found")
    elif rc != sc:
        out.append(f"  MISMATCH piece counts: README {rc}, STUDIO.md {sc}")
    else:
        out.append(f"  piece counts match: {rc}")
    with LOG.open("a") as f:
        f.write("\n".join(out) + "\n")
    return out[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repos", default=str(ROOT.parent))
    ap.add_argument("--no-links", action="store_true", help="skip the link check")
    ap.add_argument("--no-bump", action="store_true", help="do not increment the counter")
    a = ap.parse_args()
    text = README.read_text()
    i, j = text.find(START), text.find(END)
    if i < 0 or j < i:
        sys.exit("STATUS markers not found in README.md")  # checked before the counter moves
    state = json.loads(STATE.read_text()) if STATE.exists() else {"runs": 0}
    if not a.no_bump:
        state["runs"] += 1
    now = datetime.now(timezone.utc)
    state["last_run"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    STATE.write_text(json.dumps(state, indent=2) + "\n")
    rows = studio_pieces(Path(a.repos))
    i, j = text.find(PSTART), text.find(PEND)
    if rows and 0 <= i < j:
        text = text[:i] + build_pieces(rows) + text[j + len(PEND):]
    elif rows is None:
        print("studio README not found; pieces section left as is", file=sys.stderr)
    else:
        print("PIECES markers not found in README.md; pieces section left as is", file=sys.stderr)
    i, j = text.find(START), text.find(END)
    block = build(now, state["runs"], state.get("issues_fixed", 0), recent_commits(Path(a.repos)))
    text = text[:i] + block + text[j + len(END):]
    README.write_text(text)
    if not a.no_links:
        print("link check:", check_links(text, Path(a.repos), now), "(details in data/link-check.log)")
    print(f"runs={state['runs']} next={(now + INTERVAL).strftime(FMT)}")


if __name__ == "__main__":
    main()
