init: requirements.txt
	pip install -r requirements.txt
	prisma generate --schema=./servidor/schema.prisma

client: interface/main.py
	python3 interface/main.py

server: servidor/servidor.py
	prisma py fetch
	python3 servidor/servidor.py