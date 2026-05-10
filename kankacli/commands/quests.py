from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage quests in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "status", "is_completed", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "status", "quest_id", "character_id",
    "is_completed", "is_private", "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_quests(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all quests in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            quests = list(client.paginate(client.campaign_url(cid, "quests")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(quests)
    else:
        output.print_table(quests, LIST_COLUMNS)


@app.command("get")
def get_quest(
    quest_id: int = typer.Argument(..., help="Quest ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific quest."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "quests", quest_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_quest(
    name: str = typer.Option(..., "--name", help="Quest name."),
    type: Optional[str] = typer.Option(None, "--type", help="Quest type (e.g. Main, Side)."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    quest_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent quest."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the quest giver character."),
    is_completed: bool = typer.Option(False, "--completed/--active", help="Mark the quest as completed."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the quest private."),
    status_id: Optional[int] = typer.Option(None, "--status-id", help="Status ID — run `kankacli statuses list` to see options."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new quest."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_completed": is_completed, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if quest_id is not None:
        data["quest_id"] = quest_id
    if character_id is not None:
        data["character_id"] = character_id
    if status_id is not None:
        data["status_id"] = status_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "quests"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Quest created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_quest(
    quest_id: int = typer.Argument(..., help="Quest ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Quest name."),
    type: Optional[str] = typer.Option(None, "--type", help="Quest type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Description (supports markdown)."),
    parent_id: Optional[int] = typer.Option(None, "--parent-id", help="ID of the parent quest."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the quest giver character."),
    is_completed: Optional[bool] = typer.Option(None, "--completed/--active", help="Mark the quest as completed."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the quest private."),
    status_id: Optional[int] = typer.Option(None, "--status-id", help="Status ID — run `kankacli statuses list` to see options."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing quest. Only supplied fields are changed."""
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
        data["quest_id"] = parent_id
    if character_id is not None:
        data["character_id"] = character_id
    if is_completed is not None:
        data["is_completed"] = is_completed
    if is_private is not None:
        data["is_private"] = is_private
    if status_id is not None:
        data["status_id"] = status_id

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "quests", quest_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Quest {quest_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_quest(
    quest_id: int = typer.Argument(..., help="Quest ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a quest. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete quest {quest_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "quests", quest_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Quest {quest_id} deleted.")
