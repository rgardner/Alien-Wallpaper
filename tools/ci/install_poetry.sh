#!/usr/bin/env bash
# Installs poetry on Unix-like environment.

set -euo pipefail

python get-poetry.py --preview -y
source "${HOME}/.poetry/env"
