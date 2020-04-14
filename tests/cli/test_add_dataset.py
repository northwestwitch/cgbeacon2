# -*- coding: utf-8 -*-
from cgbeacon2.cli.commands import cli


def test_add_dataset_no_id(test_dataset, mock_app):
    """Test the cli command which adds a dataset to db"""

     # test add a dataset_obj using the app cli
    runner = mock_app.test_cli_runner()

    dataset = test_dataset

    # When invoking the command without the -id parameter
    result =  runner.invoke(cli, [
        'add',
        'dataset',
        '-name', dataset["name"]
        ])
    # Then the command should return error
    assert result.exit_code == 2
    assert "Missing option '-id'" in result.output


def test_add_dataset_no_name(test_dataset, mock_app):
    """Test the cli command which adds a dataset to db"""

     # test add a dataset_obj using the app cli
    runner = mock_app.test_cli_runner()

    dataset = test_dataset

    # When invoking the command without the -name parameter
    result =  runner.invoke(cli, [
        'add',
        'dataset',
        '-id', dataset["_id"]
        ])
    # Then the command should return error
    assert result.exit_code == 2
    assert "Missing option '-name'" in result.output


def test_add_dataset_wrong_build(test_dataset, mock_app):
    """Test the cli command which adds a dataset to db"""

     # test add a dataset_obj using the app cli
    runner = mock_app.test_cli_runner()

    dataset = test_dataset

    # When invoking the command without a valid genome build
    result =  runner.invoke(cli, [
        'add',
        'dataset',
        '-id', dataset["_id"],
        '-name', dataset["name"],
        '-build', "meh"
        ])
    # Then the command should return error
    assert result.exit_code == 2
    assert "Invalid value for '-build': invalid choice" in result.output
