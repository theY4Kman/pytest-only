#!/bin/bash

# Virtualenvs created in 3.12+ may malfunction with older setuptools
pip install -U setuptools

poetry install -v \
 && poetry run pip install --no-warn-conflicts "$@"
