up:
	docker-compose up

build:
	docker-compose build

pull:
	docker-compose pull

install-dependencies:
	python -m virtualenv venv
	.\venv\Scripts\activate
	pip install -r requirements.txt

test:
	python -m pytest
