import json
from typing import Any
from rich.console import Console
from rich.table import Table

console = Console()


def print_json(data: Any) -> None:
    console.print_json(json.dumps(data))


def _display(val: Any) -> str:
    if isinstance(val, dict):
        return val.get("key") or val.get("name") or json.dumps(val)
    return str(val) if val is not None else ""


def print_table(rows: list[dict], columns: list[str]) -> None:
    table = Table(show_header=True, header_style="bold cyan")
    for col in columns:
        table.add_column(col.replace("_", " ").title())
    for row in rows:
        table.add_row(*[_display(row.get(col)) for col in columns])
    console.print(table)


def print_record(record: dict, fields: list[str] | None = None) -> None:
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value")
    keys = fields if fields is not None else list(record.keys())
    for key in keys:
        val = record.get(key)
        if val is None:
            continue
        table.add_row(key.replace("_", " ").title(), _display(val))
    console.print(table)


def error(msg: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {msg}")


def success(msg: str) -> None:
    console.print(f"[bold green]✓[/bold green] {msg}")
