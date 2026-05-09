from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage notes in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "is_pinned", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "is_pinned", "is_private",
    "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_notes(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all notes in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            notes = list(client.paginate(client.campaign_url(cid, "notes")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(notes)
    else:
        output.print_table(notes, LIST_COLUMNS)


@app.command("get")
def get_note(
    note_id: int = typer.Argument(..., help="Note ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific note."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "notes", note_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_note(
    name: str = typer.Option(..., "--name", help="Note title."),
    type: Optional[str] = typer.Option(None, "--type", help="Note type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Content (supports markdown)."),
    is_pinned: bool = typer.Option(False, "--pinned/--unpinned", help="Pin the note to the dashboard."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the note private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new note."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_pinned": is_pinned, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "notes"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Note created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_note(
    note_id: int = typer.Argument(..., help="Note ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Note title."),
    type: Optional[str] = typer.Option(None, "--type", help="Note type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Content (supports markdown)."),
    is_pinned: Optional[bool] = typer.Option(None, "--pinned/--unpinned", help="Pin the note to the dashboard."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the note private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing note. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if is_pinned is not None:
        data["is_pinned"] = is_pinned
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "notes", note_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Note {note_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_note(
    note_id: int = typer.Argument(..., help="Note ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a note. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete note {note_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "notes", note_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Note {note_id} deleted.")
