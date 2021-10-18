cnf ?= config.env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

DOCKER_PATH:=".docker/."

.PHONY: help
.DEFAULT_GOAL := help

help: ## 這個幫助提示訊息
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## 建置運行容器
	docker dockeruild -t $(APP_NAME) ${DOCKER_PATH}

build-nc: ## 在不進行快取下建置運行環境
	docker build --no-cache -t $(APP_NAME) ${DOCKER_PATH}

run: ## 在 config.env 裡配置的通訊埠運行容器
	docker run -it --rm --env-file=./config.env -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME) /bin/bash

up: ## 運行容器上線
	docker-compose --file .docker/docker-compose.yml -p "$(APP_NAME)-container" up

down: ## 運行容器下線
	docker-compose --file .docker/docker-compose.yml down --rmi all

stop: ## 停止並移除正在運行的容器
	docker stop $(APP_NAME)
	docker rm $(APP_NAME)

# Docker tagging
tag: tag-latest tag-version ## 幫運行容器產生標記 {version} 與 latest 標籤

tag-latest: ## 幫運行容器產生標記 latest 標籤
	@echo '創建標籤 latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## 幫運行容器產生標記 {version} 標籤
	@echo '創建標籤 $(APP_VERSION)'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(APP_VERSION)

version: ## 輸出當前版本
	@echo $(APP_VERSION)