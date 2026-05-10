import typer
from kankacli.commands import config as config_cmd
from kankacli.commands import campaigns as campaigns_cmd
from kankacli.commands import characters as characters_cmd
from kankacli.commands import locations as locations_cmd
from kankacli.commands import quests as quests_cmd
from kankacli.commands import journals as journals_cmd
from kankacli.commands import notes as notes_cmd
from kankacli.commands import tags as tags_cmd
from kankacli.commands import families as families_cmd
from kankacli.commands import organisations as organisations_cmd
from kankacli.commands import events as events_cmd
from kankacli.commands import creatures as creatures_cmd
from kankacli.commands import races as races_cmd
from kankacli.commands import abilities as abilities_cmd
from kankacli.commands import items as items_cmd
from kankacli.commands import maps as maps_cmd
from kankacli.commands import calendars as calendars_cmd
from kankacli.commands import timelines as timelines_cmd
from kankacli.commands import posts as posts_cmd
from kankacli.commands import relations as relations_cmd
from kankacli.commands import statuses as statuses_cmd

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
app.add_typer(families_cmd.app, name="families")
app.add_typer(organisations_cmd.app, name="organisations")
app.add_typer(events_cmd.app, name="events")
app.add_typer(creatures_cmd.app, name="creatures")
app.add_typer(races_cmd.app, name="races")
app.add_typer(abilities_cmd.app, name="abilities")
app.add_typer(items_cmd.app, name="items")
app.add_typer(maps_cmd.app, name="maps")
app.add_typer(calendars_cmd.app, name="calendars")
app.add_typer(timelines_cmd.app, name="timelines")
app.add_typer(posts_cmd.app, name="posts")
app.add_typer(relations_cmd.app, name="relations")
app.add_typer(statuses_cmd.app, name="statuses")

if __name__ == "__main__":
    app()
