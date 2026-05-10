from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage characters in your campaign.")

LIST_COLUMNS = ["id", "name", "title", "type", "status", "is_dead", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "title", "age", "sex", "pronouns", "type", "status",
    "location_id", "is_dead", "is_private", "entry",
    "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_characters(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all characters in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            characters = list(client.paginate(client.campaign_url(cid, "characters")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(characters)
    else:
        output.print_table(characters, LIST_COLUMNS)


@app.command("get")
def get_character(
    character_id: int = typer.Argument(..., help="Character ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific character."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "characters", character_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_character(
    name: str = typer.Option(..., "--name", help="Character name."),
    title: Optional[str] = typer.Option(None, "--title", help="Character title or epithet."),
    age: Optional[str] = typer.Option(None, "--age", help="Age (free-form text)."),
    sex: Optional[str] = typer.Option(None, "--sex", help="Sex."),
    pronouns: Optional[str] = typer.Option(None, "--pronouns", help="Pronouns."),
    type: Optional[str] = typer.Option(None, "--type", help="Character type or class."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the character's location."),
    is_dead: bool = typer.Option(False, "--dead/--alive", help="Mark the character as dead or alive."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the character private."),
    status_id: Optional[int] = typer.Option(None, "--status-id", help="Status ID — run `kankacli statuses list` to see options."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new character."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_dead": is_dead, "is_private": is_private}
    if title is not None:
        data["title"] = title
    if age is not None:
        data["age"] = age
    if sex is not None:
        data["sex"] = sex
    if pronouns is not None:
        data["pronouns"] = pronouns
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if location_id is not None:
        data["location_id"] = location_id
    if status_id is not None:
        data["status_id"] = status_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "characters"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Character created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_character(
    character_id: int = typer.Argument(..., help="Character ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Character name."),
    title: Optional[str] = typer.Option(None, "--title", help="Character title or epithet."),
    age: Optional[str] = typer.Option(None, "--age", help="Age (free-form text)."),
    sex: Optional[str] = typer.Option(None, "--sex", help="Sex."),
    pronouns: Optional[str] = typer.Option(None, "--pronouns", help="Pronouns."),
    type: Optional[str] = typer.Option(None, "--type", help="Character type or class."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    location_id: Optional[int] = typer.Option(None, "--location-id", help="ID of the character's location."),
    is_dead: Optional[bool] = typer.Option(None, "--dead/--alive", help="Mark the character as dead or alive."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the character private."),
    status_id: Optional[int] = typer.Option(None, "--status-id", help="Status ID — run `kankacli statuses list` to see options."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing character. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if title is not None:
        data["title"] = title
    if age is not None:
        data["age"] = age
    if sex is not None:
        data["sex"] = sex
    if pronouns is not None:
        data["pronouns"] = pronouns
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if location_id is not None:
        data["location_id"] = location_id
    if is_dead is not None:
        data["is_dead"] = is_dead
    if is_private is not None:
        data["is_private"] = is_private
    if status_id is not None:
        data["status_id"] = status_id

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "characters", character_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Character {character_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_character(
    character_id: int = typer.Argument(..., help="Character ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a character. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete character {character_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "characters", character_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Character {character_id} deleted.")
