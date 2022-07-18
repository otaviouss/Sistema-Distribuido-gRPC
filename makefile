init: requirements.txt
	pip install -r requirements.txt
	prisma generate --schema=./servidor/schema.prisma

client: interface/main.py
	python3 interface/main.py
