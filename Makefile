VENV = .env
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: all install data validate clean

all: install

install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

clean:
	rm -rf __pycache__
	rm -rf $(VENV)

data: install
	$(PYTHON) src/capture_sp500.py
	$(PYTHON) src/capture_timeseries.py
	$(PYTHON) src/generate_db_schema.py
	$(PYTHON) src/pump_timeseries_to_db.py

validate: install
	$(PYTHON) -m frictionless validate data/sp500_constituents.csv
