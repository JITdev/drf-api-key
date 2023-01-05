pyenv = drfapi311
pysources = src/ test_project/ tests/

build:
	${python} setup.py sdist bdist_wheel
	twine check dist/*
	rm -r build

check:
	black --check --diff --target-version=py36 ${pysources}
	flake8 ${pysources}
	mypy ${pysources}
	isort --check --diff ${pysources}
	make migrations-check

docs:
	mkdocs build

docs-serve:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

install:
	pyenv shell ${pyenv}
	pip install -U pip wheel
	pip install -r requirements.txt
	./tools/install_django.sh pip

format:
	autoflake --in-place --recursive ${pysources}
	isort ${pysources}
	black --target-version=py36 ${pysources}

migrations:
	python -m tools.makemigrations

migrations-check:
	python -m tools.makemigrations --check

publish:
	twine upload dist/*

test:
	pytest
