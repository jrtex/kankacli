# kankacli

A command-line tool for interacting with [Kanka](https://kanka.io) worldbuilding campaigns.

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

## Usage

```
kankacli <object> <command> [options]
```

### Config

```bash
kankacli config show
kankacli config set-token <token>
kankacli config set-campaign <id>
```

### Campaigns

```bash
kankacli campaigns list
kankacli campaigns get <id>
```

### Characters

```bash
kankacli characters list
kankacli characters get <id>
kankacli characters add --name "Aria" --title "The Bold" --entry "A brave warrior."
kankacli characters update <id> --title "The Legendary"
kankacli characters delete <id>
```

All list and get commands support `--format table|json` (default: `table`).  
All entity commands support `--campaign <id>` to override the default campaign.

## Contributing

See [DEV_STATUS.md](DEV_STATUS.md) for the development roadmap (local only, not committed).
