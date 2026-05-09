import typer
from kankacli.commands import config as config_cmd

app = typer.Typer(
    name="kankacli",
    help="Interact with your Kanka worldbuilding campaign from the command line.",
    no_args_is_help=True,
)

app.add_typer(config_cmd.app, name="config")

if __name__ == "__main__":
    app()
