# main.py
import click
import sys
import os
from auditor import run
import yaml


CONFIG_FILE_NAME = ".odoo-auditor.yml"

def load_config() -> dict:
    """Cherche et charge le fichier de configuration .odoo-auditor.yml."""
    if os.path.exists(CONFIG_FILE_NAME):
        try:
            with open(CONFIG_FILE_NAME, 'r') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            click.secho(f"Warning: Could not parse config file {CONFIG_FILE_NAME}: {e}", fg="yellow")
    return {}


@click.group()
def cli():
    """Odoo Migration Auditor CLI"""
    pass

@cli.command()
@click.option(
    '--path',
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="The path to the Odoo custom addons directory to audit."
)
@click.option(
    '--api-key',
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
    config = load_config()

    # --- Logique de fusion : Ligne de commande > Fichier de config > Défaut ---
    final_path = path or config.get('path')
    final_api_key = api_key or config.get('api_key')
    final_from = from_version or config.get('from_version', 16.0)
    final_to = to_version or config.get('to_version', 17.0)
    final_output = output_file or config.get('output_file')

    if not final_path:
        raise click.UsageError("Missing option '--path'. Provide it via command line or config file.")

    if not final_api_key and not final_output:
        raise click.UsageError("You must provide either --api-key or --output-file  via command line or config file.")

    click.echo(f"Starting audit for migration from v{final_from} to v{final_to}...")
    click.echo(f"Analyzing addons at: {final_path}")

    try:
        # C'est ici qu'on appelle la logique principale de notre application.
        # Pour l'instant, on passe juste les arguments.
        # La fonction run.start_audit n'existe pas encore, on la créera plus tard.
        run.start_audit(final_path, final_api_key, final_from, final_to, final_output)

        if final_output:
            click.secho(f"\nAudit completed and submitted successfully! Report saved to {output_file}", fg="green")
        else:
            click.secho("\nAudit completed and submitted successfully!", fg="green")

    except Exception as e:
        # On attrape toutes les erreurs potentielles pour un affichage propre.
        click.secho(f"\nAn unexpected error occurred: {e}", fg="red", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()