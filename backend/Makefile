

create-superuser:
	docker-compose exec web python manage.py createsuperuser

run-migrations:
	docker-compose exec web python manage.py makemigrations

run-migrate:
	docker-compose exec web python manage.py migrate

init-db:
    create-superuser
	run-migrations
	run-migrate



