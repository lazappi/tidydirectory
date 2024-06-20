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

Expand the next section for an example.

<details>
<summary>

## Example

</summary>

Here is a more complete example using a test directory:

### 1. Create the test directory

```shell
$ bash ./make-test-dir.sh
Removing existing test directory...
Creating new test directory...
Adding new files...
Adding old files...
Adding archived files...
Adding expired files...
```

### 2. See what we are starting with

```shell
$ tree test-dir
test-dir
├── archive
│  ├── data
│  │  ├── archived-data.csv
│  │  └── expired-data.csv
│  ├── directories
│  │  ├── archived-directory
│  │  │  └── archived-directory.file
│  │  └── expired-directory
│  │     └── expired-directory.file
│  ├── documents
│  │  ├── archived-document.txt
│  │  └── expired-document.txt
│  ├── images
│  │  ├── archived-image.jpg
│  │  └── expired-image.txt
│  └── other
│     ├── archived-other.unknown
│     └── expired-other.unknown
├── new-data.csv
├── new-directory
│  └── new-directory.file
├── new-document.txt
├── new-image.jpg
├── new-other.unknown
├── old-data.csv
├── old-directory
│  └── old-directory.file
├── old-document.txt
├── old-image.jpg
└── old-other.unknown
```

### 3. Run the script

```shell
$ python tidydirectory.py --directory test-dir --archive-directory test-dir/archive --archive-age 7 --delete-age 30 --mapping-file file-mapping.yml
2024-06-14 15:38:52 INFO: Tidying: 'test-dir', Archive age: 7 days
2024-06-14 15:38:52 INFO: Archive: 'test-dir/archive', Delete age: 30 days
2024-06-14 15:38:52 INFO: Moved 'test-dir/old-other.unknown' -> 'test-dir/archive/other/old-other.unknown'
2024-06-14 15:38:52 INFO: Moved 'test-dir/old-directory' -> 'test-dir/archive/directories/old-directory'
2024-06-14 15:38:52 INFO: Moved 'test-dir/old-data.csv' -> 'test-dir/archive/data/old-data.csv'
2024-06-14 15:38:52 INFO: Moved 'test-dir/old-document.txt' -> 'test-dir/archive/documents/old-document.txt'
2024-06-14 15:38:52 INFO: Moved 'test-dir/old-image.jpg' -> 'test-dir/archive/images/old-image.jpg'
2024-06-14 15:38:52 INFO: Deleted 'test-dir/archive/images/expired-image.txt'
2024-06-14 15:38:52 INFO: Deleted 'test-dir/archive/other/expired-other.unknown'
2024-06-14 15:38:52 INFO: Deleted directory: test-dir/archive/directories/expired-directory
2024-06-14 15:38:52 INFO: Deleted 'test-dir/archive/documents/expired-document.txt'
2024-06-14 15:38:52 INFO: Deleted 'test-dir/archive/data/expired-data.csv'
2024-06-14 15:38:52 INFO: Archived 4 files and 1 directories
2024-06-14 15:38:52 INFO: Deleted 5 files/directories from the archive
2024-06-14 15:38:52 INFO: Done!
```

### 4. See the results

```shell
$ tree test-dir
test-dir
├── archive
│  ├── data
│  │  ├── archived-data.csv
│  │  └── old-data.csv
│  ├── directories
│  │  ├── archived-directory
│  │  │  └── archived-directory.file
│  │  └── old-directory
│  │     └── old-directory.file
│  ├── documents
│  │  ├── archived-document.txt
│  │  └── old-document.txt
│  ├── images
│  │  ├── archived-image.jpg
│  │  └── old-image.jpg
│  └── other
│     ├── archived-other.unknown
│     └── old-other.unknown
├── new-data.csv
├── new-directory
│  └── new-directory.file
├── new-document.txt
├── new-image.jpg
└── new-other.unknown
```

Everything starting with `old-` has been moved to the archive and everything starting with `expired-` has been deleted from the archive but those starting wth `new-` remain untouched in the main directory and those starting with `archived-` remain in the archive.

</details>

## Scheduling

The main motivation for this script was to automatically keep a downloads folder organised.
This can be done by creating a script similar to `run-tidydirectory.sh` and then scheduling it to run using **Cron**.

For example, this would run the script every day at 03:00:

```cron
0 3 * * * /path/to/mamba run -n tidydirectory /path/to/tidydirectory/run-tidydirectory.sh
```

The example command runs the script in a [**conda**](https://docs.conda.io/projects/conda/en/stable/) environment (see `environment.yml`) but if you don't want to do that you can ignore the `mamba -r -n tidydirectory` part.
