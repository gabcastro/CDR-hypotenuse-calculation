setup: requirements.txt
	pip install -r requirements.txt

run:
	python.exe ./module/core.py

clean:
    rm -rf __pycache__