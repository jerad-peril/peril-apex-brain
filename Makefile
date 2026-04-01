.PHONY: install dev snapshot simulate stress reindex ingest

install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --host 0.0.0.0 --port 9090 --reload

snapshot:
	python3 snapshot_vault.py

simulate:
	python3 jarvis_simulator.py http://localhost:9090 "What is the Airtable field ID for Insurance Carrier?"

stress:
	python3 stress_test.py http://localhost:9090 10

reindex:
	python3 apex_vector_builder.py

ingest:
	@echo "Usage: make ingest FILE=path/to/document.md"
	@test -n "$(FILE)" && python3 ingest_document.py $(FILE) || true
