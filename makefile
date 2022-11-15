GATEWAY_DIR = $(shell pwd)
WORKING_DIR = ~/repos
FRONTEND_DIR = $(WORKING_DIR)/frontend
BACKEND_DIR = $(WORKING_DIR)/backend-main

init_base:
	if [ ! -d $(WORKING_DIR) ]; then mkdir $(WORKING_DIR); fi; \
	docker network create microservice-network

init_frontend: init_base
	if [ ! -d $(FRONTEND_DIR) ]; then									\
		cd $(WORKING_DIR) &&											\
		git clone git@github.com:Projekt-DataScience/frontend.git; 		\
	fi;

init_backend: init_base
	if [ ! -d $(BACKEND_DIR) ]; then									\
		cd $(WORKING_DIR) &&											\
		git clone git@github.com:Projekt-DataScience/backend-main.git;		\
	fi;

deploy_backend: init_backend
	docker compose \
 	-f $(BACKEND_DIR)/docker-compose.yml \
 	-f $(GATEWAY_DIR)/docker-compose.yml \
 	up
deploy_frontend: init_frontend
	# cd $(FRONTEND_DIR) && docker compose up

deploy: deploy_backend deploy_frontend

gateway_test:
	python3 app/main.py