clean:
	docker compose down --volumes --remove-orphans || true && \
	docker image prune -a --force || true

format:
	docker build --target=format -t package:format -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./tests:/app/tests \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:format
	docker rmi package:format || true

lint:
	docker build --target=lint -t package:lint -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./tests:/app/tests \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:lint
	docker rmi package:lint || true

test: clean
	docker compose run test_runner; \
	EXIT_CODE=$$?; \
	docker compose down; \
	exit $$EXIT_CODE

version_patch:
	docker build --target=bump_patch -t package:bumpversion -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:bumpversion
	docker rmi package:bumpversion || true

version_minor:
	docker build --target=bump_minor -t package:bumpversion -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:bumpversion
	docker rmi package:bumpversion || true

version_major:
	docker build --target=bump_major -t package:bumpversion -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:bumpversion
	docker rmi package:bumpversion || true
