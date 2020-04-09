#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import datetime

@click.group()
def add():
    """Add items to database using the CLI"""
    pass

@add.command()
@click.option('-id', type=click.STRING, nargs=1, required=True, help="dataset ID")
@click.option('-name', type=click.STRING, nargs=1, required=True, help="dataset name")
@click.option('-build', type=click.STRING, nargs=1, required=True, help="Genome assembly", default="GRCh37")
@click.option('-desc', type=click.STRING, nargs=1, required=False, help="dataset description")
@click.option('-version', type=click.STRING, nargs=1, required=False, help="dataset version, i.e. 1.0")
@click.option('-url', type=click.STRING, nargs=1, required=False, help="external url")
@click.option('-info', type=click.STRING, nargs=1, required=False, help="key-value pair of args. i.e.: FOO 1 BAR 2")
@click.option('-cc', type=click.STRING, nargs=1, required=False, help="consent code key. i.e. HMB")
def dataset(id, name, build, desc, version, url, info, cc):
    """Creates a dataset object in the database

    Accepts:
        id(str): dataset unique ID (mandatory)
        name(str): dataset name (mandatory)
        assembly_id(str): Assembly identifier, GRCh37, GRCh38 (mandatory)
        description(str): description
        version(str): version
        externalUrl(): URL to an external system providing more dataset information (RFC 3986 format).
        info(list of tuples): Additional structured metadata, key-value pairs
        consent_code(str): https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1005772

    """

    click.echo("HELLO THERE!")
