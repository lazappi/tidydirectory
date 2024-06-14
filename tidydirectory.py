#!/usr/bin/env python

import os
import shutil
import time
import yaml
import logging
from datetime import datetime
from docopt import docopt

USAGE = """
Usage:
    tidydirectory --directory=<dir> --archive-directory=<dir> --archive-age=<days> --delete-age=<days> --mapping-file=<file> [--dry-run] [--verbose]

Options:
    -h --help                   Show this screen.
    --directory=<dir>           The directory to organize.
    --archive-directory=<dir>   The directory to archive files to.
    --archive-age=<days>        The age of files to archive (in days).
    --delete-age=<days>         The age of files to delete (in days).
    --mapping-file=<file>       YAML file containing the mapping of file extensions to categories.
    --verbose                   Enable verbose logging.
    --dry-run                   Perform a dry run without making any changes.
"""


def setup_logging(verbose: bool) -> None:
    """
    Setup logging configuration.

    Parameters
    ----------
    verbose
        If True, set log level to DEBUG, else to INFO.
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def get_file_age_in_days(file_path: str) -> float:
    """
    Get the age of a file in days based on the last access and modification times,
    whichever is more recent.

    Parameters
    ----------
    file_path
        Path to the file to get the age for.

    Returns
    -------
    The age of the file in days.
    """

    current_time = time.time()
    access_time = os.path.getatime(file_path)
    modified_time = os.path.getmtime(file_path)
    access_age_days = (current_time - access_time) / (24 * 3600)
    modified_age_days = (current_time - modified_time) / (24 * 3600)

    min_age = min(access_age_days, modified_age_days)

    logging.debug(f"FILE AGE: {file_path} - {min_age} days")

    return min_age


def get_directory_age_in_days(directory_path: str) -> float:
    """
    Get the age of a directory based on the most recent file it contains.

    Parameters
    ----------
    directory_path
        Path to the directory.

    Returns
    -------
    Age of the directory in days/.
    """
    most_recent_age = float("inf")
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_age = get_file_age_in_days(file_path)
            if file_age < most_recent_age:
                most_recent_age = file_age

    logging.debug(f"DIRECTORY AGE: {directory_path} - {most_recent_age} days")

    return most_recent_age


def move_to_archive(
    path: str, category: str, archive_directory: str, dry_run: bool
) -> None:
    """
    Move a file or directory to the archive directory under the specified category.

    Parameters
    ----------
    path
        Path to the file or directory to move.
    category
        Category to archive the path under.
    archive_directory
        Path to the archive directory.
    dry_run
        If True, changes are not executed.
    """

    category_archive = os.path.join(archive_directory, category)
    if not dry_run:
        os.makedirs(category_archive, exist_ok=True)

    archive_path = os.path.join(category_archive, os.path.basename(path))
    if os.path.exists(archive_path):
        filename, extension = os.path.splitext(archive_path)
        archive_path = f"{filename}_{datetime.now.strftime("%Y%m%d")}{extension}"

    if not dry_run:
        shutil.move(path, archive_path)

    logging.info(f"Moved '{path}' -> '{archive_path}'")


def delete_old_paths(directory: str, delete_age: int, dry_run: bool) -> int:
    """
    Delete old files and directories in a given directory.

    Parameters
    ----------
    directory
        Path to the containing file and directories to (possibly) delete.
    delete_age
        Files/directories older than this age (in days) will be deleted.
    dry_run
        If True, changes are not executed.

    Returns
    -------
    Number of files and directories deleted.
    """

    deleted = 0

    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path):
            if get_directory_age_in_days(full_path) > delete_age:
                if not dry_run:
                    shutil.rmtree(full_path)
                    deleted += 1
                logging.info(f"Deleted directory: {full_path}")
        else:
            if get_file_age_in_days(full_path) > delete_age:
                if not dry_run:
                    os.remove(full_path)
                    deleted += 1
                logging.info(f"Deleted '{full_path}'")

    return deleted


def check_and_archive(
    directory: str,
    archive_directory: str,
    archive_age: int,
    file_type_mapping: dict,
    dry_run: bool,
) -> tuple[int, int]:
    """
    Check the age of files and directories in a given directory and archive them
    if needed.

    Parameters
    ----------
    directory
        Path to the directory to check.
    archive_directory
        Path to the archive directory.
    archive_age
        Age of files to archive in days.
    file_type_mapping
        Mapping of file types to categories.
    dry_run
        If True, changes are not executed.

    Returns
    -------
    Tuple containing the number of files and directories moved to the archive.
    """

    moved_files = 0
    moved_directories = 0

    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path):
            if os.path.samefile(full_path, archive_directory):
                continue
            if get_directory_age_in_days(full_path) > archive_age:
                move_to_archive(full_path, "directories", archive_directory, dry_run)
                moved_directories += 1
        else:
            if get_file_age_in_days(full_path) > archive_age:
                file_extension = os.path.splitext(full_path)[1]
                category = file_type_mapping.get(file_extension, "other")
                move_to_archive(full_path, category, archive_directory, dry_run)
                moved_files += 1

    return (moved_files, moved_directories)


def check_archive_and_delete(
    archive_directory: str, delete_age: int, dry_run: bool
) -> int:
    """
    Check the archive directory and delete old files and directories.

    Parameters
    ----------
    archive_directory
        Path to the archive directory.
    delete_age
        Files/directories older than this age (in days) will be deleted.
    dry_run
        If True, changes are not executed.

    Returns
    -------
    Number of files and directories deleted.
    """

    deleted = 0

    for category in os.listdir(archive_directory):
        category_path = os.path.join(archive_directory, category)
        if os.path.isdir(category_path):
            deleted += delete_old_paths(category_path, delete_age, dry_run)

    return deleted


def read_file_type_mapping(mapping_file: str) -> dict:
    """
    Read the file mapping from a YAML file.

    Parameters
    ----------
    mapping_file
        Path to the YAML file containing the mapping.

    Returns
    -------
    Dictionary mapping file extensions to categories.
    """
    with open(mapping_file, "r") as file:
        yaml_mapping = yaml.safe_load(file)

    file_mapping = {}
    for category, extensions in yaml_mapping.items():
        for extension in extensions:
            file_mapping[extension] = category

    return file_mapping


# Main script execution
if __name__ == "__main__":
    arguments = docopt(USAGE)

    directory = arguments["--directory"]
    archive_directory = arguments["--archive-directory"]
    archive_age = int(arguments["--archive-age"])
    delete_age = int(arguments["--delete-age"])
    mapping_file = arguments["--mapping-file"]
    verbose = arguments["--verbose"]
    dry_run = arguments["--dry-run"]

    setup_logging(verbose)


    logging.info(f"Tidying: '{directory}', Archive age: {archive_age} days")
    logging.info(f"Archive: '{archive_directory}', Delete age: {delete_age} days")
    if dry_run:
        logging.info("Running in dry-run mode. Changes will be listed but not made.")

    file_type_mapping = read_file_type_mapping(mapping_file)
    archived_files, archived_directories = check_and_archive(
        directory,
        archive_directory,
        archive_age,
        file_type_mapping,
        dry_run,
    )
    deleted = check_archive_and_delete(archive_directory, delete_age, dry_run)

    logging.info(
        f"Archived {archived_files} files and {archived_directories} directories"
    )
    logging.info(f"Deleted {deleted} files/directories from the archive")
    logging.info(f"Done!")
