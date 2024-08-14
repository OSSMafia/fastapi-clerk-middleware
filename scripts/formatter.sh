#!/bin/sh -e
set -x

pip install -r requirements-dev.txt
ruff check fastapi_clerk_auth tests --fix
ruff format fastapi_clerk_auth tests