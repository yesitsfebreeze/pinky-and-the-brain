# p&b MCP Server

MCP server for Pinky & The Brain — provides typed tool calls and resource access so AI assistants interact with brain memory programmatically instead of writing raw markdown.

## Tools

| Tool | Description |
|---|---|
| `remember(text, concepts[], sources[], rating?)` | Store a rated note into thoughts.md |
| `forget(query)` | Search + remove matching notes |
| `query(topic, depth?)` | Search thoughts.md + linked repos with concept expansion |
| `prune(threshold?)` | Remove notes below threshold |
| `sync()` | Pull brain repo, rebase, push |
| `plan_add(todo)` | Add a todo below the @plan separator |
| `plan_next()` | Return the next highest-impact todo |
| `plan_complete(todo)` | Mark a todo done and remove it |

## Resources

| URI | Description |
|---|---|
| `patb://thoughts` | Full note pool (thoughts.md) |
| `patb://tree` | File impact map (tree.md) |
| `patb://changes` | Cross-project changelog (changes.md) |
| `patb://plan` | Current @plan file contents |

## Setup

```json
// .vscode/mcp.json
{
  "servers": {
    "patb": {
      "command": "node",
      "args": ["${workspaceFolder}/../.agents/skills/patb/mcp/dist/index.js"]
    }
  }
}
```

## Structure

```
mcp/
  package.json
  tsconfig.json
  src/
    index.ts              — MCP server entry
    config.ts             — parse @brain YAML config
    tools/
      remember.ts
      forget.ts
      query.ts
      prune.ts
      sync.ts
      plan.ts
    resources/
      thoughts.ts
      tree.ts
      changes.ts
      plan.ts
    lib/
      storage.ts          — read/write markdown memory files
      note.ts             — note schema + validation
      concepts.ts         — concept tag index (concepts.md)
      git.ts              — git operations (pull, commit, push)
```
