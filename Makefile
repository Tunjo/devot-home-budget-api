.PHONY:
	run-dev
	backend-tests

run-dev:
	docker-compose -f docker-compose.yml up

backend-tests:
	docker exec -it  home_budget_backend pytest