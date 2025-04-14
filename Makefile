.PHONY:
	run-dev
	load-data
	backend-tests

run-dev:
	docker-compose -f docker-compose.yml up

load-data:
	@echo "Hashing passwords in the temporary fixture..."
	docker exec -it home_budget_backend sh -c "cp account/fixtures/users.json users_temp.json && python3 hash_fixture_passwords.py users_temp.json"
	@echo "Loading the temporary fixture..."
	docker exec -it home_budget_backend python3 manage.py loaddata users_temp.json
	@echo "Cleaning up the temporary fixture..."
	docker exec -it home_budget_backend rm users_temp.json
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