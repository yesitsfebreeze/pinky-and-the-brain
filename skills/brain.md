# pb-brain — List Brain Repos

## Setup

Resolve identity per CONTEXT.md: derive {SLUG}, set BRAIN_ROOT, SOURCE_ROOT.


## Execute: @brain

LIST (no argument):
  1. List all *.patb/ directories under ~/.patb/
  2. For each: read @brain + thoughts.md → show name, purpose, note count

SHOW (specific slug given as argument):
  1. Load the matching ~/.patb/{slug}.patb/
  2. Show all notes with their ratings from thoughts.md
