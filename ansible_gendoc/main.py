from pathlib import Path
from re import template
from ansible_gendoc import __version__
from ansible_gendoc.gendoc import Gendoc
from typing import Optional
import typer
import os
import sys
import shutil


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        versionText = typer.style(
            f"ansible-gendoc v{__version__}", fg=typer.colors.RED, bg=typer.colors.WHITE
        )
        typer.echo(versionText)
        raise typer.Exit()


@app.command()
def init(
    path: Path = typer.Argument(
        default="./", help="The path of your role.", exists=True
    ),
    force: Optional[bool] = typer.Option(
        False, "--force", "-f", help="Replace existing Template README.j2 in templates folder."
    ),
):
    """
    Copy templates README.j2 from packages in templates/role folder.
    """
    role_path = os.path.join(path, "meta/main.yml")
    if not os.path.isfile(role_path):
        print("There is no role in this Path !!!!")
        raise typer.Exit(code=1)
    template_path = os.path.join(path, "templates/")
    if not os.path.isfile(os.path.join(path, "templates")):
        Path(os.path.dirname(template_path)).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(os.path.join(template_path, "README.j2")) or force:
        pkgdir = sys.modules['ansible_gendoc'].__path__[0]
        fullpath = os.path.join(pkgdir, "templates/README.j2")
        shutil.copy(fullpath, template_path)
    else:
        print("The template already exist !!!!")
        print("use --force to replace the existent.")
        raise typer.Exit(code=1)



@app.command()
def render(
    path: Path = typer.Argument(
        default="./", help="The path of your role.", exists=True
    ),
    dry_run: Optional[bool] = typer.Option(
        False,
        "--dry_run",
        "-d",
        help="dry run, Outputs pure markdown to stdout nothing is written to disk",
    ),
    verbose: Optional[bool] = typer.Option(
        False, "--verbose", "-v", help="verbose mode"
    ),
):
    """
    Build the Documentation
    """
    gendoc = Gendoc(
        dry_run=dry_run,
        verbose=verbose,
        path=path,
    )
    gendoc.render()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return

if __name__ == "__main__":
    app()
