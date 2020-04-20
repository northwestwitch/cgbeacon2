#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from flask.cli import with_appcontext, current_app

from cgbeacon2.utils.delete import delete_dataset


@click.group()
def delete():
    """Delete items from database using the CLI"""
    pass


@delete.command()
@with_appcontext
@click.option("-id", type=click.STRING, nargs=1, required=True, help="dataset ID")
def dataset(id):
    """Delete a dataset using its _id key

    Accepts:
        id(str): dataset _id field
    """

    click.echo(f"deleting dataset with id '{id}' from database")

    deleted = delete_dataset(mongo_db=current_app.db, id=id)

    if deleted is None:
        click.echo("Aborting")
    elif deleted == 0:
        click.echo(f"Coundn't find a dataset with id '{id}' in database.")
    elif deleted == 1:
        click.echo("Dataset was successfully deleted")


@delete.command()
@with_appcontext
@click.option("-ds", type=click.STRING, nargs=1, required=True, help="dataset ID")
@click.option(
    "-sample",
    type=click.STRING,
    multiple=True,
    required=True,
    help="one or more samples to remove variants for",
)
def variants(ds, sample):
    """Remove variants for one or more samples of a dataset

    Accepts:
        ds(str): id of a dataset already existing in the database
        sample(str) sample name as it's written in the VCF file, option repeated for each sample
    """

    click.confirm(f"Deleting variants for sample {sample}, dataset '{ds}'. Do you want to continue?", abort=True)

    # Make sure dataset exists and contains the provided sample(s)
    dataset = current_app.db["dataset"].find_one({"_id": ds})
    if dataset is None:
        click.echo(f"Couldn't find any dataset with id '{ds}' in the database")
        raise click.Abort()

    click.echo(f"Samples:{sample}, type:{type(sample)}")
    for s in sample:
        if s not in dataset.get("samples", []):
            click.echo(f"Couldn't find any sample '{s}' in the sample list of dataset 'dataset'")
            raise click.Abort()
