# Pinky & The Brain — Updater

This file is fetched and executed when a version mismatch is detected.
The SKILL.md session lifecycle triggers this check automatically.


## Version Check

Remote version URLs (raw from main branch):
```
INSTALL_VERSION_URL: https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/install.version
SKILL_VERSION_URL:   https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/skill.version
```

Local version files:
```
{BRAIN_ROOT}/install.version   — written during install
~/.agents/skills/patb/skill.version  — written during install
```

Each version file has two lines:
```
{SEMVER}
{ISO8601_TIMESTAMP}
```

Compare by timestamp (line 2). If remote is newer → update needed.
Report to the user which component(s) are outdated before proceeding.


## Skill Update

When `skill.version` is outdated:

1. Delete `~/.agents/skills/patb/SKILL.md`
2. Delete `~/.agents/skills/patb/skill.version`
3. Re-create both using the current INSTALL.md Skill Bootstrap section:
   - Fetch INSTALL.md from remote
   - Execute only the **Skill Bootstrap** section
4. Write the new remote `skill.version` content to `~/.agents/skills/patb/skill.version`
5. Inform the user: "Skill updated to {NEW_VERSION}."


## Install Update

When `install.version` is outdated:

1. Fetch the current INSTALL.md from remote:
   ```
   https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/INSTALL.md
   ```

2. Compare each installed artifact against what the new INSTALL.md would produce.
   Only update artifacts that have actually changed — preserve user content where noted.

### Artifacts to check:

**Always-Active Instructions** (environment-specific path):
  - Re-detect environment using the INSTALL.md detection table
  - Compare current instructions file content against new template
  - If different: overwrite with new content (fill in project-specific variables)

**@pinky** ({SOURCE_ROOT}/@pinky):
  - Format is user-managed (repo URL + linked repos)
  - Do NOT overwrite — only verify line 1 has a valid URL

**@brain** ({BRAIN_ROOT}/@brain):
  - Compare structure against new INSTALL.md @brain template
  - Preserve: user-edited YAML values (MAX_NOTES, MIN_RATING, FOLLOW, AVOID)
  - Preserve: user-edited title and description
  - Update: any new required fields the template introduces
  - If new fields were added: merge them in with defaults

**Memory files** (thoughts.md, tree.md, changes.md, sync.md):
  - Do NOT overwrite — these contain accumulated data
  - Only create if missing (same as install behavior)

3. Write the new remote `install.version` content to `{BRAIN_ROOT}/install.version`

4. Commit and push brain repo:
   ```
   git -C {BRAIN_ROOT} add -A
   git -C {BRAIN_ROOT} diff --cached --quiet || git -C {BRAIN_ROOT} commit -m "pb: update install to {NEW_VERSION}"
   git -C {BRAIN_ROOT} push
   ```

5. Inform the user: "Install updated to {NEW_VERSION}. Changed: {LIST_OF_UPDATED_ARTIFACTS}."


## Both Outdated

If both are outdated, run Skill Update first, then Install Update.
Report a combined summary at the end.
