# -*- coding: utf-8 -*-
import click

from cgbeacon2.cli.commands import cli

def test_delete_variants_confirm(mock_app):
    """Test confirm question in delete variants command"""

    runner = mock_app.test_cli_runner()
    # When invoking the command without confirming the action
    result = runner.invoke(cli, [
        "delete",
        "variants",
        "-ds", "foo",
        "-sample", "bar"
    ])
    # Then the command should exit
    assert result.exit_code == 1
    assert  "Do you want to continue?" in result.output


def test_delete_variant_non_existing_dataset(mock_app):
    """Test the command to delete variants when the dataset provided doesn't exist in database"""

    runner = mock_app.test_cli_runner()

    # When invoking the command with a dataset not present in database
    result = runner.invoke(cli, [
        "delete",
        "variants",
        "-ds", "foo",
        "-sample", "bar"
    ], input='y\n')

    assert result.exit_code == 1
    assert  "Couldn't find any dataset with id 'foo' in the database" in result.output


def test_delete_variants_non_existing_sample(mock_app, test_dataset_cli, database):
    """Test the command to delete variants when the sample is not found in database"""

    runner = mock_app.test_cli_runner()

    # Having a database containing a dataset
    dataset = test_dataset_cli
    database["dataset"].insert_one(dataset)

    # When invoking the command without a sample not present in dataset samples
    result = runner.invoke(cli, [
        "delete",
        "variants",
        "-ds", test_dataset_cli["_id"],
        "-sample", "bar"
    ], input='y\n')

    assert result.exit_code == 1
    assert  "Couldn't find any sample 'bar' in the sample list of dataset" in result.output
