FROM python:3.11-slim AS base
WORKDIR /app
COPY ./fastapi_clerk_auth ./fastapi_clerk_auth
COPY ./pyproject.toml ./pyproject.toml
COPY .bumpversion.cfg .bumpversion.cfg


FROM base AS lint
COPY ./tests ./tests
RUN pip install -e .[dev]
CMD ["ruff", "check", "."]


FROM base AS format
COPY ./tests ./tests
RUN pip install -e .[dev]
CMD ["ruff", "check", ".", "--fix"]


FROM base AS bumpversion
RUN pip install bumpversion


FROM bumpversion AS bump_patch
RUN bump2version patch


FROM bumpversion AS bump_minor
RUN bump2version minor


FROM bumpversion AS bump_major
RUN bump2version major


FROM base AS jwks
RUN pip install -e .[dev]
COPY ./tests ./tests
WORKDIR /app/tests
CMD ["python", "mock_servers/jwks_server.py"]


FROM base AS api
RUN pip install -e .[dev]
COPY ./tests ./tests
WORKDIR /app/tests
CMD ["python", "mock_servers/api_server.py"]


FROM base AS test
RUN pip install -e .[dev]
COPY ./tests ./tests
WORKDIR /app/tests
CMD ["pytest", "-vv"]
