.PHONY: clean clean-build clean-pyc lint test setup help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

setup: ## install python project dependencies
	pip install --upgrade -r requirements.txt
	anyblok_createdb -c app.cfg || anyblok_updatedb -c app.cfg

setup-tests: ## install python project dependencies for tests
	pip install --upgrade -r requirements.test.txt
	anyblok_createdb -c app.test.cfg || anyblok_updatedb -c app.test.cfg

setup-dev: ## install python project dependencies for development
	pip install --upgrade -r requirements.dev.txt
	anyblok_createdb -c app.dev.cfg || anyblok_updatedb -c app.dev.cfg

run-dev: ## launch pyramid development server
	anyblok_pyramid -c app.dev.cfg --wsgi-host 0.0.0.0

run-gunicorn: ## launch pyramid server with gunicorn
	gunicorn_anyblok_pyramid --anyblok-configfile app.cfg

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check style with flake8
	flake8 canigoo_radio

test: ## run anyblok nose tests
	anyblok_nose -c app.test.cfg -- -v -s canigoo_radio

documentation: ## generate documentation
	anyblok_doc -c app.test.cfg --doc-format RST --doc-output doc/source/apidoc.rst
	make -C doc/ html

node-setup-dev: ## install node within virtualenv
	pip install -r requirements.dev.txt
	npm --version || nodeenv -p
	npm install canigoo_radio/canigoo_radio/templates/radio-manager  
node-run-dev: ## serve with hot reload at :8080
	npm run dev

node-run-build: ## build for production with minification
	npm run build
