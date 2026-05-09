import typer
from kankacli.commands import config as config_cmd
from kankacli.commands import campaigns as campaigns_cmd
from kankacli.commands import characters as characters_cmd
from kankacli.commands import locations as locations_cmd
from kankacli.commands import quests as quests_cmd
from kankacli.commands import journals as journals_cmd
from kankacli.commands import notes as notes_cmd
from kankacli.commands import tags as tags_cmd

app = typer.Typer(
    name="kankacli",
    help="Interact with your Kanka worldbuilding campaign from the command line.",
    no_args_is_help=True,
)

app.add_typer(config_cmd.app, name="config")
app.add_typer(campaigns_cmd.app, name="campaigns")
app.add_typer(characters_cmd.app, name="characters")
app.add_typer(locations_cmd.app, name="locations")
app.add_typer(quests_cmd.app, name="quests")
app.add_typer(journals_cmd.app, name="journals")
app.add_typer(notes_cmd.app, name="notes")
app.add_typer(tags_cmd.app, name="tags")

if __name__ == "__main__":
    app()
