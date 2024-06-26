#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 Mesh Research
#
# invenio-record-importer is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""
Functions to convert and migrate legacy CORE deposits to InvenioRDM

Relies on the following environment variables:

MIGRATION_SERVER_DATA_DIR   The full path to the local directory where
                            the source json files (exported from legacy
                            CORE) can be found.

Normally these variables can be set in the .env file in your base
knowledge_commons_works directory.
"""

import click
from flask import current_app as app
from flask.cli import with_appcontext
from typing import Optional

from invenio_record_importer.serializer import serialize_json
from invenio_record_importer.services import SerializationService
from invenio_record_importer.record_loader import (
    load_records_into_invenio,
    delete_records_from_invenio,
)

# from invenio_record_importer.legacy.fedora_fetcher import fetch_fedora_records
import json
from pprint import pprint


@click.group()
def cli():
    pass


@cli.command(name="serialize")
@with_appcontext
def serialize_command_wrapper():
    """
    Serialize all exported legacy CORE deposits as JSON that Invenio can ingest
    """
    serialize_json()


@cli.command(name="load")
@click.argument("records", nargs=-1)
@click.option(
    "-n",
    "--no-updates",
    is_flag=True,
    default=False,
    help=(
        "If True, do not update existing records where a record with the same"
        " DOI already exists."
    ),
)
@click.option(
    "-r",
    "--retry-failed",
    is_flag=True,
    default=False,
    help=(
        "If True, try to load in all previously failed records that have not"
        " already been repaired successfully."
    ),
)
@click.option(
    "-s",
    "--use-sourceids",
    is_flag=True,
    default=False,
    help=(
        "If True, the positional arguments are interpreted as ids in the"
        " source system instead of positional indices."
    ),
)
@click.option(
    "--scheme",
    default="hclegacy-pid",
    help=(
        "The identifier scheme to use for the records when the --use-sourceids "
        "flag is True. Defaults to 'hclegacy-pid' for the ids used by the old "
        "Humanities Commons CORE repository."
    ),
)
@click.option(
    "-a",
    "--aggregate",
    is_flag=True,
    default=False,
    help=(
        "If True, aggregate the record view and download statistics for all"
        " records after loading. (This may take a long time.)"
    ),
)
@click.option(
    "--start-date",
    default=None,
    help=(
        "The start date for the record events to aggregate if the --aggregate "
        "flag is True. If not specified, the aggregation will begin from the "
        "earliest creation date of the migrated records. The date should be "
        "formatted in ISO format, i.e. as 'YYYY-MM-DD'."
    ),
)
@click.option(
    "--end-date",
    default=None,
    help=(
        "The end date for the record events to aggregate if the --aggregate "
        "flag is True. If not specified, the aggregation will end with the "
        "current date. The date should be formatted in ISO format, i.e. as "
        "'YYYY-MM-DD'."
    ),
)
@click.option(
    "-c",
    "--clean-filenames",
    is_flag=True,
    default=False,
    help=(
        "If True, clean up the filenames of the uploaded files to remove"
        " special characters and spaces."
    ),
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Print and log verbose output",
)
@click.option(
    "-x",
    "--stop-on-error",
    is_flag=True,
    default=False,
    help="Stop loading records if an error is encountered",
)
@with_appcontext
def load_records(
    records: list,
    no_updates: bool,
    retry_failed: bool,
    use_sourceids: bool,
    scheme: str,
    aggregate: bool,
    start_date: Optional[str],
    end_date: Optional[str],
    clean_filenames: bool,
    verbose: bool,
    stop_on_error: bool,
):
    """
    Load serialized exported records into InvenioRDM.


    If RECORDS is not specified, all records will be loaded. Otherwise,
    RECORDS should be a list of positional arguments specifying which records
    to load.

    Examples:

        To load records 1, 2, 3, and 5, run:

            invenio importer load 1 2 3 5

        A range can be specified in the RECORDS by linking two integers with a
        hyphen. For example, to load only the first 100 records, run:

            invenio importer load 1-100

        If the range ends in a hyphen with no second integer, the program will
        load all records from the start index to the end of the input file. For
        example, to load all records from 100 to the end of the file, run:

            invenio importer load 100-

        Records may be loaded by id in the source system instead of by index.
        For example, to load records with ids hc:4723, hc:8271, and hc:2246,
        run:

            invenio importer load --use-sourceids hc:4723 hc:8271 hc:2246

        To aggregate usage statistics after loading, add the --aggregate flag.
        For example, to load all records and aggregate usage statistics, run:

            invenio importer load --aggregate

    Notes:

        This program must be run from the base knowledge_commons_works
        directory. It will look for the exported records in the directory
        specified by the MIGRATION_SERVER_DATA_DIR environment variable.

        The program must also be run inside the pipenv virtual environment for
        the knowledge_commons_works instance. All of the commands must be
        preceded by `pipenv run` or the pipenv environment must first be
        activated with `pipenv shell`.

        The operations involved require authenitcation as an admin user in the
        knowledge_commons_works instance. This program will look for the
        admin user's api token in the MIGRATION_API_TOKEN environment variable.
        Where it's necessary to invite this user to a community, the program
        will look for the community's id in the P_TOKEN environment variable.

        Where necessary this program will create top-level domain communities,
        assign the records to the correct domain communities, create
        new Invenio users corresponding to the users who uploaded the
        original deposits, and transfer ownership of the Invenio record to
        the correct users.

        If a record with the same DOI already exists in Invenio, the program
        will try to update the existing record with any new metadata and/or
        files, creating a new draft of published records if necessary.
        Unpublished existing drafts will be submitted to the appropriate
        community and published. Alternately, if the --no-updates flag is set,
        the program will skip any records that match DOIs for records that
        already exist in Invenio.

        Since the operations involved are time-consuming, the program should
        be run as a background process (adding & to the end of the command).
        A running log of the program's progress will be written to the file
        invenio_record_importer.log in the base invenio_record_importer/logs
        directory. A record of all records that have been touched (a load
        attempt has been made) is recorded in the file
        invenio_record_importer_touched.json in the base
        invenio_record_importer/logs directory. A record of all records that
        have failed to load is recorded in the file
        invenio_record_importer_failed.json in the
        invenio_record_importer/logs directory. If failed records are later
        successfully repaired, they will be removed from the failed records
        file.

    Args:

        records (list, optional): A list of the provided positional arguments
            specifying which records to load. Defaults to [].

            If no positional arguments are provided, all records will be
            loaded.

            If positional arguments are provided, they should be either
            integers specifying the line numbers of the records to load,
            or source ids specifying the ids of the records to load in
            the source system. These will be interpreted as line numbers
            in the jsonl file of records for import (beginning at 1)
            unless the --use-sourceids flag is set.

            If a range is specified in the RECORDS by linking two integers with
            a hyphen, the program will load all records between the two
            indices, inclusive. If the range ends in a hyphen with no second
            integer, the program will load all records from the start index to
            the end of the input file.

        no_updates (bool, optional): If True, do not update existing records
            where a record with the same DOI already exists. Defaults to False.

        retry_failed (bool, optional): If True, try to load in all previously
            failed records that have not already been repaired successfully.
            Defaults to False.

        use_sourceids (bool, optional): If True, the positional arguments
            are interpreted as ids in the source system instead of positional
            indices. Defaults to False.

        scheme (str, optional): The identifier scheme to use for the records
            when the --use-sourceids flag is True. Defaults to 'hclegacy-pid'
            for the ids used by the old Humanities Commons CORE repository.

        aggregate (bool, optional): If True, aggregate the record view and
            download statistics for all records after loading. Defaults to
            False.

        start_date (str, optional): The start date for the record events to
            aggregate if the --aggregate flag is True. If not specified, the
            aggregation will begin from the earliest creation date of the
            migrated records. The date should be formatted in ISO format,
            i.e. as 'YYYY-MM-DD'. Defaults to None.

        end_date (str, optional): The end date for the record events to
            aggregate if the --aggregate flag is True. If not specified, the
            aggregation will end with the current date. The date should be
            formatted in ISO format, i.e. as 'YYYY-MM-DD'. Defaults to None.

        clean_filenames (bool, optional): If True, clean up the filenames of
            the uploaded files to remove special characters and spaces.

        verbose (bool, optional): Print and log verbose output. Defaults to
            False.

        stop_on_error (bool, optional): Stop loading records if an error is
            encountered. Defaults to False.

    Returns:

        None
    """
    named_params = {
        "no_updates": no_updates,
        "retry_failed": retry_failed,
        "use_sourceids": use_sourceids,
        "sourceid_scheme": scheme,
        "aggregate": aggregate,
        "start_date": start_date,
        "end_date": end_date,
        "clean_filenames": clean_filenames,
        "verbose": verbose,
        "stop_on_error": stop_on_error,
    }
    if len(records) > 0 and "-" in records[0]:
        if use_sourceids:
            print("Error: Cannot use source ids with ranges.")
            app.logger.error(
                "Ranges can only be specified using record indices, not source"
                " ids."
            )
            return
        named_params["start_index"], named_params["stop_index"] = records[
            0
        ].split("-")
        named_params["start_index"] = int(named_params["start_index"])
        if named_params["stop_index"] == "":
            named_params["stop_index"] = -1
        else:
            named_params["stop_index"] = int(named_params["stop_index"])
    else:
        if not use_sourceids:
            named_params["nonconsecutive"] = [int(arg) for arg in records]
        else:
            records = [arg.replace("\-", "-") for arg in records]
            named_params["nonconsecutive"] = records

    load_records_into_invenio(**named_params)


@cli.command(name="read")
@click.argument("records", nargs=-1)
@click.option(
    "-s",
    "--use-sourceids",
    is_flag=True,
    default=False,
)
@click.option(
    "--scheme",
    default="doi",
    help=(
        "The identifier scheme to use for the records when the --use-sourceids "
        "flag is True. Defaults to 'doi'."
    ),
)
@click.option(
    "-r",
    "--raw-input",
    is_flag=True,
    default=False,
    help=(
        "If True, the returned records will be in the raw format read from the"
        " source file, rather than the serialized format."
    ),
)
@click.option(
    "-p",
    "--field-path",
    default="",
    help=(
        "A dot-separated string of field names to specify a subfield of the"
        " record(s) to read."
    ),
)
@with_appcontext
def read_records(
    records, scheme, raw_input, use_sourceids, field_path
) -> None:
    """
    Read serialized records or raw input from the source file or original data.

    params:
        records: list
            A list of positional arguments specifying which records to read.
            If positional arguments are provided, they should be either
            integers specifying the line numbers of the records to read,
            or source ids specifying the ids of the records to read in
            the source system. These will be interpreted as line numbers
            in the jsonl file of records for import (beginning at 1)
            unless the --use-sourceids flag is set.

        scheme: str
            The identifier scheme to use for the records when the --use-sourceids
            flag is True. Defaults to 'doi'.

        raw_input: bool
            If True, the returned records will be in the raw format read from the
            source file, rather than the serialized format.

        use_sourceids: bool
            If True, the positional arguments are interpreted as ids in the
            source system instead of positional indices.

        field_path: str
            A dot-separated string of field names to specify a subfield of the
            record(s) to read.
    """
    service = SerializationService()
    args = {"field_path": field_path}
    if use_sourceids:
        args["id_scheme"] = scheme
        args["identifiers"] = records
    else:
        args["indices"] = records

    if raw_input:
        raw_records = service.read_raw(**args)
        for r in raw_records:
            print(f"Raw (unserialized) source data for record {r['id']}:")
            pprint(r["record"])
    else:
        records = service.read_serialized(**args)
        for c in records:
            print(f"Processed (serialized) input data for record {c['id']}:")
            pprint(c["record"])


@cli.command(name="delete")
@click.argument("records", nargs=-1)
def delete_records(records):
    """
    Delete one or more records from InvenioRDM by record id.
    """
    delete_records_from_invenio(records)


# @cli.command(name="fedora")
# @click.option(
#     "--count", default=20, help="Maximum number of records to return"
# )
# @click.option(
#     "--query", default=None, help="A query string to limit the records"
# )
# @click.option(
#     "--protocol",
#     default="fedora-xml",
#     help="The api protocol to use for the request",
# )
# @click.option(
#     "--pid",
#     default=None,
#     help="A pid or regular expression to select records by pid",
# )
# @click.option(
#     "--terms",
#     default=None,
#     help="One or more subject terms to filter the records",
# )
# @click.option(
#     "--fields",
#     default=None,
#     help="A comma separated string list of fields to return for each record",
# )
# def fetch_fedora(
#     query: Optional[str],
#     protocol: str,
#     pid: Optional[str],
#     terms: Optional[str],
#     fields: Optional[str],
#     count: int,
# ) -> list[dict]:
#     """Deprecated: Fetch records from the Fedora repository."""
#     fetch_fedora_records(query, protocol, pid, terms, fields, count)


if __name__ == "__main__":
    cli()
