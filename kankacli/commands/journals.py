from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage journal entries in your campaign.")

LIST_COLUMNS = ["id", "name", "type", "date", "character_id", "is_private"]
DETAIL_FIELDS = [
    "id", "name", "type", "date", "character_id",
    "is_private", "entry", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


@app.command("list")
def list_journals(
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all journal entries in the campaign."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            journals = list(client.paginate(client.campaign_url(cid, "journals")))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(journals)
    else:
        output.print_table(journals, LIST_COLUMNS)


@app.command("get")
def get_journal(
    journal_id: int = typer.Argument(..., help="Journal ID."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """Get details for a specific journal entry."""
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            result = client.get(client.campaign_url(cid, "journals", journal_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    if format == Format.json:
        output.print_json(record)
    else:
        output.print_record(record, DETAIL_FIELDS)


@app.command("add")
def add_journal(
    name: str = typer.Option(..., "--name", help="Journal entry title."),
    type: Optional[str] = typer.Option(None, "--type", help="Journal type (e.g. Session, Dream)."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Content (supports markdown)."),
    date: Optional[str] = typer.Option(None, "--date", help="In-world date of the entry."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the author character."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the entry private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a new journal entry."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"name": name, "is_private": is_private}
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if date is not None:
        data["date"] = date
    if character_id is not None:
        data["character_id"] = character_id

    try:
        with KankaClient(token) as client:
            result = client.post(client.campaign_url(cid, "journals"), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Journal entry created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_journal(
    journal_id: int = typer.Argument(..., help="Journal ID to update."),
    name: Optional[str] = typer.Option(None, "--name", help="Journal entry title."),
    type: Optional[str] = typer.Option(None, "--type", help="Journal type."),
    entry: Optional[str] = typer.Option(None, "--entry", help="Content (supports markdown)."),
    date: Optional[str] = typer.Option(None, "--date", help="In-world date of the entry."),
    character_id: Optional[int] = typer.Option(None, "--character-id", help="ID of the author character."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the entry private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update an existing journal entry. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if name is not None:
        data["name"] = name
    if type is not None:
        data["type"] = type
    if entry is not None:
        data["entry"] = entry
    if date is not None:
        data["date"] = date
    if character_id is not None:
        data["character_id"] = character_id
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(client.campaign_url(cid, "journals", journal_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Journal entry {journal_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_journal(
    journal_id: int = typer.Argument(..., help="Journal ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a journal entry. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete journal entry {journal_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(client.campaign_url(cid, "journals", journal_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Journal entry {journal_id} deleted.")
