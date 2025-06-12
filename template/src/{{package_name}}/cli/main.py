import typer
from {{ package_name }} import __version__

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        help="Show the version and exit.",
        is_eager=True,
        callback=version_callback,
    ),
):
    """
    {{ project_name }}: {{ description }}
    Run with --help for more info.
    """
    pass


app.command()
