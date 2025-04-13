.PHONY:
	run-dev
	load-data
	backend-tests

run-dev:
	docker-compose -f docker-compose.yml up

load-data:
	@echo "Creating a temporary copy of users.json..."
	cp account/fixtures/users.json /tmp/users_temp.json
	@echo "Hashing passwords in the temporary fixture..."
	docker exec -it home_budget_backend python3 hash_fixture_passwords.py /tmp/users_temp.json
	@echo "Loading the temporary fixture..."
	docker exec -it home_budget_backend python3 manage.py loaddata /tmp/users_temp.json
	@echo "Cleaning up the temporary fixture..."
	rm /tmp/users_temp.json
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