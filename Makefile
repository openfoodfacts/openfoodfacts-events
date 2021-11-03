#!/usr/bin/make

NAME = "events"
ENV_FILE ?= .env
DOCKER_COMPOSE=docker-compose --env-file=${ENV_FILE}

.DEFAULT_GOAL := dev
# avoid target corresponding to file names, to depends on them
.PHONY: *

#------#
# Info #
#------#
info:
	@echo "${NAME} version: ${VERSION}"

hello:
	@echo "🥫 Welcome to the Events API dev environment setup!"
	@echo "🥫 Thanks for contributing to Events API!"
	@echo ""

goodbye:
	@echo "🥫 Cleaning up dev environment (remove containers, remove local folder binds, prune Docker system) …"

#-------#
# Local #
#-------#
dev: hello up
	@echo "🥫 You should be able to access your local install of Events API at http://localhost:8000"
	@echo "🥫 You should be able to access Events API metrics at http://localhost:8000/metrics"

#----------------#
# Docker Compose #
#----------------#
up:
	@echo "🥫 Building and starting containers …"
	${DOCKER_COMPOSE} up -d --build 2>&1

down:
	@echo "🥫 Bringing down containers …"
	${DOCKER_COMPOSE} down

hdown:
	@echo "🥫 Bringing down containers and associated volumes …"
	${DOCKER_COMPOSE} down -v

restart:
	@echo "🥫 Restarting containers …"
	${DOCKER_COMPOSE} restart

status:
	@echo "🥫 Getting container status …"
	${DOCKER_COMPOSE} ps

livecheck:
	@echo "🥫 Running livecheck …"
	docker/docker-livecheck.sh

log:
	@echo "🥫 Reading logs (docker-compose) …"
	${DOCKER_COMPOSE} logs -f

#------------#
# Quality    #
#------------#

flake8:
	${DOCKER_COMPOSE} run --rm --no-deps api flake8

black-check:
	${DOCKER_COMPOSE} run --rm --no-deps api black --check .

black:
	${DOCKER_COMPOSE} run --rm --no-deps api black .

mypy:
	${DOCKER_COMPOSE} run --rm --no-deps api mypy .

isort-check:
	${DOCKER_COMPOSE} run --rm --no-deps api isort --check .

isort:
	${DOCKER_COMPOSE} run --rm --no-deps api isort .

checks: flake8 black-check mypy isort-check

lint: isort black

integration:
	make dev
	newman run tests/integration/openfoodfacts-events.postman_collection.json -e tests/integration/off-local.postman_environment.json
	make hdown

unit:
	pip install pytest
	pip install -r requirements.txt
	ADMIN_USERNAME=test ADMIN_PASSWORD=test pytest -vv tests/unit

#------------#
# Production #
#------------#
create_external_volumes:
	@echo "🥫 Creating external volumes (production only) …"
	docker volume create events-data

#---------#
# Cleanup #
#---------#
prune:
	@echo "🥫 Pruning unused Docker artifacts (save space) …"
	docker system prune -af

prune_cache:
	@echo "🥫 Pruning Docker builder cache …"
	docker builder prune -f

clean: goodbye hdown prune prune_cache
