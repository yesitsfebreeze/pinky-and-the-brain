# pb-forget — Remove a Note

## Version Check

Fetch: `https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/version`
Compare line 1 to local `~/.agents/skills/patb/version`.
If missing or differs: run @resync, then continue.

## Setup

Resolve identity per CONTEXT.md: derive {SLUG}, set BRAIN_ROOT, SOURCE_ROOT.
Sync: `git -C {BRAIN_ROOT} pull --rebase`


## Execute: @forget

FORGET:
  1. Search {BRAIN_ROOT}/thoughts.md for matching notes
  2. Show matches, ask for confirmation
  3. Remove confirmed notes
  4. Re-sort by rating (highest first)
  5. Commit and push:

```
git -C {BRAIN_ROOT} pull --rebase
git -C {BRAIN_ROOT} add -A
git -C {BRAIN_ROOT} diff --cached --quiet || git -C {BRAIN_ROOT} commit -m "pb: forget - {SUMMARY}"
git -C {BRAIN_ROOT} push
```
