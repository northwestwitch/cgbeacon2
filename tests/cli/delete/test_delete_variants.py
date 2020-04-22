# -*- coding: utf-8 -*-
import click

from cgbeacon2.cli.commands import cli
from cgbeacon2.resources import test_snv_vcf_path, panel1_path


def test_delete_variants_confirm(mock_app):
    """Test confirm question in delete variants command"""

    runner = mock_app.test_cli_runner()
    # When invoking the command without confirming the action
    result = runner.invoke(cli, ["delete", "variants", "-ds", "foo", "-sample", "bar"])
    # Then the command should exit
    assert result.exit_code == 1
    assert "Do you want to continue?" in result.output


def test_delete_variant_non_existing_dataset(mock_app):
    """Test the command to delete variants when the dataset provided doesn't exist in database"""

    runner = mock_app.test_cli_runner()

    # When invoking the command with a dataset not present in database
    result = runner.invoke(
        cli, ["delete", "variants", "-ds", "foo", "-sample", "bar"], input="y\n"
    )

    assert result.exit_code == 1
    assert "Couldn't find any dataset with id 'foo' in the database" in result.output


def test_delete_variants_non_existing_sample(mock_app, test_dataset_cli, database):
    """Test the command to delete variants when the sample is not found in database"""

    runner = mock_app.test_cli_runner()

    # Having a database containing a dataset
    dataset = test_dataset_cli
    database["dataset"].insert_one(dataset)

    # When invoking the command without a sample not present in dataset samples
    result = runner.invoke(
        cli,
        ["delete", "variants", "-ds", test_dataset_cli["_id"], "-sample", "bar"],
        input="y\n",
    )

    assert result.exit_code == 1
    assert (
        "Couldn't find any sample 'bar' in the sample list of dataset" in result.output
    )


def test_delete_variants(mock_app, test_dataset_cli, database):
    """Test the command to delete variants"""

    runner = mock_app.test_cli_runner()

    # Having a database containing a dataset
    dataset = test_dataset_cli
    database["dataset"].insert_one(dataset)

    # And a variants from 2 different samples of a dataset
    sample = "ADM1059A1"
    sample2 = "ADM1059A2"

    result = runner.invoke(
        cli,
        [
            "add",
            "variants",
            "-ds",
            dataset["_id"],
            "-vcf",
            test_snv_vcf_path,
            "-sample",
            sample,
            "-sample",
            sample2,
            "-panel",
            panel1_path
        ],
    )
    initial_vars = sum(1 for i in database["variant"].find())
    assert initial_vars > 0

    # Then when using the cli command to remove onw of the samples
    result = runner.invoke(
        cli,
        ["delete", "variants", "-ds", test_dataset_cli["_id"], "-sample", sample],
        input="y\n",
    )

    # Then there should be less variants left in the database
    remaining_vars = sum(1 for i in database["variant"].find())
    assert remaining_vars > 0
    assert remaining_vars < initial_vars

    # And the sample should disappear from the list of dataset samples
    dataset_obj = database["dataset"].find_one({"_id": dataset["_id"]})
    assert sample not in dataset_obj["samples"]
