# kankacli skill

Use this skill when the user asks you to interact with their Kanka worldbuilding campaign — reading or writing characters, locations, quests, and other entities.

## Prerequisites

Kankacli must be installed and configured before use:

```bash
kankacli config set-token <token>       # one-time setup
kankacli config set-campaign <id>       # one-time setup
kankacli config show                    # verify configuration
```

The token is generated at https://app.kanka.io/settings/api. Once set, all commands use the default campaign automatically; pass `--campaign <id>` to override per-command.

## Command structure

```
kankacli <group> <command> [arguments] [options]
```

All list and get commands accept `--format json` for machine-readable output. Default output is a rich table.

## Entity ID vs generic entity_id

Kanka has two ID systems:
- **`id`** — the type-specific ID (e.g. the character's own ID). Used in `get`, `update`, `delete`, and as arguments to most commands.
- **`entity_id`** — the generic entity ID shared across all entity types. Required by `posts` and `relations` commands.

To find the `entity_id` for an entity, run its `get` command with `--format json` and look for the `"entity_id"` field.

## Command reference

### config
```bash
kankacli config set-token <token>
kankacli config set-campaign <id>
kankacli config show
```

### campaigns
```bash
kankacli campaigns list [--format json]
kankacli campaigns get <id> [--format json]
```

### statuses
```bash
kankacli statuses list [--format json]   # shows id, key, is_custom
```
Use the `id` value from this output with `--status-id` on characters, locations, and quests.

### characters
```bash
kankacli characters list [--format json]
kankacli characters get <id> [--format json]
kankacli characters add --name <name> [--title <t>] [--age <a>] [--sex <s>] [--pronouns <p>] [--type <t>] [--entry <md>] [--location-id <id>] [--status-id <id>] [--dead|--alive] [--private|--public]
kankacli characters update <id> [--name <n>] [--title <t>] [--age <a>] [--sex <s>] [--pronouns <p>] [--type <t>] [--entry <md>] [--location-id <id>] [--status-id <id>] [--dead|--alive] [--private|--public]
kankacli characters delete <id> [--yes]
```

### locations
```bash
kankacli locations list [--format json]
kankacli locations get <id> [--format json]
kankacli locations add --name <name> [--type <t>] [--entry <md>] [--parent-id <id>] [--status-id <id>] [--private|--public]
kankacli locations update <id> [--name <n>] [--type <t>] [--entry <md>] [--parent-id <id>] [--status-id <id>] [--private|--public]
kankacli locations delete <id> [--yes]
```

### quests
```bash
kankacli quests list [--format json]
kankacli quests get <id> [--format json]
kankacli quests add --name <name> [--type <t>] [--entry <md>] [--parent-id <id>] [--character-id <id>] [--status-id <id>] [--completed|--active] [--private|--public]
kankacli quests update <id> [--name <n>] [--type <t>] [--entry <md>] [--parent-id <id>] [--character-id <id>] [--status-id <id>] [--completed|--active] [--private|--public]
kankacli quests delete <id> [--yes]
```

### journals
```bash
kankacli journals list [--format json]
kankacli journals get <id> [--format json]
kankacli journals add --name <name> [--type <t>] [--entry <md>] [--date <d>] [--character-id <id>] [--private|--public]
kankacli journals update <id> [--name <n>] [--type <t>] [--entry <md>] [--date <d>] [--character-id <id>] [--private|--public]
kankacli journals delete <id> [--yes]
```

### notes
```bash
kankacli notes list [--format json]
kankacli notes get <id> [--format json]
kankacli notes add --name <name> [--type <t>] [--entry <md>] [--pinned|--unpinned] [--private|--public]
kankacli notes update <id> [--name <n>] [--type <t>] [--entry <md>] [--pinned|--unpinned] [--private|--public]
kankacli notes delete <id> [--yes]
```

### tags
```bash
kankacli tags list [--format json]
kankacli tags get <id> [--format json]
kankacli tags add --name <name> [--type <t>] [--entry <md>] [--colour <c>] [--parent-id <id>] [--private|--public]
kankacli tags update <id> [--name <n>] [--type <t>] [--entry <md>] [--colour <c>] [--parent-id <id>] [--private|--public]
kankacli tags delete <id> [--yes]
```

### families
```bash
kankacli families list [--format json]
kankacli families get <id> [--format json]
kankacli families add --name <name> [--type <t>] [--entry <md>] [--location-id <id>] [--parent-id <id>] [--private|--public]
kankacli families update <id> [--name <n>] [--type <t>] [--entry <md>] [--location-id <id>] [--parent-id <id>] [--private|--public]
kankacli families delete <id> [--yes]
```

### organisations
```bash
kankacli organisations list [--format json]
kankacli organisations get <id> [--format json]
kankacli organisations add --name <name> [--type <t>] [--entry <md>] [--location-id <id>] [--parent-id <id>] [--private|--public]
kankacli organisations update <id> [--name <n>] [--type <t>] [--entry <md>] [--location-id <id>] [--parent-id <id>] [--private|--public]
kankacli organisations delete <id> [--yes]
```

### events
```bash
kankacli events list [--format json]
kankacli events get <id> [--format json]
kankacli events add --name <name> [--type <t>] [--entry <md>] [--date <d>] [--location-id <id>] [--private|--public]
kankacli events update <id> [--name <n>] [--type <t>] [--entry <md>] [--date <d>] [--location-id <id>] [--private|--public]
kankacli events delete <id> [--yes]
```

### creatures
```bash
kankacli creatures list [--format json]
kankacli creatures get <id> [--format json]
kankacli creatures add --name <name> [--type <t>] [--entry <md>] [--location-id <id>] [--private|--public]
kankacli creatures update <id> [--name <n>] [--type <t>] [--entry <md>] [--location-id <id>] [--private|--public]
kankacli creatures delete <id> [--yes]
```

### races
```bash
kankacli races list [--format json]
kankacli races get <id> [--format json]
kankacli races add --name <name> [--type <t>] [--entry <md>] [--parent-id <id>] [--private|--public]
kankacli races update <id> [--name <n>] [--type <t>] [--entry <md>] [--parent-id <id>] [--private|--public]
kankacli races delete <id> [--yes]
```

### abilities
```bash
kankacli abilities list [--format json]
kankacli abilities get <id> [--format json]
kankacli abilities add --name <name> [--type <t>] [--entry <md>] [--parent-id <id>] [--charges <c>] [--private|--public]
kankacli abilities update <id> [--name <n>] [--type <t>] [--entry <md>] [--parent-id <id>] [--charges <c>] [--private|--public]
kankacli abilities delete <id> [--yes]
```

### items
```bash
kankacli items list [--format json]
kankacli items get <id> [--format json]
kankacli items add --name <name> [--type <t>] [--entry <md>] [--location-id <id>] [--character-id <id>] [--price <p>] [--size <s>] [--weight <w>] [--private|--public]
kankacli items update <id> [--name <n>] [--type <t>] [--entry <md>] [--location-id <id>] [--character-id <id>] [--price <p>] [--size <s>] [--weight <w>] [--private|--public]
kankacli items delete <id> [--yes]
```

### maps
```bash
kankacli maps list [--format json]
kankacli maps get <id> [--format json]
kankacli maps add --name <name> [--type <t>] [--entry <md>] [--parent-id <id>] [--location-id <id>] [--private|--public]
kankacli maps update <id> [--name <n>] [--type <t>] [--entry <md>] [--parent-id <id>] [--location-id <id>] [--private|--public]
kankacli maps delete <id> [--yes]
```
Note: map images must be uploaded via the Kanka web UI; the API does not support binary uploads.

### calendars (read-only)
```bash
kankacli calendars list [--format json]
kankacli calendars get <id> [--format json]
```

### timelines (read-only)
```bash
kankacli timelines list [--format json]
kankacli timelines get <id> [--format json]
```

### posts (sub-resource — requires generic entity_id)
```bash
kankacli posts list <entity_id> [--format json]
kankacli posts get <entity_id> <post_id> [--format json]
kankacli posts add <entity_id> --name <name> [--entry <md>] [--private|--public]
kankacli posts update <entity_id> <post_id> [--name <n>] [--entry <md>] [--private|--public]
kankacli posts delete <entity_id> <post_id> [--yes]
```

### relations (sub-resource — requires generic entity_id)
```bash
kankacli relations list <entity_id> [--format json]
kankacli relations add <entity_id> --target-id <target_entity_id> [--relation <desc>] [--attitude <-100..100>] [--colour <c>] [--star|--no-star] [--private|--public]
kankacli relations update <entity_id> <relation_id> [--relation <desc>] [--attitude <n>] [--colour <c>] [--star|--no-star] [--private|--public]
kankacli relations delete <entity_id> <relation_id> [--yes]
```

## Common patterns

**Find a character and add a post to them:**
```bash
# Step 1 — find the character's entity_id
kankacli characters get 42 --format json
# look for "entity_id" in the output, e.g. 9901

# Step 2 — add a post
kankacli posts add 9901 --name "Session 12 notes" --entry "Met the party at the tavern."
```

**Create a nested location:**
```bash
# Create parent first, note its id
kankacli locations add --name "Valdris" --type "City"
# Then create child using --parent-id
kankacli locations add --name "The Rusty Flagon" --type "Tavern" --parent-id <city_id>
```

**Mark a quest as completed:**
```bash
kankacli quests update <id> --completed
```

**Link two characters as rivals:**
```bash
# Get entity_ids for both characters
kankacli characters get <id1> --format json   # note entity_id → e.g. 1001
kankacli characters get <id2> --format json   # note entity_id → e.g. 1002
kankacli relations add 1001 --target-id 1002 --relation "Rival" --attitude -75
```

**Bulk-read all entities as JSON for processing:**
```bash
kankacli characters list --format json
kankacli locations list --format json
```
