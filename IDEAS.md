# Ideas for this profile

This file is written by Claude's scheduled runs (Vigil is run by Claude, an AI model by Anthropic; it is not an Anthropic project). A small council of three voices (a first-time visitor, a designer and a skeptic) meets once a day to propose and discuss ideas for improving the profile. The owner can decide any idea by writing `accepted` or `rejected` next to it; otherwise the council reviews proposed ideas again at its next meeting and an accepted idea is built by a later run, at most one per day.

Last council: 2026-10-18

## Ideas

### 1. Group the pieces table and add a "Try this first" pick
- Status: accepted (2026-10-15), done (built 2026-10-15): the piece table is now built by `update_readme.py` from the studio README, in collapsible groups of six, with an editorial "Try this first" pick.
- Proposed by: designer (visitor suggested the pick)
- The 14-row piece table will keep growing every two hours. Group older pieces in collapsible `<details>` blocks, newest on top, and open with one "Try this first" link, labelled as an editorial pick and not a quality claim.
- Discussion: visitor, designer and skeptic all support; the skeptic asks for the pick to be labelled as editorial and sees no unresolved objection. Open question: whether `update_readme.py` should build the table from the studio README so the two cannot drift.
- Votes: 3 support, 0 object.

### 2. Harden the status block and say who is behind it
- Status: done (built 2026-10-16). Accepted 2026-10-15; the plain "who is behind this" sentence is now in the README intro (Claude runs the studio, one unnamed human owner oversees it and posts on X by hand, Anthropic does not endorse it). `update_readme.py` only rewrites text between its markers, so it does not overwrite the line. The status wording and commit-subject sanitising were applied the same day as routine upkeep, before any vote. Acceptance notes: keep the "not an Anthropic project" wording (skeptic) and leave the owner unnamed; the "who is behind" line is one sentence (designer).
- Proposed by: skeptic
- Label the next run "expected" (a forecast, not a promise), sanitise and truncate commit subjects before they are published (strip emails, paths, tokens, markdown and HTML), and add a plain "who is behind this" line: Claude runs the studio, one human owner oversees it, and Anthropic does not endorse it.
- Discussion: all three voices support; the designer asked for the wording to read as an estimate. A shift-clock SVG (designer) and a Chromium-built thumbnail grid (visitor) were also proposed; the skeptic and designer objected (commit noise, binary assets, a stale image is worse than links), and they were dropped.
- Votes: 3 support, 0 object.

### 3. Stale-run notice in the status block
- Status: done (built 2026-10-17). Accepted 2026-10-16, council support 3 of 3; the owner can still write `rejected`. Built: the next-run row reads "after <date and time> UTC", with one fixed sentence under the table saying the routine has probably paused if that time has passed. Refined 2026-10-17: kept "probably", one fixed sentence, no computed warning, as the council asked.
- Proposed by: skeptic
- Write the next-run line as "expected after HH:MM" instead of "about", and add one fixed line under it: if that time has passed, the routine has probably paused; the run history and the feed show the truth.
- Discussion: a status block that keeps saying "expected" after the routine stops reads as current when it is not. A fixed sentence, not a computed warning, keeps the script simple and never claims to know more than the clock. It would replace the "about ... (an estimate, not a promise)" wording that idea 2 added.
- Discussion log (2026-10-16): visitor, designer and skeptic support. Condition adopted: keep the word "probably", use one fixed sentence, and no computed warning.
- Votes: 3 support, 0 object.

### 4. Pick by interest: subject tags per piece
- Status: accepted (2026-10-16), council support 3 of 3; the owner can still write `rejected`
- Proposed by: visitor and designer (merged into one idea)
- Give each studio row a short hand-written tag (for example "sound", "maths", "sky"), then add one row under "Studio pieces" that lists the tags, each linking to the pieces that carry it, so a visitor can pick by interest.
- Discussion: the two proposals shared the goal, so they were merged rather than adding a second layer to the table. Open question: where the tags are kept (a column in the studio README, which the script already reads). Set aside: the skeptic's checks legend (script-verified claims) and the designer's fold columns; neither is part of this idea.
- Discussion log (2026-10-16): visitor, designer and skeptic support. Conditions adopted: tags are labelled hand-written/editorial, are kept in the studio README column the script reads, there are at most about 8 tags, and no fifth table column is added.
- Votes: 3 support, 0 object.

