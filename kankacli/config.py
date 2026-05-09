import os
import tomllib
import tomli_w
from pathlib import Path

CONFIG_DIR = Path.home() / ".kankacli"
CONFIG_FILE = CONFIG_DIR / "config.toml"


def load_config() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    with open(CONFIG_FILE, "rb") as f:
        return tomllib.load(f)


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "wb") as f:
        tomli_w.dump(config, f)


def get_token() -> str | None:
    return os.getenv("KANKA_TOKEN") or load_config().get("token")


def get_campaign_id() -> int | None:
    env = os.getenv("KANKA_CAMPAIGN")
    if env:
        return int(env)
    return load_config().get("campaign_id")


def require_token() -> str:
    token = get_token()
    if not token:
        import typer
        typer.echo(
            "No API token configured. Run: kankacli config set-token <token>", err=True
        )
        raise typer.Exit(1)
    return token


def require_campaign_id() -> int:
    campaign_id = get_campaign_id()
    if not campaign_id:
        import typer
        typer.echo(
            "No default campaign set. Run: kankacli config set-campaign <id>", err=True
        )
        raise typer.Exit(1)
    return campaign_id
