cnf ?= config.env
include $(cnf)

ifeq ($(OS), Windows_NT)
	detected_OS := Windows
else
	detected_OS := $(shell sh -c 'uname -s 2>/dev/null || echo not')
	export $(shell sed 's/=.*//' $(cnf))
endif

DOCKER_PATH := .docker/Dockerfile

$(info Detected OS: $(detected_OS))
$(info Docker Path: $(DOCKER_PATH))

.PHONY: help
.DEFAULT_GOAL := help

help: ## This help message
ifeq ($(detected_OS), Windows)
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "%-30s %s\n", $$1, $$2}' $(MAKEFILE_LIST)
else
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
endif

build: ## Build the container
	docker build -t $(APP_NAME) -f ${DOCKER_PATH} .

build-nc: ## Build the container without cache
	docker build --no-cache -t $(APP_NAME) -f ${DOCKER_PATH} .

run: ## Run the container on the port configured in config.env
	docker run -it --rm --env-file=./config.env -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME) /bin/bash

up: build ## Bring the container online
	docker-compose --file .docker/docker-compose.yml -p "$(APP_NAME)-container" up

down: ## Bring the container offline
	docker-compose --file .docker/docker-compose.yml down --rmi all

ssh: ## Into the container
	docker exec -it $(APP_NAME) /bin/bash

stop: ## Stop and remove the running container
	docker stop $(APP_NAME)
	docker rm $(APP_NAME)

# Docker tagging
tag: tag-latest tag-version ## Generate tags {version} and latest tags for containers

tag-latest: ## Generate tags latest for containers
	@echo '創建標籤 latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate tags {version} for containers
	@echo '創建標籤 $(APP_VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(APP_VERSION)

version: ## current version
	@echo $(APP_VERSION)