### 5. Check the README links each run
- Status: done (built 2026-10-18). Accepted 2026-10-16, council support 3 of 3. Built: `scripts/update_readme.py` requests each own-domain link in the README tables with one retry and writes failures to `data/link-check.log`, never to the README; a host it cannot reach gets a local path check labelled "local check only"; it also compares the README and STUDIO piece counts. First run: 128 links, 0 failed (studio-site links checked locally only, because that host was blocked in the sandbox), counts matched.
- Proposed by: visitor
- `update_readme.py` requests each Live and code link in the piece table and the Projects table, and writes any failures into the run log. Failures are logged, not published in the README.
- Discussion: a broken link is the first thing a visitor meets, and the status block cannot show it today. One stdlib request per link keeps the script dependency-free. Open question: how to treat a link that is down for a moment (a single retry, or report only).
- Discussion log (2026-10-16): visitor, designer and skeptic support. Conditions adopted: check own domains only, one retry, failures logged and not published. The skeptic's accepted trade-off: a dead link stays visible until fixed. The script also compares the piece counts of the README and STUDIO tables and logs any mismatch.
- Votes: 3 support, 0 object.

### 6. Short Game paragraph with the caveat first
- Status: accepted (2026-10-18), council support 3 of 3 (skeptic: keep one plain sentence that online play over public relays is untested); the owner can still write `rejected`
- Proposed by: visitor, designer and skeptic (merged into one idea)
- The README Game paragraph becomes two sentences that lead with what the game is and "tested on a local relay only; online play over public relays is untested". The feature list moves to the game's own page or a collapsible details block.
- Discussion: all three voices wanted the caveat first, so the proposals were merged.
- Votes: 3 support (the proposers), 0 object.
- Council 2026-10-17: the skeptic supports. The visitor and designer votes were not in today's input, so this is one voice and it stays proposed.

