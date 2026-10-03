.PHONY: lint test serve setup

VENV_PATH = /mnt/sda5/Projects/QT/.venv
PYTHON = $(VENV_PATH)/bin/python
RUFF = $(VENV_PATH)/bin/ruff
PYTEST = $(VENV_PATH)/bin/pytest
STREAMLIT = $(VENV_PATH)/bin/streamlit

lint:
	$(RUFF) check .
	$(RUFF) format --check .

test:
	$(PYTEST) tests/ -v

serve:
	$(STREAMLIT) run app/Home.py

setup:
	@echo "Using QT project virtual environment: $(VENV_PATH)"
	$(PYTHON) -m pip install -e .[dev]
