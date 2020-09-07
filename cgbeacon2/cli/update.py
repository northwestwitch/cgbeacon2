#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext
from cgbeacon2.utils.ensembl_biomart import EnsemblBiomartClient
from cgbeacon2.utils.request_resources import ebi_genenames

@click.group()
def update():
    """Update items in the database using the cli"""
    pass

@update.command()
@with_appcontext
@click.option(
    "-build",
    type=click.Choice(["GRCh37", "GRCh38"]),
    nargs=1,
    help="Genome assembly (default:GRCh37)",
    default="GRCh37",
)
def genes(build):
    """Update genes and gene coordinates in database"""

    click.echo("Collecting gene names from EBI..")
    #client = EnsemblBiomartClient(build)

    hgnc_lines = ebi_genenames()
    click.echo(hgnc_lines)
