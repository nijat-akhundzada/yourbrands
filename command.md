docker-compose run --rm app sh -c "django-admin startproject e_commerce ."
docker volume ls
docker volume rm e-commerce-maestro_dev-db-data
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"
