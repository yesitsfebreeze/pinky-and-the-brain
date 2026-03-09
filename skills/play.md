# pb-play — Execute Next Todo

## Setup

Resolve identity per CONTEXT.md: derive {SLUG}, set BRAIN_ROOT, SOURCE_ROOT.
Sync: `git -C {BRAIN_ROOT} pull --rebase`


## Execute: @play

TODO WORKFLOW:
  1. Open {SOURCE_ROOT}/@plan.
     If missing: inform user, offer to create it.
     WRITE STATUS play: read @pinky, update or append `STATUS: play`, save.
  2. Parse the separator line (█████████████████████):
     - Content above the separator: raw ideas
     - Content below the separator: AI-generated actionable todos
  3. Select the next todo:
     - If AI-generated todos exist (below separator): pick the most impactful one
       based on current session context and brain notes.
     - If no AI-generated todos exist: look at raw ideas (above separator),
       select the most actionable, convert it to a todo and append below the separator,
       then proceed to implement it.
  4. Gather context: load relevant notes from thoughts.md, check tree.md for
     impacted files, read source files as needed.
  5. Implement the selected todo using available tools.
  6. When done: delete the todo text from {SOURCE_ROOT}/@plan (below separator).
  7. Commit all changes to the source repo:

```
git -C {SOURCE_ROOT} add -A
git -C {SOURCE_ROOT} diff --cached --quiet || git -C {SOURCE_ROOT} commit -m "{SUMMARY}"
```

  8. When no todos remain (above or below separator):
     CLEAR STATUS: read @pinky, remove any `STATUS: ...` line, save.
  9. Report what was done and what the next todo would be.

If `@play` is called with no above-separator content and no below-separator todos:
  Inform the user and ask what to work on.
