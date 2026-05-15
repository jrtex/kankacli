# kankacli

Manage your [Kanka](https://kanka.io) worldbuilding campaign from the command line — browse, create, update, and delete entities without ever opening a browser.

## What you can do

```bash
# List all characters with title, type, status, and race
kankacli characters list

# Add a new character in one line
kankacli characters add --name "Aria" --title "The Bold" --type "Fighter" --private

# Update a character after a dramatic session
kankacli characters update 42 --title "Champion of the Realm" --status-id 3

# Log a session as a journal entry
kankacli journals add --name "Session 12" --entry "The party uncovered the truth about the cult."

# Mark a quest as completed
kankacli quests update 7 --completed

# Pipe JSON output into jq for scripting
kankacli characters list --format json | jq '.[] | select(.is_dead == true) | .name'
```

## Supported entities

| Entity        | list | get | add | update | delete |
|---------------|:----:|:---:|:---:|:------:|:------:|
| characters    | ✓    | ✓   | ✓   | ✓      | ✓      |
| locations     | ✓    | ✓   | ✓   | ✓      | ✓      |
| organisations | ✓    | ✓   | ✓   | ✓      | ✓      |
| quests        | ✓    | ✓   | ✓   | ✓      | ✓      |
| journals      | ✓    | ✓   | ✓   | ✓      | ✓      |
| events        | ✓    | ✓   | ✓   | ✓      | ✓      |
| items         | ✓    | ✓   | ✓   | ✓      | ✓      |
| notes         | ✓    | ✓   | ✓   | ✓      | ✓      |
| tags          | ✓    | ✓   | ✓   | ✓      | ✓      |
| families      | ✓    | ✓   | ✓   | ✓      | ✓      |
| races         | ✓    | ✓   | ✓   | ✓      | ✓      |
| creatures     | ✓    | ✓   | ✓   | ✓      | ✓      |
| abilities     | ✓    | ✓   | ✓   | ✓      | ✓      |
| maps          | ✓    | ✓   | ✓   | ✓      | ✓      |
| posts         | ✓    | ✓   | ✓   | ✓      | ✓      |
| relations     | ✓    |     | ✓   | ✓      | ✓      |
| timelines     | ✓    | ✓   |     |        |        |
| calendars     | ✓    | ✓   |     |        |        |
| campaigns     | ✓    | ✓   |     |        |        |
| statuses      | ✓    |     |     |        |        |

## Installation

Requires Python 3.11+ and [pipx](https://pipx.pypa.io/).

```bash
pipx install git+https://github.com/jrtex/kankacli.git
```

## Setup

1. Generate an API token at <https://app.kanka.io/settings/api>
2. Configure the token:
   ```bash
   kankacli config set-token <your-token>
   ```
3. Set your default campaign:
   ```bash
   kankacli config set-campaign <campaign-id>
   ```

Your config is stored at `~/.kankacli/config.toml` and is never committed to the repository.

You can also use environment variables instead of the config file:

```bash
export KANKA_TOKEN=your_token_here
export KANKA_CAMPAIGN=12345
```

## Command reference

```
kankacli <entity> <command> [options]
```

All `list` and `get` commands support `--format table|json` (default: `table`).  
All entity commands support `--campaign <id>` to override the default campaign.

### Config

```bash
kankacli config show
kankacli config set-token <token>
kankacli config set-campaign <id>
```

### Characters

```bash
kankacli characters list
kankacli characters get <id>
kankacli characters add --name "Aria" --title "The Bold" --entry "A brave warrior."
kankacli characters update <id> --title "The Legendary"
kankacli characters delete <id>
```

### Locations

```bash
kankacli locations list
kankacli locations get <id>
kankacli locations add --name "The Sunken Archive"
kankacli locations update <id> --entry "Flooded after the siege."
kankacli locations delete <id>
```

### Organisations

```bash
kankacli organisations list
kankacli organisations get <id>
kankacli organisations add --name "The Iron Covenant" --type "Guild"
kankacli organisations update <id> --name "The Shattered Covenant"
kankacli organisations delete <id>
```

### Quests

```bash
kankacli quests list
kankacli quests get <id>
kankacli quests add --name "Retrieve the Amulet" --type "Main"
kankacli quests update <id> --completed
kankacli quests delete <id>
```

### Journals

```bash
kankacli journals list
kankacli journals get <id>
kankacli journals add --name "Session 12" --entry "The party descended into the vault."
kankacli journals update <id> --name "Session 12 (revised)"
kankacli journals delete <id>
```

### Other entities

The same `list / get / add / update / delete` pattern applies to:
`events`, `items`, `notes`, `tags`, `families`, `races`, `creatures`, `abilities`, `maps`, `posts`.

Relations support `list / add / update / delete`.  
Timelines, calendars, and campaigns are read-only (`list`, `get`).  
Statuses support `list` only and are useful for looking up IDs to pass via `--status-id`.

```bash
kankacli statuses list
```
