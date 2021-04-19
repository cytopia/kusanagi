ifneq (,)
.error This Makefile requires GNU Make.
endif


# -------------------------------------------------------------------------------------------------
# Can be changed
# -------------------------------------------------------------------------------------------------
# This can be adjusted
PYTHON_VERSION = 3.6


# -------------------------------------------------------------------------------------------------
# Default configuration
# -------------------------------------------------------------------------------------------------
.PHONY: help lint code test autoformat build clean
SHELL := /bin/bash

NAME = $(shell grep -E '^[[:space:]]*name' setup.py  | awk -F'"' '{print $$2}' | sed 's/-/_/g' )
VENV = venv
SRC  = kusanagi

FL_VERSION = 0.4
FL_IGNORES = .git/,.github/,$(NAME).egg-info,.mypy_cache/,$(ENV)


# -------------------------------------------------------------------------------------------------
# Default Target
# -------------------------------------------------------------------------------------------------
help:
	@echo "lint              Lint repository files"
	@echo "code              Run code linters: black, mypy, pylint, pydocstyle, pycodestyle"
	@echo "test              Run integration tests"
	@echo "autoformat        Autoformat code according to Python Black standard"
	@echo "build             Build Python package"
	@echo "clean             Clean current Python package build"


# -------------------------------------------------------------------------------------------------
# Lint Targets
# -------------------------------------------------------------------------------------------------
lint: _lint-files
lint: _lint-version
lint: _lint-bin-name
lint: _lint-pkg-name
lint: _lint-description

.PHONY: _lint-files
_lint-files:
	@echo "# --------------------------------------------------------------------"
	@echo "# Lint files"
	@echo "# -------------------------------------------------------------------- #"
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-cr --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-crlf --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-trailing-single-newline --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-trailing-space --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-utf8 --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) file-utf8-bom --text --ignore '$(FL_IGNORES)' --path .
	@docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/file-lint:$(FL_VERSION) git-conflicts --text --ignore '$(FL_IGNORES)' --path .

.PHONY: _lint-version
_lint-version:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check version"
	@echo "# -------------------------------------------------------------------- #"
	@VERSION_CODE=$$( cat $(SRC)/defaults.py  | grep ^DEF_VERSION | awk -F'"' '{print $$2}' ); \
	VERSION_SETUP=$$( grep version= setup.py | awk -F'"' '{print $$2}' || true ); \
	if [ "$${VERSION_CODE}" != "$${VERSION_SETUP}" ]; then \
		echo "[ERROR] Version mismatch"; \
		echo "$(SRC)/defaults.py   $${VERSION_CODE}"; \
		echo "setup.py:              $${VERSION_SETUP}"; \
		exit 1; \
	else \
		echo "[OK] Version match"; \
		echo "$(SRC)/defaults.py   $${VERSION_CODE}"; \
		echo "setup.py:              $${VERSION_SETUP}"; \
		exit 0; \
	fi \

.PHONY: _lint-bin-name
_lint-bin-name:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check binary name"
	@echo "# -------------------------------------------------------------------- #"
	@NAME_CODE=$$( cat $(SRC)/defaults.py  | grep ^DEF_BIN | awk -F'"' '{print $$2}' ); \
	NAME_SETUP=$$( grep ':main' setup.py | awk -F'"' '{print $$2}' | awk -F'=' '{print $$1}' ); \
	if [ "$${NAME_CODE}" != "$${NAME_SETUP}" ]; then \
		echo "[ERROR] Name mismatch"; \
		echo "$(SRC)/defaults.py   $${NAME_CODE}"; \
		echo "setup.py:              $${NAME_SETUP}"; \
		exit 1; \
	else \
		echo "[OK] Name match"; \
		echo "$(SRC)/defaults.py   $${NAME_CODE}"; \
		echo "setup.py:              $${NAME_SETUP}"; \
		exit 0; \
	fi \

.PHONY: _lint-pkg-name
_lint-pkg-name:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check package name"
	@echo "# -------------------------------------------------------------------- #"
	@NAME_CODE=$$( cat $(SRC)/defaults.py  | grep ^DEF_NAME | awk -F'"' '{print $$2}' ); \
	NAME_SETUP=$$( grep 'name=' setup.py | awk -F'"' '{print $$2}' | awk -F'=' '{print $$1}' ); \
	if [ "$${NAME_CODE}" != "$${NAME_SETUP}" ]; then \
		echo "[ERROR] Name mismatch"; \
		echo "$(SRC)/defaults.py   $${NAME_CODE}"; \
		echo "setup.py:              $${NAME_SETUP}"; \
		exit 1; \
	else \
		echo "[OK] Name match"; \
		echo "$(SRC)/defaults.py   $${NAME_CODE}"; \
		echo "setup.py:              $${NAME_SETUP}"; \
		exit 0; \
	fi \


