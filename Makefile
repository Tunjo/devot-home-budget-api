.PHONY:
	run-dev
	backend-tests

run-dev:
	docker-compose -f docker-compose.yml up

load-data:
    @echo "Loading users.json..."
    docker exec -it home_budget_backend python3 manage.py loaddata account/fixtures/users.json
    @echo "Triggering user signals..."
    docker exec -it home_budget_backend python3 manage.py trigger_user_signals
    @sleep 1

    @echo "Loading categories.json..."
    docker exec -it home_budget_backend python3 manage.py loaddata category/fixtures/categories.json
    @sleep 1

    @echo "Loading expenses.json..."
    docker exec -it home_budget_backend python3 manage.py loaddata category/fixtures/expenses.json
    @echo "Triggering expense signals..."
    docker exec -it home_budget_backend python3 manage.py trigger_expense_signals
    @sleep 1

    @echo "All data loaded successfully!"

backend-tests:
	docker exec -it  home_budget_backend pytest