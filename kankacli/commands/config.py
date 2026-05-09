import typer
from rich.console import Console
from rich.table import Table
from kankacli.config import load_config, save_config, CONFIG_FILE

app = typer.Typer(help="Manage kankacli configuration.")
console = Console()


@app.command("set-token")
def set_token(
    token: str = typer.Argument(..., help="Your Kanka API token from https://app.kanka.io/settings/api"),
):
    """Store your Kanka API token in the local config file."""
    config = load_config()
    config["token"] = token
    save_config(config)
    console.print(f"[green]Token saved to {CONFIG_FILE}[/green]")


@app.command("set-campaign")
def set_campaign(
    campaign_id: int = typer.Argument(..., help="Kanka campaign ID to use by default"),
):
    """Set the default campaign ID (used when --campaign is not specified)."""
    config = load_config()
    config["campaign_id"] = campaign_id
    save_config(config)
    console.print(f"[green]Default campaign set to {campaign_id}[/green]")


@app.command("show")
def show():
    """Show current configuration. The token is masked for safety."""
    config = load_config()

    if not config:
        console.print("[yellow]No configuration found.[/yellow]")
        console.print(f"Config file: {CONFIG_FILE}")
        return

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Key", style="bold cyan", no_wrap=True)
    table.add_column("Value")

    for key, val in config.items():
        if key == "token":
            s = str(val)
            display = s[:8] + "…" + s[-4:] if len(s) > 12 else "***"
        else:
            display = str(val)
        table.add_row(key, display)

    console.print(table)
    console.print(f"\n[dim]Config file: {CONFIG_FILE}[/dim]")
