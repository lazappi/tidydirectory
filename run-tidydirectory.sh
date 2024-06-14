#!/usr/bin/env bash

cd ~/path/to/tidydirectory

./tidydirectory.py \
    --directory /path/to/directory \
    --archive-directory /path/to/directory/archive \
    --archive-age 7 \
    --delete-age 30 \
    --mapping-file file-mapping.yml \
    --dry-run 2>&1 | \
    tee .tidydirectory.log
