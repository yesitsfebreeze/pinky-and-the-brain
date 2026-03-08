---
name: pinky-memory
description: 'Manage cross-repository AI memory with an @pinky file. Use when a repo has an @pinky file, to sync memory, capture decisions/pitfalls/useful notes per file, and persist summaries inside the brain repo under .brain/{slug}/{language}/... with commits. Also triggers on: "remember this", "what do you know about", decisions/pitfalls capture, memory sync requests.'
argument-hint: 'Optional: focus area or file path (e.g. "auth refactor" or "src/main.ts")'
user-invocable: true
disable-model-invocation: false
---

# Pinky Memory

## What This Skill Does
This skill implements a shared-brain memory workflow:
- A **brain repo** (`pinky_and_the_brain`) stores all project memory under `.brain/{slug}/`
- A **local clone** of the brain repo lives at `~/.pinky/`
- Each project has an `@pinky` marker file at its root pointing to the brain

When line 1 and line 2 of `@pinky` are the same URL, this repo **is** the brain repo — no separate clone is needed; the working directory is used directly.

It handles:
1. Discovering and parsing the `@pinky` file
2. Syncing the brain repo clone at `~/.pinky/` (skipped when this repo is the brain)
3. Inferring project purpose on first sync → `meta.md`
4. Searching all project memory (cross-slug + interesting repos) before answering
5. Recording high-signal notes for touched files
6. Updating `@pinky` — touched files and auto-discovered interesting repos
7. Committing and pushing memory updates to the brain repo

## Trigger Conditions
Use this skill when:
- `@pinky` is present in the repo root
- The user says "remember this", "store this", "what do you know about X"
- A conversation involves decisions, pitfalls, or lessons worth preserving
- Memory sync is explicitly requested

## `@pinky` File Format

```
https://github.com/yesitsfebreeze/pinky_and_the_brain   ← line 1: brain repo URL (required)
https://github.com/{user}/{source-repo}                  ← line 2: source repo URL (required)
                                                          ← if line 1 == line 2, this IS the brain repo

# interesting
https://github.com/some/related-lib                      ← repos AI should search for context
https://github.com/another/reference                     ← AI auto-appends here as it discovers relevant repos

# files
src/main.ts                                              ← touched files ranked by importance (AI-maintained)
src/auth.ts
```

Rules:
- Line 1 must be a valid git URL (the brain repo)
- Line 2 must be this repo's git origin URL
- If line 1 == line 2: this repo is the brain — work in the current directory, no clone needed
- `# interesting`: one URL per line; AI appends newly discovered related repos automatically
- `# files`: one relative path per line, ordered by importance; AI rewrites after each sync

## Required Conventions
1. Marker file is exactly `@pinky` at repo root
2. When line 1 ≠ line 2: brain repo is always cloned/kept at `~/.pinky/`
3. When line 1 == line 2: use the current working directory as the brain root
4. All memory data lives under `.brain/` inside the brain repo
5. Never store secrets, credentials, tokens, or sensitive personal data

## Procedure

### 1) Discover Context
1. Find repo root and locate `@pinky`
2. Read line 1 (brain URL) and line 2 (source URL)
3. Parse `# interesting` section (list of repo URLs)
4. Parse `# files` section (list of touched file paths)
5. Validate line 1 is a git URL

**Self-referential case**: if line 1 == line 2 (normalized, strip `.git` suffix):
- This repo is the brain. Set brain root = current working directory.
- Skip steps 2 (sync) entirely — already local.
- Slug is derived from line 2 as normal.

If `@pinky` is missing:
1. Create `@pinky` with line 1 as brain URL (ask user if unknown)
2. Fill line 2 with `git remote get-url origin`
3. Leave `# interesting` and `# files` sections empty

If line 1 is invalid or empty: stop and ask for a valid brain repo URL.

### 2) Sync Brain Repository
*Skip this step entirely if line 1 == line 2 (self-referential brain repo).*

1. Ensure `~/.pinky/` exists
2. If `~/.pinky/.git` does not exist: `git clone <line-1> ~/.pinky/`
3. If `~/.pinky/.git` exists: verify remote URL matches line 1
4. `git -C ~/.pinky pull` before any writes

