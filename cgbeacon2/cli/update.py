#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext
from cgbeacon2.utils.ensembl_biomart import EnsemblBiomartClient


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

    click.echo(f"Collecting gene names from EBI, genome build ->{build}")
    client = EnsemblBiomartClient(build)
    gene_lines = client.query_service()
