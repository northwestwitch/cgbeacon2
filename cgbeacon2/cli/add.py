#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import datetime
from flask.cli import with_appcontext, current_app

from cgbeacon2.constants import CONSENT_CODES
from cgbeacon2.utils.add import add_dataset

@click.group()
def add():
    """Add items to database using the CLI"""
    pass

@add.command()
@click.option('-id', type=click.STRING, nargs=1, required=True, help="dataset ID")
@click.option('-name', type=click.STRING, nargs=1, required=True, help="dataset name")
@click.option('-build', type=click.Choice(['GRCh37', 'GRCh38']), nargs=1, required=True, help="Genome assembly", default="GRCh37")
@click.option('-desc', type=click.STRING, nargs=1, required=False, help="dataset description")
@click.option('-version', type=click.FLOAT, nargs=1, required=False, help="dataset version, i.e. 1.0")
@click.option('-url', type=click.STRING, nargs=1, required=False, help="external url")
@click.option('-cc', type=click.STRING, nargs=1, required=False, help="consent code key. i.e. HMB")
@click.option('-info', type=(str, str), multiple=True, required=False, help="key-value pair of args. i.e.: FOO 1")
@with_appcontext
def dataset(id, name, build, desc, version, url, cc, info, ):
    """Creates a dataset object in the database

    Accepts:
        id(str): dataset unique ID (mandatory)
        name(str): dataset name (mandatory)
        build(str): Assembly identifier, GRCh37, GRCh38 (mandatory)
        description(str): description
        version(str): version
        url(): URL to an external system providing more dataset information (RFC 3986 format).
        cc(str): https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1005772
        info(list of tuples): Additional structured metadata, key-value pairs
    """

    click.echo("Adding a new dataset to database")

    dataset_obj = {
        '_id' : id,
        'name' : name,
        'assembly_id' : build,
        'created' : datetime.datetime.now(),
    }
    if desc is not None:
        dataset_obj["description"] = desc

    if version is not None:
        dataset_obj["version"] = version
    else:
        dataset_obj["version"] = 1.0

    if url is not None:
        dataset_obj["external_url"] = url

    if info is not None:
        info_dict = {}
        for info_tuple in info:
            info_dict[info_tuple[0]] = info_tuple[1]
        dataset_obj["info"] = info_dict

    if cc is not None and cc not in CONSENT_CODES:
        # This can be improved, doesn't consider Codes with XX yet
        # Make sure consent code is among is an official consent code

        click.echo("Consent code seem to have a non-standard value. Accepted consent code values:")
        count = 1
        for code, item in  CONSENT_CODES.items():
            click.echo(f'{count})\t{item["abbr"]}\t{item["name"]}\t{item["description"]}')
            count += 1
        click.Abort()

    dataset_obj["consent_code"] = cc

    inserted_id, collection = add_dataset(mongo_db=current_app.db, dataset_dict=dataset_obj)

    if inserted_id:
        click.echo(f"Inserted dataset with ID '{inserted_id}' into database collection '{collection}'")
    else:
        click.echo('Aborted')
