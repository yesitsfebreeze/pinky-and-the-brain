# pb-brain — List Brain Repos

## Version Check

Read local version file: `~/.ptba/@brain/version`
Compare line 1 to local `~/.agents/skills/patb/version`.
If missing or differs: run @resync, then continue.

## Setup

Resolve identity per CONTEXT.md: derive {SLUG}, set BRAIN_ROOT, SOURCE_ROOT.


## Execute: @brain

LIST (no argument):
  1. Prefer central catalog at ~/.patb/@brain/repos.md for fast listing
  2. If catalog missing/stale, fall back to listing *.patb/ directories under ~/.patb/
  3. For each repo: read @brain + thoughts.md → show name, purpose, note count

SHOW (specific slug given as argument):
  1. Load the matching ~/.patb/{slug}.patb/
  2. Show all notes with their ratings from thoughts.md
