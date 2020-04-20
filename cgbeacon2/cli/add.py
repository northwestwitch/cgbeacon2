#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import datetime
from flask.cli import with_appcontext, current_app

from cgbeacon2.constants import CONSENT_CODES
from cgbeacon2.utils.add import add_dataset, add_variants
from cgbeacon2.utils.parse import extract_variants, count_variants
from cgbeacon2.utils.update import update_dataset_samples


@click.group()
def add():
    """Add items to database using the CLI"""
    pass


@add.command()
@click.option("-id", type=click.STRING, nargs=1, required=True, help="dataset ID")
@click.option("-name", type=click.STRING, nargs=1, required=True, help="dataset name")
@click.option(
    "-build",
    type=click.Choice(["GRCh37", "GRCh38"]),
    nargs=1,
    required=True,
    help="Genome assembly",
    default="GRCh37",
)
@click.option(
    "-desc", type=click.STRING, nargs=1, required=False, help="dataset description"
)
@click.option(
    "-version",
    type=click.FLOAT,
    nargs=1,
    required=False,
    help="dataset version, i.e. 1.0",
)
@click.option("-url", type=click.STRING, nargs=1, required=False, help="external url")
@click.option(
    "-cc", type=click.STRING, nargs=1, required=False, help="consent code key. i.e. HMB"
)
@click.option(
    "-info",
    type=(str, str),
    multiple=True,
    required=False,
    help="key-value pair of args. i.e.: FOO 1",
)
@click.option("--update", is_flag=True)
@with_appcontext
def dataset(id, name, build, desc, version, url, cc, info, update):
    """Creates a dataset object in the database or updates a pre-existing one

    Accepts:
        id(str): dataset unique ID (mandatory)
        name(str): dataset name (mandatory)
        build(str): Assembly identifier, GRCh37, GRCh38 (mandatory)
        description(str): description
        version(str): version
        url(): URL to an external system providing more dataset information (RFC 3986 format).
        cc(str): https://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1005772
        info(list of tuples): Additional structured metadata, key-value pairs
        update(bool): Update a dataset already present in the database with the same id
    """

    dataset_obj = {"_id": id, "name": name, "assembly_id": build}

    if update is True:
        dataset_obj["updated"] = datetime.datetime.now()
    else:
        dataset_obj["created"] = datetime.datetime.now()

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

    if cc is not None:
        # This can be improved, doesn't consider Codes with XX yet
        # Make sure consent code is among is an official consent code
        if cc not in CONSENT_CODES:
            click.echo(
                "Consent code seem to have a non-standard value. Accepted consent code values:"
            )
            count = 1
            for code, item in CONSENT_CODES.items():
                click.echo(
                    f'{count})\t{item["abbr"]}\t{item["name"]}\t{item["description"]}'
                )
                count += 1
            raise click.Abort()

        dataset_obj["consent_code"] = cc

    inserted_id = add_dataset(
        database=current_app.db, dataset_dict=dataset_obj, update=update
    )

    if inserted_id:
        click.echo(
            f"Dataset collection was successfully updated with dataset '{inserted_id}'"
        )
    else:
        click.echo(f"An error occurred while updating dataset collection")


@add.command()
@click.option("-ds", type=click.STRING, nargs=1, required=True, help="dataset ID")
@click.option("-vcf", type=click.Path(exists=True), required=True)
@click.option(
    "-sample",
    type=click.STRING,
    multiple=True,
    required=True,
    help="one or more samples to save variants for",
)
@with_appcontext
def variants(ds, vcf, sample):
    """Add variants from a VCF file to a dataset

    Accepts:
        ds(str): id of a dataset already existing in the database
        vcf(str): path to a VCF file
        sample(str) sample name as it's written in the VCF file, option repeated for each sample
    """
    # make sure dataset id corresponds to a dataset in the database
    dataset = current_app.db["dataset"].find_one({"_id": ds})
    if dataset is None:
        click.echo(f"Couldn't find any dataset with id '{ds}' in the database")
        raise click.Abort()

    vcf_obj = extract_variants(vcf_file=vcf)
    if vcf_obj is None:
        click.echo(f"Coundn't parse provided VCF file")
        raise click.Abort()

    nr_variants = count_variants(vcf_obj)
    if nr_variants == 0:
        click.echo(f"Provided VCF file doesn't contain any variant")
        raise click.Abort()

    # check if provided samples names correspond to those in the VCF file
    vcf_samples = set(vcf_obj.samples)  # set of samples contained in VCF file
    custom_samples = set(sample)  # set of samples provided by users
    if len(custom_samples & vcf_samples) < len(custom_samples):
        click.echo(
            f"Error. One or more provided samples are not contained in the VCF file"
        )
        raise click.Abort()

    vcf_obj = extract_variants(vcf_file=vcf)

    # Parse VCF variants
    added = add_variants(
        database=current_app.db,
        vcf_obj=vcf_obj,
        samples=custom_samples,
        assembly=dataset["assembly_id"],
        dataset_id=ds,
        nr_variants=nr_variants,
    )
    click.echo(f"{added} variants loaded into the database")

    if added > 0:
        # update list of samples in beacon for this dataset
        result = update_dataset_samples(
            database=current_app.db, dataset_id=ds, samples=custom_samples, add=True
        )

        if result is not None:
            click.echo(
                f"Samples {custom_samples} were successfully added to dataset list of samples"
            )
        else:
            click.echo("List of dataset samples was left unchanged")
