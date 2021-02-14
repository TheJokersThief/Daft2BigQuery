.PHONY: test coverage lint docs clean dev install help export_conf

project_name="daft2bigquery"
project_id=""

help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

ensure-poetry:
	@if ! [ -x $(command -v poetry) ]; then \
		echo "Please install poetry (e.g. pip install poetry)"; \
		exit 1; \
	fi

lint: ensure-poetry  ## Lint files for common errors and styling fixes
	poetry check
	poetry run flake8 --ignore F821,W504 $(project)

test: ensure-poetry lint  ## Run unit tests
	poetry run pytest tests --cov=$(project) --strict tests

coverage: ensure-poetry test  ## Output coverage stats
	poetry run coverage report -m
	poetry run coverage html
	@echo "coverage report: file://`pwd`/htmlcov/index.html"

clean:
	find . -name '*.pyc' -delete
	find . -name __pycache__ -delete
	rm -rf .coverage dist build htmlcov *.egg-info

dev: ensure-poetry clean  ## Install project and dev dependencies
	poetry install

install: ensure-poetry clean  ## Install project without dev dependencies
	poetry install --no-dev

export_conf:  ## Export the poetry lockfile to requirements.txt
	poetry export -f requirements.txt --output requirements.txt --without-hashes

create_pubsub_topic:
	gcloud pubsub topics create "trigger-${project_name}"

deploy_to_gfunctions: create_pubsub_topic
	gcloud functions deploy ${project_name} --region europe-west1 --project $project_id --runtime python38 --memory 256MB --entry-point execute_daft2bigquery --trigger-topic "trigger-${project_name}" --timeout 600s --max-instances 1 --retry

publish: deploy_to_gfunctions  ## Publish project to google cloud functions
	@echo "Published"
