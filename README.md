# Tidy directory

A Python script for tidying directories.
Files older than a given age are moved to an archive directory.
Separately, old files in the archive are deleted.

## Usage

```shell
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
```

## Scheduling

The main motivation for this script was to automatically keep a downloads folder organised.
This can be done by creating a script similar to `run-tidydirectory.sh` and then scheduling it to run using **Cron**.

For example, this would run the script every day at 03:00:

```cron
0 3 * * * mamba run -n tidydirectory /path/to/tidydirectory/run-tidydirectory.sh
```

The example command runs the script in a [**conda**](https://docs.conda.io/projects/conda/en/stable/) environment (see `envrionment.yml`) but if you don't want to do that you can ignore the `mamba -r -n tidydirectory` part.
