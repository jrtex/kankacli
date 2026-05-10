from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="List available statuses for entities in your campaign.")

LIST_COLUMNS = ["id", "key", "is_custom"]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_statuses(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all available statuses in the campaign.

    Use the 'id' value with --status-id on characters, locations, and quests.
    """
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            statuses = list(client.paginate(f"/campaigns/{cid}/entity_types"))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(statuses)
    else:
        output.print_table(statuses, LIST_COLUMNS)
