.PHONY: format lint upload_record

format:
	isort .
	black .

lint: format
	flake8 .

upload_record:
	python record_collector.py \
		--upload

write_record_to_local:
	python record_collector.py \
		--path past_record.json