install:
	pip install -r requirements.dev.txt

test:
	cd play && ENV=local pytest

run:
	cd play && ENV=local ./manage.py runserver

migrate:
	cd play && ENV=local ./manage.py migrate

shell:
	cd play && ENV=local ./manage.py shell_plus
