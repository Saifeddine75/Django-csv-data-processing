

create-superuser:
    docker-compose exec web python manage.py createsuperuser

run-migrations:
	docker-compose exec web python manage.py makemigrations

run-migrate:
	docker-compose exec web python manage.py migrate

run:
	docker-compose exec web python manage.py runserver

create-db:
	psql -U postgres -d postgres -c "CREATE DATABASE visualizer;"

drop-db:
	psql -U postgres -d postgres -c "DROP DATABASE visualizer;"

init-db:
	create-db
	create-superuser
	run-migrations
	run-migrate



