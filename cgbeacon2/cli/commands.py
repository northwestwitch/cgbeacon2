#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from cgbeacon2 import __version__
from flask.cli import FlaskGroup

from cgbeacon2.server import create_app

@click.version_option(__version__)
@click.group(cls=FlaskGroup, create_app=create_app, invoke_without_command=False, add_default_commands=True,
    add_version_option=False)
def cli(**_):
    """Base command for invoking the command line"""
    pass


def create_dataset():
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



#def load_variants(vcf_file, panels=[]):
#    """Load variants into database from a VCF file

#    Accepts:
