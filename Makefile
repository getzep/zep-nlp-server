.PHONY: all format lint test tests download-language-model coverage run run-dev docker-build docker-run

CONTAINER_NAME := zep-nlp-server
LANGUAGE_MODEL := en_core_web_sm

all: download-language-model format lint test

run:
	poetry run python main.py

run-dev:
	poetry run uvicorn main:app --reload --log-level debug --port 8080

docker-build:
	DOCKER_BUILDKIT=1 docker build -t $(CONTAINER_NAME) .

docker-run:
	docker run -p 8080:8080 $(CONTAINER_NAME)

download-language-model:
	poetry run python -m spacy download $(LANGUAGE_MODEL)

coverage:
	poetry run pytest --cov \
		--cov-config=.coveragerc \
		--cov-report xml \
		--cov-report term-missing:skip-covered

format:
	poetry run black  .
	poetry run ruff --select I --fix  .

lint:
	poetry run mypy .
	poetry run black . --check
	poetry run ruff .

test:
	poetry run pytest app/tests

loadtest:
	poetry run locust -f load_test.py --headless --run-time 60 -u 50 --host http://0.0.0.0:8080