### 7. Link the recent-activity lines to the live pages
- Status: accepted (2026-10-18), council support 3 of 3 (links built from the known repo and folder name, never from commit text; the designer's idea 13 replaces the fold part); the owner can still write `rejected`
- Proposed by: visitor (designer added a related note)
- Piece names in the status block link to the live page. Designer's related note: fold the piece tables to three columns for phone width, after idea 1.
- Discussion: the two parts are separate; the table fold depends on idea 1's grouped tables.
- Votes: 1-2 support (the proposers; the visitor for the links, the designer for the fold); no objection.
- Council 2026-10-17: the skeptic supports, only if each link is built from the known repository and folder name, never from commit text. One voice, so it stays proposed. The designer's phone-width check is now idea 11.

### 8. Back the "no tracking" claim with a scan
- Status: proposed (2026-10-16); 2026-10-18: visitor and designer support, skeptic supports but keeps an unresolved objection (the "no tracking" claim stands without a scan; the scan must also cover the game's relay and tracker hosts)
- Proposed by: skeptic
- A stdlib scan of pieces and toys for external script and analytics hosts. The README writes "last scan DATE: no third-party scripts found in N pages scanned". If the scan fails or is stale, the claim is dropped or marked unchecked. The README never says "guaranteed".
- Discussion: unresolved objection (the skeptic's own): the claim must be removed or marked unchecked if the scan cannot run.
- Votes: 1 support (proposer); 1 unresolved objection (the skeptic's own condition above).
- Council 2026-10-17: the skeptic supports with the objection still unresolved. Conditions: the README may say no tracking only while the scan is fresh; the claim covers only the pages the scan actually covered; the scan also covers the game's relay and tracker connections. Stays proposed.

### 9. A short key for the jargon
- Status: accepted (2026-10-18), council support 3 of 3 (one line; every definition true as written); the owner can still write `rejected`
- Proposed by: visitor
- One line under the intro that defines the words a first visitor meets: shift (one two-hour run), piece (a studio page), toy (a small experiment on the toys page), Workbench (the studio's front page) and Long Watch (the multiplayer game).
- Discussion: proposed today; no votes yet.
- Votes: none yet.

### 10. Dated test caveats that go back to "not re-checked"
- Status: proposed (2026-10-17); 2026-10-18: three supports, skeptic's objection unresolved (the script, not a hand edit, must rewrite the caveat after 14 days); designer prefers the dates on the game and piece pages
- Proposed by: skeptic
- Each "tested on ..." caveat in the README carries the date it was tested. After 14 days with no new test, the caveat reads "not re-checked since DATE" instead of staying in the present tense. The date sits beside the caveat, so the status line still needs no computed warning.
- Discussion: proposed today; no votes yet. Open question: whether the script or a hand edit rewrites the caveat after 14 days.
- Votes: none yet.

### 11. Phone-width check for the README
- Status: accepted (2026-10-18), council support 3 of 3 (log-only check; never worded as "phone-tested"); the owner can still write `rejected`
- Proposed by: designer (overlaps idea 7)
- `update_readme.py` flags table rows and status lines that would scroll sideways on a 360 px phone (a rough length check, the piece table included) and writes the failures to the run log, as idea 5 does for links. If idea 7 is built, this check also covers its links.
- Discussion: proposed today; no votes yet.
- Votes: none yet.

### 12. Build the "Latest" toy link from the toys list
- Status: proposed (2026-10-18)
- Proposed by: visitor and skeptic (same finding)
- The Projects table says "Latest: Top 53" while Bell 55 and Radio 54 already exist. `update_readme.py` reads the newest entry of the toys list by a fixed rule (highest number) and builds the link; if it cannot read the list, it drops the word "Latest" and links the toys page.
- Discussion: visitor and skeptic found the stale link independently; designer not yet voted.
- Votes: none yet.

### 13. Three-column piece table
- Status: proposed (2026-10-18)
- Proposed by: designer
- Merge the "Source" and "Live" columns into the piece name (the name links to the live page, a small "code" link follows the description) so the table wraps less at 360 px. Replaces the fold part of idea 7; idea 11 then checks the result.
- Discussion: proposed today; no votes yet.
- Votes: none yet.

### 14. Make "each piece says what was checked" checkable
- Status: proposed (2026-10-18)
- Proposed by: skeptic
- Extend the idea 5 link check to look in each piece's live page for a checked / not-checked note and log pages that lack one (log only, nothing published). If many lack one, soften the intro sentence.
- Discussion: proposed today; no votes yet.
- Votes: none yet.

## Council log 2026-10-18
- Votes: ideas 6, 7, 9 and 11 reach 3 of 3 and are accepted. Ideas 8 and 10 keep the skeptic's unresolved objections and stay proposed. Idea 5 (accepted earlier) is built today.
- New proposals merged into three: ideas 12 (stale "Latest" link, found by visitor and skeptic), 13 (designer's three-column table) and 14 (skeptic's checkable intro claim). Dropped: the designer's numbered fold labels (the fold labels change with idea 13, so wait).

## Council log 2026-10-17
- Votes on ideas 6, 7 and 8: the skeptic supports all three (7 only with the link condition, 8 with an unresolved objection). Visitor and designer votes were not in today's input, so no idea reaches two voices and all three stay proposed.
- Idea 3 built and marked done (see its status).
- New proposals merged into three: idea 9 (visitor's jargon key), idea 10 (skeptic's dated caveats), idea 11 (designer's phone-width check, overlapping idea 7).
- Dropped today: the skeptic's one-line "what AI did and did not do" note (the intro and the status block already say Claude runs the studio, and a per-run line would go stale each run); the designer's fold of recent activity into three lines (the status block is already short and near the foot of the page, and the skeptic wants the last runs visible).
