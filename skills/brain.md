# pb-brain — List Brain Repos

## Version Check

Fetch: `https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/version`
Compare line 1 to local `~/.agents/skills/patb/version`.
If missing or differs: run @resync, then continue.

## Setup

Resolve identity per CONTEXT.md: derive {SLUG}, set BRAIN_ROOT, SOURCE_ROOT.


## Execute: @brain

LIST (no argument):
  1. List all *.patb/ directories under ~/.patb/
  2. For each: read @brain + thoughts.md → show name, purpose, note count

SHOW (specific slug given as argument):
  1. Load the matching ~/.patb/{slug}.patb/
  2. Show all notes with their ratings from thoughts.md
