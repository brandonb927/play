install:
	pip install -r src/requirements.dev.txt

test:
	cd src && ENV=local ./manage.py test

run:
	cd src && ENV=local ./manage.py runserver

migrate:
	cd src && ENV=local ./manage.py migrate
