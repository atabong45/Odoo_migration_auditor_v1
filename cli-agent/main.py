# main.py
import click
import sys
from auditor import run

@click.group()
def cli():
    """Odoo Migration Auditor CLI"""
    pass

@cli.command()
@click.option(
    '--path',
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="The path to the Odoo custom addons directory to audit."
)
@click.option(
    '--api-key',
    required=True,
    type=str,
    help="Your project API Key from the Odoo Auditor platform."
)
@click.option(
    '--from-version',
    default='16.0', # Pour l'instant, on fixe la valeur par défaut.
    type=float,
    help="Odoo source version (e.g., 16.0)."
)
@click.option(
    '--to-version',
    default='17.0', # Pour l'instant, on fixe la valeur par défaut.
    type=float,
    help="Odoo target version (e.g., 17.0)."
)
@click.option(
    '--output-file',
    type=click.Path(dir_okay=False, writable=True), # Doit être un fichier inscriptible
    help="Save the audit report to a local JSON file instead of submitting it."
)
def audit(path, api_key, from_version, to_version, output_file):
    """
    Run a migration audit on a given addons directory.
    """

    if not output_file and not api_key:
        raise click.UsageError("You must provide either --api-key or --output-file.")
    
    click.echo(f"Starting audit for migration from v{from_version} to v{to_version}...")
    click.echo(f"Analyzing addons at: {path}")

    try:
        # C'est ici qu'on appelle la logique principale de notre application.
        # Pour l'instant, on passe juste les arguments.
        # La fonction run.start_audit n'existe pas encore, on la créera plus tard.
        run.start_audit(path, api_key, from_version, to_version, output_file)
        
        if output_file:
            click.secho(f"\nAudit completed successfully! Report saved to {output_file}", fg="green")
        else:
            click.secho("\nAudit completed and submitted successfully!", fg="green")

    except Exception as e:
        # On attrape toutes les erreurs potentielles pour un affichage propre.
        click.secho(f"\nAn unexpected error occurred: {e}", fg="red", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()