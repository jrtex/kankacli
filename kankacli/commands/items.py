from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage items in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "location_id", "character_id", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "location_id", "character_id",
    "price", "size", "weight", "is_private", "entry",
    "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_items(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all items in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            items = list(client.paginate(client.campaign_url(cid, "items")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(items)
    else:
        output.print_table(items, LIST_COLUMNS)


@app.command("get")
def get_item(
    item_id: int = typer.Argument(..., help="Item ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific item."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "items", item_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_item(
    name: str = typer.Option(..., "--name", help="Item name."),
    type: Optional[str] = typer.Option(None, "--type", help="Item type (e.g. Weapon, Artifact, Consumable)."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the location where the item is stored."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the character who owns the item."),
    price: Optional[str] = typer.Option(None, "--price", help="Item price (free-form text, e.g. '50 gold')."),
    size: Optional[str] = typer.Option(None, "--size", help="Item size (free-form text)."),
    weight: Optional[str] = typer.Option(None, "--weight", help="Item weight (free-form text)."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the item private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new item."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if location_id is not None:
        data["location_id"] = location_id
    if character_id is not None:
        data["character_id"] = character_id
    if price is not None:
        data["price"] = price
    if size is not None:
        data["size"] = size
    if weight is not None:
        data["weight"] = weight

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "items"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Item created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_item(
    item_id: int = typer.Argument(..., help="Item ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Item name."),
    type: Optional[str] = typer.Option(None, "--type", help="Item type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the location where the item is stored."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the character who owns the item."),
    price: Optional[str] = typer.Option(None, "--price", help="Item price."),
    size: Optional[str] = typer.Option(None, "--size", help="Item size."),
    weight: Optional[str] = typer.Option(None, "--weight", help="Item weight."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the item private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing item. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if location_id is not None:
        data["location_id"] = location_id
    if character_id is not None:
        data["character_id"] = character_id
    if price is not None:
        data["price"] = price
    if size is not None:
        data["size"] = size
    if weight is not None:
        data["weight"] = weight
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "items", item_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Item {item_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_item(
    item_id: int = typer.Argument(..., help="Item ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete an item. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete item {item_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "items", item_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Item {item_id} deleted.")
