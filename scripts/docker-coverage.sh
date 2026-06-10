#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports
docker compose run --rm coverage
