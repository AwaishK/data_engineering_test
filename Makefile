dev-env:
	python3.11 -m venv env
	. env/bin/activate
	pip install -r requirements.txt


setup-airflow:
	airflow standalone 
