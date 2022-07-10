init: requirements.txt
	pip install -r requirements.txt
	prisma generate

client: main.py
	python3 main.py

server: servidor.py
	prisma py fetch
	python3 servidor.py