setup:
	@pipx install 'poetry==1.8.3'

install:
	@poetry install

run:
	@poetry run python src/main.py