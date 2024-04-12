docker-compose run --rm app sh -c "django-admin startproject e_commerce ."
docker volume ls
docker volume rm e-commerce-maestro_dev-db-data
