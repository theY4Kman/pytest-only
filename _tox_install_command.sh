#!/bin/bash
poetry install -v \
 && poetry run pip install --no-warn-conflicts "$@"
