from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage maps in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "map_id", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "map_id", "location_id",
    "is_private", "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_maps(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all maps in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            maps = list(client.paginate(client.campaign_url(cid, "maps")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(maps)
    else:
        output.print_table(maps, LIST_COLUMNS)


@app.command("get")
def get_map(
    map_id: int = typer.Argument(..., help="Map ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific map."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "maps", map_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_map(
    name: str = typer.Option(..., "--name", help="Map name."),
    type: Optional[str] = typer.Option(None, "--type", help="Map type (e.g. World, Region, Dungeon)."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    map_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent map."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the linked location."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the map private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new map. Use the Kanka web UI to upload the map image after creation."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if map_id is not None:
        data["map_id"] = map_id
    if location_id is not None:
        data["location_id"] = location_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "maps"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Map created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_map(
    map_id: int = typer.Argument(..., help="Map ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Map name."),
    type: Optional[str] = typer.Option(None, "--type", help="Map type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    parent_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent map."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the linked location."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the map private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing map. Only supplied fields are changed."""
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
        data["map_id"] = parent_id
    if location_id is not None:
        data["location_id"] = location_id
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "maps", map_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Map {map_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_map(
    map_id: int = typer.Argument(..., help="Map ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a map. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete map {map_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "maps", map_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Map {map_id} deleted.")
