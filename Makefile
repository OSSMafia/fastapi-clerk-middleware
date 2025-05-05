format:
	docker build --target=format -t package:format -f dockerfile . && \
	docker run --rm \
		-v ./fastapi_clerk_auth:/app/fastapi_clerk_auth \
		-v ./.bumpversion.cfg:/app/.bumpversion.cfg \
		-v ./pyproject.toml:/app/pyproject.toml \
		package:format
	docker rmi package:format || true

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
