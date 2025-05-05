FROM python:3.11-slim AS base
WORKDIR /app
COPY ./fastapi_clerk_auth ./fastapi_clerk_auth
COPY ./pyproject.toml ./pyproject.toml
COPY .bumpversion.cfg .bumpversion.cfg


FROM base AS format
COPY ./ruff.toml ./ruff.toml
RUN pip install -e .[dev]
WORKDIR /app/fastapi_clerk_auth
CMD ruff check ./ --fix --config ../ruff.toml && ruff format ./ --config ../ruff.toml


FROM base AS bumpversion
RUN pip install bumpversion


FROM bumpversion AS bump_patch
RUN bump2version patch


FROM bumpversion AS bump_minor
RUN bump2version minor


FROM bumpversion AS bump_major
RUN bump2version major