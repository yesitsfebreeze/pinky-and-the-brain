# pb-resync — Re-install p&b from Latest Main

## Main Repo Sync

Before executing this command, ensure main p&b repo is current:
`git -C ~/.patb/@brain pull --rebase`
If `~/.patb/@brain/.git` is missing, clone first:
`git clone https://github.com/yesitsfebreeze/pinky-and-the-brain ~/.patb/@brain`
If sync fails, stop and report the error.

## Execute: @resync

RESYNC WORKFLOW:
  1. Inform the user: "Running @resync — re-installing p&b from latest main. Your notes, linked repos, and MCP server will be updated."
  2. Set RESYNC = TRUE internally.
  3. Capture current main-repo head before running setup:
    `OLD_HEAD=$(git -C ~/.patb/@brain rev-parse HEAD)`
  4. Read and execute: `~/.patb/@brain/SETUP.md`
    (Runs in UPDATE mode, preserving user content and overwriting infrastructure.)
  5. After setup, detect whether MCP sources changed between heads:
    `NEW_HEAD=$(git -C ~/.patb/@brain rev-parse HEAD)`
    `git -C ~/.patb/@brain diff --name-only "$OLD_HEAD" "$NEW_HEAD" -- mcp/`
  6. If any path under `mcp/` changed, rebuild MCP immediately:
    - Linux/macOS:
     `npm install --prefix "$HOME/.agents/skills/patb/mcp" && npm run build --prefix "$HOME/.agents/skills/patb/mcp"`
    - Windows:
     `npm install --prefix "%USERPROFILE%\\.agents\\skills\\patb\\mcp" && npm run build --prefix "%USERPROFILE%\\.agents\\skills\\patb\\mcp"`
  7. If rebuild fails, report the error and instruct the user to fix Node.js/npm and rerun `@resync`.
