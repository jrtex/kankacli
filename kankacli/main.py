import typer
from kankacli.commands import config as config_cmd
from kankacli.commands import campaigns as campaigns_cmd
from kankacli.commands import characters as characters_cmd

app = typer.Typer(
    name="kankacli",
    help="Interact with your Kanka worldbuilding campaign from the command line.",
    no_args_is_help=True,
)

app.add_typer(config_cmd.app, name="config")
app.add_typer(campaigns_cmd.app, name="campaigns")
app.add_typer(characters_cmd.app, name="characters")

if __name__ == "__main__":
    app()
