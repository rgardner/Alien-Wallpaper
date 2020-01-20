#!/usr/bin/env bash
# Installs poetry on Unix-like environment.

set -euo pipefail

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
source "${HOME}/.poetry/env"
