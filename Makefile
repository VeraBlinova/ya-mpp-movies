load_data:
	docker compose exec django sh -c "cd /in_data/ && python3 load_data.py"

install-pytest:
	. venv/bin/activate && pip install pytest

test-fastapi: install-pytest
	. venv/bin/activate && cd fastapi_solution && pytest

create_superuser:
	docker compose exec authapi sh -c "python superuser.py -l $(login) -p $(password) -fn $(first_name) -ln $(last_name)"

create_superuser_test:
	docker compose exec authapi bash -c "python superuser.py -l string -p string -fn Ad -ln Min"

create_superuser_admin:
	docker compose exec authapi bash -c "python superuser.py -l ad@m.in -p 123qwe -fn Ad -ln Min"

test-eventapi:

test-eventapi:
	cd ./ugc/src && pytest
