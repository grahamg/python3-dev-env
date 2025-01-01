.PHONY: build up down test shell

build:
	docker-compose build

# By default, we might just run dev
up:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

down:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml down

test:
	# Run pytest in the dev container
	docker exec -it dev_env pytest

shell:
	docker exec -it dev_env /bin/bash
