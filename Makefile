.venv:
	python -m venv .venv
	.venv/bin/pip install -e .

run: .venv
	.venv/bin/python main.py

install: .venv

clean:
	rm -rf .venv