.PHONY: _lint-description
_lint-description:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check description"
	@echo "# -------------------------------------------------------------------- #"
	@DESC_CODE=$$( \
		grep -A2 -E '^DEF_DESC\s*=\s*("|\()' $(SRC)/defaults.py \
		| grep -E '".+"' \
		| awk -F'"' '{print $$2}' \
	); \
	DESC_SETUP=$$( grep description= setup.py | awk -F'"' '{print $$2}' || true ); \
	if [ "$${DESC_CODE}" != "$${DESC_SETUP}" ]; then \
		echo "[ERROR] Desc mismatch"; \
		echo "$(SRC)/defaults.py   $${DESC_CODE}"; \
		echo "setup.py:              $${DESC_SETUP}"; \
		exit 1; \
	else \
		echo "[OK] Desc match"; \
		echo "$(SRC)/defaults.py   $${DESC_CODE}"; \
		echo "setup.py:              $${DESC_SETUP}"; \
		exit 0; \
	fi \


# -------------------------------------------------------------------------------------------------
# Code Style Targets
# -------------------------------------------------------------------------------------------------
code: _code-pycodestyle
code: _code-pydocstyle
code: _code-pylint
code: _code-black
code: _code-mypy

.PHONY: _code-pycodestyle
_code-pycodestyle:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check pycodestyle"
	@echo "# -------------------------------------------------------------------- #"
	docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/pycodestyle --config=setup.cfg $(SRC)/

.PHONY: _code-pydocstyle
_code-pydocstyle:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check pydocstyle"
	@echo "# -------------------------------------------------------------------- #"
	docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data cytopia/pydocstyle --explain --config=setup.cfg $(SRC)/

.PHONY: _code-pylint
_code-pylint:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check pylint"
	@echo "# -------------------------------------------------------------------- #"
	docker run --rm $$(tty -s && echo "-it" || echo) -v $(PWD):/data --entrypoint=sh cytopia/pylint -c '\
		pip3 install -r requirements.txt \
		&& pylint --rcfile=setup.cfg $(SRC)/'

.PHONY: _code-black
_code-black:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check Python Black"
	@echo "# -------------------------------------------------------------------- #"
	docker run --rm $$(tty -s && echo "-it" || echo) -v ${PWD}:/data cytopia/black -l 100 --check --diff $(SRC)/

.PHONY: _code-mypy
_code-mypy:
	@echo "# -------------------------------------------------------------------- #"
	@echo "# Check mypy"
	@echo "# -------------------------------------------------------------------- #"
	docker run --rm $$(tty -s && echo "-it" || echo) -v ${PWD}:/data cytopia/mypy --config-file setup.cfg $(SRC)/


# -------------------------------------------------------------------------------------------------
# Test Targets
# -------------------------------------------------------------------------------------------------
.PHONY: test
test:
	@echo "Check Python package"
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		python:$(PYTHON_VERSION)-alpine sh -c "\
			pip install -r requirements.txt \
			&& ./bin/kusa --help \
			&& ./bin/kusa cmd --help \
			&& ./bin/kusa cmd localhost \
			&& ./bin/kusa cmd localhost 4445 \
			&& ./bin/kusa cmd localhost -e nc \
			&& ./bin/kusa cmd localhost -s sh \
			&& ./bin/kusa cmd localhost -b '/' \
			&& ./bin/kusa cmd localhost -o bsd \
			&& ./bin/kusa cmd localhost -o linux \
			&& ./bin/kusa cmd localhost -o mac \
			&& ./bin/kusa cmd localhost -o windows \
			&& ./bin/kusa cmd localhost -m 100 \
			&& ./bin/kusa cmd localhost --enc url \
			&& ./bin/kusa cmd localhost --enc url hex \
			"


# -------------------------------------------------------------------------------------------------
# Build Targets
# -------------------------------------------------------------------------------------------------
build: clean
build: _lint-version
build: _build-source_dist
build: _build-binary_dist
build: _build-python_package
build: _build-check_python_package

.PHONY: _build_source_dist
_build-source_dist:
	@echo "Create source distribution"
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		-u $$(id -u):$$(id -g) \
		python:$(PYTHON_VERSION)-alpine \
		python setup.py sdist

.PHONY: _build_binary_dist
_build-binary_dist:
	@echo "Create binary distribution"
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		-u $$(id -u):$$(id -g) \
		python:$(PYTHON_VERSION)-alpine \
		python setup.py bdist_wheel --universal

.PHONY: _build_python_package
_build-python_package:
	@echo "Build Python package"
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		-u $$(id -u):$$(id -g) \
		python:$(PYTHON_VERSION)-alpine \
		python setup.py build

.PHONY: _build_check_python_package
_build-check_python_package:
	@echo "Check Python package"
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		python:$(PYTHON_VERSION)-slim \
		sh -c "pip install twine \
		&& twine check dist/*"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf $(NAME).egg-info
	find . -type f -name '*.pyc' -exec rm {} \;
	find . -type d -name '__pycache__' -prune -exec rmdir {} \;

.PHONY: venv
venv:
	python3 -m venv $(VENV)
	@echo source $(VENV)/bin/activate
	@echo python3 setup.py install


# -------------------------------------------------------------------------------------------------
# Publish Targets
# -------------------------------------------------------------------------------------------------
deploy: _build-check_python_package
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		python:$(PYTHON_VERSION)-slim \
		sh -c "pip install twine \
		&& twine upload dist/*"


# -------------------------------------------------------------------------------------------------
# Misc Targets
# -------------------------------------------------------------------------------------------------
autoformat:
	docker run \
		--rm \
		$$(tty -s && echo "-it" || echo) \
		-v $(PWD):/data \
		-w /data \
		cytopia/black -l 100 $(SRC)/
