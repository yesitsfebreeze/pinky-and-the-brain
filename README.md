# 🧠 Pinky & The Brain

Persistent AI memory that lives in your repo. One URL. Zero config.

## Why It Exists

AI coding assistants are stateless. Every new session starts cold — no memory of
your rules, your decisions, your half-finished ideas, or the quirks of your codebase.
You spend the first few minutes re-explaining context that the agent already "knew"
yesterday.

Pinky & The Brain fixes this by giving the agent a structured memory it reads on
every session start. It's not a plugin or an extension — it's just a file (`pinky.brain`)
that tells the agent what to remember and how to maintain it.

## Why It Works

- **It's just instructions.** `pinky.brain` is a plain text file the agent reads at boot.
  No API keys, no servers, no integrations. Any agent that can read a file can use it.
- **The agent maintains itself.** The brain tells the agent exactly when and how to write
  to memory — rules, ideas, notes, todos, files. The agent handles everything else.
- **Memory is scored and decayed.** Entries are ranked by relevance and impact. Low-signal
  notes decay and get discarded over time so the brain stays focused, not bloated.
- **Branches stay clean.** Memory lives on a separate orphan branch (`pinky`) via a git
  worktree at `.pinky/`. Your working branches never see brain files in their history.
- **It travels with the repo.** `pinky.brain` is committed to your project. Any agent
  opening the repo picks it up immediately — no setup required per machine or collaborator.

## Install

Tell your AI agent:

```
Follow instructions in https://raw.githubusercontent.com/yesitsfebreeze/pinky-and-the-brain/refs/heads/main/pinky.brain?v=3
```

That's it. The agent will:
1. Fetch `pinky.brain` and save it to your project root
2. Create `.pinky/` with the required data files
3. Add `.pinky/` to `.gitignore`
4. Start remembering

Works with any AI coding assistant that can read URLs and write files.

## What It Does

- **Rules** — Coding preferences that persist across sessions
- **Ideas** — Things to build, scored by relevance + impact
- **Notes** — Discovered context, auto-decayed by freshness
- **Todos** — Tracked tasks with priority scoring
- **Files** — Registry of important files in your project

## Multi-Repo

Each subfolder can have its own `.pinky/` — monorepos, submodules, vendor packages.
Add external brain repos to the SOURCES section in `pinky.brain`:

```
@https://github.com/org/shared-standards.git
@https://github.com/org/team-conventions.git
```

## Branch Isolation

Memory data lives on a separate orphan branch (`pinky`).
Your working branches stay clean — no `.brain` files in your commits.
