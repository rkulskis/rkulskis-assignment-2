install:
	pip install -r requirements.txt --break-system-packages
run:
	FLASK_APP=app.py FLASK_ENV=development flask run --host=localhost --port=3000
