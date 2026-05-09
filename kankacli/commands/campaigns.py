from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token
from kankacli import output

app = typer.Typer(help="List and inspect campaigns.")


class Format(str, Enum):
    table = "table"
    json = "json"


@app.command("list")
def list_campaigns(
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all campaigns you have access to."""
    token = require_token()
    try:
        with KankaClient(token) as client:
            campaigns = list(client.paginate("/campaigns"))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(campaigns)
    else:
        output.print_table(campaigns, ["id", "name", "locale", "is_public"])


@app.command("get")
def get_campaign(
    campaign_id: int = typer.Argument(..., help="Campaign ID."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific campaign."""
    token = require_token()
    try:
        with KankaClient(token) as client:
            result = client.get(f"/campaigns/{campaign_id}")
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)

    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, fields=[
            "id", "name", "locale", "entry", "is_public",
            "created_at", "updated_at",
        ])
