
.PHONY: create-superuser
create-superuser:
    docker-compose exec web python manage.py createsuperuser

.PHONY: run-migrations
run-migrations:
	docker-compose exec web python manage.py makemigrations

.PHONY: run-migrate
run-migrate:
	docker-compose exec web python manage.py migrate

.PHONY: run
run:
	docker-compose exec web python manage.py runserver

.PHONY: create-db
create-db:
	psql -U postgres -d postgres -c "CREATE DATABASE visualizer;"

.PHONY: drop-db
drop-db:
	psql -U postgres -d postgres -c "DROP DATABASE visualizer;"

.PHONY: init-db
init-db:
	create-db
	create-superuser
	run-migrations
	run-migrate



