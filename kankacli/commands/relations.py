from enum import Enum
from typing import Optional
import typer
from kankacli.client import KankaClient, KankaError
from kankacli.config import require_token, require_campaign_id
from kankacli import output

app = typer.Typer(help="Manage relations between entities.")

LIST_COLUMNS = ["id", "owner_id", "target_id", "relation", "attitude", "is_private"]
DETAIL_FIELDS = [
    "id", "owner_id", "target_id", "relation", "attitude",
    "colour", "is_star", "is_private", "created_at", "updated_at",
]


class Format(str, Enum):
    table = "table"
    json = "json"


def _campaign(override: Optional[int]) -> int:
    return override if override is not None else require_campaign_id()


def _entity_url(cid: int, entity_id: int, *parts) -> str:
    base = f"/campaigns/{cid}/entities/{entity_id}/relations"
    if parts:
        return base + "/" + "/".join(str(p) for p in parts)
    return base


@app.command("list")
def list_relations(
    entity_id: int = typer.Argument(..., help="Generic entity ID (the 'entity_id' field in JSON output)."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
    format: Format = typer.Option(Format.table, "--format", "-f", help="Output format."),
):
    """List all relations for an entity.

    The entity_id is the generic 'entity_id' field returned by any entity command
    with --format json, not the type-specific 'id' field.
    """
    token = require_token()
    cid = _campaign(campaign)
    try:
        with KankaClient(token) as client:
            relations = list(client.paginate(_entity_url(cid, entity_id)))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    if format == Format.json:
        output.print_json(relations)
    else:
        output.print_table(relations, LIST_COLUMNS)


@app.command("add")
def add_relation(
    entity_id: int = typer.Argument(..., help="Generic entity ID of the source entity."),
    target_id: int = typer.Option(..., "--target-id", help="Generic entity ID of the target entity."),
    relation: Optional[str] = typer.Option(None, "--relation", help="Relation description (e.g. 'Ally', 'Rival')."),
    attitude: Optional[int] = typer.Option(None, "--attitude", min=- 100, max=100, help="Attitude score from -100 (hostile) to 100 (friendly)."),
    colour: Optional[str] = typer.Option(None, "--colour", help="Relation colour (e.g. red, green)."),
    is_star: bool = typer.Option(False, "--star/--no-star", help="Pin this relation."),
    is_private: bool = typer.Option(False, "--private/--public", help="Make the relation private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Create a relation from one entity to another."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {"target_id": target_id, "is_star": is_star, "is_private": is_private}
    if relation is not None:
        data["relation"] = relation
    if attitude is not None:
        data["attitude"] = attitude
    if colour is not None:
        data["colour"] = colour

    try:
        with KankaClient(token) as client:
            result = client.post(_entity_url(cid, entity_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Relation created (id: {record['id']})")
    output.print_record(record, DETAIL_FIELDS)


@app.command("update")
def update_relation(
    entity_id: int = typer.Argument(..., help="Generic entity ID of the source entity."),
    relation_id: int = typer.Argument(..., help="Relation ID to update."),
    relation: Optional[str] = typer.Option(None, "--relation", help="Relation description."),
    attitude: Optional[int] = typer.Option(None, "--attitude", min=-100, max=100, help="Attitude score from -100 to 100."),
    colour: Optional[str] = typer.Option(None, "--colour", help="Relation colour."),
    is_star: Optional[bool] = typer.Option(None, "--star/--no-star", help="Pin this relation."),
    is_private: Optional[bool] = typer.Option(None, "--private/--public", help="Make the relation private."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Update a relation. Only supplied fields are changed."""
    token = require_token()
    cid = _campaign(campaign)

    data: dict = {}
    if relation is not None:
        data["relation"] = relation
    if attitude is not None:
        data["attitude"] = attitude
    if colour is not None:
        data["colour"] = colour
    if is_star is not None:
        data["is_star"] = is_star
    if is_private is not None:
        data["is_private"] = is_private

    if not data:
        output.error("No fields provided. Pass at least one option to update.")
        raise typer.Exit(1)

    try:
        with KankaClient(token) as client:
            result = client.patch(_entity_url(cid, entity_id, relation_id), data)
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    record = result.get("data", result)
    output.success(f"Relation {relation_id} updated.")
    output.print_record(record, DETAIL_FIELDS)


@app.command("delete")
def delete_relation(
    entity_id: int = typer.Argument(..., help="Generic entity ID of the source entity."),
    relation_id: int = typer.Argument(..., help="Relation ID to delete."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
    campaign: Optional[int] = typer.Option(None, "--campaign", "-c", help="Campaign ID (overrides default)."),
):
    """Delete a relation. Prompts for confirmation unless --yes is passed."""
    token = require_token()
    cid = _campaign(campaign)

    if not yes:
        typer.confirm(f"Delete relation {relation_id}? This cannot be undone.", abort=True)

    try:
        with KankaClient(token) as client:
            client.delete(_entity_url(cid, entity_id, relation_id))
    except KankaError as e:
        output.error(str(e))
        raise typer.Exit(1)

    output.success(f"Relation {relation_id} deleted.")
