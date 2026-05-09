from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage races in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "race_id", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "race_id",
    "is_private", "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_races(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all races in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            races = list(client.paginate(client.campaign_url(cid, "races")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(races)
    else:
        output.print_table(races, LIST_COLUMNS)


@app.command("get")
def get_race(
    race_id: int = typer.Argument(..., help="Race ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific race."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "races", race_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_race(
    name: str = typer.Option(..., "--name", help="Race name."),
    type: Optional[str] = typer.Option(None, "--type", help="Race type (e.g. Humanoid, Fey, Elemental)."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    race_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent race (for sub-races)."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the race private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new race."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if race_id is not None:
        data["race_id"] = race_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "races"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Race created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_race(
    race_id: int = typer.Argument(..., help="Race ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Race name."),
    type: Optional[str] = typer.Option(None, "--type", help="Race type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    parent_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent race."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the race private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing race. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if parent_id is not None:
        data["race_id"] = parent_id
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "races", race_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Race {race_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_race(
    race_id: int = typer.Argument(..., help="Race ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a race. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete race {race_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "races", race_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Race {race_id} deleted.")
