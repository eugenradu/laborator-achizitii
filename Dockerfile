# Utilizează o imagine Python oficială ca bază
FROM python:3.10-slim-buster

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierul requirements.txt și instalează dependințele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază restul codului aplicației în directorul de lucru
COPY . .

# Expune portul pe care rulează Flask
EXPOSE 5000

# Definește variabila de mediu pentru Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0 
# Permite accesul de pe orice interfață

# Comanda pentru a rula aplicația Flask
# create_tables_and_initial_data() va fi apelat la pornire în app.py
CMD ["flask", "run"]