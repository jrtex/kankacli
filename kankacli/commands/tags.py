from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage tags in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "colour", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "colour", "tag_id",
    "is_private", "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_tags(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all tags in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            tags = list(client.paginate(client.campaign_url(cid, "tags")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(tags)
    else:
        output.print_table(tags, LIST_COLUMNS)


@app.command("get")
def get_tag(
    tag_id: int = typer.Argument(..., help="Tag ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific tag."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "tags", tag_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_tag(
    name: str = typer.Option(..., "--name", help="Tag name."),
    type: Optional[str] = typer.Option(None, "--type", help="Tag type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    colour: Optional[str] = typer.Option(None, "--colour", help="Tag colour (e.g. red, blue, green)."),
    tag_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent tag."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the tag private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new tag."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if colour is not None:
        data["colour"] = colour
    if tag_id is not None:
        data["tag_id"] = tag_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "tags"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Tag created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_tag(
    tag_id: int = typer.Argument(..., help="Tag ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Tag name."),
    type: Optional[str] = typer.Option(None, "--type", help="Tag type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    colour: Optional[str] = typer.Option(None, "--colour", help="Tag colour."),
    parent_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent tag."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the tag private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing tag. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if colour is not None:
        data["colour"] = colour
    if parent_id is not None:
        data["tag_id"] = parent_id
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "tags", tag_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Tag {tag_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_tag(
    tag_id: int = typer.Argument(..., help="Tag ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a tag. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete tag {tag_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "tags", tag_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Tag {tag_id} deleted.")
