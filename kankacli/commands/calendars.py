from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="List and inspect calendars in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "is_private",
    "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_calendars(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all calendars in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            calendars = list(client.paginate(client.campaign_url(cid, "calendars")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(calendars)
    else:
        output.print_table(calendars, LIST_COLUMNS)


@app.command("get")
def get_calendar(
    calendar_id: int = typer.Argument(..., help="Calendar ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific calendar."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "calendars", calendar_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)