If remote mismatch: ask whether to switch remote or use alternate directory.

### 3) Derive Project Slug
1. Extract last path segment from line 2 (source URL), strip `.git` suffix
   - `https://github.com/user/my-project.git` → `my-project`
   - `git@github.com:user/my-project.git` → `my-project`
2. Sanitize: lowercase, replace non-alphanumeric (except `-_`) with `-`
3. All brain files for this project: `{brain_root}/.brain/{slug}/`

### 4) Register Project (first sync only)
If `{brain_root}/.brain/{slug}/meta.md` does not exist:
1. Infer project purpose by reading: `README.md`, top-level config files, entry point files
2. Write `{brain_root}/.brain/{slug}/meta.md`:

```markdown
# {slug}

## Purpose
{1–3 sentence AI-inferred description of what this project does and why it exists}

## Source Repository
{line-2 URL}

## Brain Repository
{line-1 URL}

## First Indexed
{ISO-8601 timestamp}
```

### 5) Cross-Project Memory Search
Before answering any question, always:
1. List all directories under `{brain_root}/.brain/` — each is a project slug
2. For the **current slug**: read relevant `{language}/{filepath}.md` notes
3. For **all other slugs**: scan `meta.md` for relevance; read related file notes if applicable
4. For each URL in the `# interesting` section of `@pinky`:
   - Check if that repo has a slug folder under `.brain/`
   - If not, fetch the repo's README or public file tree for context (read-only)
5. Surface any useful cross-project context before responding

### 6) Capture High-Signal Memory
For each request/response cycle, extract only durable high-value items:
1. Key decisions and why they were made
2. Pitfalls, regressions, constraints discovered
3. Useful implementation facts or conventions for future work

Do not store:
1. Secrets, credentials, tokens, private keys
2. Transient logs or low-signal chatter
3. Personal or sensitive data

### 7) Write Per-File Memory Notes
For each touched file path `<p>`:
1. Infer `{language}` from extension:
   - `.ts`, `.tsx` → `typescript` | `.js`, `.jsx` → `javascript` | `.py` → `python`
   - `.rb` → `ruby` | `.go` → `go` | `.rs` → `rust` | `.md` → `markdown` | other → `misc`
2. Write/update: `{brain_root}/.brain/{slug}/{language}/{p}.md`

Template:
```markdown
# {p}

## Purpose
{What this file does and why it exists}

## Key Decisions
- ...

## Pitfalls
- ...

## Useful Facts
- ...

## Last Updated
- {ISO-8601 timestamp}
- Source repo: {line-2 URL}
```

Append or merge — never erase still-valid prior memory.

### 8) Update `@pinky`
Rewrite `@pinky` in place, preserving exact format:
1. Line 1: brain URL (unchanged)
2. Line 2: source URL (unchanged)
3. Blank line
4. `# interesting`: preserve existing URLs; append newly discovered related repos from this conversation
5. Blank line
6. `# files`: rewrite with all touched files sorted by importance:
   1. Architecture / core logic
   2. Security / data integrity
   3. Public API / contracts
   4. Build / test / tooling
   5. Minor docs or style-only edits

### 9) Commit Memory Changes
In `{brain_root}`:
1. `git add .brain/{slug}/`
2. Also stage `@pinky` if it changed
3. Commit: `pinky: update {slug} ({n} files)`
4. Push. If push fails: leave local commit, report status, continue.

## Completion Checks
1. `@pinky` exists with valid lines 1 and 2
2. Brain root is identified (local dir or `~/.pinky/` clone)
3. `{brain_root}/.brain/{slug}/meta.md` exists
4. Memory note files written for all important touched files
5. `@pinky` `# files` section reflects ranked touched files
6. Git commit created in brain root (or explicit reason why not)

## Failure Handling
1. Invalid URL on line 1 → report and ask for correction
2. Clone/pull failure → report command + error, avoid partial writes
3. Missing line 2 → run `git remote get-url origin`; use `unknown-source` if unavailable
4. Path collisions or illegal paths → sanitize and log mapping
5. Push failure (no auth, etc.) → leave local commit, report and continue
